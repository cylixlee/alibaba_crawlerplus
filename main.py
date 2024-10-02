import pickle

from scrapy import cmdline

from src.conf import CACHE_DIR
from src.items import Catalog, Detail
from src.util import AdministrativeArea


def inspect_main() -> None:
    print("=== Catalogs ===")
    with open(CACHE_DIR / "catalogs.pickle", "rb") as f:
        data: dict[AdministrativeArea, list[Catalog]] = pickle.load(f)
    for area, catalogs in data.items():
        print(f"for area {area.name} ({len(catalogs)})")
        # for catalog in catalogs:
        #     print(f"\t{catalog}")

    print("=== Details ===")
    with open(CACHE_DIR / "details.pickle", "rb") as f:
        data: dict[AdministrativeArea, list[Detail]] = pickle.load(f)
    for area, details in data.items():
        print(f"for area {area.name} ({len(details)})")
        # for detail in details:
        #     print(f"\t{detail}")


def debugger_main() -> None:
    cmdline.execute("scrapy crawl detail".split())


if __name__ == "__main__":
    inspect_main()
    # debugger_main()
