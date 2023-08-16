import collections
from tools import *
import pandas as pd
import time
def main(train_path):
    pass


if __name__ == "__main__":
    input = pd.read_csv(get_fcsv_path())
    start = time.time()
    print(len(input["源IP"].unique()))
    end = time.time()
    print(f"运行时间：{end - start}秒")
    start = time.time()
    print(input["源IP"].nunique())
    end = time.time()
    print(f"运行时间：{end - start}秒")