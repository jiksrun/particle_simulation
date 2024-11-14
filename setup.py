import pygame

class Setup:
    def __init__(self):
        self.SCREEN_WIDTH = 800 
        self.SCREEN_HEIGHT = 600
        self.scale = 0.5
        self.particles_surface = pygame.Surface((self.SCREEN_WIDTH/self.scale, self.SCREEN_HEIGHT/self.scale), pygame.SRCALPHA)
        self.WIN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Particle Swarm Optimization")

class Color:
    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        self.ORANGE= (255, 165, 0)
        self.GREY = (128, 128, 128)
        self.TURQUOISE = (64, 224, 208)


