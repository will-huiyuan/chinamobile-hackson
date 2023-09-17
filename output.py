
class Output:
    def __init__(self, path):
        self.path = path
        self.file = open(path, 'w', encoding='utf-8')
        self.board=""


    def append(self, content: list):
        self.board+=f"{content[0]},{content[1].strftime('%Y-%m-%d %H:%M')},{content[2]}\n"

