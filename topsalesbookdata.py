import time
import os
import pandas as pd
import multiprocessing as mp
import nameTobook_v2


def import_csv(wd=""):
    wd = str(wd)
    wd = "./data/allSalesDataWithOutPublisher.csv" if wd == "" else wd
    return pd.read_csv(wd)


def extract_title(_df):
    return _df["title"]


def remove_duplicate(series):
    return series.drop_duplicates()


def get_data(req_str):
    spyder = nameTobook_v2.Spyder()
    water = spyder.getpaper(req_str)
    auth1, pub1, date1 = nameTobook_v2.getbookdata(water)
    return [auth1, pub1, date1]


def get_and_record_data(args: list):
    title_, lock_, file_path, counter, total = args
    temp = get_data(title_)
    with lock_, open(file_path, "a") as f:
        f.write(
            f"{title_.replace(',', '.')},{str(temp[0]).replace(',', '.')},{str(temp[1]).replace(',', '.')},{str(temp[2]).replace(',', '.')}\n")
        counter.value += 1
        print(f"Progress: {counter.value}/{total} - {title_}")
    return 0


if __name__ == "__main__":
    df = import_csv("./data/allSalesDataWithOutPublisher.csv")
    title = extract_title(df)
    title = remove_duplicate(title)
    title = list(title)

    file_path = "./book_info/publicDateAllSales.csv"

    if os.path.exists(file_path):
        cur = pd.read_csv(file_path)
        title = [t for t in title if t not in cur["title"].values]
    else:
        if not os.path.exists('./book_info/'):
            os.mkdir("./book_info/")
        with open(file_path, "w") as f:
            f.write("title,author,published,date\n")

    total = len(title)
    pool = mp.Pool(4)
    manager = mp.Manager()
    lock = manager.Lock()
    counter = manager.Value('i', 0)  # Shared counter for progress

    # Use map to process data
    args = [(t, lock, file_path, counter, total) for t in title]
    pool.map_async(get_and_record_data, args)

    pool.close()
    pool.join()
    print("Done")
