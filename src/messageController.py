import tkinter as tk
from tkinter import messagebox as tkMessageBox

def destroy(root):
	root.destroy()

def displayDialogBox(message):
	dialogBox = tk.Tk()
	dialogBox.withdraw()
	tkMessageBox.showinfo('Message', message)
	destroy(dialogBox)

def displayErrorBox(message):
	errorBox = tk.Tk()
	errorBox.withdraw()
	tkMessageBox.showerror('Error', message)
	destroy(errorBox)
	