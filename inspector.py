from main import CACHE_DIR, OffersCrawler


def _main():
    with open("inspect.txt", "w") as f:
        crawler = OffersCrawler.load(CACHE_DIR / "offers.pickle")
        for area, offers in crawler._offers.items():
            print(f"area {area.name} ({area.address}) with {len(offers)} offers.")
            print(f"====== for area {area.name} ({area.address}) ======:", file=f)
            for offer in offers:
                print(offer, file=f)


if __name__ == "__main__":
    _main()
