import json
import time

import openpyxl
import requests
from bs4 import BeautifulSoup
from lxml import etree

# https://www.alibaba.com/trade/search?n=38&keyword=suqian&indexArea=company_en&f1=y&viewType=L&Country=CN&Page=2
headers = {
    "Cookie": "_uab_collina=169405065959743810418285; ali_apache_id=33.50.230.51.1694050657601.299391.2; t=29688e0840912c48eabf7fbd4b3c9701; xman_us_f=x_l=1; xlly_s=1; _ga=GA1.1.191190536.1694051776; cna=vjSAHX5wOGECATtSPXFgwvQ/; _ga_GKMVMVMZNM=GS1.1.1694059454.2.1.1694059476.0.0.0; cookie2=1cb91aef8bf8e369f0afa7baa72168a2; _tb_token_=ee3b61aee8ebe; XSRF-TOKEN=e2c0b4d8-f8e0-484b-bc36-9992d66a70cc; acs_usuc_t=acs_rt=78a6f136bce746d096decfa0753de246; _samesite_flag_=true; xman_t=TBbxCy1GalAzAJ1HgOriENh4hkmOAU7dtq32qSlKuR7B+P3vpOBO3XthWtNRMpVS7G/WoOgQLD92SvZ94KRi06ERM1kOr8YJ; _csrf_token=1694239091207; JSESSIONID=8788332DE5E4E70E139AF187A2FE130F; ali_apache_track="
    "; ali_apache_tracktmp="
    "; _m_h5_tk=b955a517dd02ad4d595f5e6a0b2a4773_1694255893415; _m_h5_tk_enc=f60616484c0dff63195678fd30c3a74d; x5sec=7b22733b32223a2236363562303238393434623062643139222c22736370726f78793b32223a22666164653533333163616364346334623165393163616265326464356166306543507a56384b6347454f7170696263474d4c72393833394141773d3d227d; sc_g_cfg_f=sc_b_locale=en_US&sc_b_site=CN; xman_f=H6+olgW+A/jfA0469nvhalHYPpBjcTR4J7LNRs6LXHLtzLgMC4iZwsV1f9I5+hwl/aNUKIMHLK6ED8Qo8ErInJLSJ2llowfWoA0jo4GJqTtNoSgWwou+pw==; ug_se_c=organic_1694247807311; tfstk=dgVw5tjA71CN2ok0nYl4zFwZyuhtTbISoSijor4m5cmM1ieVgoqrnRaboj74fo_OkOUm0orIv5i_5jG43PwKcqG1ks74VDZXGPZXWJE7rCN1BjOq6jhcVg15NNUtMjb2q_1WZgcMHgs5N_MhbeehVSt7joXPBcS2lHkGqlm31qFkvL943DRDaU3ZIjC-YIA0TVzEqOReD2Y-ESewmKkiJ2o58w8iEsLV.; l=fBOB1yLuNvFINnFzBOfwourza77tAIRAguPzaNbMi9fPOaCD5GUfW1TpEE8kCnGVFsOXR3rNfwKXBeYBqIxTG2cT_7-CYMkmnhkSGN5..; isg=BGBg0SElEF-9QqxeowV3eJsYMW4yaUQz8Y4D-dpxC3sP1QD_gnwGwvTnbX3V5fwL",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69",
    "Referer": "https://www.alibaba.com/sw.js?v=2.13.23&_flasher_manifest_=https://s.alicdn.com/@xconfig/flasher_classic/manifest",
}
url = "https://www.alibaba.com/trade/search?n=38&SearchText=Suqian&indexArea=company_en&Country=CN"


# 详情链接内容
def get_data(url, companyName):
    item = {}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    xml_parser = etree.HTML(str(soup))
    elements = xml_parser.xpath(
        '//*[@id="8919138051"]/div/div/div/div[3]/div/table/tr[3]/td[2]/div/div/div'
    )
    if elements:
        money = elements[0].text
    else:
        money = ""
    address_em = xml_parser.xpath(
        '//*[@id="8919138051"]/div/div/div/div[3]/div/table/tr[1]/td[4]/div/div/div'
    )
    if address_em:
        address = address_em[0].text
    else:
        address = ""
    item["address"] = address
    if (
        str(address).lower().casefold().find("taizhou") >= 0
        or str(address).lower().casefold().find("su qian") >= 0
        or str(companyName).lower().casefold().find("taizhou") >= 0
    ):
        item["shi"] = "泰州市"
        if str(address).lower().casefold().find("economic") >= 0:
            item["qu"] = "经济开发区"
    else:
        item["shi"] = ""
        item["qu"] = ""
    if (
        str(address).lower().casefold().find("taizhou") >= 0
        or str(companyName).lower().casefold().find("hailing") >= 0
    ) and (
        str(address).lower().casefold().find("jiangsu") >= 0
        or str(address).lower().casefold().find("taizhou") >= 0
    ):
        item["shi"] = "泰州市"
        item["qu"] = "海陵区"
    elif (
        str(address).lower().casefold().find("gaogang") >= 0
        or str(companyName).lower().casefold().find("gaogang") >= 0
    ) and (
        str(address).lower().casefold().find("jiangsu") >= 0
        or str(address).lower().casefold().find("taizhou") >= 0
    ):
        item["shi"] = "泰州市"
        item["qu"] = "高港区"
    elif (
        str(address).lower().casefold().find("jiangyan") >= 0
        or str(companyName).lower().casefold().find("jiangyan") >= 0
    ) and (
        str(address).lower().casefold().find("jiangsu") >= 0
        or str(address).lower().casefold().find("taizhou") >= 0
    ):
        item["shi"] = "泰州市"
        item["qu"] = "姜堰区"
    elif (
        str(address).lower().casefold().find("xinghua") >= 0
        or str(companyName).lower().casefold().find("xinghua") >= 0
    ) and (
        str(address).lower().casefold().find("jiangsu") >= 0
        or str(address).lower().casefold().find("taizhou") >= 0
    ):
        item["shi"] = "泰州市"
        item["qu"] = "兴化市"
    elif (
        str(address).lower().casefold().find("jingjiang") >= 0
        or str(companyName).lower().casefold().find("jingjiang") >= 0
    ) and (
        str(address).lower().casefold().find("jiangsu") >= 0
        or str(address).lower().casefold().find("taizhou") >= 0
    ):
        item["shi"] = "泰州市"
        item["qu"] = "靖江市"
    elif (
        str(address).lower().casefold().find("taixing") >= 0
        or str(companyName).lower().casefold().find("taixing") >= 0
    ) and (
        str(address).lower().casefold().find("jiangsu") >= 0
        or str(address).lower().casefold().find("taizhou") >= 0
    ):
        item["shi"] = "泰州市"
        item["qu"] = "泰兴市"
    # ------------------------------

    # if str(address).lower().casefold().find("suqian") >= 0 or str(address).lower().casefold().find("su qian") >= 0 or \
    #         str(companyName).lower().casefold().find("suqian") >= 0:
    #     item['shi'] = "宿迁市"
    #     if str(address).lower().casefold().find("economic") >= 0:
    #         item['qu'] = "经济开发区"
    # else:
    #     item['shi'] = ""
    #     item['qu'] = ""
    # if (str(address).lower().casefold().find("shuyang") >= 0 or str(companyName).lower().casefold().find("shuyang") >= 0) and \
    #         (str(address).lower().casefold().find("jiangsu") >= 0 or str(address).lower().casefold().find("suqian") >= 0):
    #     item['shi'] = "宿迁市"
    #     item['qu'] = "沭阳县"
    # elif (str(address).lower().casefold().find("siyang") >= 0 or str(companyName).lower().casefold().find("siyang") >= 0) and \
    #         (str(address).lower().casefold().find("jiangsu") >= 0 or str(address).lower().casefold().find("suqian") >= 0):
    #     item['shi'] = "宿迁市"
    #     item['qu'] = "泗阳县"
    # elif (str(address).lower().casefold().find("sihong") >= 0 or str(companyName).lower().casefold().find("sihong") >= 0) and \
    #         (str(address).lower().casefold().find("jiangsu") >= 0 or str(address).lower().casefold().find("suqian") >= 0):
    #     item['shi'] = "宿迁市"
    #     item['qu'] = "泗洪县"
    # elif (str(address).lower().casefold().find("sucheng") >= 0 or str(companyName).lower().casefold().find("sucheng") >= 0) and \
    #         (str(address).lower().casefold().find("jiangsu") >= 0 or str(address).lower().casefold().find("suqian") >= 0):
    #     item['shi'] = "宿迁市"
    #     item['qu'] = "宿城区"
    # elif (str(address).lower().casefold().find("suyu") >= 0 or str(companyName).lower().casefold().find("suyu") >= 0) and \
    #         (str(address).lower().casefold().find("jiangsu") >= 0 or str(address).lower().casefold().find("suqian") >= 0):
    #     item['shi'] = "宿迁市"
    #     item['qu'] = "宿豫区"
    else:
        qu = str(address)
        item["qu"] = ""
    item["date"] = str(time.strftime("%Y%m%d"))
    item["money"] = money.replace("US$", "")
    return item


workbook = openpyxl.Workbook()
sheet = workbook.active
# 写入表头
sheet.append(
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
workbook.encoding = "utf-8"


# 获取页码
def get_page(url, page=-1):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find(
        "script", text=lambda text: text and "_PAGE_DATA_" in text
    ).text
    lines = script_tag.splitlines()
    PAGE_DATA = lines[2][28:-1]
    json_object = json.loads(PAGE_DATA)
    # print(json_object)
    pageCount = json_object.get("pageNavigationData").get("pageCount")
    # print(pageCount)
    if page != -1:
        offerList = json_object.get("offerResultData").get("offerList")
        for offer in offerList:
            url = "https:" + offer.get("action")  # url
            companyId = offer.get("companyId")  # 公司id
            companyName = offer.get("companyName")  # 公司名称
            goldYears = offer.get("goldYears")  # 经营时间
            provideProducts = offer.get("provideProducts")  # 主要产品描述
            replyAvgTime = offer.get("replyAvgTime")  # 响应时间
            tmp_name = str(url.split(".en")[0])
            name = tmp_name.split("//")[1]
            item = get_data(url, companyName)
            item["name"] = name
            item["company"] = companyName
            item["jingyingfanwei"] = provideProducts
            item["platform"] = "阿里巴巴国际站"
            item["customes_harbor"] = ""
            item["ie_type"] = ""
            item["destination_country"] = ""
            item["regulation_method"] = ""
            item["customes_code"] = ""
            item["transport_mode"] = ""
            item["hs_code"] = ""
            item["id"] = name
            if item["shi"] == "" and item["qu"] == "":
                pass
            else:
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
                sheet.append(line)
                print(line)
                workbook.save("alibaba_data3.xlsx")
        return None
    else:
        return pageCount


if __name__ == "__main__":
    # keywords = ["Suqian", "Shuyang", "Siyang", "Sihong", "Sucheng", "Suyu", "Jiangsu"]
    keywords = ["Hailing", "Gaogang", "Jiangyan", "Xinghua", "Jingjiang", "Taixing"]
    for key in keywords:
        url = f"https://www.alibaba.com/trade/search?n=38&SearchText={key}&indexArea=company_en&Country=CN"
        pages = get_page(url)
        # print(pages)
        for i in range(pages):
            page = i + 1
            url = f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&country=CN&keywords={key}&tab=supplier&&page={page}"
            print(f"{key},共{pages}页，正在处理第{page}页")
            try:
                get_page(url, page)
            except:
                pass


#########################################

# url2="https://abi.en.alibaba.com/company_profile.html?spm=a2700.supplier_search.0.0.120438a7TT5bNi"
# response=requests.get(url2,headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')
# # print(soup)
# # 使用lxml的etree模块创建一个XPath解析器
# xml_parser = etree.HTML(str(soup))
# # 使用XPath查询找到匹配的元素
# # 以下示例查找所有带有'class'属性为'my-class'的<div>元素
# elements = xml_parser.xpath('//*[@id="8919138051"]/div/div/div/div[3]/div/table/tr[3]/td[2]/div/div/div')
# # 打印找到的元素
# many=elements[0].text
# address_em=xml_parser.xpath('//*[@id="8919138051"]/div/div/div/div[3]/div/table/tr[1]/td[4]/div/div/div')
# address=address_em[0].text
