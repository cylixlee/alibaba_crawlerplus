import pathlib
import pickle
import weakref
from collections import OrderedDict

import pandas as pd

from src.conf import CACHE_DIR, SHEET_DIR
from src.items import Detail
from src.util import AdministrativeArea


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

    def fillcolumn(self, column: str, value: str) -> None:
        assert column in self._headers.keys(), "unrecognized key"
        self._frame[self._headers[column]] = value


def sheetwriter_main() -> None:
    headers = OrderedDict(
        orderdate="订单日期\n（格式：YYYYMMDD）",
        name="营业单位\n（中文名称）",
        domain="店铺名称",
        city="市",
        district="区县",
        port="指运港/抵运岗\n（海关港口代码）",
        typ="进出口类型\n(I:进口，E:出口)",
        destination="运抵国/贸易国\n（海关国别代码）",
        supervise="监管方式\n（海关监管代码）",
        code="海关编码\n（申报海关代码）",
        transport="运输方式\n（运输方式代码）",
        hs="HS编码\n（10位商品编码）",
        orders="订单数",
        bills="销售额",
        currency="币种\n（币种代码）",
        platform="平台名称\n（数据来源平台名称）",
        provide="经营范围",
    )

    with open(CACHE_DIR / "details.pickle", "rb") as f:
        data: dict[AdministrativeArea, list[Detail]] = pickle.load(f)

    original = SHEET_DIR / "未筛选"
    filtered = SHEET_DIR / "已筛选"

    if not original.exists():
        original.mkdir(parents=True)
    if not filtered.exists():
        filtered.mkdir(parents=True)

    for area, details in data.items():
        u = SheetWriter(original / f"{area.name}.xlsx", headers)
        f = SheetWriter(filtered / f"{area.name}.xlsx", headers)
        for detail in details:
            if detail.administrative_address:
                city = detail.administrative_address[0]
                if len(detail.administrative_address) > 1:
                    district = detail.administrative_address[1]
                else:
                    district = ""
                f.write(
                    name=detail.name,
                    domain=detail.domain,
                    city=city,
                    district=district,
                    orders=detail.orders,
                    bills=detail.bill,
                    provide=detail.provided_products,
                )
            else:
                city = ""
                district = ""
            u.write(
                name=detail.name,
                domain=detail.domain,
                city=city,
                district=district,
                orders=detail.orders,
                bills=detail.bill,
                provide=detail.provided_products,
            )
        u.fillcolumn("currency", "美元")
        u.fillcolumn("platform", "阿里巴巴国际站")
        f.fillcolumn("currency", "美元")
        f.fillcolumn("platform", "阿里巴巴国际站")


if __name__ == "__main__":
    sheetwriter_main()
