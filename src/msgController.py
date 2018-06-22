import tkinter as tk
from tkinter.messagebox import showinfo, showerror

def destroy(root):
	root.destroy()

def displayDialogBox(message):
	dialogBox = tk.Tk()
	dialogBox.withdraw()
	showinfo('Message', message)
	destroy(dialogBox)

def displayErrorBox(message):
	errorBox = tk.Tk()
	errorBox.withdraw()
	showerror('Error', message)
	destroy(errorBox)
