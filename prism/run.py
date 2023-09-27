from requests import Session
from time import time as t

import meta
from utils import L

def run(session: Session):
    meta.run(session)

if __name__ == "__main__":
    L("Download target set to Prism Launcher")

    start = t()

    session = Session()

    L("Download session initialized")

    run(session)

    time = str(int((t() - start) * 1000) / 1000)

    L(f"Done in {time}s")