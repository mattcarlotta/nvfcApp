# Nvidia GPU Fan Controller (nvfcApp)
a GTK3 GUI application that creates a modifiable 2D curve of [temp, speed] points that are used to control a Nvidia GPU fan within a Linux environment.

![nvfc.png](https://code.mattcarlotta.io/root/nvfcApp/raw/master/nvfcApp.png)

## Quickstart for running python 2.7:

* Install python3:  
  `sudo apt-get install python`
* Install matplotlib:  
  `sudo apt-get install python-matplotlib`
* Install Tkinter:  
  `sudo apt-get install python-tk`
* Install pyGTK:  
  `sudo apt-get install libgtk-2-dev`
* Install cairocffi:  
  `sudo apt-get install python-cairocffi`  
* Install libcanberra-gtk:  
  `sudo apt-get install libcanberra-gtk-module`
* Allow the Nvidia card's fan to be controlled:  
  `sudo nvidia-xconfig --enable-all-gpus` and `sudo nvidia-xconfig --cool-bits=28`
* Reboot your computer for the GPU settings to take effect:  
  `sudo reboot`
* Open a terminal in the folder containing nvfc.py, then execute:  
  `python nvfcapp.py`

## Quickstart for running python 3.6:

* Install python3:  
  `sudo apt-get install python3.6`
* Install matplotlib:  
  `sudo apt-get install python3-matplotlib`
* Install Tkinter:  
  `sudo apt-get install python3-tk`
* Install pyGTK:  
  `sudo apt-get install libgtk-3-dev`
* Install cairocffi:  
  `sudo apt-get install python3-cairocffi`  
* Install libcanberra-gtk3:  
  `sudo apt-get install libcanberra-gtk3-module`
* Allow the Nvidia card's fan to be controlled:  
  `sudo nvidia-xconfig --enable-all-gpus` and `sudo nvidia-xconfig --cool-bits=28`
* Reboot your computer for the GPU settings to take effect:  
  `sudo reboot`
* Open a terminal in the folder containing nvfc.py, then execute:  
  `python3 nvfcapp.py`

## Button Actions

* Apply - Applies the curve to the GPU fan speed for the duration of the session.
* Disable - Disables GPU fan control.
* Enable - Enables GPU fan control for the duration of the session (on application startup, if available, this is enabled).
* Open - Allows a different curve configuration to be loaded for the duration of the session. See notes below for more information.
* Quit - Exits the application and gives fan control back to the driver.
* Reset - Sets the curve to default values (can be values from `default.csv` or a loaded `.csv` file).
* Save - A "Save as" file dialog pops open. Simply input a file name, click save, and it'll automatically add a .csv extension. See notes below for more information.

## Live Chart Updates

* Temperature - Current GPU temperature (°C)
* Fan Speed - Current GPU fan speed (%)

## Notes
⚠️ On start up, this application only looks for a `default.csv` file within the application's directory. If missing, it'll load a pre-configured default curve.

⚠️ You must click the Apply button if you wish for the curve to be saved to a configuration file.

⚠️ When saving a configuration, the filename can be named anything, but must contain the `.csv` extension (automatically applied, so no need to explicitly write it). When loading a configuration, the configuration will only be used for the duration of the application session. Upon application reload, it'll look for and load a `default.csv` if available.

⚠️ Only works on Linux OS's that support python and have Nvidia proprietary drivers installed.

⚠️ Nvidia driver versions 349.12 and 349.16 are not supported due to a driver regression.

⚠️ No SLI support (only single GPU configuration).

⚠️ It currently must be used with an open terminal.

⚠️ Closing the application resets the GPU's fan to be controlled by the Nvidia driver.


## Dependencies:

* python3
* matplotlib
* Tkinter
* pyGTK
* cairocffi
* libcanberra-gtk
* proprietary Nvidia driver

Based on the work of Luke Frisken and Mister Pup:  
* https://code.google.com/p/nvidia-fanspeed/
* https://github.com/MisterPup/Nvidia-Dynamic-Fan-Control
