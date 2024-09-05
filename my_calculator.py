import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Calculator with Graph")
        master.geometry("1000x600")

        # Create frames
        self.display_frame = tk.Frame(master)
        self.buttons_frame = tk.Frame(master)
        self.graph_frame = tk.Frame(master)

        self.display_frame.grid(row=0, column=0, sticky="nsew")
        self.buttons_frame.grid(row=1, column=0, sticky="nsew")
        self.graph_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Configure grid
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=2)
        master.grid_rowconfigure(1, weight=1)

        # Display
        self.display_var = tk.StringVar()
        self.display = tk.Entry(self.display_frame, textvariable=self.display_var, font=('Arial', 20), justify='right')
        self.display.pack(fill=tk.BOTH, expand=True)

        # Buttons
        buttons = [
            'x', 'y', '(', ')', 'C', '⌫',
            'sin', 'cos', 'tan', '7', '8', '9', '/',
            'asin', 'acos', 'atan', '4', '5', '6', '*',
            'log', 'ln', 'e', '1', '2', '3', '-',
            'x²', '√', 'π', '0', '.', '=', '+'
        ]

        row, col = 0, 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            tk.Button(self.buttons_frame, text=button, command=cmd, width=5, height=2).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            col += 1
            if col > 6:
                col = 0
                row += 1

        # Configure button grid
        for i in range(7):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)

        # Graph
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def click(self, key):
        if key == '=':
            try:
                expression = self.display_var.get()
                if 'x' in expression or 'y' in expression:
                    self.plot_function(expression)
                else:
                    result = self.evaluate(expression)
                    self.display_var.set(result)
            except Exception as e:
                self.display_var.set(f"Error: {str(e)}")
        elif key == 'C':
            self.display_var.set("")
        elif key == '⌫':
            current = self.display_var.get()
            self.display_var.set(current[:-1])
        elif key in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'ln']:
            self.display_var.set(self.display_var.get() + key + "(")
        elif key == 'x²':
            self.display_var.set(self.display_var.get() + "**2")
        elif key == '√':
            self.display_var.set(self.display_var.get() + "sqrt(")
        elif key == 'π':
            self.display_var.set(self.display_var.get() + "pi")
        elif key == 'e':
            self.display_var.set(self.display_var.get() + "e")
        else:
            self.display_var.set(self.display_var.get() + key)

    def evaluate(self, expression):
        # Define safe versions of math functions
        safe_dict = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'log': math.log, 'ln': math.log, 'sqrt': math.sqrt,
            'pi': math.pi, 'e': math.e,
            'abs': abs, 'pow': pow
        }
        return eval(expression, {"__builtins__": None}, safe_dict)
    
    def plot_function(self, func_str):
        self.ax.clear()
        x = np.linspace(-10, 10, 1000)
        try:
            safe_dict = {
                'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                'asin': np.arcsin, 'acos': np.arccos, 'atan': np.arctan,
                'log': np.log, 'ln': np.log, 'sqrt': np.sqrt,
                'pi': np.pi, 'e': np.e,
                'abs': np.abs, 'pow': np.power
            }
            if 'y' in func_str:
                y = np.linspace(-10, 10, 1000)
                X, Y = np.meshgrid(x, y)
                Z = eval(func_str, {"__builtins__": None, "x": X, "y": Y, "np": np}, safe_dict)
                self.ax.contour(X, Y, Z, [0])
                self.ax.set_title(f"{func_str} = 0")
            else:
                y = eval(func_str, {"__builtins__": None, "x": x, "np": np}, safe_dict)
                self.ax.plot(x, y)
                self.ax.set_title(f"y = {func_str}")
            
            self.ax.axhline(y=0, color='k')
            self.ax.axvline(x=0, color='k')
            self.ax.grid(True)
            self.ax.set_xlim(-10, 10)
            self.ax.set_ylim(-10, 10)
            self.canvas.draw()
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Invalid function: {str(e)}", ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()