from selenium import webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup
import random
import os


# 啟用無頭模式

def canbuy(driver, url: str) -> bool:
    # 開啟目標網頁
    driver.get(url)

    # 等待頁面加載完成
    time.sleep(random.randint(0, 1))  # 根據需要調整等待時間

    try:
        content = driver.page_source
    except Exception as e:
        print(f"Error: {e}")
        return False

    soup = BeautifulSoup(content, 'html.parser')

    try:
        return soup.find_all(attrs={'class': 'clearfix easycart'})[0].span.text == '直接購買'
    except IndexError:
        return False


if __name__ == '__main__':
    pd.options.mode.copy_on_write = True

    cookies = [
        {"name": "test", "value": "test"},
        {"name": "__eoi", "value": "ID=d9cc9f038c0c2526:T=1722751518:RT=1722766762:S=AA-Afjb81yP6TpRmV1F0ugsxCQKU"},
        {"name": "__gads",
         "value": "ID=8308f4d7ce5b6927:T=1722751518:RT=1722766762:S=ALNI_MZhLAxGoYX1lYmICbbKivBqEHPHMA"},
        {"name": "__gpi",
         "value": "UID=00000eb2c12eddf8:T=1722751518:RT=1722766762:S=ALNI_MbUNbjxiIv-f8s4_DQOLLyjpGZKKQ"},
        {"name": "__lt__cid", "value": "eb095995-8f50-4b41-b545-36e3081a118b"},
        {"name": "__lt__sid", "value": "c81a9318-834f84c1"},
        {"name": "_fbp", "value": "fb.2.1722751421411.517682522306563214"},
        {"name": "_ga", "value": "GA1.1.603052269.1722751420"},
        {"name": "_ga_TR763QQ559", "value": "GS1.1.1722766760.2.1.1722767905.0.0.0"},
        {"name": "_gcl_au", "value": "1.1.814412782.1722751419"},
        {"name": "_gid", "value": "GA1.3.1704837694.1722751420"},
        {"name": "add_url", "value": "https%3A%2F%2Fwww.books.com.tw%2F"},
        {"name": "bday", "value": "1995%2F09%2F01"},
        {"name": "bid", "value": "65dbf7855f688"},
        {"name": "bt", "value": "show7y"},
        {"name": "cid", "value": "marsneko"},
        {"name": "csrc", "value": "B"},
        {"name": "gud",
         "value": "ea5c9db2db2cd317c7f86797172b9513b95e454b8fcffa07316cdc7c9892f3f0567f1e19aa934e54c9257ecffb74e2b1"
                  "91286aa93fb626ff3ed54243543b04a0"},
        {"name": "home_tbanner", "value": "0"},
        {"name": "item_history",
         "value": "0010995727+0010069584+0010997376+0010807929+0010986446+0010995152+0010997356+0010997353+0010996557"
                  "+0010997371+0010995165+"},
        {"name": "lgw", "value": "B"},
        {"name": "lpk", "value": "8aed8bbfc006e7cd3926a7951d76d71930fa87f2de7e15901bf59db438a0d9ef56e5fd175be733eb"},
        {"name": "ltime", "value": "2024%2F08%2F04+18%3A19%3A55"},
        {"name": "pd",
         "value": "7a868e9f98f833072b23a01bd02bf6e0a4a2f3890617d1d9469db2f83c68d614ebfd68d1ca285b6da8153601fe11fc6794a"
                  "5b742657e2390069bd1aa6d6cb41e"},
        {"name": "session", "value": "Zq8aqN87zorzNQ6vN7MEDQAAABc"},
        {"name": "ssid", "value": "65dbf7855f688.1722766760"},
        {"name": "stepsession", "value": "Zq9V20waXcVl0EWT7zrU3AAAADg"}
    ]

    ls = list(map(lambda x: "publisher_data_withlink/" + x, [f for f in os.listdir('./publisher_data_withlink') if not f.startswith('.')]))
    for link in ls:
        driver_path = "chromedriver.exe"  #
        brave_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = brave_path
        # chrome_options.add_argument("--headless")

        # 啟動瀏覽器
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.books.com.tw/")
        for cookie in cookies:
            driver.add_cookie(cookie)

        df = pd.read_csv(link)
        dflen = len(df)
        if os.path.exists(link.replace('.csv', "")
                                  .replace('withlink','buyable') + '_canbuy.csv'):
            targetdf = pd.read_csv(link.replace('.csv', "")
                                   .replace('withlink','buyable') + '_canbuy.csv')
        else:
            targetdf = pd.DataFrame(columns=['title', 'author', 'publisher', 'publication_date', 'discount', 'price',
                                             'url', 'canbuy'])
        df = df[~df['url'].isin(targetdf['url'])]
        temp = []
        timer = 0
        for _ in df['url']:
            temp.append(canbuy(driver, _))
            print(f"Progress: {len(temp)+len(targetdf)}/{dflen} - {_} - {temp[-1]}", end='\r')
            timer += 1
            if timer == 200:
                timer = 0
                adddf = df.iloc[:len(temp)]
                df = df.iloc[len(temp):]
                adddf['canbuy'] = temp
                temp = []
                targetdf = pd.concat([targetdf, adddf])
                targetdf.to_csv(link.replace('.csv', "")
                                .replace('withlink','buyable') + '_canbuy.csv', index=False)
                driver.quit()
                time.sleep(10)
                driver = webdriver.Chrome(options=chrome_options)
                driver.get("https://www.books.com.tw/")
                for cookie in cookies:
                    driver.add_cookie(cookie)

        adddf = df.iloc[:len(temp)]
        adddf['canbuy'] = temp
        targetdf = pd.concat([targetdf, adddf])
        targetdf.to_csv(link.replace('.csv', "")
                     .replace('withlink','buyable') + '_canbuy.csv', index=False)
        driver.quit()

# %%
