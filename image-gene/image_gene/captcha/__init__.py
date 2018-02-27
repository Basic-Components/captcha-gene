import asyncio
import base64
from functools import partial
from sanic.response import json
from sanic.log import logger
from sanic import Blueprint
from .captcha_gene import gene_code

captcha_q = asyncio.Queue(maxsize=100)

captcha = Blueprint('captcha', url_prefix="/captcha")


async def captcha_producer(app, loop):
    font_path = app.config.CAPTCHA_FONT_PATH
    _gene_code = partial(gene_code, font_path)
    while True:
        if captcha_q.full():
            await asyncio.sleep(3)
        else:
            pic, text = await loop.run_in_executor(None, _gene_code)
            await captcha_q.put((pic, text))


@captcha.listener('before_server_start')
async def run_captcha_producer(app, loop):
    app.captcha_producer_task = asyncio.ensure_future(captcha_producer(app=app, loop=loop), loop=loop)
    logger.info("captcha_producer_task started")


@captcha.listener('before_server_stop')
async def stop_captcha_producer(app, loop):
    app.captcha_producer_task.cancel()
    while True:
        if app.captcha_producer_task.cancelled():
            break
        else:
            await asyncio.sleep(1)
    logger.info("captcha_producer_task stoped")


@captcha.post("/")
async def sync_query(request):
    """同步返回执行结果."""
    if captcha_q.empty():
        loop = asyncio.get_event_loop()
        font_path = request.app.config.CAPTCHA_FONT_PATH
        _gene_code = partial(gene_code, font_path)
        pic, text = await loop.run_in_executor(None, _gene_code)
    else:
        pic, text = await captcha_q.get()
    return json({
        "msg": text,
        "img_b64": base64.b64encode(pic).decode("ascii")
    })
