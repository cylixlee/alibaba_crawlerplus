from src.addressing import administrative_address_of


def main():
    """
    Entrypoint of this program.

    Adopting ``if __name__ == "__main__"`` pattern and defining ``main()`` function
    simultaneously is **VERY** necessary.

    1. We use :var:`__name__` variable to detect whether the current module is executed
    as a script, not imported as lib.

    2. If we don't define the ``main`` function, any variable declared in the ``if``
    statement will become **GLOBAL**. That may cause some covert errors and bugs.

    Additionally, the `main()` function should not receive any arguments. Startup
    arguments should be written in configuration files.
    """

    # # Temporary code to fetch contents.
    # hub = DefaultRequestHub(timedelta(seconds=3))
    # url = AlibabaSearchUrl(
    #     "Hailing",
    #     tab=AlibabaSearchTab.Suppliers,
    #     country=AlibabaSupplierCountry.China,
    #     page=33,
    # )
    # print(url)
    # content = hub.request(url)

    # with open(DATA_DIR / "sample-nooffers.html", "w", encoding="utf8") as f:
    #     f.write(content)

    # # Temporary code to parse page.
    # with open(DATA_DIR / "sample-nooffers.html", encoding="utf8") as f:
    #     content = f.read()
    # parser = AlibabaPageJsonParser()
    # with open(DATA_DIR / "sample-nooffers.json", "w", encoding="utf8") as f:
    #     jsonobj = parser.parse(content)
    #     json.dump(jsonobj, f, indent=4)

    # # Temporary code to parse offers.
    # with open(DATA_DIR / "sample.json", encoding="utf8") as f:
    #     jsonobj = json.load(f)
    # parser = AlibabaJsonOffersParser()
    # offers = parser.parse(jsonobj)
    # with open(DATA_DIR / "sample-detail-urls.txt", "w", encoding="utf8") as f:
    #     f.writelines([str(offer) + "\n" for offer in offers])

    # # Temporary code to fetch detail page.
    # with open(DATA_DIR / "sample-detail.html", "w", encoding="utf8") as f:
    #     content = hub.request(offers[0].detail_url)
    #     f.write(content)

    # Temporary code to test addressing.
    print(
        administrative_address_of("Taizhou Gaogang District Miaorun Trading Co., Ltd")
    )


# Guideline recommended Main Guard
#
# This is VERY necessary to both adopting ``if __name__ == "__main__"`` pattern and
# self-defined ``main()`` function. About more detail, see :func:`main`.
if __name__ == "__main__":
    main()
