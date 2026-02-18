# A To-Do List application is a useful project that helps users manage
# and organize their tasks efficiently. This project aims to create a
# command-line or GUI-based application using Python, allowing

# users to create, update, and track their to-do lists

import customtkinter as ctk
import tkinter as tk
from PIL import Image
import Data

class SideCheek(ctk.CTkFrame):
    def __init__(self, master, DataStorage: Data.DictStore, on_select=None, **kwargs):
        super().__init__(master, fg_color="#161B22", **kwargs)

        self.on_select = on_select

        # MAIN GRID
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # header
        self.grid_rowconfigure(1, weight=1)  # scrollable list
        self.grid_rowconfigure(2, weight=0)  # button

        self.DataStorage = DataStorage

        # ================= HEADER =================
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", ipadx=0, padx=20, pady=(20, 10))
        header.grid_columnconfigure(1, weight=1)

        logo = Image.open("./logo.png")
        self.logo_img = ctk.CTkImage(logo, logo, size=(78, 55))

        ctk.CTkLabel(header, image=self.logo_img, text="").grid(
            row=0, column=0, sticky="w", padx=(0, 0),
        )

        ctk.CTkLabel(
            header,
            text="Sections",
            font=("Segoe UI Variable", 28, "bold")
        ).grid(row=0, column=1, padx=(0, 10), sticky="w")


            
        # ================= SCROLLABLE LIST =================
        self.section_list = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
        )
        self.section_list.grid(
            row=1, column=0, sticky="nsew", padx=20
        )
        self.section_list._scrollbar.grid_remove()
        self.section_list.grid_columnconfigure(0, weight=1)

        # dynamic items
        self.sections = [" 📖 Today", " ☆ Important", " 📅 Planned", " 🗑 Trash"]
        self.section_buttons = []
        self.activeButton = None

        for i, name in enumerate(self.sections):
            btn = ctk.CTkButton(
                self.section_list,
                text=name,
                font=("Segoe UI Variable", 18),
                fg_color="transparent",
                hover_color="#1C2128",
                anchor="w",
                height=49,
            )
            btn.configure(command=lambda b=btn: self.on_section_click(b))
            self.attach_context_menu(btn)

            btn.grid(
                row=i,
                column=0,
                padx=(13, 0),
                pady=3,
                sticky="ew"
            )
            self.section_buttons.append(btn)

        self.section_count = len(self.sections)

        # ================= BUTTON =================

        def NewListADD():
            name = f"List {self.section_count + 1}"

            btn = ctk.CTkButton(
                self.section_list,
                text= " ⭕ " + name,
                font=("Segoe UI Variable", 18),
                fg_color="transparent",
                hover_color="#1C2128",
                anchor="w",
                height=49,
            )
            btn.configure(command=lambda b=btn: self.on_section_click(b))
            self.attach_context_menu(btn)

            btn.grid(
                row=self.section_count,
                column=0,
                padx=(13, 0),
                pady=3,
                sticky="ew"
            )

            self.sections.append(name)
            self.section_buttons.append(btn)
            self.section_count += 1

            self.DataStorage.TaskInSection[name] = []
            self.DataStorage.save()


        self.new_list_btn = ctk.CTkButton(
            self,
            text="➕ New List",
            height=44,
            fg_color="#161B22",
            text_color="#1158C3",
            hover_color="#0D1117",
            command=NewListADD, 
            font=("Segoe UI Variable", 16)
        )
        self.new_list_btn.grid(
            row=2, column=0, sticky="ew", padx=20, pady=20
        )

    def on_section_click(self, name:ctk.CTkButton):

        if self.on_select:
            self.on_select(name)

            
        if self.activeButton:
            self.activeButton.configure(
                fg_color="transparent",
                hover_color="#1C2128"
            )

        # set new active
        name.configure(
            fg_color="#422FD0",    # important
            hover_color="#3A29B8"  # important
        )

        self.activeButton = name

        print(f"Selected section: {name.cget('text')}")
    

    def attach_context_menu(self, btn):
        menu = tk.Menu(btn, tearoff=0, background="#20272E", foreground="white", activebackground="#6588d4",font=("Segoe UI Variable", 14))
        menu.add_command(
            label="Delete",
            command=lambda b=btn: self.remove_section(b)
        )
        menu.add_command(
            label="Clear All",
            command=lambda b=btn: self.DataStorage.TaskInSection[b.cget("text")].clear()
        )
        btn.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    def remove_section(self, btn):

        # find the index
        index = self.section_buttons.index(btn)

        # remove from the data
        section_name = btn.cget("text")
        self.DataStorage.TaskInSection.pop(section_name, None)
        # remove from UI
        btn.destroy()

        # remove from lists
        del self.section_buttons[index]
        del self.sections[index]
        self.section_count -= 1
        

        # reset active
        if self.activeButton == btn:
            self.activeButton = None

        for i, b in enumerate(self.section_buttons):
            b.grid_configure(row=i)

        self.DataStorage.save()


        
class Maincheek(ctk.CTkFrame):
    def __init__(self, master, DataStorage: Data.DictStore,  **kwargs):
        super().__init__(master, **kwargs, fg_color="#0D1117")

        # GRID
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # title
        self.grid_rowconfigure(1, weight=1)  # list area
        self.grid_rowconfigure(2, weight=0)  # input bar

        self.DataStorage = DataStorage
        self.activeSection = None

        # ================= TITLE =================
        self.title_frame = ctk.CTkFrame(self, fg_color="#222A35", height=64)
        self.title_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(8, 17))
        self.title_frame.grid_propagate(False)
        self.title_frame.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(
            self.title_frame,
            text="No Section Opened",
            font=("Segoe UI Variable", 28, "bold")
        )
        self.label.grid(row=0, column=0, padx=20, ipady=20, sticky="w")

        # ================= LIST AREA =================
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="#2E3948")
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=1)

        placeholder = "No tasks here, Honestus :("

        lbl = ctk.CTkLabel(
                self.list_frame,
                text=placeholder,
                text_color="#F6F8FA",
                font=("Segoe UI Variable", 19)
            )
        lbl.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        # ================= INPUT BAR =================
        self.input_frame = ctk.CTkFrame(
            self,
            fg_color="#2A3442",
            height=82,
        )
        self.input_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(17, 8))
        self.input_frame.grid_propagate(False)

        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=0)

        # Entry – big, clean, confident
        self.entry = ctk.CTkEntry(
            self.input_frame,
            height=52,
            corner_radius=6,
            font=("Segoe UI Variable", 17),
            placeholder_text="Add a new task…",
            fg_color="#0F1720",
            border_color="#3B4656",
            border_width=1,
            text_color="#E6EDF3",
            placeholder_text_color="#8B949E",
        )        
        self.entry.bind("<Return>", self.add_task)
        self.entry.grid(
            row=0,
            column=0,
            padx=(18, 10),
            pady=14,
            sticky="ew"
        )

        # Button – authoritative, not playfu
        self.add_btn = ctk.CTkButton(
            self.input_frame,
            text="Add Task",
            height=52,
            width=140,
            corner_radius=14,
            font=("Segoe UI Variable", 16, "bold"),
            fg_color="#3A5FFF",
            hover_color="#2F4DE0",
            text_color="white",
            command=self.add_task
        )
        self.add_btn.grid(
            row=0,
            column=1,
            padx=(0, 18),
            pady=14
        )

    def load_tasks(self):

        for w in self.list_frame.winfo_children():
            w.destroy()

        tasks = self.DataStorage.Fetch(str(self.activeSection)) or []

        for i, task in enumerate(tasks):

            row_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row_frame.grid(row=i, column=0, pady=6, sticky="ew")
            row_frame.grid_columnconfigure(1, weight=1)

            # Checkbox
            check = ctk.CTkCheckBox(
                row_frame,
                text="",
                width=24,
                command=lambda idx=i: self.toggle_task(idx)
            )

            if task["done"]:
                check.select()

            check.grid(row=0, column=0, padx=(0, 10))

            # Task Label
            text_color = "#8B949E" if task["done"] else "#F6F8FA"

            lbl = ctk.CTkLabel(
                row_frame,
                text=task["text"],
                font=("Segoe UI Variable", 19),
                text_color=text_color
            )
            lbl.grid(row=0, column=1, sticky="w")

            # Delete Button
            del_btn = ctk.CTkButton(
                row_frame,
                text="✕",
                width=32,
                height=28,
                fg_color="#3A2B2B",
                hover_color="#4A1F1F",
                command=lambda idx=i: self.delete_task(idx)
            )
            del_btn.grid(row=0, column=2, padx=(10, 0))

            
    def toggle_task(self, index):
        self.DataStorage.ToggleDone(str(self.activeSection), index)
        self.load_tasks()

    def delete_task(self, index):
        self.DataStorage.Delete(str(self.activeSection), index)
        self.load_tasks()


    def add_task(self, event=None):

        task = self.entry.get().strip()

        if not task or not self.activeSection:
            return

        self.DataStorage.Push(self.activeSection, [task])
        self.entry.delete(0, "end")
        self.load_tasks()

    def set_section(self, text:str):
        self.activeSection = text
        self.label.configure(text=text)
        self.load_tasks()

    
class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#0D1117")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.geometry("900x550")
        # self.minsize(900, 550) - Not Needed as this is not fucking working with the tiling Window Manager
        self.title("TO-DO")

        #Layout Baddie - MC ketlo time khai gyuuu
        self.grid_rowconfigure(0, weight=1)
        # Sidebar = fixed
        self.grid_columnconfigure(0, weight=0)
        # Main area = flexible
        self.grid_columnconfigure(1, weight=1)

        self.DataStorage = Data.DictStore()

        self.SideBar = SideCheek(master=self,  DataStorage=self.DataStorage, on_select=self.update_main)
        self.SideBar.grid(row=0, column=0, padx=(20, 2), pady=22, sticky="nsew")
        self.SideBar.grid_propagate(False)

        # Trash will remove it later ,activeSection=self.SideBar.activeButton

        self.Main = Maincheek(master=self, DataStorage=self.DataStorage)
        self.Main.grid(row=0, column=1, padx=(3, 20), pady=16, sticky="nsew")

    def update_main(self, btn:ctk.CTkButton):
        self.Main.set_section(btn.cget("text")) 



def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()