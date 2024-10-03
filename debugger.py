from scrapy import cmdline


def debugger_main() -> None:
    cmdline.execute("scrapy crawl detail".split())


if __name__ == "__main__":
    debugger_main()
