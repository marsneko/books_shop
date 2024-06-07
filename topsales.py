#!/usr/bin/python3

import io
import json
import requests
import time

from bs4 import BeautifulSoup


def gettops(links, attr, cate, page):
    """
    s = requests.Session()
    s.headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 '
            'Safari/605.1.15'}
    water = s.get(links)
    hostname = socket.gethostname()
    iPAddr = socket.gethostbyname(hostname)
    print("Your Computer IP Address is:" + iPAddr)
    """
    print(links)
    water = requests.get(links, headers={
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 '
            'Safari/605.1.15'})
    if water.status_code != 200:
        f = open(f"./logs/{time.strftime('%Y-%m-%d', time.localtime())}logs.txt", "a+")
        f.write(f"can't get links:{links}\n"
                f"the status_code code is {water.status_code}\n"
                )
        print("logfile is created in ./logs/")
        f.close()
    print(water.status_code)
    soup = BeautifulSoup(water.text, features="lxml")
    print(soup.title.text)
    res = soup.find_all(attrs={"class": "type02_bd-a"})
    output = []
    for _, __ in enumerate(res):
        # print(_.contents[1].text)
        # print([__.text for __ in _.contents])
        # output.append([__.text for __ in _.contents])
        # output.append([_.contents[1].text].extend(_.contents[3].text.split("\n")))
        try:
            output.append(
                {"attr": str(attr),
                 "cate": str(cate),
                 "rank": _,
                 "title": __.h4.text if __.h4.text != "" else None,
                 "author": __.find(attrs={"class": "msg"}).a.text if __.find(
                     attrs={"class": "msg"}).a is not None else None,
                 "price": __.find(attrs={"class": "price_a"}).text if __.find(
                     attrs={"class": "price_a"}) is not None else None,
                 "page": page,
                 }
            )
        except:
            print(__)
        # print([__.text for ___ in __.contents])
    print(output[0])
    return output


def saletops():
    cate = ["", "01", "02",
            "03", "04", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
            "18", "19", "20", "22"]
    attr = ["7", "30"]
    saltop = []

    print("____Sale tops____________________________\n")
    for __ in attr:
        for _ in cate:
            try:
                time.sleep(5)
                print(f"sale tops in cate {_} and attr {__}")
                saltop.append(
                    {
                        "cate": _,
                        "attr": __,
                        "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        "data": gettops(f"https://www.books.com.tw/web/sys_saletopb/books/{_}?attribute={__}", __, _,
                                        "tops")
                    }
                )
            except:
                print(f"error in cate {_} and attr {__}")
    with io.open(
            f'/Users/eric/Documents/SchoolCourses/112/112-2/bookcart_crawler/topSales/sale_{time.strftime("%Y-%m-%d", time.localtime())}.json',
            "w", encoding="utf8") as f:
        json.dump(saltop, f, ensure_ascii=False)
    f.close()


def newtops():
    cate = ["", "01", "02",
            "03", "04", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
            "18", "19", "20", "22"]
    newtop = []
    print("____New tops____________________________\n")
    for _ in cate:
        try:
            print(f"new tops in cate {_}")
            newtop.append(
                {
                    "cate": _,
                    "attr": None,
                    "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    "data": gettops(f"https://www.books.com.tw/web/sys_newtopb/books/{_}", None, _, "newtops")
                }
            )
            time.sleep(5)
            # print(newtop[-1])
        except:
            print(f"error in cate {_}")
    with open(
            f'/Users/eric/Documents/SchoolCourses/112/112-2/bookcart_crawler/newSales/new_{time.strftime("%Y-%m-%d", time.localtime())}.json',
            "w", encoding="utf8") as f:
        json.dump(newtop, f, ensure_ascii=False)
    f.close()


def pretops():
    pretop = []
    print("____Pre tops____________________________\n")
    try:
        print(f"pre tops")
        pretop.append(
            {
                "cate": None,
                "attr": None,
                "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "data": gettops(f"https://www.books.com.tw/web/sys_pretopb/books/", None, None, "pretops")
            }
        )
        time.sleep(5)

    except:
        print(f"error in cat pretops")
    with open(
            f'/Users/eric/Documents/SchoolCourses/112/112-2/bookcart_crawler/preSales/pre_{time.strftime("%Y-%m-%d", time.localtime())}.json',
            "w", encoding="utf8") as f:
        json.dump(pretop, f, ensure_ascii=False)
    f.close()
    # return saltop, newtop, pretop


if __name__ == "__main__":
    """
    # gettops("https://www.books.com.tw/web/sys_newtopb/books/02/?loc=P_0002_003")
    sal, new, pre = difftops()
    with io.open(f'./topSales/sale{time.strftime("%Y-%m-%d", time.localtime())}.json', "w", encoding="utf8") as f:
        json.dump(sal, f, ensure_ascii=False)
    with open(f'./newSales/new_{time.strftime("%Y-%m-%d", time.localtime())}.json', "w", encoding="utf8") as f:
        json.dump(new, f, ensure_ascii=False)
    with open(f'./preSales/pre_{time.strftime("%Y-%m-%d", time.localtime())}.json', "w", encoding="utf8") as f:
        json.dump(pre, f, ensure_ascii=False)
    """
    saletops()
    newtops()
    pretops()
    print("done")
