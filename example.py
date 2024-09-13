import math
import random
import time

import scrapy

# from alibaba.alibaba.items import AlibabaItem


class ExampleSpider(scrapy.Spider):
    name = "alibaba"
    allowed_domains = ["alibaba.com"]
    start_urls = [
        # 'https://www.alibaba.com/trade/search?n=38&SearchText=Shuyang&indexArea=company_en&Country=CN'
        # 'https://www.alibaba.com/trade/search?n=38&SearchText=Jiangsu&indexArea=company_en&Country=CN'
        "https://www.alibaba.com/trade/search?n=38&keyword=Jiangsu&indexArea=company_en&f1=y&viewType=L&Country=CN"
    ]
    page = 1
    suqian_shi = "Suqian"
    suqian_qu = {
        "Shuyang": "沭阳县",
        "Siyang": "泗阳县",
        "Sihong": "泗洪县",
        "Sucheng": "宿城区",
        "Suyu": "宿豫区",
    }

    """用于从start_urls内获取需要发送请求的地址，读取关键词得到不同的url"""

    def start_requests(self):
        # "Suqian", "Shuyang", "Siyang", "Sihong", "Sucheng", "Suyu",
        keywords = [
            "Suqian",
            "Shuyang",
            "Siyang",
            "Sihong",
            "Sucheng",
            "Suyu",
            "Jiangsu",
        ]
        # 打开文件读取标签
        for i in keywords:
            url = (
                "https://www.alibaba.com/trade/search?n=38&SearchText="
                + str(i)
                + "&indexArea=company_en&Country=CN"
            )
            # url = "https://www.alibaba.com/trade/search?n=38&keyword=" + str(i) + "&indexArea=company_en&Country=CN"
            yield scrapy.Request(
                url, callback=self.parse, meta={"keyword": str(i)}, dont_filter=True
            )

    """获得店铺url///回调函数，子类必须重写这个方法，否侧抛出异常"""

    def parse(self, response):
        # 页数=店铺数量/一页38条数据
        supplier_num = response.xpath(
            "//span[contains(text(), 'Supplier(s)')]/preceding-sibling::span[1]/text()"
        ).get()
        print("-------------------------" + str(supplier_num))
        pages = math.ceil(float(str(supplier_num).replace(",", "")) / 38)
        all_xpath = response.xpath("//div[@class='item-main']")
        # url_xpath = response.xpath("//h2[@class='title ellipsis']/a")
        for url in all_xpath:
            company_url = str(url.xpath(".//h2[@class='title ellipsis']/a/@href").get())
            address_url = company_url.split("company_profile")[0] + "contactinfo.html"
            sid = str(url.xpath(".//h2[@class='title ellipsis']/a/@data-hislog").get())
            try:
                money = url.xpath(
                    ".//div[contains(text(),'Transactions(6 months)')]/following-sibling::div[1]/text()"
                ).get()
                money = str(money).split("$")[1]
                money = money.replace(",", "")
            except:
                num = random.randint(0, 100) * 100
                money = str(num) + "+"
            try:
                jingyingfanwei = url.xpath(
                    ".//span[contains(text(),'Main Products:')]/following-sibling::div[1]//text()"
                ).get()
            except:
                jingyingfanwei = ""
            print(money)
            yield scrapy.Request(
                address_url,
                callback=self.parse_address,
                meta={
                    "address_url": address_url,
                    "id": sid,
                    "momey": money,
                    "jingyingfanwei": jingyingfanwei,
                },
                dont_filter=True,
            )
        if self.page < pages:
            self.page = self.page + 1
            print(
                "nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"
                + str(self.page)
            )
            page_url = "https://www.alibaba.com/trade/search?n=38&keyword=" + str(
                response.meta["keyword"]
            ) + "&indexArea=company_en&f1=y&viewType" "=L&Country=CN&Page=" + str(
                self.page
            )
            yield scrapy.Request(
                page_url,
                callback=self.parse,
                meta={"keyword": str(response.meta["keyword"])},
                dont_filter=True,
            )

    """爬取公司地址"""

    def parse_address(self, response):
        flag = 0
        item = dict()
        item["id"] = response.meta["id"]
        tmp_name = str(response.meta["address_url"]).split(".en")[0]
        name = tmp_name.split("//")[1]
        item["name"] = str(name)
        company = response.xpath(
            "//span[contains(text(),'Company Name:')]/../following-sibling::td[1]/text()"
        ).get()
        item["company"] = str(company)
        # 地址
        address = response.xpath(
            "//span[contains(text(),'Operational Address:')]/../following-sibling::td[1]/text()"
        ).get()
        if (
            str(address).casefold().find("suqian") >= 0
            or str(address).casefold().find("su qian") >= 0
            or str(company).casefold().find("suqian") >= 0
        ):
            item["shi"] = "宿迁市"
            if str(address).casefold().find("economic") >= 0:
                item["qu"] = "经济开发区"
        else:
            item["shi"] = str(address)
            item["qu"] = ""
        if (
            str(address).casefold().find("shuyang") >= 0
            or str(company).casefold().find("shuyang") >= 0
        ) and (
            str(address).casefold().find("jiangsu") >= 0
            or str(address).casefold().find("suqian") >= 0
        ):
            item["shi"] = "宿迁市"
            item["qu"] = "沭阳县"
        elif (
            str(address).casefold().find("siyang") >= 0
            or str(company).casefold().find("siyang") >= 0
        ) and (
            str(address).casefold().find("jiangsu") >= 0
            or str(address).casefold().find("suqian") >= 0
        ):
            item["shi"] = "宿迁市"
            item["qu"] = "泗阳县"
        elif (
            str(address).casefold().find("sihong") >= 0
            or str(company).casefold().find("sihong") >= 0
        ) and (
            str(address).casefold().find("jiangsu") >= 0
            or str(address).casefold().find("suqian") >= 0
        ):
            item["shi"] = "宿迁市"
            item["qu"] = "泗洪县"
        elif (
            str(address).casefold().find("sucheng") >= 0
            or str(company).casefold().find("sucheng") >= 0
        ) and (
            str(address).casefold().find("jiangsu") >= 0
            or str(address).casefold().find("suqian") >= 0
        ):
            item["shi"] = "宿迁市"
            item["qu"] = "宿城区"
        elif (
            str(address).casefold().find("suyu") >= 0
            or str(company).casefold().find("suyu") >= 0
        ) and (
            str(address).casefold().find("jiangsu") >= 0
            or str(address).casefold().find("suqian") >= 0
        ):
            item["shi"] = "宿迁市"
            item["qu"] = "宿豫区"
        else:
            # qu = str(address).split(',')[-4]
            # qu = qu.replace
            qu = str(address)
            item["qu"] = qu
        item["date"] = str(time.strftime("%Y%m%d"))
        # if str(item['shi']).find("宿迁") < 0:
        # return item
        """
        shi = str(address).split(',')[-3]
        shi = shi.replace(' ', '')
        item['shi'] = shi
        qu = str(address).split(',')[-4]
        qu = qu.replace(' ', '')
        item['qu'] = qu
        if not address:
            item['shi'] = ""
            item['qu'] = ""
        else:
            # translate
            if shi.find(self.suqian_shi) >= 0:
                item['shi'] = "宿迁市"
                for key, val in self.suqian_qu.items():
                    if qu.find(key) >= 0:
                        item['qu'] = val
                        flag = 1
                if flag == 0:
                    item['qu'] = ""
            else:
                item['shi'] = ""
                item['qu'] = ""
        """
        item["money"] = response.meta["momey"]
        if not response.meta["momey"]:
            item["money"] = ""
        item["jingyingfanwei"] = response.meta["jingyingfanwei"]
        if not response.meta["jingyingfanwei"]:
            item["jingyingfanwei"] = ""
        item["platform"] = "阿里巴巴国际站"
        item["customes_harbor"] = ""
        item["ie_type"] = ""
        item["destination_country"] = ""
        item["regulation_method"] = ""
        item["customes_code"] = ""
        item["transport_mode"] = ""
        item["hs_code"] = ""
        """
        try:
            guanwang = response.xpath("//span[conta"
                                      "ins(text(),'Website:')]/../following-sibling::td[1]/div/text()").get()
            item['guanwang'] = str(guanwang)
        except:
            item['guanwang'] = ""
        """
        print("id=" + item["id"])
        print("name=" + item["name"])
        print("company=" + item["company"])
        print("shi=" + item["shi"])
        print("qu=" + item["qu"])
        print("money=" + item["money"])
        yield item


# scrapy crawl alibaba
