import sys
import database
import os
from algorithm import singly_linked_list
import preprocess
import unusual_check
import output
from datetime import datetime


def main(file_path,result_save_path):
    actions = preprocess.main(file_path)
    out = output.Output(result_save_path)
    for action in actions:
        unusual_check.unusual_ip(action,output)
        unusual_check.unusual_login(action,output)
        unusual_check.not_in_worktime(action,output)
        unusual_check.account_repeat(action,output)
        unusual_check.high_frequency_visit(action,output)
    out.save()


main("test.csv",0)

'''if __name__ == "__main__":
    to_pred_path  = sys.argv[1] # 数据路径
    result_save_path = sys.argv[2] # 输出路径
    main(to_pred_path,result_save_path) # 运行主函数'''