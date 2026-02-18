
class DictStore:
    def __init__(self) -> None:
        self.TaskInSection = {
            " 📖 Today" : ["Collge buddy"],
            " ☆ Important" : [],
            " 📅 Planned" : [],
            " 🗑 Trash" : []
        }

    def Push(self, section:str, tasks:list[str]):
        for task in tasks:
            self.TaskInSection[section].append(task)
            print(self.TaskInSection[section])

    def Fetch(self, section:str) -> list:
        return self.TaskInSection[section]
    

if __name__ == "__main__":
    dicty = DictStore()
    dicty.Push(" 📖 Today", ["kaboom"])
    dicty.Push(" 📖 Today", ["madagascar"])
    print(dicty.Fetch(" 📖 Today"))