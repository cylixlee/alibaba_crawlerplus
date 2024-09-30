import pickle

from scrapy import cmdline

from src.conf import CACHE_DIR
from src.items import Catalog
from src.util import AdministrativeArea


def inspect_main() -> None:
    # cmdline.execute("scrapy crawl catalog".split())
    with open(CACHE_DIR / "catalogs.pickle", "rb") as f:
        data: dict[AdministrativeArea, list[Catalog]] = pickle.load(f)
    for area, catalogs in data.items():
        print(f"=== for area {area.name} ({len(catalogs)})====")
        # for catalog in catalogs:
        #     print(catalog.name)


def debugger_main() -> None:
    cmdline.execute("scrapy crawl catalog".split())


if __name__ == "__main__":
    inspect_main()
    # debugger_main()
