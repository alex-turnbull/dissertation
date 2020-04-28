import pygame
import settings
from agent import Agent
from track import Track
from particle import Particle
from ray import Ray


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.scrn_TITLE)
        self.screen = pygame.display.set_mode((settings.scrn_WIDTH,settings.scrn_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        agent = Agent()
        track = Track()

        sprites = pygame.sprite.Group()
        sprites.add(track)

        p = Particle()
        rays = []

        rays.append(Ray(p, agent.angle))

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                if event.type == pygame.KEYDOWN:
                    if is_number(pygame.key.name(event.key)):
                        if int(pygame.key.name(event.key)) >= 0 or int(pygame.key.name(event.key)) <= settings.sim_MAXDEBUGLEVEL:
                            settings.sim_DEBUGLEVEL = int(pygame.key.name(event.key))

            # User input
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                self.exit = True

            # Logic
            agent.update(pressed, dt)
            if pygame.sprite.spritecollide(agent, sprites, False, pygame.sprite.collide_mask):
                agent.onTrack = False
            else:
                agent.onTrack = True

            print("Agent is on track? " + str(agent.onTrack) + "  ", end="\r", flush=True)

            # Drawing
            self.screen.fill((0, 0, 0))
            self.screen.blit(track.image, track.rect)
            self.screen.blit(agent.image, agent.rect)
            print(agent.forward.x)
            print(agent.forward.y)
            pygame.draw.line(self.screen, (255,255,255), agent.position, agent.forward)

            if settings.sim_DEBUGLEVEL > 1:
                olist = agent.mask.outline()
                pygame.draw.lines(agent.image, (255, 255, 255), 1, olist)


            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()
