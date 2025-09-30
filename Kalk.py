import tkinter as tk
from tkinter import messagebox


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Калькулятор")
        self.window.geometry("300x400")
        self.window.resizable(False, False)

        
        self.display_font = ("Arial", 18)
        self.button_font = ("Arial", 14)

        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")


        self.create_display()
        self.create_buttons()

    def create_display(self):

        display_frame = tk.Frame(self.window, height=100)
        display_frame.pack(pady=20, padx=20, fill=tk.X)

        display = tk.Entry(display_frame,
                           textvariable=self.result_var,
                           font=self.display_font,
                           justify="right",
                           state="readonly",
                           bd=0,
                           bg="#f0f0f0")
        display.pack(fill=tk.BOTH, ipady=10)

    def create_buttons(self):

        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)


        buttons = [
            ['C', '±', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '=']
        ]

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text:  
                    if text in ['/', '*', '-', '+', '=']:
                        bg_color = "#ff9500"
                        fg_color = "white"
                    elif text in ['C', '±', '%']:
                        bg_color = "#a6a6a6"
                        fg_color = "black"
                    else:
                        bg_color = "#333333"
                        fg_color = "white"

                    if text == '0':
                        btn = tk.Button(buttons_frame,
                                        text=text,
                                        font=self.button_font,
                                        bg=bg_color,
                                        fg=fg_color,
                                        bd=0,
                                        command=lambda t=text: self.button_click(t))
                        btn.grid(row=i, column=j, columnspan=2, sticky="ew", padx=1, pady=1)
                    else:
                        btn = tk.Button(buttons_frame,
                                        text=text,
                                        font=self.button_font,
                                        bg=bg_color,
                                        fg=fg_color,
                                        bd=0,
                                        command=lambda t=text: self.button_click(t))
                        btn.grid(row=i, column=j, sticky="ew", padx=1, pady=1)

        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)

    def button_click(self, text):
        try:
            if text.isdigit() or text == '.':
                self.input_number(text)
            elif text in ['+', '-', '*', '/']:
                self.input_operator(text)
            elif text == '=':
                self.calculate()
            elif text == 'C':
                self.clear()
            elif text == '±':
                self.toggle_sign()
            elif text == '%':
                self.percentage()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.clear()

    def input_number(self, num):
        if self.result_var.get() == "0" or self.result_var.get() == "Ошибка":
            if num == '.':
                self.current_input = "0."
            else:
                self.current_input = num
        else:
            if num == '.' and '.' in self.current_input:
                return
            self.current_input += num

        self.result_var.set(self.current_input)

    def input_operator(self, op):
        if self.current_input and self.current_input[-1] not in ['+', '-', '*', '/']:
            self.current_input += op
            self.result_var.set(self.current_input)

    def calculate(self):
        try:
            if self.current_input:
                expression = self.current_input.replace('×', '*').replace('÷', '/')

                result = eval(expression)

                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

                self.result_var.set(str(result))
                self.current_input = str(result)
        except ZeroDivisionError:
            self.result_var.set("Ошибка")
            self.current_input = ""
            messagebox.showerror("Ошибка", "Деление на ноль!")
        except:
            self.result_var.set("Ошибка")
            self.current_input = ""
            messagebox.showerror("Ошибка", "Некорректное выражение!")

    def clear(self):
        self.current_input = ""
        self.result_var.set("0")

    def toggle_sign(self):
        if self.current_input and self.current_input != "0":
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.result_var.set(self.current_input)

    def percentage(self):
        try:
            if self.current_input:
                value = float(self.current_input)
                result = value / 100
                self.current_input = str(result)
                self.result_var.set(self.current_input)
        except:
            pass

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()