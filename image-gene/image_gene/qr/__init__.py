"""二维码编码解码接口,全部同步接口."""
import base64
import asyncio
from functools import partial
from sanic.response import json
from sanic.log import logger
from sanic import Blueprint
from sanic.exceptions import abort

from .qr_encoder import encode_qrcode

qr = Blueprint('qr', url_prefix="/qr")


#@qr.post("/encode")
@qr.post("/")
async def encode(request):
    """同步返回执行结果.

    要求使用post方法传输json,且包含`content`字段.返回的是base64编码的图片,图片为png.
    """
    loop = asyncio.get_event_loop()
    content = request.json.get("content")
    if content is None:
        return json(
            {
                'error': "must have field 'content' !"
            },
            status_code=400
        )
    if request.app.config.LOGO_PATH:
        _encode_qrcode = partial(
            encode_qrcode,
            string=content
        )
    else:
        _encode_qrcode = partial(
            encode_qrcode,
            string=content,
            logo_path=request.app.config.LOGO_PATH
        )
    b = await loop.run_in_executor(None, _encode_qrcode)
    return json({
        "img_b64": base64.b64encode(b).decode("ascii"),
    })


# @qr.post("/decode")
# async def decode(request):
#     """同步返回执行结果."""
#     loop = asyncio.get_event_loop()
#     img_b64 = request.json.get("img_b64")
#     if img_b64 is None:
#         return json(
#             {
#                 'error': "must have field 'img_b64' !"
#             },
#             status_code=400
#         )
#     img_bytes = base64.b64decode(img_b64)
#     _decode_qrcode = partial(
#         decode_qrcode,
#         img_bytes
#     )
#     content = await loop.run_in_executor(None, _decode_qrcode)
#     return json({
#         "content": content,
#     })
