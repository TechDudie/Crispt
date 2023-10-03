import sys
from crispt import log as L, error as E

try:
    TARGET = sys.argv[1]
except:
    E("No input file specified, compilation failed", True)

L(f"Compile target set to {TARGET}")

try:
    with open(TARGET) as handle:
        FILE = handle.read()
except FileNotFoundError:
    E("Invalid file specified, compilation failed", True)