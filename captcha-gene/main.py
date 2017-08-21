import sys
import argparse
import asyncio
from zmq.asyncio import Context
import zmq
from handlers import gen_captcha_handler
from conf import env_factory
zmq.asyncio.install()

def serve(env):
    ctx = Context.instance()
    socket = ctx.socket(zmq.REP)
    socket.bind(env.URL)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.ensure_future(gen_captcha_handler(socket, env))
    try:
        print("server start @", env.URL)
        print("font @", env.CAPTCHA_FONT)
        loop.run_forever()
        
    finally:
        loop.close()
        print("worker closed")
        socket.close()


def run(args):
    env = env_factory(args.env)
    serve(env)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    run_parsers = subparsers.add_parser("run")
    run_group = run_parsers.add_mutually_exclusive_group(required=False)
    run_group.add_argument('-e', '--env', choices=["local", "debug", "testing", "production"], default="local")
    run_parsers.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
