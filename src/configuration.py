"""
Configurations of the crawler.

The crawler needs some metadata to parse, save and load data. Instead of hard-coding them,
decoupling them into configuration files is a more flexible and common practice.

This module contains global variables of pathlib created absolute paths (since relative
paths in Python is hard to manage), and the unique CONFIG variable loaded from TOML.
"""

import pathlib

import yaml

__all__ = [
    "PROJECT_DIR",
    "DATA_DIR",
    "CONFIG",
]


def __load_config(path: pathlib.Path):
    with open(path, encoding="utf8") as f:
        return yaml.load(f, Loader=yaml.Loader)


PROJECT_DIR = pathlib.Path(__file__).parent.parent.absolute()
DATA_DIR = PROJECT_DIR / "data"

CONFIG = __load_config(PROJECT_DIR / "crawler-config.yaml")
