import sys

import pygame
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from settings import *
from tile import Tile

from player import Player


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    # TODO change the camera method to stop this stupid fucking lag [no more offsets]
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Rocket Simulation")
        self.clock = pygame.time.Clock()

        # Groups
        self.all_sprites = AllSprites()

        self.setup()

    def setup(self):
        tmx_map = load_pygame("../Map File/RocketGame.tmx")

        # Normal Tiles without collision
        layer_list = [
            "Background Sky",
            "Ground",
            "Ground Tiles",
            "Background Space 1",
            "Background Space 2",
            "Background Space 3",
        ]
        for layer in layer_list:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile(
                    pos=(x * 16, y * 16),
                    surf=surf,
                    group=self.all_sprites,
                    z=LAYERS[layer],
                )

        # Player creation
        for obj in tmx_map.get_layer_by_name("Player"):
            if obj.name == "Player":
                self.player = Player(
                    (obj.x, obj.y), self.all_sprites, "../Player/keyframes"
                )

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Run Delta Time
            dt = self.clock.tick() / 1000
            # Update Sprites
            self.all_sprites.update(dt)

            # Drawing
            self.display_surface.fill((100, 100, 100))
``            self.all_sprites.custom_draw(self.player)
``
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
