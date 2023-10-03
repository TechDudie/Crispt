from lib.crispt import *

def run(s):
    download = generate_download_func(s)
    
    log("")
    log("======== Downloading Minecraft Metadata ========")
    log("")
    download(s, "https://codeload.github.com/PrismLauncher/meta-launcher/zip/refs/heads/master", "meta.zip")
    unzip("meta.zip")
    move("meta-launcher-master", "meta")
    log("")
    log("======== Finished Downloading Minecraft Metadata ========")
    log("")