import shutil

from inspector import INSPECT_DIR
from main import PROJECT_DIR
from writer import SHEET_DIR


def main() -> None:
    # clean outputs.
    if INSPECT_DIR.exists():
        print(f"CLEAN {INSPECT_DIR}")
        shutil.rmtree(str(INSPECT_DIR))
    if SHEET_DIR.exists():
        print(f"CLEAN {SHEET_DIR}")
        shutil.rmtree(str(SHEET_DIR))

    # clean Python bytecodes
    for cache_dir in PROJECT_DIR.glob("**/__pycache__"):
        cache_dir = cache_dir.absolute()
        if ".venv" in str(cache_dir):
            continue
        print(f"CLEAN {cache_dir}")
        shutil.rmtree(str(cache_dir))


if __name__ == "__main__":
    main()
