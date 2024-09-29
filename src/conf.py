import pathlib

import toml

__all__ = ["PROJECT_DIR", "CONFIG"]

PROJECT_DIR = pathlib.Path(__file__).parent.parent.absolute()

CONFIG = toml.load(PROJECT_DIR / "crawler-config.toml")
