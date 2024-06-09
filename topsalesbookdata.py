import time
import os
import pandas as pd
import multiprocessing as mp

import nameTobook_v2


def import_csv(wd=""):
    wd = str(wd)
    wd = "./data/2024-04-20_allSales.csv" if wd == "" else wd
    return pd.read_csv(wd)


def extract_title(_df):
    return _df["title"]


def remove_duplicate(series):
    return series.drop_duplicates()


def get_data(req_str):
    spyder = nameTobook_v2.Spyder()
    water = spyder.getpaper(req_str)
    auth1, pub1, date1 = nameTobook_v2.getbookdata(water)
    # print(auth1, pub1, date1,end='\n')

    return [auth1, pub1, date1]


"""
    water = spyder.getebook(req_str)
    auth2, pub2 = nameTobook_v2.getbookdata(water)
    print(auth2, pub2)
    return [[auth1, pub1], [auth2, pub2]]
"""

if __name__ == "__main__":
    df = import_csv("./data/2024-04-29_allSales.csv")
    title = extract_title(df)
    title = remove_duplicate(title)
    list(title)
    if os.path.exists("./book_info/publicDateAllSales.csv"):
        f = open("./book_info/publicDateAllSales.csv", "a")
        cur = pd.read_csv("book_info/publicDateAllSales.csv")
        # remove duplicate title in cur
        title = title[~title.isin(cur["title"])]
    elif os.path.exists('./book_info/'):
        f = open("book_info/publicDateAllSales.csv", "w")
        f.write("title,author,published,date\n")
    else:
        os.mkdir("./book_info/")
        f = open("book_info/publicDateAllSales.csv", "w")
        f.write("title,author,published,date\n")
    total = len(title)
    for idx, string in enumerate(title):
        # title[idx] = [string].extend([j for i in get_data(string) for j in i])
        temp = get_data(string)

        # dic = {
        #    "title": string,
        #    "author": temp[0],
        #   "published": temp[1],
        #   "date": temp[2]
        # }
        # json.dump(dic)
        f.write(
            f"{string.replace(',', '.')},{str(temp[0]).replace(',', '.')},{str(temp[1]).replace(',', '.')},{str(temp[2]).replace(',', '.')}\n")
        print(f"\r{idx+1}/{total}")
    title = pd.DataFrame(title)
    title.to_csv(f"book_info/paper_{time.strftime('%Y-%m-%d',time.localtime())}_allSales.csv", encoding="utf8", index=False)
    f.close()
