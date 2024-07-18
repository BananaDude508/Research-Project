###
### This is the primary script, which brings everything together
###


import pygame
pygame.init()
from game import Game
from pendulum import Pendulum
from cart import Cart


def main():
    WIDTH = 700
    HEIGHT = 500
    TITLE = "Pendulum Simulation"
    cart = Cart()
    pendulums = [Pendulum()] # We use a list incase we want to try using more than 1 linked pendulums
    game = Game(WIDTH, HEIGHT, TITLE, cart, pendulums) # Initialise the game and game window
    window = game.window # The display window that we will actually see running the MLA

    gravity = -9.81  # Some other information related to the simulation
    resistance = 0.1

    FPS = 60
    clock = pygame.time.Clock()
    run = True
    while run:
        delta_time = clock.tick(FPS) / 1000 # Limit the framerate to something consistent
        for event in pygame.event.get():
                if event.type == pygame.QUIT: # If we close the window, the simulation and execution stops
                    run = False
                    break
        
        pygame.display.update() # Updates the screen to display the current frame


if __name__ == '__main__': # Only run if this is the executed program, 
    main()                 # and doesnt run if its imported into another script
    