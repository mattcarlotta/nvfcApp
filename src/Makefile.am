## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(pkgdatadir)/ui
ui_DATA = nvfcapp.ui


## The main script
bin_SCRIPTS = nvfcapp.py

## Directory where .class files will be installed
nvfcappdir = $(pythondir)/nvfcapp


nvfcapp_PYTHON = \
	nvfcapp.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)
