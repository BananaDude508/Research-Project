###
### This script will manage the physics simulations of the pendulum
###


import pygame
pygame.init()
from math import sin,cos,pi

class Pendulum:
    def __init__(self, radius:float, angle:float, origin:tuple[float,float], mass:float, gravity:float, resistance:float) -> None:
        self.origin_x = origin[0] # Positive, between 0 and screen width
        self.origin_y = origin[1] # Positive, between 0 and screen height
        self.radius = radius # Positive
        self.angle = angle # Positive or negative
        self.angular_velocity = 0 # Positive or negative
        self.angular_acceleration = 0 # Positive or negative
        self.mass = mass #  Positive
        self.gravity = gravity # Positive or negative, positiveve causes a downwards fall
        self.resistance = resistance # Positive, between 0 and 1
        self.calculate_end_position()

        self.child = None
    
    def create_child(self, radius:float, angle:float, mass:float, resistance:float): # Creates a child as a linked list
        self.child = Pendulum(radius, angle, (self.x, self.y), mass, self.gravity, resistance)
        return self.child

    def create_child_clone(self): # Creates a child as a linked list
        self.child = Pendulum(self.radius, self.angle, (self.x, self.y), self.mass, self.gravity, self.resistance)
        return self.child

    def draw(self, window, draw_child:bool=True) -> None: # Drawing the pendulum to the window
        pygame.draw.line(window, (0,0,255), (self.origin_x, self.origin_y), (self.x, self.y), 2)
        pygame.draw.circle(window, (255,0,0), (self.x, self.y), 5)

        if self.child is not None and draw_child: 
            self.child.draw(window, True)

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

        if self.child is not None and loop_child:
            self.child.origin_x = self.x
            self.child.origin_y = self.y

            angle_sum = old_angle + self.child.angle

            self.child.angle = angle_sum - self.angle

            self.child.loop(delta_time, True)