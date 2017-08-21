import asyncio
try:
    import ujson as json
except:
    import json

from .captcha_gen import gene_code


async def gen_captcha_handler(socket, env):
    loop = asyncio.get_event_loop()
    #while True:
    msg = await socket.recv()
    print('received', msg)
    message = json.loads(msg.decode("utf-8"))
    result = {}
    if message.get("method") == "img_code":
        loop = asyncio.get_event_loop()
        img, text = await loop.run_in_executor(None,gene_code, env.CAPTCHA_FONT)
        result["code"] = 200
        result["message"] = {
            "img": img,
            "text": text
        }
    else:
        result["code"] = 404
        result["message"] = "unknown method"

    send_message = json.dumps(result).encode("utf-8")
    print("send",send_message)
    await socket.send(send_message)