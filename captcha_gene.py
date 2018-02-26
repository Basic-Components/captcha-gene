import asyncio
from pathlib import Path
import uuid
import random
import string
import math
import base64
from io import BytesIO
from functools import partial
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import aioredis
from sanic import Sanic
from sanic.response import json

app = Sanic()


def _gene_text(number=6):
    """生成随机字符."""
    source = string.ascii_letters + string.digits
    return ''.join(random.sample(source, number))


def _gene_line(draw, width, height):
    """用来绘制干扰线."""
    linecolor = (255, 0, 0)
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=linecolor)


def _gene_code(CAPTCHA_FONT, number=6):
    """用来绘制字符."""
    # 生成验证码图片的高度和宽度
    size = (120, 30)
    # 背景颜色，默认为白色
    bgcolor = (255, 255, 255)
    # 字体颜色，默认为蓝色
    fontcolor = (0, 0, 255)
    # 干扰线颜色。默认为红色

    # 是否要加入干扰线
    draw_line = True
    # 加入干扰线条数的上下限
    line_number = (1, 5)
    width, height = size  # 宽和高
    font = ImageFont.truetype(CAPTCHA_FONT, 25)
    image = Image.new('RGBA', (width, height), bgcolor)  # 创建图片
    draw = ImageDraw.Draw(image)  # 创建画笔
    text = _gene_text(number)  # 生成字符串
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text,
              font=font, fill=fontcolor)  # 填充字符串

    if draw_line:
        _gene_line(draw, width, height)
    # image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
    image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
    with BytesIO() as f:
        image.save(f, 'png')
        b = base64.b64encode(f.getvalue()).decode("ascii")
    return b, text


@app.listener('before_server_start')
async def setup_default_executor(app, loop):
    """设置默认执行器为多进程."""
    executor = ProcessPoolExecutor()
    loop.set_default_executor(executor)


@app.post("/sync")
async def sync_query(request):
    """同步返回执行结果."""
    loop = asyncio.get_event_loop()
    font_path = Path(__file__).absolute().parent.joinpath("font/Arial.ttf")
    gene_code = partial(_gene_code, str(font_path))
    pic, text = await loop.run_in_executor(None, gene_code)
    return json({
        "msg": text,
        "pic": pic
    })

async def save_to_redis(uid,redis_url, ttl=None):
    loop = asyncio.get_event_loop()
    font_path = Path(__file__).absolute().parent.joinpath("font/Arial.ttf")
    gene_code = partial(_gene_code, str(font_path))
    pic, text = await loop.run_in_executor(None, gene_code)
    redis = await aioredis.create_redis(
        redis_url
    )
    await redis.hmset(uid, {
        "pic":pic,
        "text":text
    })
    if ttl:
        redis.expire(uid, ttl)  
    redis.close()
    await redis.wait_closed()

@app.post("/async")
async def async_query(request):
    """同步返回执行结果."""
    uid = str(uuid.uuid4())
    data = request.json
    redis_url = data.get("redis_url")
    ttl = data.get('ttl')
    uuid = asyncio.ensure_future(save_to_redis(uid, redis_url, ttl=ttl))
    return json({
        "uuid": uid
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
