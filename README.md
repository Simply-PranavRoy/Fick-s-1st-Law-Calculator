# Fick's First Law Calculator

**Author:** Pranav Roy  
**Created:** August 2025

© 2025 Pranav Roy. All rights reserved.

This project and its code are original works by Pranav Roy.  
If you use or share this code, please credit the author.

---

## Contact

- **Email:** pranavroy282@gmail.com
- **LinkedIn:** www.linkedin.com/in/pranav-roy-64314b184

---

## Overview

This project provides two Python-based calculators for Fick's First Law of Diffusion:
- A command-line calculator (`Fick_s 1st-Law_calculator.py`)
- A graphical user interface (GUI) calculator (`Fick_s 1st-Law_calculator_GUI.pyw`)

Both tools help you solve for:
- Diffusion flux (J)
- Diffusion coefficient (D)
- Concentrations (C_A, C_B)
- Positions (x_A, x_B)
- Thickness

with built-in error handling, logging, and unit conversion.

---

## Scientific Background

**Fick's 1st Law of Diffusion:**
Describes the flux of a diffusing species under steady-state conditions.

**Equation:**
    J = -D · (dC/dx)

**Where:**
- J = Diffusive flux (amount per area per time)
- D = Diffusion coefficient (m²/s)
- C = Concentration of species (kg/m³, mol/m³, etc.)
- x = Position (m)
- dC/dx = Concentration gradient
- The negative sign indicates flux is from high to low concentration

---

## Features

### Command-line calculator (`Fick_s 1st-Law_calculator.py`)
- Interactive prompts for variable selection and input
- Error handling for invalid inputs and divide-by-zero cases
- Logs calculations with date and time in `ficks_1st_law_log.txt`
- Supports basic unit conversions (cm, mm, nm, mol/cm³, mol/mm³)

### GUI calculator (`Fick_s 1st-Law_calculator_GUI.pyw`)
- Intuitive interface using Tkinter
- Select which variable to solve for
- Only relevant input fields are shown
- Buttons for calculation, clearing, and quitting
- Extensive unit converter for D, J, C, x (supports m²/s, cm²/s, mm²/s, µm²/s, ft²/s, in²/s, m²/hr, cm²/hr, mol/(m²·s), mol/(cm²·s), mol/(cm²·hr), kg/(m²·s), g/(cm²·s), g/(m²·s), mol/m³, mol/L, mol/cm³, mmol/L, µmol/L, kg/m³, g/L, g/cm³, mg/mL, mg/L, µg/mL, m, cm, mm, µm, nm, ft, in)
- Error messages for missing/invalid input and divide-by-zero
- Scientific explanation panel for Fick's Law and variables

---

## Getting Started

### Prerequisites
- Python 3.x installed on your system
- Tkinter (included with standard Python installations)

### Running the Command-Line Calculator
1. Open a terminal and navigate to the project folder.
2. Run:
   ```
   python "Flick_s Law Calculators/1st Law/Fick_s 1st-Law_calculator.py"
   ```
3. Follow the prompts to select a variable and enter values.

### Running the GUI Calculator
1. Open a terminal and navigate to the project folder.
2. Run:
   ```
   python "Flick_s Law Calculators/1st Law/Fick_s 1st-Law_calculator_GUI.pyw"
   ```
3. The GUI window will appear. Select the variable to solve for, enter the required values, and click **Calculate**. Use the unit converter as needed.

---

## Logging
- All calculations in the command-line version are logged to `ficks_1st_law_log.txt` with date and time.
- You can use this log for record-keeping or analysis.

---

## License
This project is provided for educational and research purposes.

---

**Feel free to modify and expand the calculator for your needs!**
