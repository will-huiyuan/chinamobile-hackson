import database
import output
from datetime import datetime, timedelta


def unusual_ip(database: database, output):
    # 仅在100次以上记录时才进行后续操作
    if len(database.operations) >= 100:
        uncommon_ips = {}
        usual_ip = set()
        # 遍历数据，找出非常用ip
        for log_entry in database.operations:
            ip = log_entry[2]  # IP地址在元组中的第三个位置
            if (ip not in usual_ip):
                # 累计记录出现次数
                if (ip in uncommon_ips):
                    if uncommon_ips[ip][0] < 4:
                        uncommon_ips[ip][0] += 1
                        uncommon_ips[ip][1].append(log_entry)
                    # 若出现了超过4次，即为合理ip，移除记录
                    else:
                        del uncommon_ips[ip]
                        usual_ip.add(ip)
                # ip第一次出现，添加记录
                else:
                    uncommon_ips[ip] = [1, [log_entry]]
        # 输出结果
        for key in uncommon_ips:
            for log in uncommon_ips[key][1]:
                output.append([database.account, log[0], "非常用IP访问"])
        database.uncommon_ips = uncommon_ips


def not_in_worktime(database: database, output: output):
    # 定义工作时间
    start_work_time = 8
    end_work_time = 19
    operations = database.operations
    # 遍历数据库中的所有登录条目
    time_index = database.time_index
    for t in range(len(time_index)):
        # 通过time index来获取不同的时间所在的index
        operation_index = time_index[t]
        # 解析时间
        now_time = operations[operation_index][0].hour
        if (now_time < start_work_time) or (now_time >= end_work_time):
            try:
                for i in range(operation_index, time_index[t + 1]):
                    if operations[i][1] == "用户登陆":
                        output.append([database.account, operations[i][0], "非工作时间访问"])
            # 当遍历到最后一项时会index error，用列表长度作为下一个时间节点
            except IndexError:
                for i in range(operation_index, len(operations)):
                    if operations[i][1] == "用户登陆":
                        output.append([database.account, operations[i][0], "非工作时间访问"])

def unusual_login(database: database, output):
    timeindex = database.time_index
    operations = database.operations
    # 通过time index来获取不同的时间所在的index
    for i in range(len(timeindex)):
        # 一分钟内访问次数 >= 8
        this_time_i = timeindex[i]
        try:
            next_time_i = timeindex[i + 1]
        # 当遍历到最后一项时会index error，用列表长度作为下一个时间节点
        except:
            next_time_i = len(database.operations)
        # 访问次数 >= 8
        if next_time_i - this_time_i >= 8:
            for action_index in range(this_time_i, next_time_i):
                output.append([database.account, operations[action_index][0], "登录异常"])
        # 一分钟有两个ip访问
        else:
            ip_set = set()
            for action_index in range(this_time_i, next_time_i):
                # set中相同值只存在一次
                ip_set.add(operations[action_index][2])
                if len(ip_set) > 1:
                    for action_i in range(this_time_i, next_time_i):
                        output.append([database.account, operations[action_i][0], "登录异常"])
                    break


# 检查高频业务访问
def high_frequency_visit(database, output):
    # 记录该账号不同分钟的业务以及对应的时间
    business_list = []
    time_list = []

    i = 0
    # loop through 单个不同分钟的所有访问记录
    while i < len(database.time_index)-1:
        # 记录单个分钟所有的访问记录
        business_sublist = []
        # 记录当前时间，time_list和business_list中的index一一对应
        time_list.append(database.operations[database.time_index[i]][0])
        for j in range(database.time_index[i], database.time_index[i+1]):
            business_sublist.append(database.operations[j][1])
        # 将该一分钟访问的业务sublist添加到总业务list
        business_list.append(business_sublist)
        i += 1

    # 防止 index out of bound，单独处理最后一个不同分钟的访问记录
    business_sublist = []
    for j in range(database.time_index[i], len(database.operations)):
        business_sublist.append(database.operations[j][1])
    business_list.append(business_sublist)
    time_list.append(database.operations[database.time_index[i]][0])

    # loop through 每分钟的业务访问记录
    for m in range(len(business_list)):
        # 记录不同业务的名称以及对应的访问次数
        business_record = []
        count_record = []
        for business in business_list[m]:
            if business not in business_record:
                business_record.append(business)
                count_record.append(0)
            else:
                count_record[business_record.index(business)] += 1
        # loop through 所有业务的访问次数，每次达到五次及以上，则输出异常提示
        for num in count_record:
            if num >= 5:
                output.append([database.account, time_list[m], "业务高频访问"])


# 检查账号复用
def account_repeat(database, output):
    # 记录该账号每不同分钟的ip以及对应的时间
    ip_list = []
    time_list = []

    i = 0
    # loop through 单个不同分钟的所有访问记录
    while i < len(database.time_index)-1:
        # 记录两分钟内所有访问的ip
        ip_sublist = []

        time_list.append(database.operations[database.time_index[i]][0])
        for j in range(database.time_index[i], database.time_index[i+1]):
            ip_sublist.append(database.operations[j][2])

        # 检查下一个不同分钟是否与这一分钟是连续的两分钟，如果是，则添加下一分钟访问的所有所有ip到当前的ip_sublist
        if (database.operations[database.time_index[i+1]][0] - database.operations[database.time_index[i]][0]) <= timedelta(minutes=2):
            # 防止 index out of bound，单独处理是连续两分钟且第二分钟是最后一个不同分钟的情况
            if i == len(database.time_index)-2:
                for k in range(database.time_index[i+1], len(database.operations)):
                    ip_sublist.append(database.operations[k][2])
            # 其余普通情况
            else:
                for p in range(database.time_index[i+1], database.time_index[i+2]):
                    ip_sublist.append(database.operations[p][2])
        i += 1
        # 将该一分钟/连续两分钟访问的ip sublist添加到总ip list
        ip_list.append(ip_sublist)

    # 防止 index out of bound，单独处理最后一个不同分钟不在连续的两分钟内的情况
    if i < len(database.time_index):
        ip_sublist = []
        for j in range(database.time_index[i], len(database.operations)):
            ip_sublist.append(database.operations[j][2])
        ip_list.append(ip_sublist)
        time_list.append(database.operations[database.time_index[i]][0])

    # loop through 每两分钟的ip记录
    for n in range(len(ip_list)):
        # 记录不同的ip
        ip_record = []
        for ip in ip_list[n]:
            if ip not in ip_record:
                ip_record.append(ip)
        # 如果该两分钟内ip个数达到3个以及上，则输出异常提示
        if len(ip_record) >= 3:
            output.append([database.account, time_list[n], "账号复用"])
            
