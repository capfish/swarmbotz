import swisclient_wp as swisclient
#import swisclient_single_wp as swisclient
import math, time, sys, serial, socket, constants

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

class swarm:    

    def __init__(self):
        #self.ser = serial.Serial("/dev/ttyUSB0", 9600)
        self.port = constants.PORT_BTLE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swis = swisclient.SwisClient()
        self.NUM_ROBOTS = self.swis.NUM_ROBOTS
        self.lastHeadings = [None, None] #None # Differential control keeps track of past steps
        self.secondLastHeadings = [None, None]
        self.lastDistances = [None, None] #None
#       self.waypoints = "320,240 : 1,100 : 20,20 : 30,40 : 50,40"
	#self.waypoints = [(450, 100), (450, 350), (100, 350), (100,100)]
        self.waypoints = []
        self.check = [0,1]      
        self.initCheck = [0,1]
        self.reverse = [False, False]
        #self.initialized = [False, False]
        self.initialized = [True, True]
        self.startPos = []
            
        # Initialize serial port components
        time.sleep(2)
        #self.ser.setDTR()
        #self.ser.flushInput()
        #self.ser.flushOutput()
        
        self.sock.connect(('127.0.0.1',self.port))

       
        print "__INIT__"
    # Close the serial connection
    
    # Reads data from the processing program.
    # There are two types of command, waypoint and color.  Color commands are formatted as c:#RRGGBB where
    # #RRGGBB is a hex representation of an RGB value.
    # Waypoint commands are of the form x1,y1:x2,y2:x3,y3: etc.
    def readData(self):
        processingSock = socket.socket()

        processingSock.connect((constants.HOST_PROCESSING,constants.PORT_PROCESSING))
        points = None
        dataPacket = True
#        print "receiving data"
        try:
            data = processingSock.recv(1024)
            print data
        except ValueError:
            print "no data"
#        print "received data, ", data
        if data != "No data":
            points = data.split(":")
            if (points[0]=='c'):  # Is the data a color command?
#                colorval = (byte)points[1]
                print(points[1])
                color = self.hex_to_rgb(points[1])  # Converts the hex value to a list color[0] = red, color[1] = green, color[2] = blue
                print color
                for i in range(self.NUM_ROBOTS):
                    message = str(i)+',10,'+str(color[0])+','+str(color[1])+','+str(color[2])  # Format message to send via bluetooth
                    self.sock.sendall(message) # Send the message
                    print message
            else: # The data is a waypoint command
            #print points, " split up points"
        
                tempWaypoints = self.waypoints
                self.waypoints = []
                if points:
                    self.waypoints = []
                    for point in points: # Populate the list of waypoints with the command.
                        p = point.split(",")
                        print p
                        x = int(p[0])
                        y = int(p[1])
                        self.waypoints.append((x,y))
                    dataPacket = False
                    points = None
                    print "tempwaypoints: ", tempWaypoints
                    print "waypoints: ", self.waypoints
                    if tempWaypoints != self.waypoints: # Has the command changed? If so, move back to the beginning of the waypoint list as it is reset
                        self.check = [0,1]#self.initCheck
                        print "Resetting check"
                    print "is check reset: ", self.check
                        
#        print "closing socket"
        processingSock.close()
#        print "finished processing data"
        return

    def closeSerial(self):
        time.sleep(1)
    #    self.ser.close()

    def write(string):
        pass


# Populates the waypoint array with the starting positions.
    def initialize(self):
        time.sleep(0.05)
        while 1:
            print "tick"
            d, h = self.swis.generateHeadings((0,0))
            print "init headings, ",h
#            print "check, ", self.waypoints[self.check[0]]
            if h != None:
                for i in xrange(self.NUM_ROBOTS):
                    self.startPos.append((h[i][2], h[i][3], h[i][4]))
                    self.waypoints.append((h[i][2], h[i][3]))
                return

# Convert a hex value to a list of form [red, green, blue]
    def hex_to_rgb(self, color):
        value = int(color)
        blue =  value & 255
        green = (value >> 8) & 255
        red =   (value >> 16) & 255
        return (red, green, blue)

    def closeSocket(self):
        self.sock.close()
    #for key in string:                                                                    
        #if (ord(key) == 13):                                                              
            #key = chr(10)                                                                 
    #ser.write(key)                                                                        
     #   self.ser.write(string)


    # Uses a PD loop to generate velocity for each robot,
    # given a list of waypoints.
    def step(self):
        #print "step"
        #self.waypoints = [(320,240),(200,200)] 
        self.readData() # Populate the waypoint list.

        message = ""
        # PD control parameters
        P = 3.0
        D = 0.4
        DMax = 0.3
        rotationMax = 1.4
        motorMax = 2.0
        triggerDistance = 25
        output = 0.0
        #j = 0

        #distances = self.swis.generateDistances(self.waypoints) # Current distances
        # Go through each robot and update its velocity
        for i in range(0, self.NUM_ROBOTS):
            time.sleep(0.02)


            msg = ""
            distances, headings = self.swis.generateHeadings(self.waypoints[self.check[i]]) # Heading to next waypoint
            if distances == None and headings == None:
                return
            # Get heading in radians
            heading = headings[i][1]
            print str(i), "heading, ", heading
            # P control
            #output = P * heading
            
            # If this is the first time through the loop, populate the waypoints with a point 100 pixels dead ahead.
            # The robot then attempts to move toward the point. This is to determine which direction it starts in for
            # tracking that does not have intrinsic directionality (e.g. single color tracking)
            if not self.initialized[i]:
 #               print "Initializing statement 1"
                distances, headings = self.swis.generateHeadings(self.startPos[i])
                if distances == None and headings == None:
                    return
                angle = float(self.startPos[i][2])
                destX = float(self.startPos[i][0]) + 100 * math.cos(angle)
                destY = float(self.startPos[i][1]) + 100 * math.sin(angle)
                distances, headings = self.swis.generateHeadings((destX, destY))
                heading = headings[i][1]
#                print "Starting distances: ", distances[i][1]
            # If the angle isn't too big, use D control
            if self.lastHeadings[i] != None:
                lastHeading = self.lastHeadings[i]
                if abs(abs(heading - lastHeading) - 3.1416) < 0.2 : # If the heading flips 180 degrees during non-directional tracking
                    self.reverse[i] = not self.reverse[i] # Flip the direction of the robot
            # Deal with the robot facing the wrong direction
                if self.reverse[i]:
                    if heading < 0.0:
                        heading = heading + 3.141
                        print "neg reverse"
                    else:
                        print "pos reverse"
                        heading = heading - 3.141
#                if self.secondLastHeadings[i] != None:
#                    secondLastHeading = self.secondLastHeadings[i]
#                    if abs(heading-lastHeading) > abs(lastHeading - secondLastHeading) + 0.2:
#                        heading = heading - 3.142
#                        if heading < -3.142:
#                            heading = 6.281+heading
# D control
                if abs(heading - lastHeading) < DMax:
                    output += D * (heading - lastHeading)
#                if abs(heading - lastHeading) > 2.0:                
#                    heading = heading - 3.142
#                    if heading < -3.142:
#                        heading = 6.281 + heading
            print str(i), "new heading, ", heading
# P control
            output += P*heading


            forward = 0.9
#            print "output ", output
            # Rotate whichever is smallest, the output value
            # or the maximum allowable rotation value
            rotate = max(min(rotationMax, output), -1*rotationMax)
#            print "rotate ", rotate
            # Move the wheels at whichever speed is smallest, the output
            # value or the maximum allowable speed.
            leftVelocity = max(min((forward - rotate), motorMax), -1*motorMax)
            rightVelocity = max(min((forward + rotate), motorMax), -1*motorMax)

            #Alright! Now convert to 80 to 100 instead of -motorMax to +motorMax
            print 'before mapping to servo vals', leftVelocity, rightVelocity
            leftVelocity = translate(leftVelocity, -1*motorMax, motorMax, 80,100)
            rightVelocity = translate(rightVelocity, -1*motorMax, motorMax, 80,100)

	    #leftVelocity = 100
	    #rightVelocity = 100
            #setVelocity(leftVelocity, rightVelocity, i)
#            0
            # If the robot is close enough to a waypoint, iterate to the
            # next waypoint for that robot
            distance = distances[i][1]
            print distance
# Determine initial directionality of the robot
            if not self.initialized[i]:
                print "Initializing..."
                if distance < 80:
                    print "Forward"
                    self.initialized[i] = True
                    return
                if distance > 120:
                    self.reverse[i] = not self.reverse[i]
                    self.initialized[i] = True
                    print "Backwards"
                    return
# When the robot hits a waypoint, pause and switch to the next waypoint
            elif distance < triggerDistance:
                print "Trigger"
                # TODO add code to move to next waypoint
                print "check: ", self.check[i]
                print "length waypoints: ", len(self.waypoints)
                leftVelocity = 90
                rightVelocity = 90
                #if self.check[i] == len(self.waypoints):
                if self.check[i] < len(self.waypoints)-1:
                    self.check[i] = self.check[i] + 1
                #self.check[i] = self.check[i]%len(self.waypoints)
                
	        
	    message = str(i) + ",20," + str(leftVelocity) + "," + str(rightVelocity)
 #           print message
	    print "waypoints, ", self.waypoints[self.check[i]]
            self.sock.sendall(message)
# Populate previous heading lists
            self.secondLastHeadings[i] = self.lastHeadings[i]
            self.lastHeadings[i] = headings[i][1]
        return
#        print message
#        print ""
        #self.ser.write(message)
#        time.sleep(0.04)

    # Sets the velocity of a robot
    # Used primarily to stop the robots on shutdown
    def setVelocity(self, left, right, robot):
        message = str(robot) + ',20,' + str(left) + ',' + str(right)
   #     print message
        self.sock.sendall(message)
    
def main():
#        s = swarm()
#        bots = s.NUM_ROBOTS
    s.initialize()
    while 1:
        try:
            s.step()
        except (KeyboardInterrupt):
            print "Exiting program, stopping robots"
            for i in range (0, bots):
                s.setVelocity(90,90,i)
                time.sleep(0.1)
            #s.closeSerial()
            s.closeSocket()
            sys.exit()

if __name__ == '__main__':
    s = swarm()
    bots = s.NUM_ROBOTS
    main()
