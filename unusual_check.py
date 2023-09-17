import database
import output
from datetime import datetime
def unusual_ip(database:database, output):
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
                        del uncommon_ips[ip]
                        usual_ip.add(ip)
                else:
                    uncommon_ips[ip] = [1, [log_entry]]

        for key in uncommon_ips:
            for log in uncommon_ips[key][1]:
                output.append([database.account,log[0],"非常用IP访问"])


def not_in_worktime(database:database,output:output):
        start_work_time = 8
        end_work_time = 19
        operations = database.operations
        # 遍历数据库中的所有登录条目
        time_index = database.time_index
        for t in range(len(time_index)):
            operation_index = time_index[t]
            # 解析时间
            now_time = operations[operation_index][0].hour
            if (now_time < start_work_time) or (now_time > end_work_time):
                for i in range(operation_index,time_index[t+1]):
                    output.append([database.account, operations[i][0], "非工作时间访问"])


def unusual_login(database:database,output):
    pass
