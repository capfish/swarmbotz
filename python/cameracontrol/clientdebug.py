import swisclient_wp as swisclient
import time, sys, serial, socket

class swarm:    

    def __init__(self):
        #self.ser = serial.Serial("/dev/ttyUSB0", 9600)
        self.port = 5027
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swis = swisclient.SwisClient()
        self.NUM_ROBOTS = self.swis.NUM_ROBOTS
        
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


    # Uses a PD loop to generate velocity for each robot,
    # given a list of waypoints.
    def step(self):
        message = ""

        # Go through each robot and update its velocity
        # TODO add functionality to move to next waypoint
        for i in range(0, self.NUM_ROBOTS):
            #message = "0," + str(leftVelocity) + "," + str(rightVelocity)
            message = "0,90,90"
            print message
            self.sock.sendall(message)

        self.lastHeadings = headings
        print message
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
