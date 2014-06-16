from scipy.integrate import quad
from scipy.optimize import fsolve
from math import cos, sin, sqrt, pi

class Circle:
    radius = 10
    def __init__(self,radius,centerx,centery):
        self.radius = radius
        self.centerx = centerx
        self.centery = centery

    def path(self, t):
        x = int(self.radius*cos(t) + self.centerx)
        y = int(self.radius*sin(t) + self.centery)
        return (x,y)

    def arcIntegrand(self, t):
        dx = -self.radius*sin(t)
        dy = self.radius*cos(t)
        return sqrt(dx*dx+dy*dy)

    def arcLength(self, lowerLimit, upperLimit):
        return quad(self.arcIntegrand, lowerLimit, upperLimit)[0]
