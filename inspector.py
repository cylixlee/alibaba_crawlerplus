from main import CACHE_DIR, PROJECT_DIR, DetailsCrawler, OffersCrawler

INSPECT_DIR = PROJECT_DIR / "inspect"


def _main():
    with open(INSPECT_DIR / "offers.txt", "w", encoding="utf8") as f:
        crawler = OffersCrawler.load(CACHE_DIR / "offers.pickle")
        for area, offers in crawler._offers.items():
            print(f"area {area.name} ({area.address}) with {len(offers)} offers.")
            print(f"====== for area {area.name} ({area.address}) ======:", file=f)
            for offer in offers:
                print(offer, file=f)
    with open(INSPECT_DIR / "details.txt", "w", encoding="utf8") as f:
        crawler = DetailsCrawler.load(CACHE_DIR / "details.pickle", None)
        for area, details in crawler._details.items():
            print(f"area {area.name} ({area.address}) with {len(details)} details.")
            print(f"====== for area {area.name} ({area.address}) ======:", file=f)
            for detail in details:
                print(detail, file=f)


if __name__ == "__main__":
    _main()
