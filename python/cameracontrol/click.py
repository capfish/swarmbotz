import swisclient_wp as swisclient
import time, sys, serial, socket, constants

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
        self.lastDistances = [None, None] #None
#       self.waypoints = "320,240 : 1,100 : 20,20 : 30,40 : 50,40"
	#self.waypoints = [(450, 100), (450, 350), (100, 350), (100,100)]
	#self.waypoints = [(450, 225), (100, 350), (100,100)]
        self.check = [0,2]

        self.clickPort = 5001
        self.clickSock = socket.socet(socket.AF_INET, socket.SOCK_STREAM)
#	self.waypoints = [(400, 200), (380, 258), (330, 295), (269, 295), (219, 258), (200, 200), (219, 141), (269, 104), (330, 104), (380, 141)]	
	#self.waypoints = [(400, 200), (399, 203), (399, 206), (399, 209), (399, 212), (398, 215), (398, 218), (397, 221), (396, 224), (396, 227), (395, 230), (394, 233), (392, 236), (391, 239), (390, 242), (389, 245), (387, 248), (386, 250), (384, 253), (382, 256), (380, 258), (379, 261), (377, 263), (375, 266), (372, 268), (370, 270), (368, 272), (366, 275), (363, 277), (361, 279), (358, 280), (356, 282), (353, 284), (350, 286), (348, 287), (345, 289), (342, 290), (339, 291), (336, 292), (333, 294), (330, 295), (327, 296), (324, 296), (321, 297), (318, 298), (315, 298), (312, 299), (309, 299), (306, 299), (303, 299), (300, 300), (296, 299), (293, 299), (290, 299), (287, 299), (284, 298), (281, 298), (278, 297), (275, 296), (272, 296), (269, 295), (266, 294), (263, 292), (260, 291), (257, 290), (254, 289), (251, 287), (249, 286), (246, 284), (243, 282), (241, 280), (238, 279), (236, 277), (233, 275), (231, 272), (229, 270), (227, 268), (224, 266), (222, 263), (220, 261), (219, 258), (217, 256), (215, 253), (213, 250), (212, 248), (210, 245), (209, 242), (208, 239), (207, 236), (205, 233), (204, 230), (203, 227), (203, 224), (202, 221), (201, 218), (201, 215), (200, 212), (200, 209), (200, 206), (200, 203), (200, 200), (200, 196), (200, 193), (200, 190), (200, 187), (201, 184), (201, 181), (202, 178), (203, 175), (203, 172), (204, 169), (205, 166), (207, 163), (208, 160), (209, 157), (210, 154), (212, 151), (213, 149), (215, 146), (217, 143), (219, 141), (220, 138), (222, 136), (224, 133), (227, 131), (229, 129), (231, 127), (233, 124), (236, 122), (238, 120), (241, 119), (243, 117), (246, 115), (249, 113), (251, 112), (254, 110), (257, 109), (260, 108), (263, 107), (266, 105), (269, 104), (272, 103), (275, 103), (278, 102), (281, 101), (284, 101), (287, 100), (290, 100), (293, 100), (296, 100), (299, 100), (303, 100), (306, 100), (309, 100), (312, 100), (315, 101), (318, 101), (321, 102), (324, 103), (327, 103), (330, 104), (333, 105), (336, 107), (339, 108), (342, 109), (345, 110), (348, 1)]



       
        # Initialize serial port components
        time.sleep(2)
        #self.ser.setDTR()
        #self.ser.flushInput()
        #self.ser.flushOutput()
        
        self.sock.connect(('127.0.0.1', self.port))
        self.clickSock.connect(('127.0.0.1', self.clickPort))
        print "__INIT__"
    # Close the serial connection
    def closeSerial(self):
        time.sleep(1)
    #    self.ser.close()

    def write(string):
        pass

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
        message = ""
        P = 3.0
        D = 0.4
        DMax = 0.3
        rotationMax = 1.4
        motorMax = 2.0
        triggerDistance = 25
        #j = 0
        
        #distances = self.swis.generateDistances(self.waypoints) # Current distances
        
        # Go through each robot and update its velocity
        # TODO add functionality to move to next waypoint
        for i in range(0, self.NUM_ROBOTS):
            time.sleep(0.06)
            msg = ""
            distances, headings = self.swis.generateHeadings(self.waypoints[self.check[i]]) # Current headings   
            if distances == None and headings == None:
                return
            heading = headings[i][1]
            print str(i), "heading, ", heading
            # P control
            output = P * heading
            
            # If the angle isn't too big, use D control
            if self.lastHeadings[i] != None:
                lastHeading = self.lastHeadings[i][1]
                if abs(heading - lastHeading) < DMax:
                    output += D * (heading - lastHeading)
 #                   print "D control"

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

            #Alright! Now convert to 0 to 180 instead of -motorMax to +motorMax
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
            if distance < triggerDistance:
  #              print "Trigger"
                # TODO add code to move to next waypoint
                #leftVelocity = 90
                #rightVelocity = 90
                self.check[i] = self.check[i]+1
		self.check[i] = self.check[i]%len(self.waypoints)
  #          message = message + str(i) + "," + str(leftVelocity) + "," + str(rightVelocity) + ":"
	        
	    message = str(i) + ",20," + str(leftVelocity) + "," + str(rightVelocity)
 #           print message
	    print self.waypoints[self.check[i]]
            self.sock.sendall(message)

            self.lastHeadings[i] = headings[i]
#        print message
#        print ""
        #self.ser.write(message)
#        time.sleep(0.04)

    # Uses pySerial to send left and right wheel velocity
    # commands to a given robot.
    def setVelocity(self, left, right, robot):
        message = str(robot) + ',20,90,90'
        print message
        self.sock.sendall(message)
    
def main():
#        s = swarm()
#        bots = s.NUM_ROBOTS
        while 1:
            try:
                s.step()
            except (KeyboardInterrupt):
                print "Exiting program, stopping robots"
                for i in range (0, bots):
                    s.setVelocity(0,0,i)
                    time.sleep(0.1)
                #s.closeSerial()
                s.closeSocket()
                sys.exit()

if __name__ == '__main__':
    s = swarm()
    bots = s.NUM_ROBOTS
    main()
