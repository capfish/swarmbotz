import serial,time
ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
time.sleep(2)
for i in range(20):
	ser.write('123')

#import Tkinter
#import serial
 
## Define a keyboard callback function. This will be called
## every time a key is pressed anywhere in the window.
#def key(event):
    #print "Sending", repr(event.char)
    #ser.write(event.char)
    #ser.write('a bright day')
 
## Open first serial port
#ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
 
## Create a Tk GUI window
#root = Tkinter.Tk()
 
## Bind all keypresses to the "key" function (define above)
#root.bind("<Key>", key)
 
## Just place a simple label in the window
#Tkinter.Label(root, text="Press some keys!").pack()
 
## Enter the Tkinter main event loop. The program will stay
## in this event loop until it's time to exit.
#root.mainloop()
 
## Close serial port
#ser.close()

