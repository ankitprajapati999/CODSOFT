# ⚡ TO-DO v1.0.0

A modern, dark-mode desktop To-Do application built with Python + CustomTkinter.

No cloud.  
No accounts.  
No nonsense.  

Just you and your tasks — stored locally.

---

## 🧠 About

TO-DO is a lightweight desktop task manager focused on:

- Speed
- Simplicity
- Clean UI
- Persistent local storage

It runs fully offline and stores everything in a JSON file.

You own your data.

---

## ✨ Features

- 📖 Default Sections (Today, Important, Planned, Trash)
- ➕ Create Custom Lists
- ✅ Mark Tasks as Done
- ❌ Delete Tasks
- 💾 Automatic JSON Persistence
- 🌙 Clean Dark Theme
- ⚡ Instant Save on Every Action

---

## 🛠 Tech Stack

- Python 3.10+
- CustomTkinter
- Pillow
- JSON (local file storage)

---

# 🚀 Quick Start (Using `uv` — Recommended)

`uv` is a fast Python package manager and environment tool.

---

## 1️⃣ Install uv (if not installed)

### Windows (PowerShell)
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### macOS / Linux

```
curl -LsSf https://astral.sh/uv/install.sh | sh

```
## 2️⃣ Clone the Repository

```
git clone https://github.com/yourusername/todo-app.git
cd todo-app

```

## 3️⃣ Create Virtual Environment

```
uv venv
```

### Activate

```
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

```
## 4️⃣ Install Dependencies

```
uv pip install customtkinter pillow

```
##  5️⃣ Run the App
```
uv run main.py

```


## 📁 Project Structure
```
|
|- main.py
|- Data.py
|- logo.png
|- tasks.json (auto-generated)

```

## 🏷 Version

v1.0.0

Initial stable release. Core functionality complete.

## ⚠ Notes

All data is stored locally.

Deleting tasks.json permanently deletes your tasks.

No external services involved.



## 🔮 Future Improvements

- Task priority system
- Due dates
- Undo feature
- SQLite backend option
- UI refinement pass


---

Now this looks:
- Clean  
- Developer-level  
- Beginner-friendly  
- Production-structured  

You’re good to tag `v1.0.0` and ship it.
