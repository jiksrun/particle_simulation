import pygame
from setup import Setup, Color
from particles import Particles
pygame.font.init()

def displayText(windows, text, color):
    font = pygame.font.SysFont('Times New Roman', 20)
    text_surface = font.render(text, False, color)
    windows.blit(text_surface, (5,5))

def main():
    windows = Setup()
    color = Color()
    # particles = Particles(50000) 
    particles = Particles(25000)
    target_pos = (0, 0)
    background_color = color.BLACK
    particle_color = color.WHITE
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False     
            if pygame.mouse.get_pressed()[2] or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                particles.spreadParticles()
           
        # windows.WIN.fill(color.BLACK)
        target_pos = pygame.mouse.get_pos()
        particles.update(target_pos)
        particles.drawParticles(windows, background_color, particle_color)
        # displayText(windows.WIN, "PRESS ESC TO QUIT", color.WHITE)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()

