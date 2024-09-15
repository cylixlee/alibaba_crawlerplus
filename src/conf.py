import pathlib

import toml

__all__ = [
    "PROJECT_DIR",
    "DATA_DIR",
    "CONFIG",
]

PROJECT_DIR = pathlib.Path(__file__).parent.parent.absolute()
DATA_DIR = PROJECT_DIR / "data"

CONFIG = toml.load(PROJECT_DIR / "crawler-config.toml")
