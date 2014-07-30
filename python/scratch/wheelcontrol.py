import scratch, time, socket, serial, sys
import constants

class arrowkeys:

    def __init__(self):
        self.s = scratch.Scratch()
        self.port = constants.PORT_BTLE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', self.port))

    def listen(self):
        print "Listening for commands..."
        while 1:
            try:
                yield self.s.receive()
            except scratch.ScratchError:
                print "Error: Could not connect to scratch"
            
    
    def run(self):
        leftVelocity = 0
        rightVelocity = 0
        leftServo = 0
        rightServo = 0
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0,0,0)] # Red, Green, Blue, off


        for scratchMsg in self.listen():
            #print scratchMsg
            if scratchMsg[0] == 'sensor-update':
                command = scratchMsg[1]
 
                if 'leftwheel' in command:
                    leftVelocity = int(command.get('leftwheel'))
                if 'rightwheel' in command:
                    rightVelocity = int(command.get('rightwheel'))
                if 'color' in command:
                    c = int(command.get('color'))%4


            # Servos stand still when they are at a value of 90
            # The max(min( makes sure that the speed is between -10 and 10
            leftServo = 90 + max(min(leftVelocity, 10), -10) 
            rightServo = 90 + max(min((rightVelocity), 10), -10)

            #print leftVelocity, rightVelocity

            speedMsg = '0,20,' + str(leftServo) + ',' + str(rightServo)
            colorMsg = '0,10,' + str(colors[c][0]) + ',' + str(colors[c][1]) + ',' + str(colors[c][2])
            self.sock.sendall(speedMsg)
            time.sleep(0.01)
            self.sock.sendall(colorMsg)
                
    def close(self):
        self.s.disconnect()

def main():
    #while 1:
        try:
            arrow.run()
        except (KeyboardInterrupt):
            arrow.close()
            sys.exit()
    

if __name__ == '__main__':
    arrow = arrowkeys()
    main()
