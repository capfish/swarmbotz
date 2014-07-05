import swisclient_wp as swisclient
import time, sys, serial, socket
import constants

class swarm:    

    def __init__(self):
        #self.ser = serial.Serial("/dev/ttyUSB0", 9600)
        self.host = constants.HOST_BTLE
        self.port = constants.PORT_BTLE 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swis = swisclient.SwisClient()
        self.NUM_ROBOTS = constants.NUM_ROBOTS
        
        self.sock.connect((self.host,self.port))

        print "__INIT__"
    # Close the serial connection
    def closeSerial(self):
        time.sleep(1)
    #    self.ser.close()

    def write(self, string):
        pass

    def closeSocket(self):
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

    def setVelocity(self, left, right, robot):
        message = '0, ', left, right
        print message
        self.sock.sendall(message)
    
def main():
#        s = swarm()
#        bots = s.NUM_ROBOTS
    PORT = int(sys.argv[1])
    while 1:
        try:
            s.step()
        except (KeyboardInterrupt):
            print "Exiting program, stopping robots"
            for i in range (0, bots):
                s.setVelocity(0,90,90)
            #s.closeSerial()
            s.closeSocket()
            sys.exit()

if __name__ == '__main__':
    s = swarm()
    bots = s.NUM_ROBOTS
    main()
