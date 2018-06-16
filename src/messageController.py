import tkinter as tk
from tkinter import messagebox as tkMessageBox

def displayDialogBox(message):
	root = tk.Tk()
	root.withdraw()
	tkMessageBox.showinfo('Message', message)
	root.destroy()

	