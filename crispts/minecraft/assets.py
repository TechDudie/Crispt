from lib.crispt import create_directory, download, log, load_json, multidownload

ASSET_URL = "https://resources.download.minecraft.net/"
VERSION_INDEX = "meta/net.minecraft/{}.json"
ASSET_INDEX = "assets/indexes/{}.json"

def run(s, version="1.20.2"):
    log("")
    log(f"======== Downloading Minecraft {version} Assets ========")
    log("")

    create_directory("assets")
    create_directory("assets/indexes")
    create_directory("assets/objects")

    with open(VERSION_INDEX.format(version)) as handle:
        json = load_json(handle)
    id = json["assetIndex"]["id"]
    url = json["assetIndex"]["url"]
    download(s, url, f"assets/indexes/{id}.json")
    with open(ASSET_INDEX.format(id)) as handle:
        assets = load_json(handle)["objects"].values()

    size = 0
    for asset in assets:
        size += asset["size"]
    size = int(size / 104857.6) / 10
    log(f"Downloading {len(assets)} assets, {size} MB")

    files = []
    for asset in assets:
        hash = asset["hash"]
        create_directory(f"assets/objects/{hash[:2]}")
        files.append((f"assets/objects/{hash[:2]}/{hash}", f"{ASSET_URL}{hash[:2]}/{hash}"))
    
    multidownload(s, files)

    log("")
    log(f"======== Finished Downloading Minecraft {version} Assets ========")
    log("")
