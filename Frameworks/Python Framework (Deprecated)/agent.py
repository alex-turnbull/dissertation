"""

The class definition for the Car entity of the game

"""

import pygame as pg
from settings import *
from pygame.math import Vector2
from math import cos, tan, sin, atan


class Agent(pg.sprite.Sprite):
    def __init__(self, pos=(420, 420)):
        super(Agent, self).__init__()
        self.image = pg.image.load(vis_CARFILE).convert_alpha()
        # pg.draw.polygon(self.image, (50, 120, 180), ((0, 0), (0, 50), (70, 25)))
        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.position = Vector2(pos)
        self.direction = Vector2(1, 0)
        self.speed = 0
        self.angle_speed = 0
        self.angle = 0
        self.mask = pg.mask.from_surface(self.image)

        self.maxSpeed = 3
        self.acceleration = 0.25
        self.deceleration = 0.1
        self.onTrack = True

        self.forward = Vector2(0,0)

    def update(self, pressed, dt):
        self.angle_speed = 0
        self.speed -= self.deceleration
        if self.speed <= 0:
            self.speed = 0
        if pressed[ctrl_FORWARD]:
            self.speed += self.acceleration
        if pressed[ctrl_REVERSE] or pressed[ctrl_BRAKE]:
            self.speed -= self.acceleration
        if pressed[ctrl_STEERLEFT]:
            self.angle_speed = -4
        if pressed[ctrl_STEERRIGHT]:
            self.angle_speed = 4

        if self.angle_speed != 0:
            # Rotate the direction vector and then the image.
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            if self.angle > 360:
                self.angle = 0
            elif self.angle < -360:
                self.angle = 0
            self.image = pg.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pg.mask.from_surface(self.image)
        # Update the position vector and the rect.
        self.position += self.direction * self.speed
        self.rect.center = self.position
        self.forward = self.direction

