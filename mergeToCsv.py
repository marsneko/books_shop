import json, io, os, pandas, re
import time


def listofData(wd=""):
    wd = str(wd)
    wd = "./" if wd == "" else wd
    ts = list(map(lambda x: ["topsales", "topSales/" + x], os.listdir(wd + "/topSales")))
    ns = list(map(lambda x: ["newsales", "newSales/" + x], os.listdir(wd + "/newSales")))
    ps = list(map(lambda x: ["presales", "preSales/" + x], os.listdir(wd + "/preSales")))

    return ts + ns + ps


def priceParser(s):
    ret1, ret2 = None, None
    try:
        ret1, ret2 = re.search(r"(\d+)折(\d+)元", s).group(1), re.search(r"(\d+)折(\d+)元", s).group(2)
    except:
        try:
            ret2 = re.search(r"(\d+)元", s).group(1)
        except:
            print(f"{s} have some problem")
    return ret1, ret2


def fromJsonToCsv(wd=""):
    wd = str(wd)
    wd = "./" if wd == "" else wd
    data = listofData(wd)
    print(data)
    pd = []
    for dd in data:
        d = dd[1]
        with open(wd + d, "r", encoding="utf8") as f:
            print(f"reading {d}")
            try:
                tep = json.load(f)
                for i in tep:
                    for j in i["data"]:
                        j["title"] = j["title"].replace(",", ".")
                        j["date"] = i["date"]
                        j["type"] = dd[0]
                        j["discount"], j["price_"] = priceParser(j["price"])
                        if j["discount"] is None or j["price_"] is None:
                            print(j)
                        pd.append(j)
            except:
                print(f"error in {d}")
    pd = pandas.DataFrame(pd)
    print(pd.dtypes)
    print(pd.shape)
    print(pd.iloc[10])
    print(pd.size)
    pd.to_csv(wd + f"./data/{time.strftime('%Y-%m-%d',time.localtime())}_allSales.csv", index=False)


if __name__ == "__main__":
    #fromJsonToCsv()
    data = [["topsales","./topSales/sale_2024-08-05.json"],["newsales", "./newSales/new_2024-08-05.json"],["presales", "./preSales/pre_2024-08-05.json"]]
    pd = []
    for dd in data:
        d = dd[1]
        with open("./" + d, "r", encoding="utf8") as f:
            print(f"reading {d}")
            try:
                tep = json.load(f)
                for i in tep:
                    for j in i["data"]:
                        j["title"] = j["title"].replace(",", ".")
                        j["date"] = i["date"]
                        j["type"] = dd[0]
                        j["discount"], j["price_"] = priceParser(j["price"])
                        if j["discount"] is None or j["price_"] is None:
                            print(j)
                        pd.append(j)
            except:
                print(f"error in {d}")
    pd = pandas.DataFrame(pd)
    print(pd.dtypes)
    print(pd.shape)
    print(pd.iloc[10])
    print(pd.size)
    pd.to_csv( f"./data/{time.strftime('%Y-%m-%d',time.localtime())}_allSales.csv", index=False)


