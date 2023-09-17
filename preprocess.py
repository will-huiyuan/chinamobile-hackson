import csv
import tools
from database import *
from algorithm import singly_linked_list

from collections import defaultdict
grouped_data = defaultdict(list)

def main(file_path):
    with open(file_path,'r', encoding='utf-8') as file:
        csv_reader=csv.reader(file)
        #skip 1st row
        next(csv_reader)

        for row in csv_reader:
            category=row[2]
            grouped_data[category].append(row)

    data_list = singly_linked_list.LinkedList()
    for category, group in grouped_data.items():
        curr_database = Database(group[0][2])
        for row in group:
            curr_action = tools.clean_access(row[4])
            curr_date = tools.convert_time(row[0])
            curr_ip = row[5]

            curr_database.add_entry(curr_date, curr_action, curr_ip)
        curr_database.sort_time()
        data_list.insert_tail(curr_database)

    #testing to print----
    '''for node in data_list:
        node.print_entries()'''
    #----
    return data_list

