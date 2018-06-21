import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


def styles():
	css_provider = Gtk.CssProvider()

	try:
		css_provider.load_from_path('./styles/styles.css')
	except:
		css_provider.load_from_path('src/styles/styles.css')

	Gtk.StyleContext.add_provider_for_screen(
	    Gdk.Screen.get_default(), css_provider,
	    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
	)
