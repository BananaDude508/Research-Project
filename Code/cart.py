import pygame
pygame.init()
from engine_math import clamped
from pendulum import Pendulum

class Cart:
    WHITE = (255,255,255)
    RED = (255,0,0)

    def __init__(self, position: tuple[float,float], acceleration:float, friction:float, child_pendulum:Pendulum) -> None:
        self.x = position[0] # Positive, between 0 and screen width
        self.y = position[1] # Positive, between 0 and screen height
        self.acceleration = abs(acceleration) # Positive
        self.friction = clamped(friction,0,1) # Positive, between 0 and 1
        self.speed = 0 # Positive or negative
        self.child_pendulum = child_pendulum # Pendulum attatched to the cart
    
    def draw(self, window, draw_rail, screen_width) -> None:
        if draw_rail:
            pygame.draw.line(window,
                             self.WHITE,
                             (0,self.y+25),
                             (screen_width,self.y+25),
                             5)
        
        pygame.draw.circle(window,
                            self.RED,
                            (self.x-25, self.y+20),
                            10)
        pygame.draw.circle(window,
                            self.RED,
                            (self.x+25, self.y+20),
                            10)
        pygame.draw.polygon(window,
                            self.RED,
                            ((self.x+25, self.y+25),
                            (self.x-25, self.y+25),
                            (self.x-20, self.y),
                            (self.x+20, self.y)))

    def loop(self, delta_time, move_dir, limit_to_screen, screen_width, pendulum_draw_radius) -> None:
        move_dir = clamped(move_dir,-1,1) # Make sure that move_dir is between 0 and 1, so we cant exceed the normal acceleration
        
        old_speed = self.speed
        
        self.speed += self.acceleration * move_dir * delta_time
        self.speed *= 1 - self.friction

        self.x += self.speed * delta_time
        
        if limit_to_screen:
            if self.x > screen_width - pendulum_draw_radius:
                self.speed = 0
                self.x = screen_width - pendulum_draw_radius
            if self.x < pendulum_draw_radius:
                self.speed = 0
                self.x = pendulum_draw_radius

        self.child_pendulum.move_cart_parent(self.x, self.speed, self.speed - old_speed)

