import pathlib

import toml

__all__ = [
    # Path definitions
    "PROJECT_DIR",
    # Configuration object
    "CONFIG",
]

# Path definitions
PROJECT_DIR = pathlib.Path(__file__).parent.parent.absolute()

# Configurations
CONFIG = toml.load(PROJECT_DIR / "crawler-config.toml")
