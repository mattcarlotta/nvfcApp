from chartController import stopControlling
from subprocess import *
from messageController import displayErrorBox

def enableGPUControl():
    try:
        print("Enabling")
        output = Popen(['sudo', 'nvidia-xconfig', '--cool-bits=28'], stdin=PIPE, stdout=PIPE)
        message = process.stdout.readlines()
        print(message)
        displayDialogBox("Successfully enabled GPU fan controlling. Please reboot for it take effect.")
    except:
        displayErrorBox("Unable to enable GPU fan controlling.")

def disableGPUControl():
    try:
        stopControlling()
        displayDialogBox("Successfully disabled GPU fan controlling")
    except:
        displayErrorBox("Unable to disable GPU fan controlling.")
