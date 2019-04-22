# Nvidia GPU Fan Controller (nvfcApp)
a GTK3 (v3.18) application that creates a modifiable 2D curve of [temp, fanspeed] points that automatically controls a Nvidia GPU's fan speed according to the GPU's temp within a Linux environment.

![nvfc.png](https://github.com/mattcarlotta/nvfcApp/blob/master/imgs/nvfcApp_512x512.png)

## Linux Quickstart:

1. Download the zipped application file from the `dist` folder
2. Extract the application's folder from the zipped file and place it anywhere
3. Open a terminal window and install the following dependencies:  
  I. Install python3: `sudo apt-get install python3.6`  
  II. Install pip3: `sudo apt-get install python3-pip`  
  III. Install matplotlib: `python3 -mpip install matplotlib`  
  IV. Install pyGTK: `sudo apt-get install libgtk-3-dev`  
  V. Install cairocffi: `sudo apt-get install python3-cairocffi`    
  VI. Install libcanberra-gtk3: `sudo apt-get install libcanberra-gtk3-module`  
  VII. Install tkinter: `sudo apt-get install python3-tk`
4. Allow the Nvidia card's fan to be controlled:  
  `sudo nvidia-xconfig --enable-all-gpus` and `sudo nvidia-xconfig --cool-bits=28`
5. Reboot your computer for the GPU settings to take effect:  
  `sudo reboot`
6. Open a terminal in the folder containing nvfcapp.py, then execute:  
  `python3 nvfcapp.py`

## Button Actions

* Apply - Applies the curve to the GPU fan speed for the duration of the session.
* Disable - Disables GPU fan control.
* Enable - Enables GPU fan control for the duration of the session (on application startup, if available, this is enabled by default).
* Open - Allows a different curve configuration to be loaded for the duration of the session. See notes below for more information.
* Quit - Exits the application and gives fan control back to the driver.
* Reset - Updates the curve to default values (can be values from `default.csv` or a different loaded `.csv` file).
* Save - A "Save as" file dialog pops open. Simply input a name, click save, and it'll automatically add a .csv extension. See notes below for more information.

## Live Chart Updates

* Temperature - Current GPU temperature (°C)
* Fan Speed - Current GPU fan speed (%)

## GPU Utilization and Statistics Updates

* Clock - Current GPU shader clock (MHz)
* Load - Current GPU load (%)
* Fan Speed - Current GPU fan speed (%)
* Memory - Current GPU memory usage (MiB)
* Power - Current GPU power draw (W)
* Temperature - Current GPU temperature (°C)

## Notes
⚠️ On start up, this application only looks for a `default.csv` file within the application's directory. If missing, it'll load a pre-configured curve.

⚠️ You must click the Apply button before saving if you wish for the curve to be saved to a configuration file.

⚠️ When saving a configuration, the filename can be named anything, but must contain the `.csv` extension (automatically applied, so no need to explicitly write it). When loading a configuration, it will only be used for the duration of the application session. Upon application reload, it'll look for and load a `default.csv` if available.

⚠️ Only works on Linux OS's that support the dependencies listed below.

⚠️ Nvidia driver versions 349.12 and 349.16 are not supported due to a driver regression.

⚠️ No SLI support (only single GPU configuration).

⚠️ It currently must be used with an open terminal.

⚠️ Closing the application resets the GPU's fan to be controlled by the Nvidia driver.


## Dependencies:

* python3 (python3.6)
* matplotlib (python3-matplotlib)
* pip3
* pyGTK (libgtk-3-dev)
* cairocffi (python3-cairocffi)
* libcanberra-gtk3
* proprietary Nvidia driver

## Credits:

Based on the work of Luke Frisken and Mister Pup:  
* https://code.google.com/p/nvidia-fanspeed/
* https://github.com/MisterPup/Nvidia-Dynamic-Fan-Control
