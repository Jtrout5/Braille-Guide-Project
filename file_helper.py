# file_picker_helper.py
import tkinter as tk
from tkinter import filedialog
import json

root = tk.Tk()
root.withdraw()

path = filedialog.askopenfilename(
    title="Select a file",
    filetypes=[
        ("All files", "*.*"),
        ("Text files", "*.txt"),
        ("PDF files", "*.pdf"),
        ("Word documents", "*.docx *.doc")
    ]
)

print(json.dumps({"path": path}))