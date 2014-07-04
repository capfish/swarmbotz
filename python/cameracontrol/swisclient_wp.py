import socket
import math

class SwisClient:
    
    def __init__(self):
        self.NUM_ROBOTS = 1
        self.host = 'localhost'
        self.port = 3000
        self.particlesBuffer = ["0,0,0,0,0"]
        self.ids = [1]
        self.initialized = False
#        print self.particlesBuffer[0]
    def readData(self):
#        while 1:
#            print 'New Frame'
            sock = socket.socket()
            sock.connect((self.host,self.port))
            #data = sock.recv(1024)
#            print data
            particles = []
            dataPacket = True
            while dataPacket:
                data = sock.recv(1024)
                print data
                if 'PARTICLE' in data and not 'FRAMENUMBER' in data:
                    particles.append(data)
#                    print data
                if 'STEP_STOP' in data:
                    dataPacket = False
            sock.close()
#            for p in particles:
#                result = p.split(',')
#                print 'Particle ID = ', result[1], ', X = ', result[2], ', Y = ', result[3], ', theta = ', result[4]
#            print particles
            return particles


    # Generates a list of headings for each robot to their given waypoint
    def generateHeadings(self, waypoints):
        numBotsInitialized = 0
        points = waypoints
        rawParticles = self.readData()
        particles = sorted(rawParticles, key=lambda idsort: idsort[1])
#        print 'length', len(particles)
#        print self.initialized
        print "particles, ", len(particles)
        if len(particles) < self.NUM_ROBOTS and self.initialized == False:
            return None, None

        if len(particles) == self.NUM_ROBOTS and self.initialized == False:
            for i in xrange(self.NUM_ROBOTS):
                p = particles[i].split(",")
                if int(p[1]) > 0:
                    self.ids[i] = p[1]
                    numBotsInitialized = numBotsInitialized + 1
                #print " ids ", len(self.ids)
            #self.ids.sort()
#            return None, None
        #if len(particles) == self.NUM_ROBOTS:
            #print " ids ", len(self.ids)
            if numBotsInitialized == self.NUM_ROBOTS:
                self.initialized = True
            return None, None
#            print "TRUE"
        
        

        if self.initialized == True:
#        print particles
#        particles = ["0,0,70,70,3.142"] # For testing
            headings = []
            sortedHeadings = []
            idents = []
            ident = 0
            print "headings"
            for i in xrange(0, self.NUM_ROBOTS):
#            print i
           # print particles
           # print points
                w = points
                pastP = self.particlesBuffer[i].split(",")
                if len(particles) > i:                
                    p = particles[i].split(",")
                #pastP = self.particlesBuffer[i].split(",")
                #print " i ", i
                    ident = int(p[1])
                    x1 = p[2]
                    y1 = p[3]
                    angle = p[4]
                    pastIdent = int(self.ids[i])
#                print pastIdent
                    if ident not in self.ids:
                        idx, dist = self.findNearestMatch(x1, y1)
                    #                    print idx
                        ident = int(self.ids[idx])
                    #print ident
                        
                else:
                #pastP = self.particlesBuffer[i].split(",")
                #print "past : ", pastP
                    #ident = int(self.ids[i])
                    x1 = pastP[2]
                    y1 = pastP[3]
                    angle = pastP[4]
                    idx, dist = self.findNearestMatch(x1, y1)
                    ident = int(self.ids[idx])
                x2 = w[0]
                y2 = w[1]
                h = self.headingTo(x1, y1, x2, y2, angle)
                print ident
                if ident in idents:
                    print "Duplicate found"
#                    return None, None
                idents.append(ident)
                headings.append((ident,h))
#        print 'headings = ',  headings
#            def find_duplicates(seq):
 #               seen = set()
 #               seen_add = seen.add
 #               seen_twice = set( x for x in seq if x in seen or seen_add(x) )
 #               if len(seen_twice) > 0:
 #                   return True
 #           if find_duplicates(headings):
 #               return None, None
            sortedHeadings = sorted(headings, key=lambda idsort: idsort[0])
#        print 'Sorted headings = ', sortedHeadings
        #print particles
        #particles = ["0,0,70,70,3.142"]
            distances = []
            sortedDistances = []
            print "distances"
            for j in xrange(0, self.NUM_ROBOTS):
            #print j
                w = points
                pastP = self.particlesBuffer[j].split(",")
                if len(particles) > j:
                    p = particles[j].split(",")
                    ident = int(p[1])
                    x1 = float(p[2])
                    y1 = float(p[3])
                    pastIdent = int(self.ids[j])
                    if ident not in self.ids:
                        idx, dist = self.findNearestMatch(x1,y1)
                        ident = int(self.ids[idx])
                else:
            #    pastP = self.particlesBuffer[j].split(",")
                    #ident = int(self.ids[j])
                    x1 = float(pastP[2])
                    y1 = float(pastP[3])
                    idx, dist =self.findNearestMatch(x1, y1)
                    ident = int(self.ids[idx])
                x2 = float(w[0])
                y2 = float(w[1])
                dist = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
#                print ident
                distances.append((ident,dist))

            if len(particles) == self.NUM_ROBOTS:
                self.particlesBuffer = particles
#        
            
            #print 'distances = ', distances
            sortedDistances = sorted(distances, key=lambda idsort: idsort[0])
#        print 'sorted distances = ', sortedDistances
        
        return sortedDistances, sortedHeadings

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

    def distanceTo(self, x1, y1, x2, y2):
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        distance = math.sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))
        return distance

    def findNearestMatch(self, x1, y1):
        index = 0
        pastP = self.particlesBuffer[0].split(",")
        x1 = float(x1)
        y1 = float(y1)
        x2 = float(pastP[2])
        y2 = float(pastP[3])
        #print "x2, y2, ", x2, y2
        distance = self.distanceTo(x1, y1, x2, y2)
        for i in xrange(1, self.NUM_ROBOTS):
            pastP = self.particlesBuffer[i].split(",")
            x2 = float(pastP[2])
            y2 = float(pastP[3])
        #    print "x2, y2, ", x2, y2
            d = self.distanceTo(x1, y1, x2, y2)
            #print d
            if d < distance:
                distance = d
                index = i
        #print "nearest match", index, distance, x1, y1, x2, y2
        return index, distance
            
        
def main():
#    client = Swisclient()
#    client.readData()
    pass
if __name__ == '__main__':
    main()
