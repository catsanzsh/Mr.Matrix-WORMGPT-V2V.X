import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess

def run_nmap():
    """
    Executes the Nmap scan based on user input and displays the output.
    """
    target = target_entry.get()
    if not target:
        messagebox.showwarning("Input Error", "Please enter a target IP or hostname.")
        return

    scan_type = scan_type_var.get()
    nmap_command = ["nmap", target]

    # Configure Nmap command based on selected scan type
    if scan_type == "Quick Scan":
        nmap_command.append("-T4")
    elif scan_type == "Intense Scan":
        nmap_command.extend(["-T4", "-A", "-v"])
    elif scan_type == "Ping Scan":
        nmap_command.append("-sn")
    elif scan_type == "Regular Scan":
        pass  # Default Nmap scan
    else:
        pass  # Additional scan types can be added here

    try:
        # Execute Nmap command and capture the output
        output = subprocess.check_output(
            nmap_command, stderr=subprocess.STDOUT, universal_newlines=True
        )
        # Display the output in the text area
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output)
    except subprocess.CalledProcessError as e:
        # Handle errors in Nmap execution
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, e.output)
    except FileNotFoundError:
        # Nmap is not installed or not found in system PATH
        messagebox.showerror("Error", "Nmap is not installed or not found in PATH.")

# Initialize the main application window
root = tk.Tk()
root.title("Nmap GUI Client")

# Target input field
tk.Label(root, text="Target IP/Hostname:").grid(
    row=0, column=0, padx=5, pady=5, sticky=tk.W
)
target_entry = tk.Entry(root, width=30)
target_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

# Scan type selection
tk.Label(root, text="Scan Type:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
scan_type_var = tk.StringVar()
scan_type_var.set("Regular Scan")  # Default scan type
scan_options = ["Regular Scan", "Quick Scan", "Intense Scan", "Ping Scan"]
scan_type_menu = tk.OptionMenu(root, scan_type_var, *scan_options)
scan_type_menu.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

# Run Scan button
run_button = tk.Button(root, text="Run Scan", command=run_nmap)
run_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Output text area with scrollbar
output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()
