import pandas as pd

# 读取Excel文件
df = pd.read_excel("alibaba_data2.xlsx")
# 如果你想保留重复项中的第一个出现项，可以不传入inplace=True参数
df = df.drop_duplicates(subset="店铺名称")


def remove_function(value):
    return str(value).replace("US$", "")


def remove_date(value):
    if value.isdigit() and len(value) == 4:
        return ""
    else:
        return value


df["销售额"] = df["销售额"].apply(remove_function)
df["销售额"] = df["销售额"].apply(remove_date)
df["销售额"] = df["销售额"].replace("nan", "")
# 将去重后的数据保存到新的Excel文件中
df = df.fillna(" ")
df.to_excel("taizhou.xlsx", index=False, na_rep=" ")
