# Fick's 1st Law Steady-State Diffusion Profile Calculator
# ------------------------------------------------------
# GUI tool for calculating and visualizing steady-state diffusion using Fick's First Law.
# Features: variable solving, unit conversion, and scientific explanation.

import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'  # Suppress Tkinter deprecation warning
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
from PIL import Image, ImageTk

# --- Dynamic Input Field Display ---
# Only show fields needed for the selected calculation.
def show_fields(*args):
    for widget in input_widgets.values():
        widget.grid_remove()
    target = variable.get()
    for field in required_fields[target]:
        input_widgets[field].grid()

# --- Calculation Logic ---
# Solves for the selected variable using Fick's First Law.
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
        # Calculation for each variable
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

# --- Clear Inputs for New Calculation ---
# Clear all input fields and result display for a new calculation.
def clear_inputs():
    for entry in input_entries.values():
        entry.delete(0, tk.END)
    result_var.set("")
    value_entry.delete(0, tk.END)
    converted_var.set("")

# --- Input Entries Dictionary ---
# Used for clearing all input fields at once.
input_entries = {}

# --- Supported Units for Converter ---
# Maps each variable to its supported units.
unit_options = {
    "D": ["m²/s", "cm²/s", "mm²/s", "µm²/s", "ft²/s", "in²/s", "m²/hr", "cm²/hr"],
    "J": ["mol/(m²·s)", "mol/(cm²·s)", "mol/(cm²·hr)", "kg/(m²·s)", "g/(cm²·s)", "g/(m²·s)"],
    "C": ["mol/m³", "mol/L", "mol/cm³", "mmol/L", "µmol/L", "kg/m³", "g/L", "g/cm³", "mg/mL", "mg/L", "µg/mL"],
    "x": ["m", "cm", "mm", "µm", "nm", "ft", "in"]
}

# --- GUI Setup ---
# Main window and mainframe for layout.
root = tk.Tk()
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)
root.title("Fick's 1st Law Steady-State Diffusion Profile")
root.resizable(True, True)
root.geometry("900x700")
mainframe = ttk.Frame(root, padding="24 24 24 24")
mainframe.grid(row=0, column=0, sticky='nw')

# --- Input Section Frame ---
# Groups all input widgets at the top-left.
input_frame = ttk.Frame(mainframe, padding="12 12 12 12")
input_frame.grid(row=0, column=0, sticky='nw')

# --- Variable Selection Dropdown ---
row = 0
ttk.Label(input_frame, text="Solve for:").grid(row=row, column=0, sticky=tk.W)
variable = tk.StringVar()
solve_options = ['J', 'D', 'C_A', 'C_B', 'x_A', 'x_B', 'thickness']
solve_menu = ttk.Combobox(input_frame, textvariable=variable, values=solve_options, state='readonly', width=12)
solve_menu.grid(row=row, column=1, sticky=tk.W)
solve_menu.current(0)
solve_menu.bind("<<ComboboxSelected>>", show_fields)

# --- Input Fields for Variables ---
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
    ttk.Label(input_frame, text=label).grid(row=row, column=0, sticky=tk.W)
    entry = ttk.Entry(input_frame, width=15)
    entry.grid(row=row, column=1, sticky=tk.W)
    entries[key] = entry
    input_widgets[key] = entry
    input_entries[key] = entry
    row += 1

# --- Required Fields for Each Calculation ---
# Dictionary mapping each variable to the required input fields
required_fields = {
    'J':     ['D', 'C_A', 'C_B', 'x_A', 'x_B'],
    'D':     ['J', 'C_A', 'C_B', 'x_A', 'x_B'],
    'C_A':   ['J', 'D', 'C_B', 'x_A', 'x_B'],
    'C_B':   ['J', 'D', 'C_A', 'x_A', 'x_B'],
    'x_A':   ['J', 'D', 'C_A', 'C_B', 'x_B'],
    'x_B':   ['J', 'D', 'C_A', 'C_B', 'x_A'],
    'thickness': ['J', 'D', 'C_A', 'C_B']
}

# --- Result Display ---
# Label to show calculation results below input fields
result_var = tk.StringVar()
result_label = ttk.Label(input_frame, textvariable=result_var, foreground="blue", font=("Segoe UI", 11, "bold"))
result_label.grid(row=row, column=0, pady=(10,0), sticky='w')

# --- Action Buttons ---
# Calculate, Calculate Another, and Quit buttons below result label
calc_btn = ttk.Button(input_frame, text="Calculate", command=calculate)
calc_btn.grid(row=row+1, column=0, pady=10, sticky='w')
calc_another_btn = ttk.Button(input_frame, text="Calculate Another", command=clear_inputs)
calc_another_btn.grid(row=row+1, column=1, pady=10, sticky='w')
quit_btn = ttk.Button(input_frame, text="Quit", command=root.quit)
quit_btn.grid(row=row+1, column=2, pady=10, sticky='w')

# --- Unit Converter Section ---
# Frame for unit conversion tools, placed below result and buttons
unit_frame = tk.LabelFrame(input_frame, text="Unit Converter", padx=10, pady=10)
unit_frame.grid(row=row+2, column=0, columnspan=2, pady=(10,0), sticky='w')

# --- Unit Converter Widgets ---
# Value entry for conversion
tk.Label(unit_frame, text="Value:").grid(row=0, column=0)
value_entry = tk.Entry(unit_frame)
value_entry.grid(row=0, column=1)

# Variable selection for conversion
tk.Label(unit_frame, text="Variable:").grid(row=1, column=0)
variable_combo = ttk.Combobox(unit_frame, values=list(unit_options.keys()))
variable_combo.grid(row=1, column=1)

# From/To unit dropdowns
from_unit_combo = ttk.Combobox(unit_frame)
from_unit_combo.grid(row=2, column=1)
to_unit_combo = ttk.Combobox(unit_frame)
to_unit_combo.grid(row=3, column=1)

def update_unit_dropdowns(event=None):
    # Update unit dropdowns based on selected variable
    var = variable_combo.get()
    units = unit_options.get(var, [])
    from_unit_combo['values'] = units
    to_unit_combo['values'] = units
    if units:
        from_unit_combo.current(0)
        to_unit_combo.current(1 if len(units) > 1 else 0)
variable_combo.bind('<<ComboboxSelected>>', update_unit_dropdowns)

# --- Conversion Factors for Units ---
# Dictionaries for converting between supported units
length_factors = {
    'm': 1.0,
    'cm': 0.01,
    'mm': 0.001,
    'µm': 1e-6,
    'nm': 1e-9,
    'ft': 0.3048,
    'in': 0.0254
}
area_factors = {
    'm²/s': 1.0,
    'cm²/s': 0.0001,
    'mm²/s': 1e-6,
    'µm²/s': 1e-12,
    'ft²/s': 0.092903,
    'in²/s': 0.00064516,
    'm²/hr': 1.0/3600,
    'cm²/hr': 0.0001/3600
}
conc_factors = {
    'mol/m³': 1.0,
    'mol/L': 1000.0,
    'mol/cm³': 1e6,
    'mmol/L': 1.0,
    'µmol/L': 1e-3,
    'kg/m³': 1.0,
    'g/L': 1.0,
    'g/cm³': 1000.0,
    'mg/mL': 1000.0,
    'mg/L': 1e-3,
    'µg/mL': 1e-6
}
flux_factors = {
    'mol/(m²·s)': 1.0,
    'mol/(cm²·s)': 0.0001,
    'mol/(cm²·hr)': 0.0001/3600,
    'kg/(m²·s)': 1.0,
    'g/(cm²·s)': 0.0001,
    'g/(m²·s)': 0.001
}

# --- Unit Conversion Logic ---
# Convert between units for D, J, C, x using the selected variable and units.
def convert_units():
    value = value_entry.get()
    var = variable_combo.get()
    from_unit = from_unit_combo.get()
    to_unit = to_unit_combo.get()
    try:
        val = float(value)
    except Exception:
        result_label.config(text="Enter a valid numeric value.", fg="red")
        return
    # Conversion logic for each variable
    if var == 'x':
        if from_unit not in length_factors or to_unit not in length_factors:
            result_label.config(text="Invalid units for length.", fg="red")
            return
        val_m = val * length_factors[from_unit]
        converted = val_m / length_factors[to_unit]
    elif var == 'C':
        if from_unit not in conc_factors or to_unit not in conc_factors:
            result_label.config(text="Invalid units for concentration.", fg="red")
            return
        val_base = val * conc_factors[from_unit]
        converted = val_base / conc_factors[to_unit]
    elif var == 'D':
        if from_unit not in area_factors or to_unit not in area_factors:
            result_label.config(text="Invalid units for D.", fg="red")
            return
        val_base = val * area_factors[from_unit]
        converted = val_base / area_factors[to_unit]
    elif var == 'J':
        if from_unit not in flux_factors or to_unit not in flux_factors:
            result_label.config(text="Invalid units for J.", fg="red")
            return
        val_base = val * flux_factors[from_unit]
        converted = val_base / flux_factors[to_unit]
    else:
        result_label.config(text="Select a valid variable.", fg="red")
        return
    result_label.config(text=f"{val} {from_unit} = {converted:.6g} {to_unit}", fg="blue")

convert_btn = tk.Button(unit_frame, text="Convert", command=convert_units)
convert_btn.grid(row=4, column=0, columnspan=2)
result_label = tk.Label(unit_frame, text="")
result_label.grid(row=5, column=0, columnspan=2)
converted_var = tk.StringVar()

# --- Fick's Law Info Section ---
# Add a LabelFrame to the right of the input section for Fick's Law info
info_frame = tk.LabelFrame(mainframe, text="About Fick's 1st Law", padx=12, pady=12)
info_frame.grid(row=0, column=1, rowspan=10, sticky='nw', padx=(40,0))

info_text = (
    "Fick's 1st Law of Diffusion:\n"
    "\n"
    "Describes the flux of a diffusing species under steady-state conditions.\n"
    "\n"
    "Equation:\n"
    "    J = -D · (dC/dx)\n"
    "\n"
    "Where:\n"
    "  J = Diffusive flux (amount per area per time)\n"
    "  D = Diffusion coefficient (m²/s)\n"
    "  C = Concentration of species (kg/m³, mol/m³, etc.)\n"
    "  x = Position (m)\n"
    "  dC/dx = Concentration gradient\n"
    "  - sign: Flux goes from high to low concentration\n"
)

info_label = tk.Label(info_frame, text=info_text, justify='left', font=("Segoe UI", 10), anchor='nw')
info_label.pack(fill='both', expand=True)

# --- Initialize GUI ---
# Show relevant input fields for the default selected variable
show_fields()

# --- Start the Tkinter event loop ---
root.mainloop()

# To run without the black terminal window, save this file as .pyw and run it.
