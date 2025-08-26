
import os
import logging
from datetime import datetime

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, 'ficks_1st_law_log.txt')

# Setup logging to write in the same folder as the script
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(message)s')

def log_block(header, data_dict):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info("\n" + "="*50)
    logging.info(f"{now} | {header}")
    logging.info("-"*50)
    for key, value in data_dict.items():
        logging.info(f"{key:<30}: {value}")
    logging.info("="*50 + "\n")

def convert_units(value, from_unit, to_unit):
    conversions = {
        ('cm', 'm'): value / 100,
        ('mm', 'm'): value / 1000,
        ('nm', 'm'): value / 1e9,
        ('mol/cm^3', 'mol/m^3'): value * 1e6,
        ('mol/mm^3', 'mol/m^3'): value * 1e9,
    }
    converted = conversions.get((from_unit, to_unit), value)
    if converted != value:
        log_block("Unit Conversion", {
            "Original Value": f"{value} {from_unit}",
            "Converted Value": f"{converted} {to_unit}"
        })
    return converted

def safe_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def ficks_first_law():
    while True:
        print("Fick's First Law: J = -D * (dC/dx)")
        print("Which variable do you want to solve for? (J, D, C_A, C_B, x_A, x_B, thickness)")
        target = input("Enter variable: ").strip()

        try:
            if target == 'J':
                D = safe_float("Enter diffusion coefficient D (in m^2/s): ")
                C_A = safe_float("Enter concentration at location A (kg/m^3): ")
                C_B = safe_float("Enter concentration at location B (kg/m^3): ")
                x_A = safe_float("Enter position A (m): ")
                x_B = safe_float("Enter position B (m): ")
                if x_A == x_B:
                    print("Error: x_A and x_B cannot be equal (division by zero).")
                else:
                    dC_dx = (C_A - C_B) / (x_A - x_B)
                    J = -D * dC_dx
                    print(f"Diffusion flux J = {J:.4e} kg/m^2·s")
                    log_block("Calculated Diffusion Flux (J)", {
                        "D (m^2/s)": f"{D:.4e}",
                        "C_A (kg/m^3)": f"{C_A:.4e}",
                        "C_B (kg/m^3)": f"{C_B:.4e}",
                        "x_A (m)": f"{x_A:.4e}",
                        "x_B (m)": f"{x_B:.4e}",
                        "dC/dx (kg/m^4)": f"{dC_dx:.4e}",
                        "J (kg/m^2·s)": f"{J:.4e}"
                    })

            elif target == 'D':
                J = safe_float("Enter diffusion flux J (in kg/m^2·s): ")
                C_A = safe_float("Enter concentration at location A (kg/m^3): ")
                C_B = safe_float("Enter concentration at location B (kg/m^3): ")
                x_A = safe_float("Enter position A (m): ")
                x_B = safe_float("Enter position B (m): ")
                if x_A == x_B:
                    print("Error: x_A and x_B cannot be equal (division by zero).")
                else:
                    dC_dx = (C_A - C_B) / (x_A - x_B)
                    if dC_dx == 0:
                        print("Error: dC/dx is zero (division by zero).")
                    else:
                        D = -J / dC_dx
                        print(f"Diffusion coefficient D = {D:.4e} m^2/s")
                        log_block("Calculated Diffusion Coefficient (D)", {
                            "J (kg/m^2·s)": f"{J:.4e}",
                            "C_A (kg/m^3)": f"{C_A:.4e}",
                            "C_B (kg/m^3)": f"{C_B:.4e}",
                            "x_A (m)": f"{x_A:.4e}",
                            "x_B (m)": f"{x_B:.4e}",
                            "dC/dx (kg/m^4)": f"{dC_dx:.4e}",
                            "D (m^2/s)": f"{D:.4e}"
                        })

            elif target == 'C_A':
                J = safe_float("Enter diffusion flux J (in kg/m^2·s): ")
                D = safe_float("Enter diffusion coefficient D (in m^2/s): ")
                C_B = safe_float("Enter concentration at location B (kg/m^3): ")
                x_A = safe_float("Enter position A (m): ")
                x_B = safe_float("Enter position B (m): ")
                if D == 0:
                    print("Error: D cannot be zero (division by zero).")
                else:
                    C_A = ((J/(-D))*(x_A-x_B))+C_B
                    print(f"Concentration at location A = {C_A:.4e} kg/m^3")
                    log_block("Calculated Concentration at A (C_A)", {
                        "J (kg/m^2·s)": f"{J:.4e}",
                        "D (m^2/s)": f"{D:.4e}",
                        "C_B (kg/m^3)": f"{C_B:.4e}",
                        "x_A (m)": f"{x_A:.4e}",
                        "x_B (m)": f"{x_B:.4e}",
                        "C_A (kg/m^3)": f"{C_A:.4e}"
                    })

            elif target == 'C_B':
                J = safe_float("Enter diffusion flux J (in kg/m^2·s): ")
                D = safe_float("Enter diffusion coefficient D (in m^2/s): ")
                C_A = safe_float("Enter concentration at location A (kg/m^3): ")
                x_A = safe_float("Enter position A (m): ")
                x_B = safe_float("Enter position B (m): ")
                if D == 0:
                    print("Error: D cannot be zero (division by zero).")
                else:
                    C_B = -(((J/(-D))*(x_A-x_B))-C_A)
                    print(f"Concentration at location B = {C_B:.4e} kg/m^3")
                    log_block("Calculated Concentration at B (C_B)", {
                        "J (kg/m^2·s)": f"{J:.4e}",
                        "D (m^2/s)": f"{D:.4e}",
                        "C_A (kg/m^3)": f"{C_A:.4e}",
                        "x_A (m)": f"{x_A:.4e}",
                        "x_B (m)": f"{x_B:.4e}",
                        "C_B (kg/m^3)": f"{C_B:.4e}"
                    })

            elif target == 'x_A':
                J = safe_float("Enter diffusion flux J (in kg/m^2·s): ")
                D = safe_float("Enter diffusion coefficient D (in m^2/s): ")
                C_A = safe_float("Enter concentration at location A (kg/m^3): ")
                C_B = safe_float("Enter concentration at location B (kg/m^3): ")
                x_B = safe_float("Enter position B (m): ")
                if J == 0:
                    print("Error: J cannot be zero (division by zero).")
                else:
                    x_A = (((-D)/J)*(C_A-C_B))+x_B
                    print(f"Location of point A = {x_A:.4e} m")
                    log_block("Calculated Position A (x_A)", {
                        "J (kg/m^2·s)": f"{J:.4e}",
                        "D (m^2/s)": f"{D:.4e}",
                        "C_A (kg/m^3)": f"{C_A:.4e}",
                        "C_B (kg/m^3)": f"{C_B:.4e}",
                        "x_B (m)": f"{x_B:.4e}",
                        "x_A (m)": f"{x_A:.4e}"
                    })

            elif target == 'x_B':
                J = safe_float("Enter diffusion flux J (in kg/m^2·s): ")
                D = safe_float("Enter diffusion coefficient D (in m^2/s): ")
                C_A = safe_float("Enter concentration at location A (kg/m^3): ")
                C_B = safe_float("Enter concentration at location B (kg/m^3): ")
                x_A = safe_float("Enter position A (m): ")
                if J == 0:
                    print("Error: J cannot be zero (division by zero).")
                else:
                    x_B = -((((-D)/J)*(C_A-C_B))-x_A)
                    print(f"Location of point B = {x_B:.4e} m")
                    log_block("Calculated Position B (x_B)", {
                        "J (kg/m^2·s)": f"{J:.4e}",
                        "D (m^2/s)": f"{D:.4e}",
                        "C_A (kg/m^3)": f"{C_A:.4e}",
                        "C_B (kg/m^3)": f"{C_B:.4e}",
                        "x_A (m)": f"{x_A:.4e}",
                        "x_B (m)": f"{x_B:.4e}"
                    })

            elif target == 'thickness':
                J = safe_float("Enter diffusion flux J (in kg/m^2·s): ")
                D = safe_float("Enter diffusion coefficient D (in m^2/s): ")
                C_A = safe_float("Enter concentration at location A (kg/m^3): ")
                C_B = safe_float("Enter concentration at location B (kg/m^3): ")
                if J == 0:
                    print("Error: J cannot be zero (division by zero).")
                else:
                    thickness = abs(((-D)/J)*(C_A-C_B))
                    print(f"Thickness = {thickness:.4e} m")
                    log_block("Calculated Thickness", {
                        "J (kg/m^2·s)": f"{J:.4e}",
                        "D (m^2/s)": f"{D:.4e}",
                        "C_A (kg/m^3)": f"{C_A:.4e}",
                        "C_B (kg/m^3)": f"{C_B:.4e}",
                        "Thickness (m)": f"{thickness:.4e}"
                    })

            else:
                print("Invalid selection. Please choose J, D, C_A, C_B, x_A, x_B or thickness.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        again = input("\nWould you like to use the calculator again? (y/n): ").strip().lower()
        if again != 'y':
            print("Thank you for using the calculator!")
            break

if __name__ == "__main__":
    ficks_first_law()
