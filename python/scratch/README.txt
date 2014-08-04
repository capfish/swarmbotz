Operating arrowkeys.py:

INSTALLATION:

wheelcontrol.py uses the scratchpy library located at https://github.com/pilliq/scratchpy

Follow the installation instructions on the page to install scratchpy

demo.sb uses scratch 1.4.  Install from http://scratch.mit.edu/scratch_1.4/

STARTUP:

1) Open the demo.sb scratch program in the scratch directory.

2) Run "sudo python btle-server.py" in the python/cameracontrol directory.  Make sure NUM_ROBOTS in constants.py is set to 1.

3) Run wheelcontrol.py in the python/scratch directory

OPERATION:

Focus must be on the scratch window
TODO:  Add support for focus on the python window (this should be simple)

Up arrow - Increment speed of both wheels by 1
Down arrow - Increment speed of both wheels by -1
Left arrow - Increment left wheel by -1, right wheel by 1
Right arrow - Increment left wheel by 1, right wheel by -1
Spacebar - Halt robot and turn off LED
c - Cycle through LED colors (Red -> Green -> Blue -> Off)