import scratch, time, socket, serial, sys
import constants

class arrowkeys:

    def __init__(self):
        self.s = scratch.Scratch()
        self.port = constants.PORT_BTLE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', self.port))

    def listen(self):
        while 1:
            try:
                yield self.s.receive()
            except scratch.ScratchError:
                print "Error: Could not connect to scratch"
    
    def run(self):
        color = [255,0,0]
        for scratchMsg in self.listen():
            #print scratchMsg
            if scratchMsg[0] == 'broadcast':
                if scratchMsg[1] == 'move':
                    msg = "0,20,95,95"
                    self.sock.sendall(msg)
                    print "Moving forward for 5 seconds..."
                    time.sleep(5)
                    msg = "0,20,90,90"
                    self.sock.sendall(msg)
                    print "Stopping.\n"
            
                elif scratchMsg[1] == 'back':
                    msg = "0,20,85,85"
                    self.sock.sendall(msg)
                    print "Moving backwards for 5 seconds..."
                    time.sleep(5)
                    msg = "0,20,90,90"
                    self.sock.sendall(msg)
                    print "Stopping.\n"
            
                elif scratchMsg[1] == 'right':
                    msg = "0,20,95,85"
                    self.sock.sendall(msg)
                    print "Turning right for two seconds..."
                    time.sleep(2)
                    msg = "0,20,90,90"
                    self.sock.sendall(msg)
                    print "Stopping.\n"
            
                elif scratchMsg[1] == 'left':
                    msg = "0,20,85,95"
                    self.sock.sendall(msg)
                    print "Turning left for two seconds..."
                    time.sleep(2)
                    msg = "0,20,90,90"
                    self.sock.sendall(msg)
                    print "Stopping.\n"

                elif scratchMsg[1] == 'red':
                    msg = "0,10,255,0,0"
                    self.sock.sendall(msg)
                    print "Turning red\n"
                
                elif scratchMsg[1] == 'green':
                    msg = "0,10,0,255,0"
                    self.sock.sendall(msg)
                    print "Turning green\n"

                elif scratchMsg[1] == 'blue':
                    msg = "0,10,0,0,255"
                    self.sock.sendall(msg)
                    print "Turning blue\n"
                
                elif scratchMsg[1] == 'black':
                    msg = "0,10,0,0,0"
                    self.sock.sendall(msg)
                    print "Turning off LED\n"

                
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
