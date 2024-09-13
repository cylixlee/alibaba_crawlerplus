# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

import pandas as pd
from openpyxl import Workbook


class AlibabaPipeline:
    def __init__(self):
        # 创建excel，填写表头
        self.wb = Workbook()
        self.ws = self.wb.active
        # self.ws.append(['id', '名称', '公司', '市', '区', '(6个月)美元', '平台', '日期', '经营范围', ])  # 设置表头
        self.ws.append(
            [
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
        )
        self.file_time = time.strftime("%Y%m%d")

    def open_spider(self, spider):
        print("爬虫开始")

    def close_spider(self, spider):
        # 处理数据
        # 1.去重 2.只得到宿迁市 3.删除没营业额的数据
        data = pd.DataFrame(
            pd.read_excel(
                "alibaba_data_" + self.file_time + ".xlsx", "Sheet", dtype=str
            )
        )
        # 查看读取数据内容
        # print(data)
        # 查看基于['id', '名称']列去除重复行的数据
        wp = data.drop_duplicates(
            subset=["营业单位\n(中文名称)", "店铺名称"], inplace=False
        )
        # print(wp)
        # 删除数据表中含有空值的行
        # x = wp.dropna(axis=0, how='any')
        x = wp[wp["销售额"].notna()]
        # print(x)
        # 得到宿迁市信息
        data1 = x.loc[(x["市"] == "宿迁市")]
        # print(data1)
        # 将去除重复行的数据输出到excel表中,无索引
        data1.to_excel("alibaba_data_suqian" + self.file_time + ".xlsx", index=False)

        print("爬虫关闭")

    def process_item(self, item, spider):
        # line = [item['id'], item['name'], item['company'], item['shi'], item['qu'],
        # item['money'], item['platform'], item['date'], item['jingyingfanwei']]
        line = [
            item["date"],
            item["company"],
            item["name"],
            item["shi"],
            item["qu"],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            item["money"],
            "美元",
            item["platform"],
            item["jingyingfanwei"],
        ]
        self.ws.append(line)
        self.wb.save("alibaba_data_" + self.file_time + ".xlsx")
        return item
