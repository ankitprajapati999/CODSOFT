import json
import os

class DictStore:
    def __init__(self, filename="tasks.json") -> None:
        self.filename = filename

        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.TaskInSection = json.load(f)
        else:
            self.TaskInSection = {
                " 📖 Today": [],
                " ☆ Important": [],
                " 📅 Planned": [],
                " 🗑 Trash": []
            }
            self.save()

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.TaskInSection, f, indent=4)

    def Push(self, section: str, tasks: list[str]):
        for task in tasks:
            self.TaskInSection[section].append({
                "text": task,
                "done": False
            })
        self.save()

    def Fetch(self, section: str):
        return self.TaskInSection.get(section, [])

    def Delete(self, section: str, index: int):
        if 0 <= index < len(self.TaskInSection[section]):
            del self.TaskInSection[section][index]
            self.save()

    def ToggleDone(self, section: str, index: int):
        task = self.TaskInSection[section][index]
        task["done"] = not task["done"]
        self.save()

    

if __name__ == "__main__":
    dicty = DictStore()
    dicty.Push(" 📖 Today", ["kaboom"])
    dicty.Push(" 📖 Today", ["madagascar"])
    print(dicty.Fetch(" 📖 Today"))