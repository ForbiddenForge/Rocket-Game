from os import walk

import pygame
from pygame.math import Vector2 as vector
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, path):
        super().__init__(group)
        self.import_assets(path)

        self.frame_index = 0
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.z = LAYERS["Background Space 3"]
        self.direction = vector()
        self.pos = vector(self.rect.topleft)
        self.speed = 100

    def import_assets(self, path):
        self.animations = {}

        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(
                    folder[2],
                    key=lambda file_name_string: int(file_name_string.split(".")[0]),
                ):
                    path = folder[0].replace("\\", "/") + "/" + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    # Normalize the size of the rocket since the
                    # idle rocket and animated rocket differ in size
                    # pixel sizes are best estimate
                    if folder[0].split("\\")[1] == "idle":
                        surf = pygame.transform.scale(surf, (50, 79))
                    else:
                        surf = pygame.transform.scale(surf, (45, 120))
                    key_value = folder[0].split("\\")[1]
                    self.animations[key_value].append(surf)

    def animate(self, dt):
        self.frame_index += 15 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "idle"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "idle"
        else:
            self.direction.x = 0
            self.status = "idle"

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "flying"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "idle"
        else:
            self.direction.y = 0
            self.status = "idle"

    # TODO
    # Make a collision method here for the collision sprites and create the collision sprites group, creating w objects in main

    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        # TODO
        # add collision text args here for self.collision horizontal

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        # TODO
        # add collision text args here for self.collision vertical

    def update(self, dt):
        # self.old_rect = self.rect.copy() include once collisions added
        self.input()
        self.move(dt)
        self.animate(dt)
