import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ================= DATA STORAGE =================
class ContactStore:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.contacts = json.load(f)
            except:
                self.contacts = []
        else:
            self.save()

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.contacts, f, indent=4)

    def add(self, contact):
        self.contacts.append(contact)
        self.save()

    def delete(self, index):
        if 0 <= index < len(self.contacts):
            del self.contacts[index]
            self.save()

    def update(self, index, new_contact):
        if 0 <= index < len(self.contacts):
            self.contacts[index] = new_contact
            self.save()

    def search(self, keyword):
        return [
            (i, c) for i, c in enumerate(self.contacts)
            if keyword.lower() in c["name"].lower()
            or keyword in c["phone"]
        ]


# ================= UI =================
class ContactApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Contact Manager")
        self.geometry("900x550")

        self.store = ContactStore()
        self.selected_index = None

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        self.load_contacts()

    # ===== Sidebar (List + Search) =====
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Search...")
        self.search_entry.pack(padx=10, pady=10, fill="x")
        self.search_entry.bind("<KeyRelease>", self.perform_search)

        self.listbox = ctk.CTkScrollableFrame(self.sidebar)
        self.listbox.pack(expand=True, fill="both", padx=10, pady=10)

    # ===== Main Area (Details + Controls) =====
    def create_main_area(self):
        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.entries = {}

        fields = ["Name", "Phone", "Email", "Address"]

        for field in fields:
            label = ctk.CTkLabel(self.main, text=field)
            label.pack(pady=(10, 0))

            entry = ctk.CTkEntry(self.main)
            entry.pack(fill="x", padx=20)

            self.entries[field.lower()] = entry

        # Buttons
        btn_frame = ctk.CTkFrame(self.main)
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Add", command=self.add_contact).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Update", command=self.update_contact).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Delete", command=self.delete_contact).grid(row=0, column=2, padx=5)

    # ===== Core Functions =====
    def load_contacts(self):
        for widget in self.listbox.winfo_children():
            widget.destroy()

        for i, contact in enumerate(self.store.contacts):
            btn = ctk.CTkButton(
                self.listbox,
                text=f"{contact['name']} - {contact['phone']}",
                anchor="w",
                command=lambda idx=i: self.select_contact(idx)
            )
            btn.pack(fill="x", pady=2)

    def select_contact(self, index):
        self.selected_index = index
        contact = self.store.contacts[index]

        for key in self.entries:
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, contact[key])

    def add_contact(self):
        contact = {k: e.get() for k, e in self.entries.items()}
        if contact["name"] and contact["phone"]:
            self.store.add(contact)
            self.load_contacts()
            self.clear_fields()

    def update_contact(self):
        if self.selected_index is not None:
            contact = {k: e.get() for k, e in self.entries.items()}
            self.store.update(self.selected_index, contact)
            self.load_contacts()

    def delete_contact(self):
        if self.selected_index is not None:
            self.store.delete(self.selected_index)
            self.load_contacts()
            self.clear_fields()
            self.selected_index = None

    def perform_search(self, event=None):
        keyword = self.search_entry.get()
        results = self.store.search(keyword)

        for widget in self.listbox.winfo_children():
            widget.destroy()

        for i, contact in results:
            btn = ctk.CTkButton(
                self.listbox,
                text=f"{contact['name']} - {contact['phone']}",
                anchor="w",
                command=lambda idx=i: self.select_contact(idx)
            )
            btn.pack(fill="x", pady=2)

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, "end")


if __name__ == "__main__":
    app = ContactApp()
    app.mainloop()
