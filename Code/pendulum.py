###
### This script will manage the physics simulations of the pendulum
###


import pygame
pygame.init()
from numpy import sin,cos,pi
from engine_math import clamped

class Pendulum:
    def __init__(self, radius:float, draw_radius:float, angle:float, origin:tuple[float,float], mass:float, gravity:float, resistance:float) -> None:
        self.origin_x = origin[0] # Positive, between 0 and screen width
        self.origin_y = origin[1] # Positive, between 0 and screen height
        self.origin_vel = 0 # Positive or negative, parent velocity X ONLY
        self.origin_accel = 0 # Positive or negative, parent acceleration X ONLY
        self.radius = abs(radius) # Positive, the radius that will be calculated
        self.draw_radius = abs(draw_radius) # Positive, the radius that will be drawn to the screen
        self.angle = angle # Positive or negative
        self.angular_velocity = 0 # Positive or negative
        self.angular_acceleration = 0 # Positive or negative
        self.mass = abs(mass) #  Positive
        self.gravity = gravity # Positive or negative, positiveve causes a downwards fall
        self.resistance = resistance # Positive
        self.calculate_end_position()

    def draw(self, window) -> None: # Drawing the pendulum to the window
        pygame.draw.line(window, (0,255,255), (self.origin_x, self.origin_y), (self.x, self.y), 5)
        pygame.draw.circle(window, (255,255,0), (self.x, self.y), 10)

    def calculate_end_position(self) -> None:
        self.x = self.origin_x + self.draw_radius*sin(self.angle)
        self.y = self.origin_y + self.draw_radius*cos(self.angle)

    def loop(self, delta_time) -> None:
        '''OLD METHOD, NO CART MOVEMENT (The Coding Train)

        #force = -1 * self.mass * self.gravity * sin(self.angle) / self.radius # Calculate acceleration
        #self.angular_acceleration = force

        #self.angular_velocity += self.angular_acceleration * delta_time # Calculate velocity
        #self.angular_velocity *= self.resistance                        #


        #self.angle += self.angular_velocity * delta_time # Calculate angle

       # self.calculate_end_position()
       '''


        ### TODO:
        ### - Figure out why pendulum sometimes stutters and doesnt move, then fix it
        ### -- Spinning right, cart moves right to push it to the left, pendulum moves right instead of changing to left???
        ### --- Not just when spinning right, and similar issues sometimes appear

        '''NEW METHOD, CART X MOVEMENT (myPhysicsLab)'''
        # I split it up into single letter vars that myPhysicsLab uses for ease of copying down
        R = self.radius
        b = self.resistance
        m = self.mass
        g = self.gravity
        x0dd = self.origin_accel # dd meaning double derivative (change in velocity over time)
        y0dd = 0
        theta = self.angle
        thetad = self.angular_velocity # d meaning derivative (change in angle over time)

        # The 4 components here are summed to find acceleration
        sum1 = (cos(theta)/R)*x0dd
        # sum2 = (cos(theta)/R)*y0dd
        sum2 = 0 # Sum 2 calculation always results in 0, because the cart should never move in Y position
        sum3 = (b/(m*R*R))*thetad
        sum4 = (g/R)*sin(theta)

        self.angular_acceleration = -sum1-sum2-sum3-sum4 
        
        -(cos(theta)/R)*x0dd-(b/(m*R*R))*thetad-(g/R)*sin(theta)
        
        self.angular_velocity += self.angular_acceleration * delta_time # Calculate velocity

        self.angle += self.angular_velocity # Calculate angle

        self.calculate_end_position()
    
    def move_cart_parent(self, new_cart_pos:float, cart_speed:float, cart_accel:float) -> None:
        self.origin_x = new_cart_pos
        self.origin_vel = cart_speed
        self.origin_accel = cart_accel

    # A debug function to draw forces like gravity and velocity to the simulation so we can view
    def draw_forces(self, window, gravity:bool=True, velocity:bool=True) -> None:
        force_color = (255,255,255)
        end_pos = (self.x, self.y)
        draw_scalar = 10
        if gravity:  pygame.draw.line(window, force_color, end_pos, (self.x, self.y + draw_scalar*self.gravity), 2)
        if velocity: pygame.draw.line(window, force_color, end_pos, (self.x + draw_scalar*(self.angular_velocity*cos(self.angle)), self.y - draw_scalar*(self.angular_velocity*sin(self.angle))), 2)


