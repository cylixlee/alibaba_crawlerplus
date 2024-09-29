from scrapy import Field, Item

__all__ = ["CatalogItem"]


class CatalogItem(Item):
    """
    An item from the catalog of search results. In this project, some information about a
    supplier (manufacturer, or business entity).

    Currently this class maintains these fields:

    - :field:`detail_url`: The URL to the supplier's detail page.
    - :field:`domain`: The last domain name of URL, used as account names of suppliers.
    - :field:`name`: The full name of the supplier.
    - :field:`provided_products`: The business range of the supplier.

    all of which are of type :type:`str`.
    """

    detail_url = Field()
    domain = Field()
    name = Field()
    provided_products = Field()
