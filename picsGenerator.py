import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from datetime import datetime
import math
import os
import time
import re


def preformatTopData(df: pd.DataFrame) -> pd.DataFrame:
    discount_map = {
        0: 100,
        1: 10,
        5: 50,
        7: 70,
        9: 90
    }
    type_map = {
        "topsales": 0,
        "newsales": 1,
        "presales": 2
    }
    cate_map = {
        1: "文學小說",
        2: "商業理財",
        3: "藝術設計",
        4: "人文社科",
        6: "自然科普",
        7: "心理勵志",
        8: "醫療保健",
        9: "飲食",
        10: "生活風格",
        11: "旅遊",
        12: "宗教命理",
        13: "親子教養",
        14: "青少年文學",
        15: "輕小說",
        16: "漫畫、圖文書",
        19: "電腦資訊",
        22: "影視偶像",
        17: "語言學習",
        18: "考試用書",
        20: "專業出版品",
        24: "國中小參考書"
    }
    cate_eng_map = {
        1: 'Literature & Fiction',
        2: 'Business & Money',
        3: 'Arts & Photography',
        4: 'Politics & Social Sciences',
        6: 'Science & Math',
        7: 'Self-Help',
        8: 'Health, Fitness & Dieting',
        9: 'Health, Fitness & Dieting',
        10: 'Cookbooks, Food & Wine',
        11: 'Travel',
        12: 'Religion & Spirituality',
        13: 'Parenting & Relationships',
        14: 'Teens',
        15: 'Literature & Fiction',
        16: 'Comics & Graphic Novels',
        19: 'Computers & Technology',
        22: 'Humor & Entertainment',
        17: 'Education & Teaching',
        18: 'Test Preparation',
        20: 'Education & Teaching',
        24: 'Education & Teaching'
    }
    # clean data ----- discount to int
    df['discount'] = df["discount"].fillna(0).astype(str)
    temp = []
    for _ in df['discount']:
        if math.ceil(float(_)) in discount_map:
            temp.append(discount_map[math.ceil(float(_))])
        else:
            temp.append(math.ceil(float(_)))
    df['discount'] = temp
    df['discount'] = df['discount'].map(lambda x: 1 if x == 0 else x / 100)

    # clean data ----- cate to english cate
    df.dropna(subset=['cate'], inplace=True)
    temp = []
    for _ in df['cate']:
        temp.append(cate_eng_map[_])
    df['eng_cate'] = temp

    # clean data ----- date, title, attr, cate
    df['date'] = [time.strftime("%Y-%m-%d", time.strptime(i, "%Y-%m-%d %H:%M:%S")) for i in df['date']]
    df['date_'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    # df['title'] = [hash(i) for i in df['title']]
    df['attr'] = [math.ceil(i) for i in df['attr'].fillna(0)]
    df['cate'] = [math.ceil(i) for i in df['cate'].fillna(0)]
    df['rank'] = [math.ceil(i) for i in df['rank'].fillna(0)]
    df['publishDate_'] = pd.to_datetime(df['publishDate'], format='%Y-%m-%d')

    # clean data ----- price
    df['salePrice'] = pd.to_numeric(df['price_'])
    temp = []
    for idx, row in df.iterrows():
        temp.append((100 * row['price_']) / row['discount'])
    df['Price'] = temp
    df['PublishDate'] = df['publishDate_']
    df = df[['title', 'rank', 'cate', 'eng_cate', 'attr', 'date', 'discount', 'Price', 'salePrice', 'publishDate_'
        , 'PublishDate', 'publisher']]
    return df


def RankDiscountScatterPlotByCategory(df: pd.DataFrame, cate: [str], path: str) -> None:
    nrows = len(cate) // 2 + 1
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(30, 6 * nrows))
    for idx in range(len(cate)):
        temp = df[df['eng_cate'] == cate[idx]]
        temp.drop_duplicates(subset=['rank', 'discount'], inplace=True)
        ax[idx // 2][idx % 2].scatter(temp['rank'], temp['discount'], s=10)
        ax[idx // 2][idx % 2].set_title(cate[idx])
        ax[idx // 2][idx % 2].set_xlabel('Rank')
        ax[idx // 2][idx % 2].set_ylabel('Discount')
        x = temp['rank']
        y = temp['discount']
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[idx // 2][idx % 2].plot(x, p(x), "r--")
    plt.suptitle('Rank-Discount Scatter Plot')
    plt.savefig(path)


def PublishDateDiscountScatterPlotByCategory(df: pd.DataFrame, cate: [str], path: str) -> None:
    nrows = len(cate) // 2 + 1
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(30, 6 * nrows))
    for idx in range(len(cate)):
        temp = df[df['eng_cate'] == cate[idx]]
        temp = temp.dropna(subset=['publishDate_', 'discount'])
        ax[idx // 2][idx % 2].scatter(temp['publishDate_'], temp['discount'], s=10)
        ax[idx // 2][idx % 2].set_title(cate[idx])
        ax[idx // 2][idx % 2].set_xlabel('Publish Date')
        ax[idx // 2][idx % 2].set_ylabel('Discount')
        x = mdates.date2num(temp['publishDate_'])
        y = temp['discount'].to_list()
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[idx // 2][idx % 2].plot(x, p(x), "r--")
    plt.suptitle('PublishDate-Discount Scatter Plot')
    plt.savefig(path)


def ScatterPlotByCategory(df: pd.DataFrame, _x: str, _y: str, cate: [str], path: str, title: str, cate_name: str = None,
                          x_is_date: bool = False,
                          y_is_date: bool = False, xlab: str = None, ylab: str = None, xlim: [int] = None,
                          ylim: [int] = None) -> None:
    nrows = math.ceil(len(cate) / 2)
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(30, 6 * nrows), sharex=True, sharey=True)
    xlabel = _x if xlab is None else xlab
    ylabel = _y if ylab is None else ylab
    cate_name = 'eng_cate' if cate_name is None else cate_name
    for idx in range(len(cate)):
        temp = df[df[cate_name] == cate[idx]]
        temp = temp.dropna(subset=[_x, _y])
        if x_is_date:
            x = mdates.date2num(temp[_x])
            ax[idx // 2][idx % 2].xaxis.set_major_formatter(DateFormatter('%Y'))
        else:
            x = temp[_x]

        if y_is_date:
            y = mdates.date2num(temp[_y])
            ax[idx // 2][idx % 2].yaxis.set_major_formatter(DateFormatter('%Y'))
        else:
            y = temp[_y]

        ax[idx // 2][idx % 2].scatter(x, y, s=10)
        ax[idx // 2][idx % 2].set_title(cate[idx], fontsize=20)
        ax[idx // 2][idx % 2].set_xlabel(xlabel, fontsize=15)
        ax[idx // 2][idx % 2].set_ylabel(ylabel, fontsize=15)
        if xlim is not None:
            ax[idx // 2][idx % 2].set_xlim(xlim[0], xlim[1])
        if ylim is not None:
            ax[idx // 2][idx % 2].set_ylim(ylim[0], ylim[1])
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[idx // 2][idx % 2].plot(x, p(x), "r--")
    if title is None:
        plt.suptitle(f'{_x}-{_y} Scatter Plot')
    elif title == '':
        pass
    else:
        plt.suptitle(title)
    plt.savefig(path, dpi=300)


def preformatAmazonData(df: pd.DataFrame) -> pd.DataFrame:
    dep1 = []
    dep2 = []
    for dep in df['department']:
        _ = re.split(r"\s\|\s", dep)

        try:
            dep1.append(_[0])
        except IndexError:
            dep1.append(None)
            dep2.append(None)
            pass

        try:
            dep2.append(_[1])
        except IndexError:
            dep2.append(None)
            pass

    df['department1'] = dep1
    df['department2'] = dep2

    price = []
    SalePrice = []
    for index, row in df.iterrows():
        orp = row['before_discount']
        orp = re.sub(r'[^0-9.]', '', orp)
        price.append(orp)
        nep = row['new_price']
        nep = re.sub(r'[^0-9.]', '', nep)
        SalePrice.append(nep)

    price = pd.to_numeric(price, errors='coerce')
    SalePrice = pd.to_numeric(SalePrice, errors='coerce')
    df['Price'] = price
    df['SalePrice'] = SalePrice
    df['discount'] = SalePrice / price

    AllRank = []
    DepRank = []
    for index, row in df.iterrows():
        alrank = str(row['all_rank'])
        alrank = re.sub(r'[#,]', '', alrank)
        AllRank.append(alrank)
        depr = str(row['dep_rank'])
        depr = re.sub(r'[#,]', '', depr)
        DepRank.append(depr)
    AllRank = pd.to_numeric(AllRank, errors='coerce')
    DepRank = pd.to_numeric(DepRank, errors='coerce')
    df['allRank'] = AllRank
    df['depRank'] = DepRank

    publish_date = []
    for index, row in df.iterrows():
        match = re.search('\((.*?)\)', row['other_list'])
        if match:
            publish_date.append(match.group(1))
        else:
            publish_date.append(np.nan)
    df['publish_date'] = publish_date
    df['PublishDate'] = pd.to_datetime(df['publish_date'], format="%B %d, %Y", errors='coerce')
    df = df.dropna(subset=['publish_date'])

    df = df[df['format'] == 'Hardcover']
    return df


def GenerateFirstDepRank(df: pd.DataFrame, cates: [str]) -> pd.DataFrame:
    df = df.dropna(subset=['department1', 'depRank'])
    output = []
    for cate in cates:
        temp = df[df['department1'] == cate]
        temp = temp.sort_values(by='allRank')
        temp = temp.drop_duplicates(subset=['title', 'department1', 'depRank'])
        temp['FirstDepRank'] = [i for i in range(1, len(temp) + 1)]
        output.append(temp)

    df = pd.concat(output)
    return df


if __name__ == "__main__":
    dfbook = pd.read_csv('./dateData/allSalesData.csv')
    dfbook = preformatTopData(dfbook)
    dfamazon = pd.read_csv('./googleDocxPic/Amazon_dep2_all.csv')
    dfamazon = preformatAmazonData(dfamazon)
    time_limit = pd.to_datetime('2000-01-01')
    dfamazon = dfamazon[dfamazon['PublishDate'] >= time_limit]
    dfbook = dfbook[dfbook['PublishDate'] >= time_limit]
    print(dfbook.head())
    print(dfamazon.head())
    cates = [
        'Literature & Fiction',
        'Business & Money',
        'Arts & Photography',
        'Politics & Social Sciences',
        'Science & Math',
        'Self-Help',
        'Health, Fitness & Dieting',
        'Cookbooks, Food & Wine',
        'Travel',
        'Religion & Spirituality',
        'Parenting & Relationships',
        'Teens',
        'Literature & Fiction',
        'Comics & Graphic Novels',
        'Computers & Technology',
        'Humor & Entertainment'
    ]
    dfamazon_ = GenerateFirstDepRank(dfamazon, cates)
    dfamazon_ = dfamazon_[dfamazon_['FirstDepRank'] <= 100]
    dfbook = dfbook[dfbook['attr'] == 7]
    dfbook = dfbook.drop_duplicates(subset=['rank','cate'])
    ScatterPlotByCategory(dfbook, 'rank', "discount", cates, title="", cate_name='eng_cate',
                          path='./googleDocxPic/BookRankDiscountScatterPlot.png'
                          , ylim=[0, 1.2])
    ScatterPlotByCategory(dfbook, 'PublishDate', 'discount', cates, title='', cate_name='eng_cate', x_is_date=True
                          , path='./googleDocxPic/BookPublishDateDiscountScatterPlotTest.png', ylim=[0, 1.2])
    ScatterPlotByCategory(dfamazon_, 'PublishDate', 'discount', cates, title='', cate_name='department1', x_is_date=True,
                          path='./googleDocxPic/AmazonDateDiscount.png', ylim=[0, 1.2])
    ScatterPlotByCategory(dfamazon_, 'FirstDepRank', 'discount', cates, title='', cate_name='department1', ylim=[0, 1.2],
                          path='./googleDocxPic/AmazonFirstDepRankDiscount.png')
# %%
