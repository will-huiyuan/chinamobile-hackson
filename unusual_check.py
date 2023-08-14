from tools import *
import pandas as pd
import datetime

"""输入文件已根据账户分组，并按时间排序"""


def high_frequency_access(timed_DF, output_file,
                          duration=1, limit_frequency=5):
    """{sorted_account}在{duration}min内，访问次数超过{limit_frequency}次"""
    pass


def repeated_account_use(time_group, output_file, duration=2, limit_ips=3):
    """{sorted_account}在{duration}min内，使用不同的IP地址>={limit_ips}个"""
    time_group = list(time_group)
    # print("in repeated_account_use")
    now_index = 0
    while now_index < len(time_group):
        check_df = time_group[now_index][1]
        now_time = time_group[now_index][0]
        # print(check_df)
        error_flag = False
        if (len(check_df["源IP"].unique()) >= limit_ips):
            output_file.append([check_df.iloc[0, 2], now_time, "账号复用",check_df])
            error_flag = True
        if(now_time.minute%2 == 0 and not error_flag):
            for i in range(1, duration):
                try:
                    if (time_group[now_index + i][0]- now_time).seconds / 60 <= duration-1:
                        check_df = pd.concat([check_df,time_group[now_index + i][1]],ignore_index=True)
                        # print("concat," + str(i))
                        now_index+=1
                        if (len(check_df["源IP"].unique()) >= limit_ips):
                            output_file.append([check_df.iloc[i, 2], time_group[now_index][0], "账号复用",check_df])
                    else:
                        break
                except IndexError:
                    break
            # print(check_df)
        now_index += 1
        # print(str(len(time_group))+"/"+str(now_index))



def unusual_ip_access(sorted_account, output_file, limit_amount=100,
                      limit_ip_access_frequency=5):
    """{sorted_account}出现访问超过{limit_amount}次，并且单个ip访问次数小于{limit_frequency}次"""
    if len(sorted_account) >= limit_amount:
        grouped_ip = sorted_account.groupby("源IP")
        for _, ip_group in enumerate(grouped_ip):
            ip = ip_group[1]
            if len(ip) < limit_ip_access_frequency:
                for i in range(len(ip)):
                    output_file.append([ip.iloc[i, 2], ip.iloc[i, 0], "非常用IP访问",ip.iloc[i,5]])


def anti_work_overtime(sorted_account, output_file):
    pass


def unusual_login(timed_DF, output_file, limit_frequency=8, limit_ips=2):
    """账号在一分钟内访问了{limit_frequency}次或者访问了{limit_ips}个不同的IP地址"""
    if len(timed_DF) >= limit_frequency:
        for i in range(len(timed_DF)):
            output_file.append([timed_DF.iloc[i, 2], timed_DF.iloc[i, 0], "登录异常",f"超过次数 {i}"])
    elif (len(timed_DF["源IP"].unique()) >= limit_ips):
        for i in range(len(timed_DF)):
            output_file.append([timed_DF.iloc[i, 2], timed_DF.iloc[i, 0], "登录异常", f"ip异常 {i},{len(timed_DF['源IP'].unique())}"])
