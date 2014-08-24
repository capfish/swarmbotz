There are five relevant files needed to do camera tracking:  A swistrack file, a swistrack client/python interface file, a robot control python file, a constants file, and the bluetooth interface file.  Optionally, there is a processing sketch that can also be run.

OPERATION:

1) Run a swistrack tracking program, located in the /swistrack folder. They are modular, so any one will work with the python code.  red blob.swistrack will detect oblong red tracking dots (oriented along the axis of movement), and redgreen.swistrack will detect red and green tracking dots.

2) Set up constants.py with the relevant number of robots, the correct port numbers, etc.

3) Run btle-server.py

4) Run a robot control file. The two most useful ones are pointandclick.py (for the processing point-and-click demo) and multi_movement.py (for controlling multiple robots in a fixed pattern).  These programs internally call up a swisclient file.

5 [optional]) Run the color_paint processing sketch.  Instructions are in the /processing/color_paint folder.