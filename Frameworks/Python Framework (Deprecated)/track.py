import pygame
import random
from settings import *


class Track(pygame.sprite.Sprite):
    def __init__(self):
        super(Track, self).__init__()
        self.surf = pygame.Surface((20, 10))
        # self.surf.fill((255, 255, 255))
        self.image = pygame.image.load(vis_TRACKFILE).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)