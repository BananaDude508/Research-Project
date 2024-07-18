###
### This is the primary script, which brings everything together
###

# www.youtube.com/watch?v=NBWMtlbbOag

import pygame
pygame.init()
from game import Game
from pendulum import Pendulum
from cart import Cart
from math import pi

def main() -> None:
    WIDTH = 700
    HEIGHT = 500
    TITLE = "Pendulum Simulation"

    GRAVITY = 9.81
    RESISTANCE = 0.99


    main_pendulum = Pendulum(100, pi/2, (WIDTH//2, HEIGHT//2), 100, GRAVITY, RESISTANCE)
    main_pendulum.create_child_clone()
    cart = Cart()
    game = Game(WIDTH, HEIGHT, TITLE, cart, main_pendulum) # Initialise the game and game window
    window = game.window # The display window that we will actually see running the MLA/player

    # We dont need to create any list for pendulums as they are "linked lists"
    # This means each one contains its child instead of one master containing all of them
    # It also means deleting one deletes all children from that point automatically

    FPS = 60
    clock = pygame.time.Clock()
    run = True
    while run:
        delta_time = clock.tick(FPS) / 1000 # Limit the framerate to something consistent
        for event in pygame.event.get():
                if event.type == pygame.QUIT: # If we close the window, the simulation and execution stops
                    run = False
                    break
        game.loop(delta_time) # Run one step of the physics simulation and draw results to the screen
        
        pygame.display.update() # Updates the screen to display the current frame


if __name__ == '__main__': # Only run if this is the executed program, 
    main()                 # and doesnt run if its imported into another script
    