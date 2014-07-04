import swisclient
import time, sys, serial, socket

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
        self.port = 5027
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swis = swisclient.SwisClient()
        self.NUM_ROBOTS = self.swis.NUM_ROBOTS
        self.lastHeadings = None # Differential control keeps track of past steps
        self.lastDistances = None
#        self.waypoints = "320,240 : 1,100 : 20,20 : 30,40 : 50,40"
        self.waypoitns =  [(500, 200), (499, 206), (499, 212), (499, 218), (498, 225), (497, 231), (496, 237), (495, 243), (493, 249), (492, 255), (490, 261), (488, 267), (485, 273), (483, 279), (480, 285), (478, 290), (475, 296), (472, 301), (468, 307), (465, 312), (461, 317), (458, 322), (454, 327), (450, 332), (445, 336), (441, 341), (436, 345), (432, 350), (427, 354), (422, 358), (417, 361), (412, 365), (407, 368), (401, 372), (396, 375), (390, 378), (385, 380), (379, 383), (373, 385), (367, 388), (361, 390), (355, 392), (349, 393), (343, 395), (337, 396), (331, 397), (325, 398), (318, 399), (312, 399), (306, 399), (300, 400), (293, 399), (287, 399), (281, 399), (274, 398), (268, 397), (262, 396), (256, 395), (250, 393), (244, 392), (238, 390), (232, 388), (226, 385), (220, 383), (214, 380), (209, 378), (203, 375), (198, 372), (192, 368), (187, 365), (182, 361), (177, 358), (172, 354), (167, 350), (163, 345), (158, 341), (154, 336), (149, 332), (145, 327), (141, 322), (138, 317), (134, 312), (131, 307), (127, 301), (124, 296), (121, 290), (119, 285), (116, 279), (114, 273), (111, 267), (109, 261), (107, 255), (106, 249), (104, 243), (103, 237), (102, 231), (101, 225), (100, 218), (100, 212), (100, 206), (100, 200), (100, 193), (100, 187), (100, 181), (101, 174), (102, 168), (103, 162), (104, 156), (106, 150), (107, 144), (109, 138), (111, 132), (114, 126), (116, 120), (119, 114), (121, 109), (124, 103), (127, 98), (131, 92), (134, 87), (138, 82), (141, 77), (145, 72), (149, 67), (154, 63), (158, 58), (163, 54), (167, 49), (172, 45), (177, 41), (182, 38), (187, 34), (192, 31), (198, 27), (203, 24), (209, 21), (214, 19), (220, 16), (226, 14), (232, 11), (238, 9), (244, 7), (250, 6), (256, 4), (262, 3), (268, 2), (274, 1), (281, 0), (287, 0), (293, 0), (299, 0), (306, 0), (312, 0), (318, 0), (325, 1), (331, 2), (337, 3), (343, 4), (349, 6), (355, 7), (361, 9), (367, 11), (373, 14), (379, 16), (385, 19), (390, 21), (396, 24), (401, 27), (407, 31), (412, 34), (417, 38), (422, 41), (427, 45)]


       
        # Initialize serial port components
        time.sleep(2)
        #self.ser.setDTR()
        #self.ser.flushInput()
        #self.ser.flushOutput()
        
        self.sock.connect(('127.0.0.1',self.port))

        print "__INIT__"
    # Close the serial connection
    def closeSerial(self):
        time.sleep(1)
    #    self.ser.close()

    def write(string):
        pass

    def closeSocket():
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
        P = 1.0
        D = 0.1
        DMax = 0.6
        rotationMax = 0.4
        motorMax = 2
        triggerDistance = 50
        j = 0
        
        #distances = self.swis.generateDistances(self.waypoints) # Current distances
        
        # Go through each robot and update its velocity
        # TODO add functionality to move to next waypoint
        for i in range(0, self.NUM_ROBOTS):
            distances, headings = self.swis.generateHeadings(self.waypoints[j]) # Current headings   
            if distances == None and headings == None:
                return
            heading = headings[i][1]
            
            # P control
            output = P * heading
            
            # If the angle isn't too big, use D control
            if self.lastHeadings != None:
                lastHeading = self.lastHeadings[i][1]
                if abs(heading - lastHeading) < DMax:
                    output += D * (heading - lastHeading)
#                    print "D control"
            forward = 1.0
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
            leftVelocity = translate(leftVelocity, -1*motorMax, motorMax, 0, 180)
            rightVelocity = translate(rightVelocity, -1*motorMax, motorMax, 0, 180)


            #setVelocity(leftVelocity, rightVelocity, i)
            
            # If the robot is close enough to a waypoint, iterate to the
            # next waypoint for that robot
            distance = distances[i][1]
            print distance
            if distance < triggerDistance:
                print "Trigger"
                # TODO add code to move to next waypoint
                #leftVelocity = 90
                #rightVelocity = 90
                j = j+1

  #          message = message + str(i) + "," + str(leftVelocity) + "," + str(rightVelocity) + ":"

            message = "0," + str(leftVelocity) + "," + str(rightVelocity)
            print message
            self.sock.sendall(message)

        self.lastHeadings = headings
        print message
        print ""
        #self.ser.write(message)
        time.sleep(0.05)

    # Uses pySerial to send left and right wheel velocity
    # commands to a given robot.
    def setVelocity(self, left, right, robot):
        message = '0, 90, 90'
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
                #s.closeSerial()
                s.closeSocket()
                sys.exit()

if __name__ == '__main__':
    s = swarm()
    bots = s.NUM_ROBOTS
    main()
