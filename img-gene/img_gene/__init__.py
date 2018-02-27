from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from sanic import Sanic
from sanic.response import json
from img_gene.captcha import captcha
from img_gene.qr import qr


__VERSION__ = '0.0.1'
app = Sanic('img_gene')
font_path = Path(__file__).absolute().parent.parent.parent.joinpath("font/Arial.ttf")

default_settings = {
    'DEBUG': True,
    'HOST': '0.0.0.0',
    'PORT': 5000,
    'WORKERS': 1,
    'ACCESS_LOG': True,
    'CAPTCHA_FONT_PATH': str(font_path),
    'LOGO_PATH': None,
    "SSL":None
}
app.config.update(default_settings)


@app.listener('before_server_start')
async def setup_default_executor(app, loop):
    """设置默认执行器为多进程."""
    executor = ProcessPoolExecutor()
    loop.set_default_executor(executor)

app.blueprint(captcha)
app.blueprint(qr)
