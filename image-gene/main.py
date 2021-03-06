"""程序入口,用于启动服务."""
import sys
import argparse
from pathlib import Path
from image_gene import app, __VERSION__
import yaml

def _load_conf(path):
    """指定地址加载配置文件为配置字典."""
    with open(path) as f:
        result = yaml.load(f)
    return result

def _make_conf(args):
    """通过命令行参数创建配置字典."""
    result = {}
    if args.port:
        result["PORT"] = args.port
    if args.host:
        result['HOST'] = args.host
    if args.nodebug:
        result['DEBUG'] = False
    if args.workers:
        result['WORKERS'] = args.workers
    if args.noaccess_log:
        result['ACCESS_LOG'] = False
    if args.ssl_cert and args.ssl_key:
        result["SSL"]={
            'cert':args.ssl_cert,
            'key':args.ssl_key
        }
    return result

def _parser_args(params):
    """解析命令行参数."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="指定端口")
    parser.add_argument("--host", type=str, help="指定主机")
    parser.add_argument("--workers", type=int, help="启动多少个进程执行")
    parser.add_argument("--nodebug", action="store_true", help="是否使用debug模式")
    parser.add_argument("--noaccess_log", action="store_true", help="是否输出access_log")
    parser.add_argument("--ssl_cert", type=str, help="指定ssl证书")
    parser.add_argument("--ssl_key", type=str, help="指定ssl密钥")

    parser.add_argument("-c", '--config', type=str, help="指定配置文件,使用yaml进行配置")
    parser.add_argument("--version", help="查看服务的版本号", action="store_true")

    args = parser.parse_args(params)
    return args

def _run_app():
    """执行启动服务的操作."""
    if app.config.WORKERS <=1:
        app.config.WORKERS = 1
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        workers = app.config.WORKERS,
        debug=app.config.DEBUG,
        access_log=app.config.ACCESS_LOG,
        ssl=app.config.SSL
    )


def main(argv=sys.argv[1:]):
    """服务启动入口.
    
    设置覆盖顺序`命令行参数`>`'-c'指定的配置文件`>`项目启动位置的配置文件`>默认配置.
    """
    args = _parser_args(argv)
    if args.version:
        print("项目名:{}".format(app.name))
        print("项目版本号:{}".format(__VERSION__))
        return True
    result = None
    p = Path("./config.ymal")
    if p.exists():
        result = _load_conf(str(p))
        app.config.update(result)
    result = None
    if args.config:
        result = _load_conf(args.config)
        app.config.update(result)
    result = _make_conf(args)
    app.config.update(result)
    _run_app()

if __name__ == '__main__':
    main()



