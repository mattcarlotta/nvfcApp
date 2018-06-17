# Nvidia GPU Fan Controller (nvfcApp)
a GTK3 GUI application that creates a modifiable 2D curve of [temp, speed] points that are used to control a Nvidia GPU fan within a Debian/GNU environment.

![nvfc.png](https://code.mattcarlotta.io/root/nvda-fcontrl/raw/master/nvfc.png)

## Quickstart Linux

* Install python3:  
  `sudo apt-get install python3.6`
* Install matplotlib:  
  `sudo apt-get install python-matplotlib`
* Install Tkinter:  
  `sudo apt-get install python3-tk`
* Install pyGTK:  
  `sudo apt-get install libgtk-3-dev`
* Install cairocffi:  
  `sudo apt-get install python3-cairocffi`  
* Install libcanberra-gtk:  
  `sudo apt-get install libcanberra-gtk-module`
* Allow the Nvidia card's fan to be controlled:  
  `sudo nvidia-xconfig --enable-all-gpus` and `sudo nvidia-xconfig --cool-bits=28`
* Reboot your computer for the GPU settings to take effect:  
  `sudo reboot`
* Open a terminal in the folder containing nvfc.py, then execute:  
  `python3 nvfcapp.py`

## Button Actions

* Apply - Applies the curve to the GPU fan for the duration of the session
* Reset - Sets the curve to default values (can be values from `config.csv`)
* Save -  A "Save as" file dialog pops open. Simply input a file name, click save, and it'll automatically add a .csv extension. See notes below for more information. 

## Live Updates

* Temperature - Current GPU temperature (°C)
* Fan Speed - Current GPU fan speed (%)

## Notes
⚠️ On start up, this application only looks for a `config.csv` file within the app directory. If missing, it'll load a default curve. 

⚠️ Only works on OS's that support python3 and have nvidia proprietary drivers installed

⚠️ Versions 349.12 and 349.16 are not supported due to a regression in the drivers

⚠️ No SLI support (only single GPU configuration)

⚠️ It currently must be used with an open terminal

⚠️ Closing the app resets the GPU fan speed to be controlled by driver


## Dependencies:

* python3
* matplotlib
* Tkinter
* pyGTK
* cairocffi
* libcanberra-gtk
* nvidia-driver-350+

Based on the work of Luke Frisken and Mister Pup:  
* https://code.google.com/p/nvidia-fanspeed/
* https://github.com/MisterPup/Nvidia-Dynamic-Fan-Control
