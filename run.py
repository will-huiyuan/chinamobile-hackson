import sys
import database
import os
from algorithm import singly_linked_list

#for testing:-----
from datetime import datetime
#-----

def main(to_pred_path,result_save_path):
    test1= database.Database("a2v3c4d5f")
    test1.add_entry(datetime(2023, 9, 15, 10, 0), "Login", "192.168.0.1")
    test1.add_entry(datetime(2023, 9, 15, 11, 30), "Logout", "192.168.0.2")
    test1.add_entry(datetime(2023, 9, 16, 11, 30), "Logout", "192.168.0.2")
    test1.add_entry(datetime(2023, 9, 15, 10, 0), "Login", "193.168.0.4")
    test1.add_entry(datetime(2023, 9, 15, 11, 31), "Logout", "122.456.2.3")
    test1.sort_time()
    test1.print_entries()

main(1,2)

'''if __name__ == "__main__":
    to_pred_path  = sys.argv[1] # 数据路径
    result_save_path = sys.argv[2] # 输出路径
    main(to_pred_path,result_save_path) # 运行主函数'''