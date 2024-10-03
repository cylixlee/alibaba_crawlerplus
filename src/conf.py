import pathlib

import toml

__all__ = ["PROJECT_DIR", "CONFIG"]

PROJECT_DIR = pathlib.Path(__file__).parent.parent.absolute()
CACHE_DIR = PROJECT_DIR / "cache"
SHEET_DIR = PROJECT_DIR / "sheet"

if not CACHE_DIR.exists():
    CACHE_DIR.mkdir(parents=True)
if not SHEET_DIR.exists():
    SHEET_DIR.mkdir(parents=True)

CONFIG = toml.load(PROJECT_DIR / "crawler-config.toml")
