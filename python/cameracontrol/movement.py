import swisclient
import time, sys, serial

class swarm:    

    def __init__(self):
        self.ser = serial.Serial("/dev/ttyUSB0", 9600)
        self.swis = swisclient.SwisClient()
        self.NUM_ROBOTS = self.swis.NUM_ROBOTS
        self.lastHeadings = None # Differential control keeps track of past steps
        self.waypoints = "320,240 : 1,100"
        
        # Initialize serial port components
        time.sleep(2)
        self.ser.setDTR()
        self.ser.flushInput()
        self.ser.flushOutput()
        
    # Close the serial connection
    def closeSerial(self):
        time.sleep(1)
        self.ser.close()

    def write(string):
    #for key in string:                                                                    
        #if (ord(key) == 13):                                                              
            #key = chr(10)                                                                 
    #ser.write(key)                                                                        
        self.ser.write(string)


    # Uses a PD loop to generate velocity for each robot,
    # given a list of waypoints.
    def step(self):
        message = ""
        P = 1.0
        D = 0.1
        DMax = 0.6
        rotationMax = 0.4
        motorMax = 2
        triggerDistance = 5
        headings = self.swis.generateHeadings(self.waypoints) # Current headings
        distances = self.swis.generateDistances(self.waypoints) # Current distances
        # Go through each robot and update its velocity
        # TODO add functionality to move to next waypoint
        for i in range(0, self.NUM_ROBOTS):
            heading = headings[i]
            
            # P control
            output = P * heading
            
            # If the angle isn't too big, use D control
            if self.lastHeadings != None:
                lastHeading = self.lastHeadings[i]
                if abs(heading - lastHeading) < DMax:
                    output += D * (heading - lastHeading)
                    print "D control"
            forward = 1.0
            print "output ", output
            # Rotate whichever is smallest, the output value
            # or the maximum allowable rotation value
            rotate = max(min(rotationMax, output), -1*rotationMax)
            print "rotate ", rotate
            # Move the wheels at whichever speed is smallest, the output
            # value or the maximum allowable speed.
            leftVelocity = int(100*max(min((forward - rotate), motorMax), -1*motorMax))
            rightVelocity = int( 100*max(min((forward + rotate), motorMax), -1*motorMax))

            #setVelocity(leftVelocity, rightVelocity, i)
            
            # If the robot is close enough to a waypoint, iterate to the
            # next waypoint for that robot
            distance = distances[i]
            if distance < triggerDistance:
                # TODO add code to move to next waypoint
                leftVelocity = 0.0
                rightVelocity = 0.0

  #          message = message + str(i) + "," + str(leftVelocity) + "," + str(rightVelocity) + ":"

            message = message + str(leftVelocity) + "," + str(rightVelocity) + ":X"

        self.lastHeadings = headings
        print message
        print ""
        self.ser.write(message)
        time.sleep(0.05)

    # Uses pySerial to send left and right wheel velocity
    # commands to a given robot.
    def setVelocity(self, left, right, robot):
        pass
    
def main():
        s = swarm()
        bots = s.NUM_ROBOTS
        while 1:
            try:
                s.step()
            except (KeyboardInterrupt):
                print "Exiting program, stopping robots"
                for i in range (0, bots):
                    s.setVelocity(0,0,i)
                s.closeSerial()
                sys.exit()

if __name__ == '__main__':
    main()
