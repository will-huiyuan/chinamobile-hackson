class Database:
  def __init__(self, account):
    # 记录“从账号”字符串
    self.account = account
    # 记录在一个时间点该账号的操作内容与源IP
    self.operations = {"time": [], "action": [], "ip": []}
    # 记录每个新分钟的第一个元素的index
    self.time_index = [0]

  def sort_time(self):
    # 对操作记录按时间排序
    self.operations = sorted(zip(self.operations['time'], self.operations['action'], self.operations['ip']))

    # 创建time_index序列以记录每一个不同的时间点，以便查找下一分钟该账户的所有执行操作
    curr = self.operations[0][0]
    for o in range(len(self.operations)):
      if self.operations[o][0] != curr:
        self.time_index.append(o)
        curr = self.operations[o][0]

  def add_entry(self, time, action, ip):
    # 添加新的操作记录
    self.operations["time"].append(time)
    self.operations["action"].append(action)
    self.operations["ip"].append(ip)

  # 用于测试,显示该database object中含有的内容
  def print_entries(self):
    for entry in self.operations:
      time, action, ip = entry
      print(f"Time: {time}, Action: {action}, IP: {ip}")
    print(f"time_index: {self.time_index}")
    
