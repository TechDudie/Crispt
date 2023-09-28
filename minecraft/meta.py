from requests import Session

from utils import L, M, D, Z, I

META_URL = "https://codeload.github.com/PrismLauncher/meta-launcher/zip/refs/heads/master"

def run(s: Session):
    L("")
    L("======== Downloading Minecraft Metadata ========")
    L("")
    D(s, META_URL, "meta.zip")
    Z("meta.zip")
    M("meta-launcher-master", "meta")
    info = I("meta")
    L(f"Extracted {info[0]} files, {info[1]} MB")
    L("")
    L("======== Finished Downloading Minecraft Metadata ========")
    L("")