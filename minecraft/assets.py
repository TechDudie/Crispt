from ctypes import c_uint16
from functools import partial
from math import floor, ceil
from multiprocessing import cpu_count, Manager, Pool
from os import get_terminal_size
from warnings import filterwarnings

filterwarnings("ignore")

from requests import Session

from utils import L, J, D, F

ASSET_URL = "https://resources.download.minecraft.net/"
VERSION_INDEX = "meta/net.minecraft/{}.json"
ASSET_INDEX = "assets/indexes/{}.json"

TERMINAL_WIDTH = get_terminal_size()[0]

def path(hash):
    return f"assets/objects/{hash[:2]}/{hash}"

def url(hash):
    return f"{ASSET_URL}{hash[:2]}/{hash}"

def data(hash):
    return (url(hash), path(hash))

def get_asset(s: Session, progress, progress_lock, data: list, target: list):
    percentage = progress.value / len(data)
    L(f"> Asset #{data.index(target)}".ljust(TERMINAL_WIDTH - 111, " ") + f"{f'{progress.value}/{len(data)}'.rjust(9, ' ')} {str(ceil(percentage * 100)).rjust(2, ' ')}% [{('█' * floor(percentage * 64)).ljust(64, ' ')}]")
    D(s, target[0], target[1])
    with progress_lock:
        progress.value += 1

def run(s: Session, version="1.20.2"):
    L("")
    L(f"======== Downloading Minecraft {version} Assets ========")
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
    manager = Manager()
    progress = manager.Value(c_uint16, 0)
    progress_lock = manager.Lock()
    pool = Pool(cpu)
    func = partial(get_asset, s, progress, progress_lock, dataset)
    pool.map(func, dataset)
    pool.close()
    pool.join()

    L("")
    L(f"======== Finished Downloading Minecraft {version} Assets ========")
    L("")