import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import tkinter as tk
from tkinter import ttk, messagebox

def show_fields(*args):
    # Hide all fields first
    for widget in input_widgets.values():
        widget.grid_remove()
    # Show only relevant fields
    target = variable.get()
    for field in required_fields[target]:
        input_widgets[field].grid()

def calculate():
    try:
        target = variable.get()
        vals = {}
        for field in required_fields[target]:
            val = entries[field].get()
            if val == "":
                messagebox.showerror("Input Error", f"Please enter {field}.")
                return
            vals[field] = float(val)
        # Calculations
        if target == 'J':
            D, C_A, C_B, x_A, x_B = vals['D'], vals['C_A'], vals['C_B'], vals['x_A'], vals['x_B']
            if x_A == x_B:
                messagebox.showerror("Math Error", "x_A and x_B cannot be equal (division by zero).")
                return
            dC_dx = (C_A - C_B) / (x_A - x_B)
            J = -D * dC_dx
            result_var.set(f"J = {J:.4e} kg/m²·s")
        elif target == 'D':
            J, C_A, C_B, x_A, x_B = vals['J'], vals['C_A'], vals['C_B'], vals['x_A'], vals['x_B']
            if x_A == x_B:
                messagebox.showerror("Math Error", "x_A and x_B cannot be equal (division by zero).")
                return
            dC_dx = (C_A - C_B) / (x_A - x_B)
            if dC_dx == 0:
                messagebox.showerror("Math Error", "dC/dx is zero (division by zero).")
                return
            D = -J / dC_dx
            result_var.set(f"D = {D:.4e} m²/s")
        elif target == 'C_A':
            J, D, C_B, x_A, x_B = vals['J'], vals['D'], vals['C_B'], vals['x_A'], vals['x_B']
            if D == 0:
                messagebox.showerror("Math Error", "D cannot be zero (division by zero).")
                return
            C_A = ((J/(-D))*(x_A-x_B))+C_B
            result_var.set(f"C_A = {C_A:.4e} kg/m³")
        elif target == 'C_B':
            J, D, C_A, x_A, x_B = vals['J'], vals['D'], vals['C_A'], vals['x_A'], vals['x_B']
            if D == 0:
                messagebox.showerror("Math Error", "D cannot be zero (division by zero).")
                return
            C_B = -(((J/(-D))*(x_A-x_B))-C_A)
            result_var.set(f"C_B = {C_B:.4e} kg/m³")
        elif target == 'x_A':
            J, D, C_A, C_B, x_B = vals['J'], vals['D'], vals['C_A'], vals['C_B'], vals['x_B']
            if J == 0:
                messagebox.showerror("Math Error", "J cannot be zero (division by zero).")
                return
            x_A = (((-D)/J)*(C_A-C_B))+x_B
            result_var.set(f"x_A = {x_A:.4e} m")
        elif target == 'x_B':
            J, D, C_A, C_B, x_A = vals['J'], vals['D'], vals['C_A'], vals['C_B'], vals['x_A']
            if J == 0:
                messagebox.showerror("Math Error", "J cannot be zero (division by zero).")
                return
            x_B = -((((-D)/J)*(C_A-C_B))-x_A)
            result_var.set(f"x_B = {x_B:.4e} m")
        elif target == 'thickness':
            J, D, C_A, C_B = vals['J'], vals['D'], vals['C_A'], vals['C_B']
            if J == 0:
                messagebox.showerror("Math Error", "J cannot be zero (division by zero).")
                return
            thickness = abs(((-D)/J)*(C_A-C_B))
            result_var.set(f"Thickness = {thickness:.4e} m")
        else:
            messagebox.showinfo("Info", "Select a variable to solve for.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

root = tk.Tk()
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)
root.title("Fick's First Law Calculator")
root.resizable(False, False)
root.geometry("350x420")  # Increased window size for better visibility 

mainframe = ttk.Frame(root, padding="16")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Variable selection
ttk.Label(mainframe, text="Solve for:").grid(row=0, column=0, sticky=tk.W)
variable = tk.StringVar()
solve_options = ['J', 'D', 'C_A', 'C_B', 'x_A', 'x_B', 'thickness']
solve_menu = ttk.Combobox(mainframe, textvariable=variable, values=solve_options, state='readonly', width=12)
solve_menu.grid(row=0, column=1, sticky=tk.W)
solve_menu.current(0)
solve_menu.bind("<<ComboboxSelected>>", show_fields)

# Input fields
fields = {
    'D': "D (m²/s):",
    'J': "J (kg/m²·s):",
    'C_A': "C_A (kg/m³):",
    'C_B': "C_B (kg/m³):",
    'x_A': "x_A (m):",
    'x_B': "x_B (m):"
}
entries = {}
input_widgets = {}
row = 1
for key, label in fields.items():
    ttk.Label(mainframe, text=label).grid(row=row, column=0, sticky=tk.W)
    entry = ttk.Entry(mainframe, width=15)
    entry.grid(row=row, column=1, sticky=tk.W)
    entries[key] = entry
    input_widgets[key] = entry
    row += 1

# Which fields are required for each calculation
required_fields = {
    'J':     ['D', 'C_A', 'C_B', 'x_A', 'x_B'],
    'D':     ['J', 'C_A', 'C_B', 'x_A', 'x_B'],
    'C_A':   ['J', 'D', 'C_B', 'x_A', 'x_B'],
    'C_B':   ['J', 'D', 'C_A', 'x_A', 'x_B'],
    'x_A':   ['J', 'D', 'C_A', 'C_B', 'x_B'],
    'x_B':   ['J', 'D', 'C_A', 'C_B', 'x_A'],
    'thickness': ['J', 'D', 'C_A', 'C_B']
}

# Result display
result_var = tk.StringVar()
ttk.Label(mainframe, textvariable=result_var, foreground="blue", font=("Segoe UI", 11, "bold")).grid(row=row, column=0, columnspan=2, pady=(10,0))

# Buttons
ttk.Button(mainframe, text="Calculate", command=calculate).grid(row=row+1, column=0, pady=10)
ttk.Button(mainframe, text="Quit", command=root.quit).grid(row=row+1, column=1, pady=10)

# Show initial fields
show_fields()

root.mainloop()

# To run without the black terminal window, save this file as .pyw (e.g., Fick_s 1st-Law_calculator_GUI.pyw) and run it.