import pandas as pd
from progress.bar import Bar


def addDate(mainData: pd.DataFrame, labelData: pd.DataFrame):
    bar = Bar('Processing', max=mainData.size)
    ser1 = []
    ser2 = []
    for num,i in enumerate(mainData['title']):
        print(f'\r{num}/{len(mainData)}', end = "\n")
        if i in labelData['title'].values:
            ser1.extend(labelData[labelData['title'] == i]['published'].values)
            ser2.extend(labelData[labelData['title'] == i]['date'].values)
        else:
            ser1.append(None)
            ser2.append(None)
        bar.next()
    mainData['publisher'] = pd.Series(ser1)
    mainData['publishDate'] = pd.Series(ser2)
    bar.finish()
    return mainData


if __name__ == '__main__':
    main = pd.read_csv("/Users/eric/Documents/SchoolCourses/112/112-2/bookcart_crawler/data/2024-04-29_allSales.csv")
    labels = pd.read_csv(
        "/Users/eric/Documents/SchoolCourses/112/112-2/bookcart_crawler/book_info/publicDateAllSales.csv")
    output = addDate(main, labels)
    output.to_csv("./dateData/2024-04-29_Date.csv")
