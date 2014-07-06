import swisclient_wp as swisclient
import time, sys, serial, socket
import constants

class swarm:    

    def __init__(self, numbots, port):
        #self.ser = serial.Serial("/dev/ttyUSB0", 9600)
        self.host = constants.HOST_BTLE
        self.port = port 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.swis = swisclient.SwisClient()
        self.NUM_ROBOTS = numbots 
        
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
            self.sock.send(message)

    def setVelocity(self, robot, left, right):
        message = '0, '+ str(left) + ', ' + str(right)
        print message
        self.sock.send(message)
    
def main():
    s = swarm(constants.NUM_ROBOTS, constants.PORT_BTLE)
    while 1:
        try:
            s.step()
            time.sleep(1)
        except (socket.error, KeyboardInterrupt):
            print "Exiting program, stopping robots"
            for i in range (0, constants.NUM_ROBOTS):
                s.setVelocity(0,90,90)
            #s.closeSerial()
            s.closeSocket()
            sys.exit()

if __name__ == '__main__':
    main()
