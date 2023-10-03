from argparse import ArgumentParser
from re import compile
from time import time as t
from warnings import filterwarnings

filterwarnings("ignore")

from requests import Session

from lib.crispt import log

CRISPT_NAMESPACE = compile("[^a-z]+")

def sanitize_namespace(namespace):
    return CRISPT_NAMESPACE.sub("", namespace)

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="crispt",
        
        description="The package manager that teachers approve of."
    )

    parser.add_argument("-p", "--proxy", metavar="proxy", type=str, help="run Crispt with a proxy")
    parser.add_argument("-t", "--tor", action="store_true", help="run Crispt through Tor")

    parser.add_argument("action", choices=[
        "download",
        "launch"
    ], help="Action")

    parser.add_argument("application", metavar="application", nargs="?", default="", type=str, help="Application to select")

    args = parser.parse_args()
    print(args)

    session = Session()

    if args.proxy is not None:
        session.proxies.update({
            "http": f"socks5h://{args.proxy}",
            "https": f"socks5h://{args.proxy}",
            "socks5": f"socks5h://{args.proxy}"
        })
    
    log("Download target set to Minecraft: Java Edition")
    start = t()
    
    match args.action:
        case "download":
            exec(f"import crispts.{sanitize_namespace(args.application)}")
        case "launch":
            pass
    
    time = str(int((t() - start) * 1000) / 1000)
    log(f"Done in {time}s!")