import serial, sys, time

def quit():
    #
    # clean up and quit
    #
    time.sleep(1)
    ser.close()
    sys.exit()


def setup():
    time.sleep(2)
    ser.setDTR()
    ser.flushInput()
    ser.flushOutput()

def write(string):
    #for key in string:
        #if (ord(key) == 13):
            #key = chr(10)
    #ser.write(key)
    ser.write(string)

if (len(sys.argv) != 3):
    print "command line: term.py serial_port speed"
    sys.exit()
port = sys.argv[1]
speed = int(sys.argv[2])
ser = serial.Serial(port, speed)

setup()
print "test"
write('hello')

quit()
