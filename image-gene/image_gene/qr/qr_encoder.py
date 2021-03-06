import os, sys
from io import BytesIO
import qrcode
from PIL import Image


def encode_qrcode(string, logo_path=""):
    """
    生成中间带logo的二维码
    需要安装qrcode, PIL库
    @参数 string: 二维码字符串
    @参数 path: 生成的二维码保存路径
    @参数 logo: logo文件路径
    @return: None
    """
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=1
    )
    qr.add_data(string)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert("RGBA")
    if logo_path and os.path.exists(logo_path):
        try:
            icon = Image.open(logo_path)
            img_w, img_h = img.size
        except Exception as e:
            print(e)
            sys.exit(1)
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        icon = icon.convert("RGBA")
        img.paste(icon, (w, h), icon)
    with BytesIO() as f:
        img.save(f,'png')
        b = f.getvalue()
    return b
    