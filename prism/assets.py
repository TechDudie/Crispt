import sys, os
from requests import Session
from multiprocessing import Pool, cpu_count
from functools import partial

from utils import L, J, D, F

ASSET_URL = "https://resources.download.minecraft.net/"
VERSION_INDEX = "meta/net.minecraft/{}.json"
ASSET_INDEX = "assets/indexes/{}.json"

def path(hash):
    return f"assets/objects/{hash[:2]}/{hash}"

def url(hash):
    return f"{ASSET_URL}objects/{hash[:2]}/{hash}"

def data(hash):
    return (url(hash), path(hash))

def get_asset(s: Session, dataset: list, target: list):
    item = dataset.index(target)
    L(f"> Asset #{item}")
    D(s, target[0], target[1])

def run(s: Session, version="1.20.2"):
    L("")
    L(f"======== Downloading Minecraft Assets ({version}) ========")
    L("")

    F("assets")
    F("assets/indexes")
    F("assets/objects")

    with open(VERSION_INDEX.format(version)) as handle:
        json = J(handle)
    id = json["assetIndex"]["id"]
    url = json["assetIndex"]["url"]
    D(s, url, f"assets/indexes/{id}.json")

    with open(ASSET_INDEX.format(id)) as handle:
        assets = J(handle)["objects"].values()

    size = 0
    for asset in assets:
        size += asset["size"]
    size = int(size / 104857.6) / 10
    L(f"Downloading {len(assets)} assets, {size} MB")

    dataset = []
    for asset in assets:
        hash = asset["hash"]
        F(f"assets/objects/{hash[:2]}")
        dataset.append(data(hash))
    
    cpu = cpu_count()
    L(f"{cpu} cores avaliable, utilizing {cpu} cores")
    pool = Pool(cpu)
    func = partial(get_asset, s, dataset)
    output = pool.map(func, dataset)
    pool.close()
    pool.join()

if __name__ == "__main__":
    run(Session())