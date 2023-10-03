from ctypes import c_uint16
from datetime import datetime
from functools import partial
from json import load as _load_json, dump as _dump_json
from math import ceil
from multiprocessing import cpu_count, Lock, Manager, Pool, Value
from os import get_terminal_size,  mkdir, remove, sep, walk
from os.path import isfile, join as join
from pathlib import Path
from requests import Session
from shutil import Error as ShutilError, move as _move
from sys import stdout
from warnings import filterwarnings
from zipfile import ZipFile

filterwarnings("ignore")

HOME = str(Path.home())
TERMINAL_WIDTH = get_terminal_size()[0]

# Helper function to write all files in "~/.crispt"
_root = partial(join, HOME, ".crispt")

# Logging utilities

def log(message: str, level="INFO"):
    """
    Log a message in the console.

    Args:
        message (str): the message to log
        level (str): severity level (defaults to `INFO`)
    
    """
    print(f"[Crispt] [{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[11:-3]}] [{level}] {message}")

def error(message: str, fatal=False):
    """
    Show an error message in the console.

    Args:
        message (str): the message to error
        fatal(bool): whether or not to terminate execution (defaults to `False`)
    
    """
    log(message, level="ERROR")
    if fatal:
        exit()

# File manipulation utilities

def read(file: str) -> str:
    """
    Read a file.

    Args:
        file (str): the filename to read from
            
    Returns:
        data (str): the data
    
    """

    with open(_root(file)) as handle:
       return handle.read()

def write(file: str, data: bytes):
    """
    Write a bytestring to a file.

    Args:
        file (str): the filename to write to
        data (bytes): the data to write
    
    """
    
    with open(_root(file), "wb") as handle:
        handle.write(data)
    
    log(f"File saved to {file}")

def move(src, dst):
    """
    Move/rename a file or directory.

    Args:
        src (str): the name of the source file
        dst (str): the name of the destination file
    
    """

    try:
        _move(src, dst)
    except ShutilError:
        remove(dst)
        _move(src, dst)

def unzip(file):
    """
    Unzip a file.

    Args:
        file (str): the filename of the zip file
    
    """

    with ZipFile(file, "r") as handle:
        handle.extractall(".")
    remove(file)
    info = directory_info("meta")
    log(f"Extracted {info[0]} files, {info[1]} MB")

# JSON manipulation utilities

def read_json(file: str) -> str:
    """
    Read a JSON file and return a dictionary.

    Args:
        file (str): the filename to read from
    
    Returns:
        json_data (dict): the JSON data
    
    """

    with open(_root(file)) as handle:
        return _load_json(handle)

def write_json(file: str, data: dict):
    """
    Write a dictionary to a JSON file.

    Args:
        file (str): the filename to write to
        data (dict): the dictionary to write
    
    """

    with open(_root(file), "w") as handle:
        _dump_json(data, handle, indent=4)

# File download utilities

def download(session: Session, url, file, quiet=False):
    """
    Download a file with a given `requests.Session`.

    Args:
        session (requests.Session): the session object to use
        url (str): the URL to download
        file (str): the filename to write to
        quiet (bool): whether or not to download silently
    
    """

    if isfile(file):
        if not quiet:
            log(f"File {file} already found cached")
        return
    
    if quiet:
        log(f"Downloading {url}")

    with open(_root(file), "wb") as handle:
        handle.write(session.get(url).content)
    
    if quiet:
        log(f"File saved to {file}")

def _download_worker(s: Session, progress: Value, progress_lock: Lock, data: list, target: tuple):
    """
    Download worker to be used in `crispt.multidownload`.

    Args:
        s (requests.Session): the session object to use
        progress (multiprocessing.Value): the progress value object to increment
        progress_lock (multiprocessing.Lock): the progress lock object to use
        data (list): the full list of download targets, ex.
            ```
            [
                ("https://example.com/download/foo", "foo.txt"),
                ("https://example.com/download/bar", "bar.txt")
            ]
            ```
        target (tuple): the tuple specifying the target url to download from
    
    """

    percentage = progress.value / len(data)
    stdout.write("\033[K")
    log(f"> Download #{data.index(target)}".ljust(TERMINAL_WIDTH - 114, " ") + f"{f'{progress.value}/{len(data)}'.rjust(9, ' ')} {str(ceil(percentage * 100)).rjust(2, ' ')}% [{('█' * ceil(percentage * 64)).ljust(64, ' ')}]")
    download(s, target[0], target[1], False)
    with progress_lock:
        progress.value += 1

def multidownload(s: Session, files: list):
    """
    Download multiple files at once by utilizing all avaliable cores.

    Args:
        s (requests.Session): the session object to use
        files (list): the list of file tuples to download, ex.
            ```
            [
                ("https://example.com/download/foo", "foo.txt"),
                ("https://example.com/download/bar", "bar.txt")
            ]
            ```
    
    """

    cpu = cpu_count()
    log(f"{cpu} cores avaliable, utilizing {cpu} cores")
    manager = Manager()
    progress = manager.Value(c_uint16, 0)
    progress_lock = manager.Lock()
    pool = Pool(cpu)
    func = partial(_download_worker, s, progress, progress_lock, files)
    print()
    pool.map(func, files)
    pool.close()
    pool.join()

def generate_download_func(session: Session):
    """
    Generate a partial function given a `requests.Session`.

    Args:
        session (requests.Session): the session object to use
    
    Returns:
        download (function): the download function with partial application of the Session
    
    """
    return (partial(download, session), partial(multidownload, session))

# Directory manipulation utilities

def create_directory(dir):
    """
    Create a directory.

    Args:
        dir (str): the name of the directory
    
    """

    try:
        mkdir(dir)
    except FileExistsError:
        pass

def directory_info(dir):
    """
    Unzip a file.

    Args:
        dir (str): the name of the directory
    
    """

    return (
        sum([len(files) for _, _, files in walk(dir)]),
        int(sum(f.stat().st_size for f in Path(dir).glob('**/*') if f.is_file()) / 104857.6) / 10
    )

# Complete initialization

create_directory(_root())