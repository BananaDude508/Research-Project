###
### This is the primary script, which brings everything together
###


# 19th July: www.youtube.com/watch?v=NBWMtlbbOag
## The Coding Train: "Coding Challenge #159: Simple Pendulum Simulation" (youtube)
## The ground work for the initial functionality and some derivation of the physics simulation

# 19th July: https://www.youtube.com/watch?v=EvV5Qtp_fYg&t
## Pezzza's Work: "How to train simple AIs" (youtube)
## How an ai can be trained, although example given in an almost identical usecase to mine so may not use this as a reference


import pygame
pygame.init()
from game import Game
from pendulum import Pendulum
from cart import Cart
from math import pi

def main() -> None:
    WIDTH = 700
    HEIGHT = 500
    MIDPOINT = (WIDTH//2, HEIGHT//2)
    TITLE = "Pendulum Simulation"

    GRAVITY = 9.81
    PENDULUM_RESISTANCE = 0.99

    CART_ACCEL = 2500
    CART_FRICTION = 0.1


    pendulum = Pendulum(100, pi/2, MIDPOINT, 100, GRAVITY, PENDULUM_RESISTANCE)
    cart = Cart(MIDPOINT, CART_ACCEL, CART_FRICTION, pendulum)
    game = Game(WIDTH, HEIGHT, TITLE, cart, pendulum) # Initialise the game and game window
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

        cart_move_dir = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            cart_move_dir = -1
        elif keys[pygame.K_d]:
            cart_move_dir = 1
                


        game.loop(delta_time, cart_move_dir) # Run one step of the physics simulation and draw results to the screen
        
        pygame.display.update() # Updates the screen to display the current frame


if __name__ == '__main__': # Only run if this is the executed program, 
    main()                 # and doesnt run if its imported into another script
    