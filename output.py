class Output:
    def __init__(self, path, testmode=False):
        self.path = path
        self.file = open(path, 'w', encoding='utf-8')
        self.testmode = testmode
        self.bord = []
        if testmode:
            self.file.write("异常账号,异常时间,异常类型,testdata\n")
        else:
            self.file.write("异常账号,异常时间,异常类型\n")

    def append(self, content: list):
        self.file.write(f"{content[0]},{content[1].strftime('%Y-%m-%d %H:%M')},{content[2]}\n")

    def close(self):
        print(f"output file saved at {self.path}")
        self.file.close()
