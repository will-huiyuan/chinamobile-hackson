
class Output:
    def __init__(self, path):
        self.path = path
<<<<<<< HEAD
        self.output=""
=======
        self.file = open(path, 'w', encoding='utf-8')
        self.board=""
>>>>>>> 05a8ceced23b946d5f3fd3a39ab05904edbf791d


    def append(self, content: list):
        self.board+=f"{content[0]},{content[1].strftime('%Y-%m-%d %H:%M')},{content[2]}\n"

    def close(self):
        self.file = open(self.path, 'w', encoding='utf-8')
        self.file.write("异常账号,异常时间,异常类型\n")
        self.file.write(f"{self.output}\n")
        print(f"output file saved at {self.path}")
        self.file.close()

