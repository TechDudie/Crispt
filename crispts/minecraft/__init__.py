from requests import Session

import meta
import assets

from lib.crispt import log

def run(session: Session):
    meta.run(session)
    log()
    assets.run(session)