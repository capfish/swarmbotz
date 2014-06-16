import socket
import sys

class Swisclient:
    
    host = 'localhost'
    port = 3000

    def __init__(self):
        pass
       
    def printData(self):
        while 1:
            print 'Particles:'
            sock = socket.socket()
            sock.connect((self.host,self.port))
            data = sock.recv(1024)
            particles = []
            dataPacket = True
            while dataPacket:
                data = sock.recv(1024)
                if 'PARTICLE' in data:
                    particles.append(data)
                if 'STEP_STOP' in data:
                    dataPacket = False
            sock.close()
            print particles

def main():
    client = Swisclient()
    client.printData()

if __name__ == '__main__':
    main()
