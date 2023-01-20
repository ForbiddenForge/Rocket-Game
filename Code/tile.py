import pygame
from pygame.math import Vector2 as vector
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, z):
        super().__init__(group)
        self.image = surf.convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class GroundCollisionTile(Tile):
    def __init__(self, pos, surf, group, z):
        super().__init__(pos, surf, group, z)
        self.old_rect = self.rect.copy()


class Clouds(Tile):
    def __init__(self, pos, surf, group, z):
        super().__init__(pos, surf, group, z)
        self.direction = vector(1, 0)
        self.speed = 0
        self.pos = vector(self.rect.topleft)

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
