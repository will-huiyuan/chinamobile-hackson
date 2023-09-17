import database
import output
from datetime import datetime
def unusual_login(database:database, output):
    if len(database.operations) >= 100:
        uncommon_ips = {}
        usual_ip = set()
        # 遍历列表并更新字典中的计数
        for log_entry in database.operations:
            ip = log_entry[2]  # IP地址在元组中的第三个位置
            if (ip not in usual_ip):
                if (ip in uncommon_ips):

                    if uncommon_ips[ip][0] < 5:
                        uncommon_ips[ip][0] += 1
                        uncommon_ips[ip][1].append(log_entry)
                    else:
                        usual_ip.add(ip)
                        del uncommon_ips[ip]
                else:
                    uncommon_ips[ip] = [1, database.operations]

        for err_set in uncommon_ips:
            output.append([database.account,err_set[1][0],"非常用IP访问"])


def not_in_worktime(database:database,output:output):
    # 每天正常工作时间为8:00~19:00，其余为非工作时间，请筛选出非工作时间的登录情况并输出到output中
        # 定义工作时间
        start_work_time = 8  # 8:00
        end_work_time = 19  # 19:00

        # 遍历数据库中的所有登录条目
        for log_entry in database.operations["time"]:
            # 解析时间
            entry_time = datetime.strptime(log_entry, '%Y-%m-%d %H:%M')

            # 检查是否在非工作时间
            if entry_time.hour < start_work_time or entry_time.hour >= end_work_time:
                output.append([database.account, entry_time, "非工作时间访问"])


def unusual_ip(database:database,output):
    pass
