class Output:
    def __init__(self, path, testmode=False):
        self.path = path
        self.file = open(path, 'w', encoding='utf-8')
        self.testmode = testmode
        if testmode:
            self.file.write("异常账号,异常时间,异常类型,testdata\n")
        else:
            self.file.write("异常账号,异常时间,异常类型\n")

    def append(self, content: list):
        if self.testmode:
            self.file.write(f"{content[0]},{content[1].strftime('%Y-%m-%d %H:%M')},{content[2]},{content[3]}\n")
        else:
            # print(content)
            self.file.write(f"{content[0]},{content[1].strftime('%Y-%m-%d %H:%M')},{content[2]}\n")
    #
    # def unusual_save(self,e):
    #     print("code exit with error: " + str(e))
    #     self.close()

    def close(self):
        print(f"output file saved at {self.path}")
        self.file.close()