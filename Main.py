import os
import sys
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import datetime
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



class HealthRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Recorder")
        self.folder_path = None
        self.memory_file = 'folder_memory.txt'
        self.root.geometry("500x400")

        if self.check_previous_folder():
            self.ask_user_choice()
        else:
            self.setup_ui()

    def setup_ui(self):
        # Welcome Label
        welcome_label = tk.Label(self.root, text="Welcome to Health Data Recorder", font=('Helvetica', 16))
        welcome_label.pack(pady=10)

        # Choose Folder Button
        self.choose_folder_button = tk.Button(self.root, text="Choose Folder to Save Data", command=self.choose_folder,
                                              height=4, width=20)
        self.choose_folder_button.pack(pady=10)

        # Developer Credit Label
        developer_label = tk.Label(self.root, text="Developed by Zheng Huang 2024", font=('Helvetica', 12))
        developer_label.pack(pady=10)

    def check_previous_folder(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as file:
                self.folder_path = file.read().strip()
                if os.path.exists(self.folder_path) and os.path.exists(os.path.join(self.folder_path, 'InitializeDataFile.csv')):
                    print(f"Using previously selected folder: {self.folder_path}")
                    return True
        return False

    def choose_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select a Folder")
        if self.folder_path:
            with open(self.memory_file, 'w') as file:
                file.write(self.folder_path)
            print(f"Folder selected: {self.folder_path}")
            self.generate_csv_file("InitializeDataFile")
            self.ask_user_choice()
        else:
            print("No folder was selected.")

    def generate_csv_file(self, file_name):
        csv_file_path = os.path.join(self.folder_path, file_name + '.csv')
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Data type", "Unit", "Data1", "Data2"])
            print(f"CSV file created at: {csv_file_path}")
        else:
            print(f"CSV file already exists at: {csv_file_path}")

    def ask_user_choice(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create labels
        label1 = tk.Label(self.root, text="Health data recorder Menu", font=('Helvetica', 16))
        label1.pack(pady=10)

        # Create buttons for user choice
        weight_button = tk.Button(self.root, text="Record weight", command=self.record_weight, height=4, width=20)
        blood_pressure_button = tk.Button(self.root, text="Record blood pressure", command=self.record_bloodpressure, height=4, width=20)
        graph_button = tk.Button(self.root, text="View history", command=self.generate_graphs, height=4, width=20)
        close_button = tk.Button(self.root, text="Exit", command=sys.exit, height=4, width=20)

        weight_button.pack(pady=10)
        blood_pressure_button.pack(pady=10)
        graph_button.pack(pady=10)
        close_button.pack(pady=10)

    def record_weight(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Creating a frame for grid layout
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady=10, expand=True, fill='both')

        # Entry variable and unit variable
        entry_var = tk.StringVar()
        unit_var = tk.StringVar(value='kg')  # Default unit

        def update_display(value):
            if value == 'clear':
                entry_var.set('')
            else:
                entry_var.set(entry_var.get() + value)

        def confirm():
            weight = entry_var.get()
            if weight:
                try:
                    weight = float(weight)  # Convert to float and validate
                    append_to_file(weight, unit_var.get())
                    messagebox.showinfo("Success", "Weight recorded successfully")
                    entry_var.set('')  # Clear the input after saving
                    self.ask_user_choice()  # Return to the main menu
                except ValueError:
                    messagebox.showerror("Error", "Invalid weight. Please enter a numeric value.")

        def append_to_file(weight, unit):
            csv_file_path = os.path.join(self.folder_path, 'InitializeDataFile.csv')
            with open(csv_file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'weight', unit, weight, "N/A"])

        # Entry display in the grid_frame
        entry_display = tk.Entry(grid_frame, textvariable=entry_var, font=('Helvetica', 16), justify='right')
        entry_display.grid(row=0, column=0, columnspan=3, sticky='nsew')

        # Numeric buttons in the grid_frame
        buttons = [
            ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
            ('.', 4, 0), ('0', 4, 1), ('clear', 4, 2)
        ]
        for text, row, col in buttons:
            button = tk.Button(grid_frame, text=text, command=lambda value=text: update_display(value),
                               font=('Helvetica', 16))
            button.grid(row=row, column=col, sticky='nsew')

        # Unit buttons in the grid_frame
        kg_button = tk.Radiobutton(grid_frame, text="kg", variable=unit_var, value='kg', font=('Helvetica', 16))
        lb_button = tk.Radiobutton(grid_frame, text="lb", variable=unit_var, value='lb', font=('Helvetica', 16))
        kg_button.grid(row=5, column=0, sticky='nsew')
        lb_button.grid(row=5, column=1, sticky='nsew')

        # Confirm button in the grid_frame
        confirm_button = tk.Button(grid_frame, text="Confirm", command=confirm, font=('Helvetica', 16))
        confirm_button.grid(row=5, column=2, sticky='nsew')

        # Configure rows and columns to expand in the grid_frame
        for i in range(6):
            grid_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            grid_frame.grid_columnconfigure(j, weight=1)

        # Return to main menu button in the main window
        main_menu_button = tk.Button(self.root, text="Main Menu", command=self.ask_user_choice, font=('Helvetica', 14))
        main_menu_button.pack(pady=10)

    def record_bloodpressure(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Creating a frame for grid layout
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady=10, expand=True, fill='both')

        # Entry variables for upper and lower pressure
        upper_pressure_var = tk.StringVar()
        lower_pressure_var = tk.StringVar()

        # Variable to keep track of the last clicked entry field
        last_clicked_entry = {"entry": None}

        # Function to update the entry fields
        def update_display(value):
            if last_clicked_entry["entry"]:
                current_var = upper_pressure_var if last_clicked_entry[
                                                        "entry"] == upper_pressure_entry else lower_pressure_var
                if value == 'clear':
                    current_var.set('')
                else:
                    current_var.set(current_var.get() + value)

        # Function to handle the confirmation of data entry
        def confirm():
            upper_pressure = upper_pressure_var.get()
            lower_pressure = lower_pressure_var.get()
            if upper_pressure and lower_pressure:
                try:
                    upper_pressure = float(upper_pressure)  # Convert to float and validate
                    lower_pressure = float(lower_pressure)
                    append_to_file(upper_pressure, lower_pressure)
                    messagebox.showinfo("Success", "Blood pressure recorded successfully")
                    upper_pressure_var.set('')  # Clear the input after saving
                    lower_pressure_var.set('')
                    self.ask_user_choice()  # Return to the main menu
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

        # Function to append the data to the file
        def append_to_file(upper_pressure, lower_pressure):
            csv_file_path = os.path.join(self.folder_path, 'InitializeDataFile.csv')
            with open(csv_file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'bloodpressure', 'mmHg', upper_pressure, lower_pressure])

        # Labels and Entry Fields for High and Low Pressure
        tk.Label(grid_frame, text="High Pressure (systolic, mmHg)", font=('Helvetica', 12)).grid(row=0, column=0,
                                                                                                 columnspan=3)
        upper_pressure_entry = tk.Entry(grid_frame, textvariable=upper_pressure_var, font=('Helvetica', 16),
                                        justify='right')
        upper_pressure_entry.grid(row=1, column=0, columnspan=3, sticky='nsew')
        upper_pressure_entry.bind("<Button-1>",
                                  lambda event: last_clicked_entry.update({"entry": upper_pressure_entry}))

        tk.Label(grid_frame, text="Low Pressure (diastolic, mmHg)", font=('Helvetica', 12)).grid(row=2, column=0,
                                                                                                 columnspan=3)
        lower_pressure_entry = tk.Entry(grid_frame, textvariable=lower_pressure_var, font=('Helvetica', 16),
                                        justify='right')
        lower_pressure_entry.grid(row=3, column=0, columnspan=3, sticky='nsew')
        lower_pressure_entry.bind("<Button-1>",
                                  lambda event: last_clicked_entry.update({"entry": lower_pressure_entry}))

        # Numeric buttons for upper and lower pressure
        buttons = [
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2),
            ('7', 6, 0), ('8', 6, 1), ('9', 6, 2),
            ('.', 7, 0), ('0', 7, 1), ('clear', 7, 2)
        ]
        for text, row, col in buttons:
            button = tk.Button(grid_frame, text=text,
                               command=lambda value=text: update_display(value),
                               font=('Helvetica', 16))
            button.grid(row=row, column=col, sticky='nsew')

        # Confirm button
        confirm_button = tk.Button(grid_frame, text="Confirm", command=confirm, font=('Helvetica', 16))
        confirm_button.grid(row=8, column=1, sticky='nsew')

        # Configure rows and columns to expand in the grid_frame
        for i in range(9):
            grid_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            grid_frame.grid_columnconfigure(j, weight=1)

        # Return to main menu button
        main_menu_button = tk.Button(self.root, text="Main Menu", command=self.ask_user_choice, font=('Helvetica', 14))
        main_menu_button.pack(pady=10)


    def generate_graphs(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

            # Frame to hold the weight graph button and unit selection radio buttons
        weight_frame = tk.Frame(self.root)
        weight_frame.pack(pady=10)

        # Button to show weight graph
        weight_graph_button = tk.Button(weight_frame, text="Show Weight Graph", command=self.plot_weight_graph,
                                        height=4, width=20)
        weight_graph_button.pack(side=tk.LEFT, padx=5)

        # Variable to hold the selected unit for the weight graph
        self.weight_graph_unit_var = tk.StringVar(value='kg')  # Default unit is kg

        # Radio buttons to select the unit for the weight graph
        kg_radio = tk.Radiobutton(weight_frame, text="kg", variable=self.weight_graph_unit_var, value='kg',
                                  font=('Helvetica', 12))
        lb_radio = tk.Radiobutton(weight_frame, text="lb", variable=self.weight_graph_unit_var, value='lb',
                                  font=('Helvetica', 12))
        kg_radio.pack(side=tk.LEFT, padx=5)
        lb_radio.pack(side=tk.LEFT, padx=5)

        # Button to show blood pressure graph
        bp_graph_button = tk.Button(self.root, text="Show Blood Pressure Graph", command=self.plot_bp_graph, height=4,
                                    width=20)
        bp_graph_button.pack(pady=10)

        # Return to main menu button
        main_menu_button = tk.Button(self.root, text="Main Menu", command=self.ask_user_choice, font=('Helvetica', 14))
        main_menu_button.pack(pady=10)

    def plot_weight_graph(self):
        csv_file_path = os.path.join(self.folder_path, 'InitializeDataFile.csv')
        try:
            df = pd.read_csv(csv_file_path)
            df['Date'] = pd.to_datetime(df['Date'])
            # Filter and create a copy to avoid setting value on a slice of df
            weight_data = df[df['Data type'] == 'weight'].copy()

            if not weight_data.empty:
                # Convert weights if necessary
                target_unit = self.weight_graph_unit_var.get()
                for index, row in weight_data.iterrows():
                    converted_weight = self.convert_weight(row['Data1'], row['Unit'], target_unit)
                    weight_data.loc[index, 'Data1'] = converted_weight

                plt.figure(figsize=(10, 5))
                plt.plot(weight_data['Date'], weight_data['Data1'], marker='o')
                plt.title('Weight')
                plt.xlabel('Date')
                plt.ylabel(f'Weight ({target_unit})')
                y_min, y_max = plt.ylim()
                plt.yticks(np.arange(y_min, y_max, step=round((y_max - y_min) / 10,0)))  # Adjust the step as needed
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate weight graph: {e}")

    def plot_bp_graph(self):
        csv_file_path = os.path.join(self.folder_path, 'InitializeDataFile.csv')
        try:
            df = pd.read_csv(csv_file_path)
            df['Date'] = pd.to_datetime(df['Date'])
            blood_pressure_data = df[df['Data type'] == 'bloodpressure'].set_index('Date')

            if not blood_pressure_data.empty:
                plt.figure(figsize=(10, 5))
                plt.plot(blood_pressure_data.index, blood_pressure_data['Data1'], marker='o', label='High Pressure (systolic)')
                plt.plot(blood_pressure_data.index, blood_pressure_data['Data2'], marker='o', label='Low Pressure (diastolic)')
                plt.title('Blood Pressure')
                plt.xlabel('Date')
                plt.ylabel('Pressure (mmHg)')
                plt.legend()
                y_min, y_max = plt.ylim()
                plt.yticks(np.arange(y_min, y_max, step=round((y_max - y_min) / 10,0)))  # Adjust the step as needed
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate blood pressure graph: {e}")

    def convert_weight(self, weight, from_unit, to_unit):
        if from_unit == to_unit:
            return weight
        if from_unit == 'kg' and to_unit == 'lb':
            return weight * 2.20462  # 1 kg = 2.20462 lb
        if from_unit == 'lb' and to_unit == 'kg':
            return weight / 2.20462  # 1 lb = 0.453592 kg


if __name__ == '__main__':
    root = tk.Tk()
    app = HealthRecorderApp(root)
    root.mainloop()
