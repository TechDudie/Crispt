from datetime import datetime
from json import load as J
from os import mkdir, remove, walk
from os.path import isfile
from pathlib import Path
from requests import Session
from shutil import move as M
from zipfile import ZipFile

def L(message="", level="INFO"): # log
    print(f"[Crispt] [{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[11:-3]}] [{level}] {message}")

def E(message, fatal=False): # error
    L(message)
    if fatal:
        exit()

def W(file, data): # write file
    with open(file, "wb") as handle:
        handle.write(data)
    L(f"Download saved to {file}")

def D(session: Session, url, file): # download url
    L(f"Downloading {url}")
    if isfile(file):
        L(f"File {file} already found cached")
        return
    content = session.get(url).content
    W(file, content)

def Z(file): # unzip file
    with ZipFile(file, "r") as handle:
        handle.extractall(".")
    remove(file)

def I(dir): # get directory info
    return (sum([len(files) for _, _, files in walk(dir)]), int(sum(f.stat().st_size for f in Path(dir).glob('**/*') if f.is_file()) / 104857.6) / 10)

def F(dir): # create directory
    try:
        mkdir(dir)
    except FileExistsError:
        pass