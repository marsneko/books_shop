import requests
from bs4 import BeautifulSoup
import time


class Spyder:
    paperlink = "https://search.books.com.tw/search/query/cat/1/sort/1/v/0/page/1/spell/3/ms2/ms2_1/key/"
    ebooklink = "https://search.books.com.tw/search/query/cat/6/sort/1/v/0/page/1/spell/3/ms2/ms2_1/key/"
    headers = dict({})

    def __init__(self, headers=None):
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        self.headers = headers

    def getpaper(self, req):
        t = 0
        time.sleep(5)
        try:
            # print(self.paperlink + req)
            water = requests.get(self.paperlink + req, headers=self.headers)

            if water.status_code == 484:
                print("Error: ", water.status_code, "too many requests - wait 10 seconds")
                while water.status_code == 484 and t < 10:
                    print(f"{t}-th try")
                    time.sleep(40)
                    water = requests.get(self.paperlink + req, headers=self.headers)
                    if water.status_code == 200:
                        return water
                    t += 1
                return None
            if water.status_code != 200:
                print("Error: ", water.status_code)
                return None
            else:
                return water
        except:
            print("can't get html")
            return None

    def getebook(self, req):
        t = 0
        time.sleep(5)
        try:
            # print(self.ebooklink + req)
            water = requests.get(self.ebooklink + req, headers=self.headers)
            if water.status_code == 484:
                print("Error: ", water.status_code, "too many requests - wait 10 seconds")
                while water.status_code == 484 and t < 10:
                    time.sleep(40)
                    water = requests.get(self.ebooklink + req, headers=self.headers)
                    if water.status_code == 200:
                        return water
                    t += 1
                return None
            if water.status_code != 200:
                print("Error: ", water.status_code)
                return None
            else:
                return water
        except:
            print("can't get html")
            return None


def getbookdata(data):
    if data is None:
        return None, None, None
    soup = BeautifulSoup(data.text, features="lxml")

    try:
        author = soup.find_all(attrs={"rel": "go_author"})[0].text
    except:
        author = None

    try:
        public = soup.find_all(attrs={'class': "list-date clearfix"})[0].find_all(attrs={"target": "_blank"})[0].text
    except:
        public = None
    try:
        date = soup.find_all(attrs={'class': "list-date clearfix"})[0].find('li').text.split('出版日期: ')[1]
    except:
        date = None

    return author, public, date


if __name__ == "__main__":
    spyder = Spyder(headers={"User-Agent": "Mozilla/5.0"})
    inp = input("book title: ")
    data = spyder.getpaper(inp)
    getbookdata(data)
    data = spyder.getebook(inp)
    getbookdata(data)
