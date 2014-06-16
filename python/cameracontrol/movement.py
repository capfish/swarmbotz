import swisclient
import time

class swarm:    

    def __init__(self):
        self.swis = swisClient()
        self.NUM_ROBOTS = swis.NUM_ROBOTS
        self.lastHeadings = None
        self.waypoints = None
    
    # Uses a PD loop to generate velocity for each robot,
    # given a list of waypoints.
    def step():
        P = 1.0
        D = 0.2
        DMax = 0.6
        rotationMax = 0.4
        motorMax = 0.5
        triggerDistance = 5
        headings = swis.generateHeadings(self.waypoints) # Current headings
        distances = swis.generateDistances(self.waypoints) # Current distances
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
                    output += D * (heading - lastStep)
        
            forward = 1.0
            # Rotate whichever is smallest, the output value
            # or the maximum allowable rotation value
            rotate = max(min(rotationMax, output), -1*rotationMax)
            
            # Move the wheels at whichever speed is smallest, the output
            # value or the maximum allowable speed.
            leftVelocity = max(min((forward - rotate), motorMax), -1*motorMax)
            rightVelocity = max(min((forward + rotate), motorMax), -1*motorMax)

            setVelocity(leftVelocity, rightVelocity, i)

            # If the robot is close enough to a waypoint, iterate to the
            # next waypoint for that robot
            distance = distances[i]
            if distance < triggerDistance:
                # TODO add code to move to next waypoint
                pass

        self.lastSteps = headings
        time.sleep(0.05)

    # Uses pySerial to send left and right wheel velocity
    # commands to a given robot.
    def setVelocity(left, right, robot):
        pass
    
def main(self):
        pass

if __name__ == '__main__':
    main()
