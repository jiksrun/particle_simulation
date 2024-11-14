import numpy as np
import pygame
from setup import Setup 

# TODO: optimize it to be able to use 100k particles

class Particles:
    windows = Setup()
    def __init__(self, num_particles=20000): 
        np.random.seed(42)
        self.num_particles = num_particles
        self.particles_pos, self.particles_v = self._makeParticles()
        # particles' parameter
        self.pBest = self.particles_pos.copy()
        self.gBest = np.zeros((1, 2), dtype=np.int16)
        self.c1 = np.abs(np.random.normal(0, 0.001, 1)).astype(np.float32)
        self.c2 = np.abs(np.random.normal(0, 0.001, 1)).astype(np.float32)
        self.r1 = np.random.random((self.num_particles, 1)).astype(np.float32)
        self.r2 = np.random.random((self.num_particles, 1)).astype(np.float32)


    def _makeParticles(self):
        rects_pos = np.random.randint(0, self.windows.SCREEN_WIDTH, (self.num_particles, 2))
        rects_v = np.random.randn(self.num_particles, 2)
        return rects_pos.astype(np.int16), rects_v.astype(np.float32)
    
    def drawParticles(self, windows, windows_color, color):
        # clear surface
        windows.particles_surface.fill(windows_color)
        color_array = np.array(color).astype(np.uint16)

        # find the scaled pos and keep it in the valid range for indexing
        scaled_pos = (self.particles_pos / windows.scale).astype(np.int16)
        scaled_width = np.array(windows.SCREEN_WIDTH / windows.scale).astype(np.int16)
        scaled_height = np.array(windows.SCREEN_HEIGHT / windows.scale).astype(np.int16)
        np.clip(scaled_pos[:, 0], 0, scaled_width-1, out=scaled_pos[:, 0])
        np.clip(scaled_pos[:, 1], 0, scaled_height-1, out=scaled_pos[:, 1])

        # set pixel
        pixels = pygame.surfarray.pixels3d(windows.particles_surface)
        pixels[scaled_pos[:, 0], scaled_pos[:,1]] = color_array

        del pixels

        # blit it it the screen
        scaled_surface = pygame.transform.smoothscale(windows.particles_surface, (windows.SCREEN_WIDTH, windows.SCREEN_HEIGHT))
        windows.WIN.blit(scaled_surface, (0,0))

    def _fitness(self, particles_pos, target_pos):
        distance = np.array(target_pos) - particles_pos
        return np.sqrt(np.sum(np.square(distance), axis=1)).astype(np.float32)

    
    def _getNormalizedDirection(self, target_pos):
        # find the distance
        distance = self._fitness(self.particles_pos, target_pos)

        distance = np.where(distance==0, 1, distance) # avoids division by 0
        normal = self.particles_pos - target_pos
        return np.array([normal[:,0] / distance, normal[:,1] / distance]).astype(np.float32).T # transpose it to be (x, y) arrays

    def _adjustVel(self, target_pos, speed_multiplier=10.0, force=5.0):
        dist = self._fitness(self.particles_pos, target_pos)
        dist = np.where(dist<force, force, dist) # prevent extreme forces when the particle is very close to the target.
        normal = self._getNormalizedDirection(target_pos)
        self.particles_v -= (normal * speed_multiplier / dist[:, np.newaxis]).astype(np.float32)

    def _velFriction(self, friction=0.99):
        self.particles_v *= friction # prevent very high velocity from multiple iteration by always only take friction*100% of it

    def _updatePersonalBest(self, target_pos):
        current_fitness = self._fitness(self.particles_pos, target_pos)
        best_fitness = self._fitness(self.pBest, target_pos)
        bestFitness = np.minimum(current_fitness, best_fitness)
        mask = (current_fitness <= bestFitness) # mask it to find which personal best should be changed
        self.pBest[mask] = self.particles_pos[mask] # update the pBest

    def _updateGlobalBest(self, target_pos):
        current_best_idx = np.argmin(self._fitness(self.particles_pos, target_pos))
        current_best_fitness = self._fitness(self.particles_pos[current_best_idx, np.newaxis], target_pos)
        gBest_fitness = self._fitness(self.gBest, target_pos)
        # update gBest with the lowest fitness
        self.gBest = np.where(gBest_fitness < current_best_fitness, gBest_fitness, self.particles_pos[current_best_idx, np.newaxis]).astype(np.int16)

    def update(self, target_pos):
        # update personal best and global best
        self._updatePersonalBest(target_pos)
        self._updateGlobalBest(target_pos)

        # update velocity
        personal_based = self.c1 * self.r1 * (self.pBest - self.particles_pos).astype(np.float32)
        global_based =  self.c2 * self.r2 * (self.gBest - self.particles_pos).astype(np.float32)
        self.particles_v += personal_based + global_based

        # adjust the velocity to move smoothly 
        self._adjustVel(target_pos, speed_multiplier=20.0, force=10.0)
        self._velFriction()

        # update position 
        self.particles_pos = self.particles_pos + self.particles_v

        # keep the particle on the screen
        self.particles_pos %= (self.windows.SCREEN_WIDTH, self.windows.SCREEN_HEIGHT)

    def spreadParticles(self):
        self.particles_pos, self.particles_v = self._makeParticles()
