#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-
#
# main.py
# Copyright (C) 2018 Matt Carlotta <carlotta.matt@gmail.com>
#
# nvfcApp is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# nvfcApp is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio, Gdk
import signal
from chartController import Chart, applyData, resetData, saveToFile, close, openFile
import sys
from styleProvider import styles
styles()

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "nvfcapp.ui"
SRC_UI_FILE = "src/nvfcapp.ui"
#UI_FILE = "/usr/local/share/nvfcapp/ui/nvfcapp.ui"

class GUI:
	def __init__(self):
		self.builder = Gtk.Builder()
		try:
			self.builder.add_from_file(UI_FILE)
		except:
			self.builder.add_from_file(SRC_UI_FILE)

		self.builder.connect_signals(self)

		self.window = self.builder.get_object('nvfcApp')
		self.pageContainer = self.builder.get_object('pageContainer')
		self.notebook = Gtk.Notebook()
		self.pageContainer.add(self.notebook)

		# appends chart graph to tab 1
		Chart(self.notebook)

		self.page2 = Gtk.Box()
		self.page2.set_border_width(10)
		self.page2.add(Gtk.Label('A page with an image for a Title.'))
		self.notebook.append_page(
			self.page2,
			Gtk.Image.new_from_icon_name(
			    "help-about",
			    Gtk.IconSize.MENU
			)
		)

		# signal traps
		signal.signal(signal.SIGINT, self.on_nvfcApp_destroy) #CTRL-C
		signal.signal(signal.SIGQUIT, self.on_nvfcApp_destroy) #CTRL-\
		signal.signal(signal.SIGHUP, self.on_nvfcApp_destroy) #terminal closed
		signal.signal(signal.SIGTERM, self.on_nvfcApp_destroy)

		self.window.show_all()

	def on_nvfcApp_destroy(s=None, w=None, d=None):
		close()
		Gtk.main_quit()

	def on_applyButton_clicked(self, widget):
		applyData()

	def on_openButton_clicked(self, widget):
		openFile()

	def on_resetButton_clicked(self, widget):
		resetData()

	def on_saveButton_clicked(self, widget):
		saveToFile()

	def on_quitButton_clicked(self, widget):
		self.on_nvfcApp_destroy()

def main():
	app = GUI()
	Gtk.main()

if __name__ == "__main__":
	sys.exit(main())
