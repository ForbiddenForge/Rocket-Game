import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, z):
        super().__init__(group)
        self.image = surf.convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class BackgroundSky(Tile):
    def __init__(self, pos, surf, group, z):
        super().__init__(pos, surf, group, z)
