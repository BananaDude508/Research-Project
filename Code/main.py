import pygame
pygame.init()
from game import Game
from pendulum import Pendulum
from cart import Cart
from math import pi
from engine_math import *
import neat
import pickle
import time
import sys

def read_from_pickle(path):
    with open(path, 'rb') as file:
        try:
            while True:
                yield pickle.load(file)
        except EOFError:
            pass

def eval_genomes(genomes, config) -> None:
    WIDTH = 700
    HEIGHT = 500
    MIDPOINT = (WIDTH//2, HEIGHT//2)
    TITLE = "Pendulum Simulation"

    GRAVITY = 10

    PENDULUM_RADIUS = 100
    PENDULUM_DRAW_RADIUS = 100
    PENDULUM_RESISTANCE = 100000
    PENDULUM_MASS = 150

    CART_ACCEL = 2500
    CART_FRICTION = 0.1
    
    FPS = 60
    clock = pygame.time.Clock()

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        pendulum = Pendulum(PENDULUM_RADIUS, PENDULUM_DRAW_RADIUS, 0, MIDPOINT, PENDULUM_MASS, GRAVITY, PENDULUM_RESISTANCE)
        cart = Cart(MIDPOINT, CART_ACCEL, CART_FRICTION, pendulum)
        game = Game(WIDTH, HEIGHT, TITLE, cart, pendulum, False)
        
        genome.fitness = 0

        run = True
        time_elapsed = 0
        timeout = 3

        while run and time_elapsed <= 10:
            delta_time = clock.tick(FPS) / 1000 # Limit the framerate to something consistent
            """
            for event in pygame.event.get():
                    if event.type == pygame.QUIT: # If we close the window, the simulation and execution stops
                        run = False
                        break
            """
            inputs = [
                pendulum.angle,
                pendulum.angular_velocity,
                cart.x,
                cart.speed,
                cart.acceleration
            ]
            
            output = net.activate(inputs)
            cart_move_dir = (output[0]-5)/10  # Neural network output
            #print(cart_move_dir)

            game.loop(delta_time, cart_move_dir, draw=False) # Run one step of the physics simulation and draw results to the screen

            genome.fitness += 1.0 - abs(pendulum.angle) / pi  # Angle closer to 0 is better
            
            if abs(pendulum.angle) < pi / 2:
                timeout -= delta_time
                if timeout <= 0:
                    run = False
                    genome.fitness -= 100
            else:
                timeout = clamped(timeout + delta_time, 0, 3)
            
            time_elapsed += delta_time
            
            # pygame.display.update() # Updates the screen to display the current frame

def run_neat(config_path):
    population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-367')
    # population = neat.Population(config)
    
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )


    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(1))

    winner = population.run(eval_genomes, 1)

    return winner

if __name__ == '__main__':
    config_path = "../Research-Project/Code/config-feedforward.txt"
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    
    f = open('output.txt', 'w')

    sysoldout = sys.stdout
    sys.stdout = f
    
    print(f"Start time: {time.asctime()}")
    start_time = time.time()

    winner = run_neat(config_path)

    print("\nBest genome:\n{!s}".format(winner))
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    
    end_time = time.time() - start_time
    print(f"End time: {time.asctime()} ({end_time} total seconds)")
    
    sys.stdout = sysoldout
    f.close()
    
    WIDTH = 700
    HEIGHT = 500
    MIDPOINT = (WIDTH//2, HEIGHT//2)
    TITLE = "Pendulum Simulation"

    GRAVITY = 10

    PENDULUM_RADIUS = 100
    PENDULUM_DRAW_RADIUS = 100
    PENDULUM_RESISTANCE = 100000
    PENDULUM_MASS = 150

    CART_ACCEL = 2500
    CART_FRICTION = 0.1
    
    FPS = 60
    clock = pygame.time.Clock()
    
    pendulum = Pendulum(PENDULUM_RADIUS, PENDULUM_DRAW_RADIUS, 0, MIDPOINT, PENDULUM_MASS, GRAVITY, PENDULUM_RESISTANCE)
    cart = Cart(MIDPOINT, CART_ACCEL, CART_FRICTION, pendulum)
    game = Game(WIDTH, HEIGHT, TITLE, cart, pendulum, True)
        
    run = True
    clock = pygame.time.Clock()
    
    while run:
        delta_time = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        inputs = [
                pendulum.angle,
                pendulum.angular_velocity,
                cart.x,
                cart.speed,
                cart.acceleration
            ]
        output = net.activate(inputs)
        cart_move_dir = (output[0]-5)/10
        print(cart_move_dir)

        game.loop(delta_time, cart_move_dir, draw=True)
        pygame.display.update()
