import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio, Gdk

# displays error dialog box
class ErrorDialogBox():
    def __init__(self, parent, message):
        dialog = Gtk.MessageDialog(parent, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "An Error Occured")
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

# displays message dialog box
class MessageDialogBox():
    def __init__(self, parent, message):
        dialog = Gtk.MessageDialog(parent, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Fan Controller Update")
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

# attempts to open a config file
class FileChooserBox():
    """ Class Variables """
    dir = None
    """ --------------- """

    def __init__(self, parent):
        dialog = Gtk.FileChooserDialog("Choose a file...", parent,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        dialog.set_default_size(800, 400)

        self.add_filters(dialog)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            FileChooserBox.dir = dialog.get_filename()
        # elif response == Gtk.ResponseType.CANCEL:
        #     FileDialogBox.dir = None

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("CSV files")
        filter_text.add_mime_type("text/csv")
        dialog.add_filter(filter_text)

# attempts to save a config file
class FileSaveBox():
    def __init__(self, parent):
        dialog = Gtk.FileChooserDialog("Save Configuration", parent, Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))

        dialog.set_default_size(800, 400)
        self.add_filters(dialog) # file filters
        Gtk.FileChooser.set_do_overwrite_confirmation(dialog, True) # if file already exists, show popup before saving

        self.dir = None # sets current file dir

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            self.dir = dialog.get_filename() # gets saved filename
            if not self.dir.lower().endswith('.csv'): self.dir = self.dir + ".csv" # if missing .csv extension, adds it

        # elif response == Gtk.ResponseType.CANCEL:
        #     FileDialogBox.dir = None

        dialog.destroy()

    def add_filters(self, dialog):
        filter = Gtk.FileFilter()
        filter.set_name("CSV Files")
        filter.add_mime_type("text/csv")
        filter.set_name("(*.csv)")
        filter.add_pattern("*.[csv]")
        dialog.add_filter(filter)

    def getFile(self): return self.dir
