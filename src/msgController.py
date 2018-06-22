try:
	# python3
	import tkinter as tk
	from tkinter.messagebox import showinfo, showerror
except ImportError:
	# python2
	import Tkinter as tk
	from tkMessageBox import showinfo, showerror


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
