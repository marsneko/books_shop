import requests
from bs4 import BeautifulSoup
import re, time


def extract_info(regex, text):
    for _ in text:
        match = regex.search(_)
        if match:
            return match.group(0)
    return None


class Spyder:
    url = str()
    req = "https://search.books.com.tw/search/query/key/"
    searchRes = ""
    Plink = ""
    _type = ""
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 '
            'Safari/605.1.15'}
    cookies = {'ssid':'65dbf7855f688.1712545858',
               'pd':'7a868e9f98f833072b23a01bd02bf6e0a4a2f3890617d1d9469db2f83c68d614ebfd68d1ca285b6da8153601fe11fc6794a5b742657e2390069bd1aa6d6cb41e',
               'lgw':'B',
               'lpk':'cfdfe00774dac6a91d7f8db5ee1d44c309b1c4ac488478c4599001a0a0f277864ea0293816aa1551',
               'ltime':'2024%2F04%2F08+11%3A11%3A16',
               'bday':'1995%2F09%2F01',
               'bid':'65dbf7855f688'
               }
    data = []
    title = ""
    output = []
    ips = ["222.109.192.34", "133.18.234.13", "103.197.71.7", "120.29.124.131"]
    nip = 0

    def gip(self):
        ans = self.ips[self.nip]
        if self.nip == 3:
            self.nip = 0
        else:
            self.nip += 1
        return ans

    def reset(self):
        self.url = str()
        self.searchRes = ""
        self.Plink = ""
        self._type = ""
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 '
                'Safari/605.1.15'}
        self.data = []
        self.title = ""
        self.output = []

    def getSearchreasult(self, bookname, typeofbook):

        if typeofbook == 1:  # 紙本書
            self._type = "/cat/BKA"
        elif typeofbook == 2:  # 電子書
            self._type = "/cat/EBA"
        """
        for i in self.ips:
            try:
                self.searchRes = requests.get(self.req + str(bookname) + self._type , headers=self.headers, proxies={'http':'ip','https': i})
            except:
                print(f"{i} is invalid")
        """
        self.searchRes = requests.get(self.req + str(bookname) + self._type, headers=self.headers)
        print(self.req + str(bookname) + self._type)

    def getPage(self):
        soup = BeautifulSoup(self.searchRes.text, features="lxml")
        self.Plink = "https:" + soup.find_all(attrs={"target": "_blank"})[0].attrs["href"]
        self.Plink = "https://www.books.com.tw/products/" + re.search(r"/item/([0-9E]+)", self.Plink).group(1)
        print(self.Plink)

    def getinfo(self):
        output = []
        """
        res = requests.get(self.Plink, headers=self.headers, proxies={'http':'ip','https': self.gip})
        """
        s = requests.Session()
        res = s.get(self.Plink, headers=self.headers, cookies=self.cookies)
        if res.status_code == 484:
            tt = 0
            while tt <= 3:
                print(f"{tt} time tried", res, res.status_code == 200)
                res = s.get(self.Plink, headers=self.headers)
                if res.status_code == 484:
                    break
                tt += 1
        soup = BeautifulSoup(res.text, features="lxml")

        try:
            for _ in soup.find(attrs={"class", "type02_p003 clearfix"}).contents[1].contents:
                output.append(_.text)
            for __ in soup.find(attrs={"class", "prod_cont_b"}).contents[1].contents:
                output.append(__.text)
            self.title = soup.find(attrs={'class': "mod type02_p002 clearfix"}).text
        except:
            print("can't get info")

        self.data = output

    def reformat(self):
        '''
        try:
            self.output.append(
                re.sub(r"\n\n\n\n\n\n已追蹤作者：|\[\xa0修改\xa0\]\n\n\n\n確定\n取消\n|\n\n\n\n確定\n取消\n|\xa0\xa0\n新功能介紹", "",
                       self.rawdata[0]))
            self.output.append(re.sub(r"\n\n", "", self.rawdata[1]))
            self.output = "".join(self.output)
        except:
            "".join(self.rawdata)
        '''

        author_regex = re.compile(r'作者：\s*(\S+)')
        publish_date_regex = re.compile(r'出版日期：(\d{4}/\d{2}/\d{2})')
        language_regex = re.compile(r'語言：(\S+)')
        original_price_regex = re.compile(r'定價：(\d+)元')
        discount_price_regex = re.compile(r'(優惠價：\d+折(\d+)元|'
                                          r'優惠價：(\d+)元)|'
                                          r'(特價再\d+折：(\d+)元)')
        discount_deadline_regex = re.compile(r'優惠期限：(\d{4}年\d{2}月\d{2}日)止')
        try:
            for _, __ in enumerate(self.data):
                self.data[_] = re.sub(r"\n\n\n\n\n\n已追蹤作者：|\[\xa0修改\xa0\]\n\n\n\n確定\n取消\n|\n\n\n\n確定\n取消\n|\xa0\xa0\n"
                                      r"新功能介紹| |\n\n\n\n\n已追蹤作者：", "", __)
            extracted_info_with_yuan = {
                'title': self.title,
                'author': extract_info(author_regex, self.data),
                # 'publisher': extract_info(publisher_regex_updated,self.output),
                # 其他字段的提取可以沿用之前的正則表達式
                'publish_date': extract_info(publish_date_regex, self.data),
                'language': extract_info(language_regex, self.data),
                'original_price': extract_info(original_price_regex, self.data),
                'discount_price': extract_info(discount_price_regex, self.data),
                'discount_deadline_regex': extract_info(discount_deadline_regex, self.data)  # 嘗試重新提取
            }
            print(extracted_info_with_yuan)
        except:
            print("regex error")
        print(self.data)

    def getpublicdate(self):
        s = requests.Session()
        res = s.get(self.Plink, headers=self.headers)
        if res.status_code == 484:
            tt = 0
            while tt <= 3:
                print(f"{tt} time tried", res, res.status_code == 200)
                res = s.get(self.Plink, headers=self.headers)
                if res.status_code == 484:
                    break
                tt += 1
        soup = BeautifulSoup(res.text, features="lxml")

        try:
            self.publicdate = soup.find(attrs={"name": "description"}).attrs['content']
        except:
            print(soup.find(attrs={"name": "description"}).attrs['content'])
            print(soup)
            __ = input("continue?")
            if __ == "y":
                self.getpublicdate()
            else:
                return None
        return re.search(re.compile(r'出版日期：(\d{4}/\d{2}/\d{2})'), self.publicdate).group(1)


if __name__ == "__main__":
    inputlist = [
        "史上最有效的美顏教科書：日本明星指定人氣教練！木村式小臉矯正計畫，消除鬆弛和皺紋，透過臉部肌肉訓練，解決顏面煩惱！", "21世紀的人生難題：憂鬱‧焦慮‧藥‧迷信‧愛‧痛（牛津非常短講II）"]

    spyder = Spyder()

    for i in inputlist:
        spyder.reset()
        spyder.getSearchreasult(i, 1)
        spyder.getPage()
        print("page geted")
        spyder.getinfo()
        print("info geted")
        spyder.reformat()

        spyder.reset()
        spyder.getSearchreasult(i, 2)
        spyder.getPage()
        print("page geted")
        spyder.getinfo()
        print("info geted")
        spyder.reformat()
