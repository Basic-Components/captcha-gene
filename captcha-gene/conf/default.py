from pathlib import Path

font_path = Path(__file__).absolute().parent.parent.parent.joinpath("font/Arial.ttf")

class DefaultSetting:
    # 服务器相关
    URL = "tcp://127.0.0.1:5555"
    CAPTCHA_FONT = str(font_path)
