from typing import override

from .abstract import AbstractDataParser

__all__ = ["ComposeParser"]


class ComposeParser(AbstractDataParser):
    """
    A utility parser that compose several parsers.

    For example, if the parser is composed of two parsers: a Html2JsonParser and a
    Json2ObjectParser, then it parses JSON from the HTML passed in as method argument
    (through the first parser), then parses objects from JSON returned by the first parser
    (through the second parser).
    """

    def __init__(self, *parsers: AbstractDataParser) -> None:
        self._parsers = parsers

    @override
    def parse(self, *args, **kwargs) -> object:
        result = self._parsers[0].parse(*args, **kwargs)
        for parser in self._parsers[1:]:
            result = parser.parse(result)
        return result
