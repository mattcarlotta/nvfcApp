#!/usr/bin/env python3
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
import matplotlib.pyplot as plt
from subprocess import *
import signal
import sys
from chartController import Chart
from sysInformation import SystemInformation
# from styleProvider import styles
# styles()

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
APP_WINDOW = "nvfcapp.ui"
#APP_WINDOW= "/usr/local/share/nvfcapp/ui/nvfcapp.ui"

class GUI:
	def __init__(self):
		self.builder = Gtk.Builder()

		try:
			self.builder.add_from_file(APP_WINDOW)
		except:
			self.builder.add_from_file("src/" + APP_WINDOW)

		self.builder.connect_signals(self)

		# main application window
		self.appWindow = self.builder.get_object('nvfcApp')
		self.appWindow.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

		# append current OS theme to toolbar
		self.appMenu = self.builder.get_object('appMenu')
		self.menuStyle = self.appMenu.get_style_context()
		self.menuStyle.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

		# about window (hidden)
		self.aboutWindow = self.builder.get_object('nvfcAbout')

		# notebook container
		self.notebook = self.builder.get_object('notebookContainer')

		# checks if Nvidia drivers are in use (if they are, enable curve button options)
		driverInUse = check_output("lspci -k | grep -EA3 'VGA|3D|Display' | grep 'use' |  sed 's/.*: //'", shell=True).decode('utf-8').strip()
		if driverInUse == 'nvidia': self.enable_curve_buttons()

		# GPU graph controller
		self.graph = self.builder.get_object('graphBox')
		# self.chart = Chart(self.appWindow, self.graph, self.disable_app_buttons)
		self.chart = Chart(self)
		self.chartsvg = GdkPixbuf.Pixbuf.new_from_file_at_scale("/home/m6d/Documents/nvfcApp/chart_512x512.png", 32, 32, True)
		self.chartIcon = Gtk.Image()
		self.chartIcon.set_from_pixbuf(self.chartsvg)
		self.notebook.append_page(self.graph, self.chartIcon)

		# system info / gpu info
		self.gpuInfo = self.builder.get_object('infoBox')
		self.nogpuInfo = self.builder.get_object('noinfoBox')

		if driverInUse == 'nvidia':
			SystemInformation(self.builder)
			self.showgpuInfo = self.gpuInfo

		else: self.showgpuInfo = self.nogpuInfo

		self.infosvg = GdkPixbuf.Pixbuf.new_from_file_at_scale("/home/m6d/Documents/nvfcApp/info_512x512.png", 32, 32, True)
		self.infoIcon = Gtk.Image()
		self.infoIcon.set_from_pixbuf(self.infosvg)
		self.notebook.append_page(self.showgpuInfo, self.infoIcon)

		# signal traps
		signal.signal(signal.SIGINT, self.on_nvfcApp_destroy) #CTRL-C
		signal.signal(signal.SIGQUIT, self.on_nvfcApp_destroy) #CTRL-\
		signal.signal(signal.SIGHUP, self.on_nvfcApp_destroy) #terminal closed
		signal.signal(signal.SIGTERM, self.on_nvfcApp_destroy)

		self.appWindow.show_all()

	def curve_button_options(self, arr, bool):
		for label in arr:
			button = self.builder.get_object(label)
			button.set_sensitive(bool)

	def enable_curve_buttons(self):
		arr1 = ['enableButton']
		arr2 = ['disableButton','applyButton', 'resetButton', 'openButton', 'saveButton']
		self.curve_button_options(arr1, False)
		self.curve_button_options(arr2, True)

	def disable_app_buttons(self):
		arr = ['enableButton', 'disableButton','applyButton', 'resetButton', 'openButton', 'saveButton']
		self.curve_button_options(arr, False)

	def disable_curve_buttons(self):
		arr1 = ['enableButton']
		arr2 = ['disableButton', 'applyButton', 'resetButton', 'openButton', 'saveButton']
		self.curve_button_options(arr1, True)
		self.curve_button_options(arr2, False)

	def on_nvfcApp_destroy(self, *args, **kwargs):
		self.chart.close()
		# plt.close('all')
		Gtk.main_quit()

	def on_nvfcAbout_delete_event(self, widget, data):
		self.aboutWindow.hide()

	def on_aboutButton_activate(self, widget):
		self.aboutWindow.show()
		self.aboutWindow.run()

	def on_applyButton_clicked(self, widget):
		self.chart.handleApplyData()

	def on_disableButton_clicked(self, widget):
		self.disable_curve_buttons()
		self.chart.handleDisableGPUControl()

	def on_fileButton_activate(self, widget):
		self.on_nvfcApp_destroy()

	def on_enableButton_clicked(self, widget):
		self.enable_curve_buttons()
		self.chart.handleEnableGPUControl()

	def on_openButton_clicked(self, widget):
		self.chart.handleOpenFile()

	def on_resetButton_clicked(self, widget):
		self.chart.handleDataReset()

	def on_saveButton_clicked(self, widget):
		self.chart.handleSaveToFile()

	def on_quitButton_clicked(self, widget):
		self.on_nvfcApp_destroy()

def main():
	app = GUI()
	Gtk.main()

if __name__ == "__main__":
	sys.exit(main())
