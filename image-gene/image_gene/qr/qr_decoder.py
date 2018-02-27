import os, sys
#import base64
from io import BytesIO
import zbar
import qrcode
from PIL import Image

def encode_qrcode(img_bytes):
    """解析二维码信息."""

    # 创建图片扫描对象
    scanner = zbar.ImageScanner()
    # 设置对象属性
    scanner.parse_config('enable')
    # 打开含有二维码的图片
    img = Image.open(io.BytesIO(img_bytes)).convert('L')
    # 获取图片的尺寸
    width, height = img.size
    # 建立zbar图片对象并扫描转换为字节信息
    qrCode = zbar.Image(width, height, 'Y800', img_bytes)
    scanner.scan(qrCode)
    # 组装解码信息
    data = ''
    for s in qrCode:
        data += s.data
    # 删除图片对象
    del img
    # 输出解码结果
    return data
