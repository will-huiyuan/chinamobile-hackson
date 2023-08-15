# 导入所需的包
import unusual_check
from output import Output
from tools import *
import pandas as pd

def main(train_path, save_path):
    output_file = Output(save_path)
    # todo disable testmode
    input = pd.read_csv(train_path)  # 读取数据
    all_account = input.groupby("从账号")
    for _, acc in enumerate(all_account):
        sorted_account = sort_by_time(acc[1])
        sorted_account["操作时间"] = pd.to_datetime(sorted_account["操作时间"])
        """"""
        unusual_check.unusual_ip_access(sorted_account, output_file)
        time_group = sorted_account.groupby("操作时间")
        """"""
        unusual_check.repeated_account_use(time_group, output_file)
        for __, timed_info in enumerate(time_group):
            timed_group = timed_info[1]
            """"""
            unusual_check.unusual_login(timed_group, output_file, limit_frequency=8, limit_ips=2)
            timed_group["操作内容"] = timed_group["操作内容"].apply(clean_access)
            operations = timed_group.groupby("操作内容")
            """"""
            unusual_check.high_freq_op_and_work_overtime(operations, output_file)
            """"""
            # unusual_check.anti_work_overtime(operations, output_file)
    output_file.close()


if __name__ == "__main__":
    import time

    # setup timer
    start = time.time()
    main(get_fcsv_path(), "out.csv")  # 运行主函数
    end = time.time()
    print(f"运行时间：{end - start}秒")

"""
if __name__ == "__main__":
    to_pred_path  = sys.argv[1] # 数据路径
    result_save_path = sys.argv[2] # 输出路径
    main(to_pred_path,result_save_path) # 运行主函数
"""
