How to use color_paint:

STARTUP:

1) Start SwisTrack.  Fire up the tracking program of your choice
(e.g. redgreen, reddetect, etc).

3) In the python/cameracontrol directory, run "sudo python btle-server.py".  Make sure NUM_ROBOTS in constants.py is set to 1.

4) Fire up Processing.  Open and run processing/color_paint/color_paint.pde

5) In the python/cameracontrol directory, run "python pointandclick.py"

OPERATION:

Click on the processing window to set waypoints, or click and drag to set a path of waypoints (red circles denote waypoints in this case).

Click on the colored swatches to change the color of the LED.  The white swatch turns the LED off.

NOTES:

For smooth operation, always close pointandclick.py before closing the processing window.

Try to set up the camera in an area with minimal variation in light and shadow.
