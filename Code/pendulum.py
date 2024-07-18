###
### This script will manage the physics simulations of the pendulum
###


import pygame
pygame.init()
from math import sin,cos,pi

class Pendulum:
    def __init__(self, radius:float, angle:float, origin:tuple[int,int]) -> None:
        self.origin_x = origin[0]
        self.origin_y = origin[1]
        self.radius = radius
        self.angle = angle
    
    def draw(self, window) -> None:
        pygame.draw.line(window, (0,0,255), (self.origin_x, self.origin_y), (self.x, self.y), 2)
        pygame.draw.circle(window, (255,0,0), (self.x, self.y), 5)

    def loop(self, delta_time) -> None:
        self.angle += 2*pi * delta_time
        self.x = self.origin_x + self.radius*sin(self.angle)
        self.y = self.origin_y + self.radius*cos(self.angle)