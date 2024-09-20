"""
An inspector to verify the correctness of cache.

This project adopts the resumable technique: whenever the program is terminated, the data
will be cached and reused in the next run. We can use this script to verify if there's
some data cached and what are they.
"""

from main import CACHE_DIR, PROJECT_DIR, DetailsCrawler, OffersCrawler

INSPECT_DIR = PROJECT_DIR / "inspect"


def main():
    # creates inspect directory if not exists.
    if not INSPECT_DIR.exists():
        INSPECT_DIR.mkdir(parents=True)

    # write offers.
    with open(INSPECT_DIR / "offers.txt", "w", encoding="utf8") as f:
        crawler = OffersCrawler.load(CACHE_DIR / "offers.pickle")
        for area, offers in crawler.offers.items():
            print(f"area {area.name} ({area.address}) with {len(offers)} offers.")
            print(f"====== for area {area.name} ({area.address}) ======:", file=f)
            for offer in offers:
                print(offer, file=f)

    # write details.
    with open(INSPECT_DIR / "details.txt", "w", encoding="utf8") as f:
        crawler = DetailsCrawler.load(CACHE_DIR / "details.pickle", None)
        for area, details in crawler.details.items():
            print(f"area {area.name} ({area.address}) with {len(details)} details.")
            print(f"====== for area {area.name} ({area.address}) ======:", file=f)
            for detail in details:
                print(detail, file=f)


if __name__ == "__main__":
    main()
