###
### This script will manage the game window and contain the pendulums and cart
###


import pygame
pygame.init()
from pendulum import Pendulum
from cart import Cart


class Game:
    FONT = pygame.font.SysFont("comicsans", 50)
    BLACK = (0, 0, 0)
    BACKGROUND = BLACK

    def __init__(self, window_width:int, window_height:int, window_title:str, cart:Cart, pendulum:Pendulum) -> None:
        self.WIDTH = window_width # The width of the display window
        self.HEIGHT = window_height # The height of the display window
        self.window = self.init_window(window_width, window_height, window_title) # The display window
        self.cart = cart # The cart that will move around
        self.pendulum = pendulum # The pendulums that will be swinging

    def init_window(self, width:int, height:int, display_title:str) -> pygame.Surface:
        w = pygame.display.set_mode((width, height)) # Set resolution
        pygame.display.set_caption(display_title) # Set title
        return w # Returns the created window

    def draw(self) -> None:
        self.window.fill(self.BACKGROUND)
        self.cart.draw(self.window)
        self.pendulum.draw(self.window)
    
    def loop(self, delta_time) -> None:
        self.cart.loop(delta_time)
        self.pendulum.loop(delta_time)
        self.draw()