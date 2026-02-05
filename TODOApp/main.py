# A To-Do List application is a useful project that helps users manage
# and organize their tasks efficiently. This project aims to create a
# command-line or GUI-based application using Python, allowing

# users to create, update, and track their to-do lists

import customtkinter as ctk
import tkinter as tk
from PIL import Image

class SideCheek(ctk.CTkFrame):
    def __init__(self, master, on_select=None, **kwargs):
        super().__init__(master, fg_color="#161B22", **kwargs)

        self.on_select = on_select

        # MAIN GRID
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # header
        self.grid_rowconfigure(1, weight=1)  # scrollable list
        self.grid_rowconfigure(2, weight=0)  # button

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
            command=lambda b=btn: self.remove_section(b)
        )
        btn.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    def remove_section(self, btn):

        # find the index
        index = self.section_buttons.index(btn)

        # remove from UI
        btn.destroy()

        # remove from lists
        del self.section_buttons[index]
        del self.sections[index]
        self.section_count -= 1

        # reset active
        if self.activeButton == btn:
            self.activeButton = None

        # re-grid remaining buttons to fix row order
        for i, b in enumerate(self.section_buttons):
            b.grid_configure(row=i)

        
class Maincheek(ctk.CTkFrame):
    def __init__(self, master, activeSection: ctk.CTkButton | None, **kwargs):
        super().__init__(master, **kwargs, fg_color="#0D1117")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
 
        self.label = ctk.CTkLabel(self, text="No Section Opened", font=("Arial", 36))
        self.label.grid(row=0, column=0, padx=(30, 9), sticky="w")

    def set_section(self, text):
        self.label.configure(text=text)



class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#0D1117")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.geometry("900x550")
        # self.minsize(900, 550) 
        self.title("TO-DO")

        #Layout Baddie - MC ketlo time khai gyuuu
        self.grid_rowconfigure(0, weight=1)
        # Sidebar = fixed
        self.grid_columnconfigure(0, weight=0)
        # Main area = flexible
        self.grid_columnconfigure(1, weight=1)


        self.SideBar = SideCheek(master=self, on_select=self.update_main)
        self.SideBar.grid(row=0, column=0, padx=(20, 10), pady=19, sticky="nsew")
        self.SideBar.grid_propagate(False)


        self.Main = Maincheek(master=self, activeSection=self.SideBar.activeButton)
        self.Main.grid(row=0, column=1, padx=6, pady=16, sticky="nsew")

    def update_main(self, btn):
        self.Main.set_section(btn.cget("text")) 



def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()