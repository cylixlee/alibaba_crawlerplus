import pathlib
import weakref
from collections import OrderedDict

import pandas as pd

from src.conf import PROJECT_DIR


class SheetWriter(object):
    _path: pathlib.Path
    _headers: OrderedDict[str, str]
    _frame: pd.DataFrame
    _finalizer: weakref.finalize

    def __init__(self, path: pathlib.Path, headers: OrderedDict[str, str]) -> None:
        self._path = path
        self._headers = headers
        self._frame = pd.DataFrame(columns=headers.values())

        # write to file when program exits
        def finalizer(frame: pd.DataFrame, path: pathlib.Path) -> None:
            frame.to_excel(path, index=False)

        self._finalizer = weakref.finalize(self, finalizer, self._frame, self._path)

    def write(self, **kwargs: str) -> None:
        default_values = ["" for _ in range(len(self._headers))]
        for key, value in kwargs.items():
            inserted = False
            for i, header in enumerate(self._headers.keys()):
                if header == key:
                    default_values[i] = value
                    inserted = True
                    break
            assert inserted, "unrecognized key"
        self._frame.loc[len(self._frame.index)] = default_values

    def fill_column(self, column: str, value: str) -> None:
        assert column in self._headers.keys(), "unrecognized key"
        self._frame[self._headers[column]] = value


def sheetwriter_main() -> None:
    headers = OrderedDict(
        apple="苹果",
        pear="梨",
        something="一些事",
    )

    writer = SheetWriter(PROJECT_DIR / "sample.xlsx", headers)
    writer.write(apple="我爱吃")
    writer.write(something="wrong")
    writer.fill_column("pear", "阿里巴巴国际站")


if __name__ == "__main__":
    sheetwriter_main()
