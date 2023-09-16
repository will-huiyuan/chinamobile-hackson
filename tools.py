import re
from datetime import datetime


def convert_time(time_str):
    day_month, year, time_str, am_pm = time_str.split()
    year = int(f"20{year[1:]}")
    day = int(day_month.split('-')[0])
    month = int(day_month.split('-')[1][:-1])

    hour, minute = time_str.split('.')[0:2]
    hour = int(hour)
    minute = int(minute)

    if am_pm == '下午' and hour != 12:
        hour += 12
    elif am_pm == '上午' and hour == 12:
        hour = 0

    # 创建datetime对象
    dt = datetime(year, month, day, hour, minute)
    return dt


def clean_access(access):
    chinese_part = re.search('[\u4e00-\u9fa5]+', str(access))
    # print(access)
    chinese_text = chinese_part.group()
    remaining_text = access[chinese_part.end():]
    cleaned_type = chinese_text.strip() + remaining_text.strip()
    # print(cleaned_type)
    return cleaned_type


"""develop intended functions"""


def get_fcsv_path():
    import os
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    file_path = os.path.join(parent_directory, 'input', '数据安全赛道', 'trainA.csv')
    # file_path = os.path.join(parent_directory, 'input', '数据安全赛道', 'testdata.csv')
    if __name__ == '__main__':
        print(file_path)
    return file_path

# todo delete this function