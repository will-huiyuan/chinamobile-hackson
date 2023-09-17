import sys
import database
import os
from algorithm import singly_linked_list
import preprocess

#for testing:-----
from datetime import datetime
#-----

def main(file_path,result_save_path):
    preprocess.main(file_path)


main("test.csv",0)

'''if __name__ == "__main__":
    to_pred_path  = sys.argv[1] # 数据路径
    result_save_path = sys.argv[2] # 输出路径
    main(to_pred_path,result_save_path) # 运行主函数'''