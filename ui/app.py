import tkinter as tk
from tkinter import filedialog, Text
import os

def list_files():
    for widget in frame.winfo_children():
        widget.destroy()
    for file in os.listdir(folder_path):
        if file.endswith('.chor'):
            label = tk.Label(frame, text=file, bg="gray")
            label.pack()

def open_file():
    filename = filedialog.askopenfilename(initialdir=folder_path, title="Select File",
                                          filetypes=(("chor files", "*.chor"), ("all files", "*.*")))
    if filename:
        with open(filename, 'r') as file:
            editor.delete(1.0, tk.END)
            editor.insert(tk.END, file.read())

def save_file():
    filename = filedialog.asksaveasfilename(defaultextension=".chor", filetypes=[("Chor files", "*.chor")])
    if filename:
        with open(filename, 'w') as file:
            file.write(editor.get(1.0, tk.END))

def execute_file():
    # Replace this comment with your logic to execute the .chor file
    print("Executing the .chor file...")  # Placeholder for execution logic

# Set the path to your folder containing .chor files
folder_path = '/Users/chukrisoueidi/Src/lena/machine/machine-lena/test'

# Create the main window
root = tk.Tk()
root.title("Chor File Manager")

# Create a frame to list files
frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.5, relx=0.1, rely=0.05)

# Add a Text widget for editing
editor = tk.Text(root, height=10)
editor.pack()

# Buttons
open_button = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#263D42", command=open_file)
open_button.pack()

save_button = tk.Button(root, text="Save File", padx=10, pady=5, fg="white", bg="#263D42", command=save_file)
save_button.pack()

execute_button = tk.Button(root, text="Execute File", padx=10, pady=5, fg="white", bg="#263D42", command=execute_file)
execute_button.pack()

# List initial files
list_files()

# Run the application
root.mainloop()
