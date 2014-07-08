import pygame
import time
import sys
import numpy
from circle import Circle
from lemniscate import Lemniscate
from scipy.integrate import quad
from scipy.optimize import fsolve
from math import cos, sin, sqrt, pi, atan2
from itertools import *
from pygame.locals import *

swarmbots = [1]#,2,3,4,5,6,7]
# robotPositions = [(10,20)]

def arcFragment(t, arc, length):
    return quad(arc, 0, t)[0] - length

def fragmentPoint(integrand, fragLength):
    return fsolve(arcFragment, 0.0, (integrand, fragLength))[0]

tupleAdd = lambda xs,ys: tuple(x + y for x, y in izip(xs,ys))

def triangleVertices(centerPoint, rotation):
    a = tupleAdd(centerPoint, (5*cos(rotation+pi/3),5*sin(rotation+pi/3)))
    b = tupleAdd(centerPoint, (5*cos(rotation-pi/3),5*sin(rotation-pi/3)))
    c = tupleAdd(centerPoint, (15*cos(rotation),15*sin(rotation)))
    return (a,b,c)

#formation = Lemniscate(150,300,200)
formation = Circle(100,300,200)
pathResolution = 10
discretePath = []
for i in xrange(0,pathResolution):
    discretePath.append(fragmentPoint(formation.arcIntegrand, i*formation.arcLength(0,2*pi)/pathResolution))
    discretePath[i] = formation.path(discretePath[i])
print discretePath
headings = []
for i in xrange(0,len(discretePath)):
    x1 = discretePath[i][0]
    y1 = discretePath[i][1]
    x2 = discretePath[(i+1)%len(discretePath)][0]
    y2 = discretePath[(i+1)%len(discretePath)][1]
    headings.append(atan2(y2-y1,x2-x1))

divisionPoints = []
for i in xrange(0,len(swarmbots)):
    divisionPoints.append(fragmentPoint(formation.arcIntegrand, i*formation.arcLength(0,2*pi)/len(swarmbots)))
    divisionPoints[i] = formation.path(divisionPoints[i])

robotPositions = list(divisionPoints)
robotPosOnPath = []
for i in xrange(0,len(swarmbots)):
    robotPosOnPath.append((discretePath.index(robotPositions[i])+1)%len(discretePath))

pygame.init()
fpsClock = pygame.time.Clock()
mainWindow = pygame.display.set_mode((640,480))

while True:
    #for i in xrange(0,len(path)):
    mainWindow.fill(pygame.Color(255,255,255))
    for i in xrange(0,len(swarmbots)):
        robotPosOnPath[i] = (robotPosOnPath[i]+1)%len(discretePath)
        #pygame.draw.circle(mainWindow, (0,255,0), discretePath[robotPosOnPath[i]], 10, 0)
        pygame.draw.polygon(mainWindow, (0,255,0), triangleVertices(discretePath[robotPosOnPath[i]], headings[robotPosOnPath[i]]))
    #this listens for closing signals
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
        
    pygame.display.update()
    fpsClock.tick(30)
