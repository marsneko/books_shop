import pandas as pd
import requests
import time
import re
from bs4 import BeautifulSoup


def geturloffirstpage(url_, headers):
    headers = headers
    water = requests.get(url_, headers=headers)
    time.sleep(2)
    if water.status_code != 200:
        raise Exception(f"can't get links:{url_}\n"
                        f"the status_code code is {water.status_code}\n")
    soup = BeautifulSoup(water.text, features="lxml")
    try:
        ans = int(soup.find(attrs={'class': 'cnt_page'}).contents[1].span.text)
        return ans
    except:
        return None


def priceParser(s):
    ret1, ret2 = None, None
    try:
        ret1, ret2 = re.search(r"(\d+)折", s).group(1), re.search(r"(\d+)元", s).group(1)
    except:
        try:
            ret2 = re.search(r"(\d+)元", s).group(1)
        except:
            print(f"{s} have some problem")
    return ret1, ret2


def getpagedata(template, num_of_pages, headers):
    df = []
    headers = headers
    for i in range(1, num_of_pages + 1):
        print("running page:", i, "of", num_of_pages, "pages")
        time.sleep(8)
        url = template + "&page=" + str(i)
        water = requests.get(url, headers=headers)
        if water.status_code != 200:
            raise Exception(f"can't get links:{url}\n"
                            f"the status_code code is {water.status_code}\n")
        soup = BeautifulSoup(water.text, features="lxml")
        for j in soup.find_all("div", attrs={'class': 'item'}):
            output = {
                "title": j.h4.text.replace('\n', '').replace(',', '.'),
                "author": j.find_all(attrs={'class': "list clearfix"})[0].li.a.text,
                "publisher": j.find_all(attrs={'class': "list clearfix"})[0].li.span.a.text,
                "publication_date": j.find_all(attrs={'class': "list clearfix"})[0].li.span.text.split('出版日期：')[1],
                'price': j.find(attrs={'class': 'price'}).li.text,
                "link": j.a.get('href')

            }
            discount, price = priceParser(output['price'])
            output = [output["title"], output["author"], output["publisher"], output["publication_date"], discount,
                      price, output["link"]]
            df.append(output)
        print(df[-1])
    df_ = pd.DataFrame(df, columns=["title", "author", "publisher", "publication_date", "discount", "price", 'url'])
    return df_


if __name__ == '__main__':
    publiser_dict = {
        'fangzhi': 'https://www.books.com.tw/web/sys_puballb/books/?pubid=fine&o=1&v=1',
        'how': 'https://www.books.com.tw/web/sys_puballb/books/?pubid=how&o=1&v=1',
        'jioujing': 'https://www.books.com.tw/web/sys_puballb/books/?pubid=athena&o=1&v=1',
        'lonely': 'https://www.books.com.tw/web/sys_puballb/books/?pubid=solo&o=1&v=1',
        'shianjiue': 'https://www.books.com.tw/web/sys_puballb/books/?pubid=yuance6c&o=1&v=1',
        'yuanshen': 'https://www.books.com.tw/web/sys_puballb/books/?pubid=yuanshen&o=1&v=1',
        #'time': "https://www.books.com.tw/web/sys_puballb/books/?pubid=ctpubco&o=1&v=1"
    }
    for name,url in publiser_dict.items():
        num = geturloffirstpage(url, headers={"User-Agent": "Mozilla/5.0"})
        df = getpagedata(url, num, headers={"User-Agent": "Mozilla/5.0"})
        df.to_csv(f"./publisher_data_withlink/{name}.csv", index=False)
        print(f"finish {name} publisher")
