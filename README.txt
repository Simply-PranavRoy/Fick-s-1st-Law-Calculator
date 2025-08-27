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

This project provides a Python-based calculator for Fick's First Law of Diffusion, including both a command-line and a graphical user interface (GUI) version. The calculator helps you solve for variables such as diffusion flux (J), diffusion coefficient (D), concentrations (C_A, C_B), positions (x_A, x_B), and thickness, with built-in error handling and logging.

## Features

- **Command-line calculator** (`Flick's 1st-Law_calculator.py`)
  - Interactive prompts for variable selection and input
  - Error handling for invalid inputs and divide-by-zero cases
  - Logs calculations with date and time in `ficks_1st_law_log.txt`
  - Supports unit conversions

- **GUI calculator** (`Flick's 1st-Law_calculator_gui.pyw`)
  - Simple, polished interface using Tkinter
  - Select which variable to solve for
  - Only relevant input fields are shown
  - Buttons for calculation and quitting
  - Error messages for missing/invalid input and divide-by-zero

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- Tkinter (included with standard Python installations)

### Running the Command-Line Calculator

1. Open a terminal and navigate to the project folder.
2. Run:
   ```
   python "Flick's Law Calculators/1st Law/Flick's 1st-Law_calculator.py"
   ```
3. Follow the prompts to select a variable and enter values.

### Running the GUI Calculator

1. Open a terminal and navigate to the project folder.
2. Run:
   ```
   python "Flick's Law Calculators/1st Law/Flick's 1st-Law_calculator_gui.pyw"
   ```
3. The GUI window will appear. Select the variable to solve for, enter the required values, and click **Calculate**.

## Logging

- All calculations in the command-line version are logged to `ficks_1st_law_log.txt` with date and time.
- You can use this log for record-keeping or analysis.


## License

This project is provided for educational and research purposes.

---


**Feel free to modify and expand the calculator for your needs!**

