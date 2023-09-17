class Output:
    def __init__(self, path):
        self.path = path
        self.output=""
    
    def append(self, content: list):
        self.output+=f"{content[0]},{content[1].strftime('%Y-%m-%d %H:%M')},{content[2]}\n"

    def save(self):
        self.file = open(self.path, 'w', encoding='utf-8')
        self.file.write("异常账号,异常时间,异常类型\n")
        self.file.write(f"{self.output}\n")
        print(f"output file saved at {self.path}")
        self.file.close()

