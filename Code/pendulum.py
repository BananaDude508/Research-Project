###
### This script will manage the physics simulations of the pendulum
###


import pygame
pygame.init()
from math import sin,cos,pi
from engine_math import clamped

class Pendulum:
    def __init__(self, radius:float, angle:float, origin:tuple[float,float], mass:float, gravity:float, resistance:float) -> None:
        self.origin_x = origin[0] # Positive, between 0 and screen width
        self.origin_y = origin[1] # Positive, between 0 and screen height
        self.radius = abs(radius) # Positive
        self.angle = angle # Positive or negative
        self.angular_velocity = 0 # Positive or negative
        self.angular_acceleration = 0 # Positive or negative
        self.mass = abs(mass) #  Positive
        self.gravity = gravity # Positive or negative, positiveve causes a downwards fall
        self.resistance = clamped(resistance,0,1) # Positive, between 0 and 1
        self.calculate_end_position()

    def draw(self, window, draw_child:bool=True) -> None: # Drawing the pendulum to the window
        pygame.draw.line(window, (0,255,255), (self.origin_x, self.origin_y), (self.x, self.y), 5)
        pygame.draw.circle(window, (255,255,0), (self.x, self.y), 10)

    def calculate_end_position(self) -> None:
        self.x = self.origin_x + self.radius*sin(self.angle)
        self.y = self.origin_y + self.radius*cos(self.angle)

    def loop(self, delta_time, loop_child:bool=True) -> None:
        force = -1 * self.mass * self.gravity * sin(self.angle) / self.radius # Calculate acceleration
        self.angular_acceleration = force

        self.angular_velocity += self.angular_acceleration * delta_time # Calculate velocity
        self.angular_velocity *= self.resistance                        #

        old_angle = self.angle

        self.angle += self.angular_velocity * delta_time # Calculate angle

        self.calculate_end_position()
    
    def move_parent(self, new_pos:tuple[float,float]) -> None:
        old_x = self.origin_x
        old_y = self.origin_y
        new_x = new_pos[0]
        new_y = new_pos[1]
        self.origin_x = new_x
        self.origin_y = new_y