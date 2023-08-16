import pandas as pd
import tools
"""输入文件已根据账户分组，并按时间排序"""

work_start_time = pd.Timestamp('08:00:00').time()
work_end_time = pd.Timestamp('19:00:00').time()

def high_freq_op_and_work_overtime(operations, output_file, limit_frequency=5):
    """{sorted_account}在1min内，访问一个业务次数超过{limit_frequency}次"""
    high_freq = False
    def not_in_work_time(timestamp):
        return not (work_start_time <= timestamp.time() <= work_end_time)
    for operation in operations:
        if len(operation[1]) > limit_frequency and not high_freq:
            output_file.append([operation[1].iloc[0, 2], operation[1].iloc[0, 0], "业务高频访问"])
            high_freq = True
        access = tools.clean_access(operation[0])
        if (access == "用户登陆" or access == "用户登录") and not_in_work_time(operation[1].iloc[0, 0]):
            for _ in range(len(operation[1])):
                output_file.append([operation[1].iloc[0, 2], operation[1].iloc[0, 0], "非工作时间访问"])


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
        if (check_df["源IP"].nunique() >= limit_ips):
            output_file.append([check_df.iloc[0, 2], now_time, "账号复用", check_df])
            error_flag = True
        if (now_time.minute % 2 == 0 and not error_flag):
            for i in range(1, duration):
                try:
                    if (time_group[now_index + i][0] - now_time).seconds / 60 <= duration - 1:
                        check_df = pd.concat([check_df, time_group[now_index + i][1]], ignore_index=True)
                        # print("concat," + str(i))
                        now_index += 1
                        if check_df["源IP"].nunique() >= limit_ips:
                            output_file.append([check_df.iloc[i, 2], time_group[now_index][0], "账号复用"])
                    else:
                        # break
                        pass
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
                    output_file.append([ip.iloc[i, 2], ip.iloc[i, 0], "非常用IP访问"])


def anti_work_overtime(operations, output_file):
    pass


def unusual_login(timed_DF, output_file, limit_frequency=8, limit_ips=2):
    """账号在一分钟内访问了{limit_frequency}次或者访问了{limit_ips}个不同的IP地址"""
    if len(timed_DF) >= limit_frequency:
        for i in range(len(timed_DF)):
            output_file.append([timed_DF.iloc[i, 2], timed_DF.iloc[i, 0], "登录异常", f"超过次数 {i}"])
    elif (timed_DF["源IP"].nunique() >= limit_ips):
        for i in range(len(timed_DF)):
            output_file.append(
                [timed_DF.iloc[i, 2], timed_DF.iloc[i, 0], "登录异常"])
