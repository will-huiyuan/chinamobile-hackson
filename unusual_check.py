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
        for t_index in database.time_index:
            # 解析时间
            now_time = operations[t_index][0].hour
            if (now_time < start_work_time) or (now_time > end_work_time):
                output.append([database.account, operations[t_index][0], "非工作时间访问"])


def unusual_login(database:database,output):
    pass


def account_repeat(database, output):
    ip_list = []
    time_list = []

    i = 0
    while i < len(database.time_index)-1:
        ip_sublist = []
        # if minute is even
        if database.operations[database.time_index[i]][0].minute % 2 == 0:
            time_list.append(database.operations[database.time_index[i]][0])
            for j in range(database.time_index[i], database.time_index[i+1]):
                ip_sublist.append(database.operations[j][2])

            # check next minute within 2
            if (database.operations[database.time_index[i+1]][0] - database.operations[database.time_index[i]][0]) < timedelta(minutes=2):
                if i == len(database.time_index)-2:
                    for k in range(database.time_index[i+1], len(database.operations)):
                        ip_sublist.append(database.operations[k][2])
                else:
                    for k in range(database.time_index[i+1], database.time_index[i+2]):
                        ip_sublist.append(database.operations[k][2])

                i += 1
            i += 1
        # if minute is odd
        else:
            time_list.append(database.operations[database.time_index[i]][0])
            for j in range(database.time_index[i], database.time_index[i+1]):
                ip_sublist.append(database.operations[j][2])
            i += 1

        ip_list.append(ip_sublist)

    if i < len(database.time_index):
        ip_sublist = []
        for j in range(database.time_index[i], len(database.operations)):
            ip_sublist.append(database.operations[j][2])
        ip_list.append(ip_sublist)
        time_list.append(database.operations[database.time_index[i]][0])

    for i in range(len(ip_list)):
        ip_record = []
        for ip in ip_list[i]:
            if ip not in ip_record:
                ip_record.append(ip)
        if len(ip_record) >= 3:
            output.append([database.account, time_list[i], "账号复用"])


def high_frequency_visit(database, output):
    business_list = []
    time_list = []

    i = 0
    while i < len(database.time_index)-1:
        business_sublist = []

        time_list.append(database.operations[database.time_index[i]][0])
        for j in range(database.time_index[i], database.time_index[i+1]):
            business_sublist.append(database.operations[j][1])

        business_list.append(business_sublist)
        i += 1

    business_sublist = []
    for j in range(database.time_index[i], len(database.operations)):
        business_sublist.append(database.operations[j][1])
    business_list.append(business_sublist)
    time_list.append(database.operations[database.time_index[i]][0])

    for m in range(len(business_list)):
        business_record = []
        count_record = []
        for business in business_list[m]:
            if business not in business_record:
                business_record.append(business)
                count_record.append(business_list[m].count(business))

        for num in count_record:
            if num >= 5:
                output.append([database.account, time_list[m], "业务高频访问"])
