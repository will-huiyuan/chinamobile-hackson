import csv
import tools
from database import *
from algorithm import singly_linked_list
from collections import defaultdict

# 创建一个 defaultdict 用于按照每一个用户账号分组数据
grouped_data = defaultdict(list)

# 执行csv文件读取，数据清洗，以及给每一个账号创建对应的数据库对象
def main(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # 跳过第一行标题行
        next(csv_reader)

        # 根据第三列的“从账号”字符串，将所有属于同一账号的操作分在同一组
        for row in csv_reader:
            category = row[2]
            grouped_data[category].append(row)

    # 创建一个单链表 data_list
    data_list = singly_linked_list.LinkedList()

    # 遍历分组数据并创建数据库对象
    for category, group in grouped_data.items():
        curr_database = Database(group[0][2])  # 使用账号名创建数据库对象

        # 处理数据与时间，再存入对象
        for row in group:
            curr_action = tools.clean_access(row[4])
            curr_date = tools.convert_time(row[0])
            curr_ip = row[5]

            curr_database.add_entry(curr_date, curr_action, curr_ip)

        curr_database.sort_time()  # 对数据库对象按照时间排序
        data_list.insert_tail(curr_database)  # 将数据库对象添加到单链表尾部

    # 用于测试的代码，打印数据
    '''for node in data_list:
        node.print_entries()'''
    # 返回单链表
    return data_list
    
