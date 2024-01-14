import tkinter as tk
from tkinter import ttk
from collections import deque
import math
class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор")
        self.geometry("600x300")

        self.expression = ""
        self.history_of_results = deque(maxlen=10)
        self.create_widgets()

    def create_widgets(self):
        button_frame = ttk.Frame(self)
        button_frame.pack(expand=True, fill="both")

        history_of_results_button = ttk.Button(button_frame, text='История результатов', command=self.show_history_of_results)
        history_of_results_button.grid(row=0, column=3, sticky="ne")

        for i in range(0, 10):
            button = ttk.Button(button_frame, text=str(i), command=lambda num=i: self.update_expression(num))
            button.grid(row=(9-i)//3+1, column=(i-1)%3, sticky="nsew", padx=5, pady=5)

        operations = ["*", "/", "+", "-", "!", "⌫"]
        for index, op in enumerate(operations):
            if op == "!":
                operation_button = ttk.Button(button_frame, text=op, command=lambda char=op: self.calculate_factorial())
            elif op == "⌫":
                operation_button = ttk.Button(button_frame, text=op, command=self.delete_last_symbol)
            else:
                operation_button = ttk.Button(button_frame, text=op, command=lambda char=op: self.update_expression(char))
            operation_button.grid(row=index+1, column=3, sticky="nsew", padx=5, pady=5)

        exit_button = ttk.Button(button_frame, text="Выход", command=self.quit)
        exit_button.grid(row=6, column=4, sticky="ne", padx=5, pady=5)
        degree_button = ttk.Button(button_frame, text="^", command=lambda char="**": self.update_expression(char))
        degree_button.grid(row=5, column=3, sticky="nsew", padx=5, pady=5)
        calculate_button = ttk.Button(button_frame, text="=", command=self.calculate)
        calculate_button.grid(row=4, column=4, sticky="nsew", padx=5, pady=5)

        self.result_label = ttk.Label(button_frame, text="Результат:")
        self.result_label.grid(row=5, column=4, sticky="nsew", padx=5, pady=5)

        self.number_tabel = ttk.Label(button_frame, text="")
        self.number_tabel.grid(row=3, column=4, sticky="ne", padx=5, pady=5)

    def calculate(self):
        try:
            result = eval(self.expression)
            if isinstance(result, float):
                result_str = f"{result:.5f}"
            else:
                result_str = str(result)
            self.result_label.config(text=f"Результат: {result_str}")
            self.history_of_results.append(result)
        except Exception as e:
            self.result_label.config(text="Неверный ввод")
        self.expression = ""
        with open("history.txt", "w") as file:
            history_list = list(self.history_of_results)
            file.write("\n".join(str(result) for result in history_list))


    def calculate_factorial(self):
        try:
            result = math.factorial(int(self.expression))
            result_str = str(result)
            self.result_label.config(text=f"Факториал: {result_str}")
            self.history_of_results.append(result)
        except Exception as e:
            self.result_label.config(text="Неверный ввод")
        self.expression = ""
        with open("history.txt", "w") as file:
            history_list = list(self.history_of_results)
            file.write("\n".join(str(result) for result in history_list))

    def update_expression(self, char):
        if char == "⌫":
            self.expression = self.expression[:-1]
        else:
            self.expression += str(char)
        self.number_tabel.config(text=self.expression)

    def delete_last_symbol(self):
        self.expression = self.expression[:-1]
        self.number_tabel.config(text=self.expression)


    def show_history_of_results(self):
        history_content = "\n".join(str(result) for result in self.history_of_results)
        history_of_results_tabel = ttk.Label(self, text=history_content)
        history_of_results_tabel.pack(anchor="ne")

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
