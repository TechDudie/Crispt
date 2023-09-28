from requests import Session
from time import time as t

import meta
import assets

from utils import L

def run(session: Session):
    meta.run(session)
    L()
    assets.run(session)

if __name__ == "__main__":
    L("Download target set to Minecraft: Java Edition")

    start = t()

    session = Session()

    session.proxies.update({'http': 'socks5h://127.0.0.1:1050', 'https': 'socks5h://127.0.0.1:1050', 'socks5': 'socks5h://127.0.0.1:1050'})

    L("Download session initialized")

    run(session)

    time = str(int((t() - start) * 1000) / 1000)

    L(f"Done in {time}s!")