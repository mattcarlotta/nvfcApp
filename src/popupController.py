import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio, Gdk


# displays error dialog box
class ErrorDialogBox():
	def __init__(self, appWindow, message):
		dialog = Gtk.MessageDialog(appWindow, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "An Error Occured")
		dialog.format_secondary_text(message)
		dialog.run()
		dialog.destroy()

# displays message dialog box
class MessageDialogBox():
	def __init__(self, appWindow, message):
		dialog = Gtk.MessageDialog(appWindow, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Information")
		dialog.format_secondary_text(message)
		dialog.run()
		dialog.destroy()

# attempts to open a config file
class FileChooserBox():
	""" Class Variables """
	dir = None
	""" --------------- """

	def __init__(self, appWindow):
		dialog = Gtk.FileChooserDialog("Choose a file...", appWindow,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		dialog.set_default_size(800, 400) # default window size

		add_filters(dialog) # CSV file filters

		response = dialog.run() # runs dialog that will return a response (OK/CANCEL)

		# if resp = OK, sets class dir variable
		if response == Gtk.ResponseType.OK:
			FileChooserBox.dir = dialog.get_filename()

		dialog.destroy()

# attempts to save a config file
class FileSaveBox():
	def __init__(self, appWindow):
		dialog = Gtk.FileChooserDialog("Save Configuration", appWindow, Gtk.FileChooserAction.SAVE,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))

		dialog.set_default_size(800, 400) # default window size
		add_filters(dialog) # file filters
		Gtk.FileChooser.set_do_overwrite_confirmation(dialog, True) # if file already exists, show popup before saving

		self.dir = None # current instance file dir variable

		response = dialog.run() # runs dialog that will return a response (ACCEPT/CANCEL)

		# if resp = ACCEPT, sets self.dir variable -- storing it to a class variable is unnecessary, esp. if user cancels
		if response == Gtk.ResponseType.ACCEPT:
			self.dir = dialog.get_filename() # gets saved /dir/to/filename
			if not self.dir.lower().endswith('.csv'): self.dir = self.dir + ".csv" # if missing, adds .csv extension

		dialog.destroy()

	def getFile(self): return self.dir

# file filters applied to open/save dialogs
def add_filters(dialog):
	filter = Gtk.FileFilter()
	filter.set_name("CSV Files")
	filter.add_mime_type("text/csv")
	dialog.add_filter(filter)
