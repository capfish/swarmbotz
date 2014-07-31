Operating arrowkeys.py:

INSTALLATION:

Arrowkeys uses the scratchpy library located at https://github.com/pilliq/scratchpy

Follow the installation instructions on the page to install scratchpy

Arrowkeys uses scratch 1.4.  Install from http://scratch.mit.edu/scratch_1.4/

STARTUP:

1) Open the arrowkeys scratch program in the scratch directory.

2) Run "sudo python btle-server.py" in the python/cameracontrol directory.  Make sure NUM_ROBOTS in constants.py is set to 1.

3) Run arrowkeys.py in the python/scratch directory

OPERATION:

Focus must be on the scratch window
TODO:  Add support for focus on the python window (this should be simple)

Up arrow -- move forward for 5 seconds
Down arrow -- move backwards for 5 seconds
Left arrow -- turn left for 2 seconds
Right arrow -- turn right for 2 seconds
r -- Light red LED
g -- light green LED
b -- light blue LED
x -- turn off LED
