import pandas as pd

from main import CACHE_DIR, PROJECT_DIR, DetailsCrawler
from src.datamodels import AdministrativeArea, AlibabaCompanyDetail

SHEET_DIR = PROJECT_DIR / "sheets"
COMPLETE_COLUMNS = [
    "订单日期\n(格式：YYYYMMDD)",
    "营业单位\n(中文名称)",
    "店铺名称",
    "市",
    "区县",
    "指运港/抵运港\n(海关港口代码)",
    "进出口类型\n(I:进口，E:出口)",
    "运抵国/贸易国\n(海关国别代码)",
    "监管方式\n(海关监管代码)",
    "海关编码\n(申报海关代码)",
    "运输方式\n(运输方式代码)",
    "HS编码\n(10位商品编码)",
    "销售额",
    "币种\n(币种代码)",
    "平台名称\n(数据来源平台名称)",
    "经营范围",
]


def main() -> None:
    if not SHEET_DIR.exists():
        SHEET_DIR.mkdir(parents=True)
    cache_path = CACHE_DIR / "details.pickle"
    cache = DetailsCrawler.load(cache_path, None)
    for area, details in cache._details.items():
        _write_area(area, details)


def _write_area(area: AdministrativeArea, details: list[AlibabaCompanyDetail]) -> None:
    sheet = pd.DataFrame(
        columns=[
            "营业单位\n(中文名称)",
            "店铺名称",
            "市",
            "区县",
            "销售额",
            "经营范围",
        ]
    )
    for detail in details:
        if detail.administrative_address:
            city = detail.administrative_address[0]
            if len(detail.administrative_address) > 1:
                district = detail.administrative_address[1]
            else:
                district = ""
        else:
            city = ""
            district = ""
        sheet.loc[len(sheet)] = [
            detail.name,
            detail.domain,
            city,
            district,
            detail.bill,
            detail.provided_products,
        ]
    for index, column in enumerate(COMPLETE_COLUMNS):
        if column not in sheet.columns:
            match column:
                case "币种\n(币种代码)":
                    sheet.insert(index, column, "美元")
                case "平台名称\n(数据来源平台名称)":
                    sheet.insert(index, column, "阿里巴巴国际站")
                case _:
                    sheet.insert(index, column, "")
    sheet.to_excel(SHEET_DIR / f"{area.name}.xlsx", index=False)


if __name__ == "__main__":
    main()
