import tkinter as tk
from tkinter import messagebox as tkMessageBox

def displayErrorBox(message):
	root = tk.Tk()
	root.withdraw()
	tkMessageBox.showerror('Error', message)
	root.destroy()

	