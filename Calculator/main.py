import tkinter as tk


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("350x500")
        self.resizable(False, False)

        self.expression = ""

        # Display
        self.display = tk.Entry(
            self,
            font=("Segoe UI", 24),
            borderwidth=5,
            relief="ridge",
            justify="right"
        )
        self.display.pack(fill="both", padx=10, pady=10, ipady=10)

        # Buttons
        buttons = [
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            ("0", ".", "=", "+"),
            ("C", "DEL")
        ]

        for row in buttons:
            frame = tk.Frame(self)
            frame.pack(expand=True, fill="both")

            for btn in row:
                button = tk.Button(
                    frame,
                    text=btn,
                    font=("Segoe UI", 18),
                    command=lambda b=btn: self.on_click(b)
                )
                button.pack(side="left", expand=True, fill="both")

    def on_click(self, char):
        if char == "C":
            self.expression = ""
            self.display.delete(0, tk.END)

        elif char == "DEL":
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

        elif char == "=":
            try:
                result = str(eval(self.expression))
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
                self.expression = result
            except Exception:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
                self.expression = ""

        else:
            self.expression += char
            self.display.insert(tk.END, char)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
