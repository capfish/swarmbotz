import socket
import math

class SwisClient:
    
    def __init__(self):
        self.NUM_ROBOTS = 1
        self.host = 'localhost'
        self.port = 3000
       
    def readData(self):
        while 1:
            print 'New Frame'
            sock = socket.socket()
            sock.connect((self.host,self.port))
            data = sock.recv(1024)
            particles = []
            dataPacket = True
            while dataPacket:
                data = sock.recv(1024)
                if 'PARTICLE' in data:
                    particles.append(data)
#                    print data
                if 'STEP_STOP' in data:
                    dataPacket = False
            sock.close()
            for p in particles:
                result = p.split(',')
#                print 'Particle ID = ', result[1], ', X = ', result[2], ', Y = ', result[3], ', theta = ', result[4]
            return particles


    # Generates a list of headings for each robot to their given waypoint
    def generateHeadings(self, waypoints):
        points = waypoints.split(" : ")
#        particles = self.readData()
        particles = ["0,0,70,70,3.142"] # For testing
        headings = []
        for i in xrange(0, self.NUM_ROBOTS):
           # print particles
           # print points
            p = particles[i].split(",")
            w = points[i].split(",")
            x1 = p[2]
            y1 = p[3]
            angle = p[4]
            x2 = w[0]
            y2 = w[1]

            h = self.headingTo(x1, y1, x2, y2, angle)
            headings.append(h)
        print headings
        return headings
    
    def generateDistances(self, waypoints):
        #particles = self.readData()
        particles = ["0,0,70,70,3.142"]
        points = waypoints.split(" : ")
        distances = []
        for i in xrange(0, self.NUM_ROBOTS):
            p = particles[i].split(",")
            w = points[i].split(",")
            x1 = float(p[2])
            y1 = float(p[3])
            x2 = float(w[0])
            y2 = float(w[1])
            dist = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
            distances.append(dist)
        print distances
        return distances

    # Returns the heading from a robot to a waypoint.
    # x1, y1, and theta are the position and absolute angle
    # of the robot, x2 and y2 are the waypoint.
    def headingTo(self, x1, y1, x2, y2, angle):
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        angle = float(angle)
        alpha = math.atan2(y2-y1, x2-x1)
        theta = angle - alpha
        return theta
        
def main():
    client = Swisclient()
    client.readData()

if __name__ == '__main__':
    main()
