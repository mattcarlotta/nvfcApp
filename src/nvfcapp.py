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
from subprocess import *
import signal
import sys
from chartController import *
from gpuControlActions import *
from styleProvider import styles
styles()

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_WINDOWS = ["nvfcapp.ui"]
#UI_FILE = "/usr/local/share/nvfcapp/ui/nvfcapp.ui"

class GUI:
	def __init__(self):
		self.builder = Gtk.Builder()
		try:
			for window in UI_WINDOWS: self.builder.add_from_file(window)
		except:
			for window in UI_WINDOWS: self.builder.add_from_file("src/" + window)

		self.builder.connect_signals(self)

		# main application window
		self.appWindow = self.builder.get_object('nvfcApp')
		self.appWindow.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

		# about window (hidden)
		self.aboutWindow = self.builder.get_object('nvfcAbout')

		# notebook container
		self.notebook = self.builder.get_object('notebookContainer')

		# checks if Nvidia drivers are in use (if they are, enable curve button options)
		driverInUse = check_output("lspci -k | grep -EA3 'VGA|3D|Display' | grep 'use' |  sed 's/.*: //'", shell=True).decode('utf-8').strip()
		if driverInUse == 'nvidia': self.enable_curve_buttons()

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

		self.appWindow.show_all()

	def on_nvfcApp_destroy(s=None, w=None, d=None):
		close()
		Gtk.main_quit()

	def	on_aboutOkButton_clicked(self, widget):
		self.aboutWindow.destroy()

	def on_aboutButton_activate(self, widget):
		self.aboutWindow.show_all()

	def on_applyButton_clicked(self, widget):
		clickedApplyData()

	def on_disableButton_clicked(self, widget):
		self.disable_curve_buttons()
		disableGPUControl()

	def on_fileButton_activate(self, widget):
		self.on_nvfcApp_destroy()

	def on_enableButton_clicked(self, widget):
		self.enable_curve_buttons()
		enableGPUControl()

	def on_openButton_clicked(self, widget):
		clickedOpenFile()

	def on_resetButton_clicked(self, widget):
		clickedDataReset()

	def on_saveButton_clicked(self, widget):
		clickedSaveToFile()

	def on_quitButton_clicked(self, widget):
		self.on_nvfcApp_destroy()

	def curve_button_options(self, arr, bool):
		for label in arr:
			button = self.builder.get_object(label)
			button.set_sensitive(bool)

	def enable_curve_buttons(self):
		arr1 = ['enableButton']
		arr2 = ['disableButton','applyButton', 'resetButton', 'openButton', 'saveButton']
		self.curve_button_options(arr1, False)
		self.curve_button_options(arr2, True)

	def disable_curve_buttons(self):
		arr1 = ['enableButton']
		arr2 = ['disableButton', 'applyButton', 'resetButton', 'openButton', 'saveButton']
		self.curve_button_options(arr1, True)
		self.curve_button_options(arr2, False)

def main():
	app = GUI()
	Gtk.main()

if __name__ == "__main__":
	sys.exit(main())
