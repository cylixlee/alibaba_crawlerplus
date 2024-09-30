from scrapy import cmdline


def main() -> None:
    cmdline.execute("scrapy crawl catalog".split())


if __name__ == "__main__":
    main()
