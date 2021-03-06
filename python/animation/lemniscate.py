from scipy.integrate import quad
from scipy.optimize import fsolve
from math import cos, sin, sqrt, pi

class Lemniscate:
    a = 120
    def __init__(self,a,centerx,centery):
        self.a = a
        self.centerx = centerx
        self.centery = centery

    def path(self, t):
        x = int(self.a*sqrt(2)*cos(t)/(sin(t)*sin(t)+1)) + self.centerx
        y = int(self.a*sqrt(2)*cos(t)*sin(t)/(sin(t)*sin(t)+1)) + self.centery
        return (x,y)

    def arcIntegrand(self, t):
        dx = -(2*sqrt(2)*self.a*sin(t)*(cos(2*t)+5))/(cos(2*t)-3)**2
        dy = self.a*(3*cos(2*t)-1)/(sqrt(2)*(sin(t)*sin(t)+1)**2)
        return sqrt(dx*dx+dy*dy)

    def arcLength(self, lowerLimit, upperLimit):
        return quad(self.arcIntegrand, lowerLimit, upperLimit)[0]
