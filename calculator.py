"""A standalone calculator using only Python's standard library."""

import tkinter as tk
from decimal import Decimal, InvalidOperation, localcontext


def calculate(left, operator, right):
    with localcontext() as context:
        context.prec = 28
        a, b = Decimal(left), Decimal(right)
        if operator == "+":
            result = a + b
        elif operator == "−":
            result = a - b
        elif operator == "×":
            result = a * b
        elif operator == "÷":
            if b == 0:
                raise ValueError("Cannot divide by zero")
            result = a / b
        else:
            raise ValueError("Unknown operator")
        return format(result, "f").rstrip("0").rstrip(".") if "." in format(result, "f") else format(result, "f")


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("380x560")
        self.minsize(320, 470)
        self.configure(bg="#13151c")
        self.value = "0"
        self.left = None
        self.operator = None
        self.fresh = True
        self.error = False
        self.history = tk.StringVar(value="Ready to calculate")
        self.display = tk.StringVar(value="0")

        tk.Label(self, text="CALCULATOR", bg="#13151c", fg="#939aaf",
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", padx=24, pady=(24, 12))
        tk.Label(self, textvariable=self.history, bg="#13151c", fg="#939aaf",
                 font=("Segoe UI", 11), anchor="e").pack(fill="x", padx=24)
        self.screen = tk.Label(self, textvariable=self.display, bg="#13151c", fg="#f4f6fc",
                               font=("Segoe UI", 34), anchor="e")
        self.screen.pack(fill="x", padx=24, pady=(4, 20))
        keys = tk.Frame(self, bg="#13151c")
        keys.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        for column in range(4):
            keys.columnconfigure(column, weight=1, uniform="keys")
        for row in range(5):
            keys.rowconfigure(row, weight=1, uniform="keys")
        layout = [("C", 0, 0, 3), ("÷", 0, 3, 1),
                  ("7", 1, 0, 1), ("8", 1, 1, 1), ("9", 1, 2, 1), ("×", 1, 3, 1),
                  ("4", 2, 0, 1), ("5", 2, 1, 1), ("6", 2, 2, 1), ("−", 2, 3, 1),
                  ("1", 3, 0, 1), ("2", 3, 1, 1), ("3", 3, 2, 1), ("+", 3, 3, 1),
                  ("0", 4, 0, 2), (".", 4, 2, 1), ("=", 4, 3, 1)]
        for label, row, column, span in layout:
            color = "#7565ee" if label == "=" else "#30334b" if label in "+−×÷" else "#242833"
            tk.Button(keys, text=label, command=lambda key=label: self.press(key),
                      bg=color, fg="#ffffff", activebackground="#4c5069",
                      activeforeground="white", relief="flat", bd=0, cursor="hand2",
                      font=("Segoe UI", 21), takefocus=True).grid(
                          row=row, column=column, columnspan=span, sticky="nsew", padx=4, pady=4)
        tk.Label(self, text="Enter  =     •     Esc  clear     •     Backspace  delete",
                 bg="#13151c", fg="#939aaf", font=("Segoe UI", 9)).pack(pady=(0, 14))
        self.bind("<Key>", self.keyboard)

    def keyboard(self, event):
        aliases = {"Return": "=", "KP_Enter": "=", "Escape": "C", "BackSpace": "delete"}
        key = aliases.get(event.keysym, event.char)
        key = {"*": "×", "/": "÷", "-": "−", "c": "C", "C": "C"}.get(key, key)
        if key and key in list("0123456789.+−×÷=C") + ["delete"]:
            self.press(key)
            return "break"

    def press(self, key):
        if key == "C" or self.error:
            self.value, self.left, self.operator = "0", None, None
            self.fresh, self.error = True, False
            self.history.set("Ready to calculate")
            if key == "C":
                self.refresh()
                return
        try:
            if key in "0123456789.":
                if self.fresh:
                    self.value = "0"
                    self.fresh = False
                if key == ".":
                    if "." not in self.value:
                        self.value += "."
                elif len(self.value) < 24:
                    self.value = key if self.value == "0" else self.value + key
            elif key == "delete":
                if not self.fresh:
                    self.value = self.value[:-1] or "0"
            elif key in ("+", "−", "×", "÷"):
                if self.operator and not self.fresh:
                    self.value = calculate(self.left, self.operator, self.value)
                self.left, self.operator, self.fresh = self.value, key, True
                self.history.set(f"{self.left} {key}")
            elif key == "=" and self.operator and not self.fresh:
                self.history.set(f"{self.left} {self.operator} {self.value} =")
                self.value = calculate(self.left, self.operator, self.value)
                self.left, self.operator, self.fresh = None, None, True
        except (ValueError, InvalidOperation, ArithmeticError) as error:
            self.history.set(str(error) if isinstance(error, ValueError) else "Unable to calculate")
            self.value, self.error = "Error", True
        self.refresh()

    def refresh(self):
        shown = self.value
        if len(shown) > 20:
            shown = format(Decimal(shown), ".12g")
        self.display.set(shown)
        self.screen.configure(font=("Segoe UI", 34 if len(shown) < 13 else 22))


if __name__ == "__main__":
    Calculator().mainloop()
