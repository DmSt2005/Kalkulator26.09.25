import tkinter as tk
from tkinter import messagebox


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Калькулятор")
        self.window.geometry("300x400")
        self.window.resizable(False, False)

        # Настройка шрифтов (должны быть объявлены ДО создания элементов)
        self.display_font = ("Arial", 18)
        self.button_font = ("Arial", 14)

        # Переменные для хранения данных
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")

        # Создание интерфейса
        self.create_display()
        self.create_buttons()

    def create_display(self):
        """Создание дисплея калькулятора"""
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
        """Создание кнопок калькулятора"""
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Расположение кнопок
        buttons = [
            ['C', '±', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '=']
        ]

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text:  # Пропускаем пустые кнопки
                    # Определяем цвет кнопки
                    if text in ['/', '*', '-', '+', '=']:
                        bg_color = "#ff9500"
                        fg_color = "white"
                    elif text in ['C', '±', '%']:
                        bg_color = "#a6a6a6"
                        fg_color = "black"
                    else:
                        bg_color = "#333333"
                        fg_color = "white"

                    # Особый размер для кнопки 0
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

        # Настройка весов строк и столбцов для правильного растяжения
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)

    def button_click(self, text):
        """Обработка нажатия кнопок"""
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
        """Ввод чисел и точки"""
        if self.result_var.get() == "0" or self.result_var.get() == "Ошибка":
            if num == '.':
                self.current_input = "0."
            else:
                self.current_input = num
        else:
            if num == '.' and '.' in self.current_input:
                return  # Не допускаем две точки
            self.current_input += num

        self.result_var.set(self.current_input)

    def input_operator(self, op):
        """Ввод оператора"""
        if self.current_input and self.current_input[-1] not in ['+', '-', '*', '/']:
            self.current_input += op
            self.result_var.set(self.current_input)

    def calculate(self):
        """Вычисление результата"""
        try:
            if self.current_input:
                # Заменяем символы для корректного вычисления
                expression = self.current_input.replace('×', '*').replace('÷', '/')

                # Безопасное вычисление
                result = eval(expression)

                # Форматирование результата
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)  # Ограничиваем количество знаков после запятой

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
        """Очистка калькулятора"""
        self.current_input = ""
        self.result_var.set("0")

    def toggle_sign(self):
        """Смена знака"""
        if self.current_input and self.current_input != "0":
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.result_var.set(self.current_input)

    def percentage(self):
        """Вычисление процента"""
        try:
            if self.current_input:
                value = float(self.current_input)
                result = value / 100
                self.current_input = str(result)
                self.result_var.set(self.current_input)
        except:
            pass

    def run(self):
        """Запуск калькулятора"""
        self.window.mainloop()


# Создание и запуск калькулятора
if __name__ == "__main__":
    calc = Calculator()
    calc.run()