import sys

import pygame
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from settings import *
from tile import Clouds, GroundCollisionTile, Tile

from player import Player


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # self.display_surface = pygame.display.get_surface()
        # create offset for the player camera in vector format
        self.offset = vector()
        self.bg_sky = pygame.image.load("../Map File/bg_sky.png").convert()
        self.bg_space_1 = pygame.image.load(
            "../Map File/bg_space_1.png"
        ).convert_alpha()
        self.bg_space_2 = pygame.image.load(
            "../Map File/bg_space_2.png"
        ).convert_alpha()
        self.bg_space_3 = pygame.image.load(
            "../Map File/bg_space_3.png"
        ).convert_alpha()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # Blit the bg / fg images in order, before blitting the sprite objects on TOP nahmean
        game.display_surface.blit(self.bg_sky, -self.offset)
        game.display_surface.blit(self.bg_space_1, -self.offset)
        game.display_surface.blit(self.bg_space_2, -self.offset)
        game.display_surface.blit(self.bg_space_3, -self.offset)

        # Draw sprites according to their z value (only pertains to objects, bg's order are above, idiot)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            # Only draw[blit] the sprites that are on screen. If not, they can fuck off
            blit = True
            if (
                offset_rect.right <= 0
                or offset_rect.left >= WINDOW_WIDTH
                or offset_rect.bottom <= 0
                or offset_rect.top >= WINDOW_HEIGHT
            ):
                blit = False

            if blit:
                game.display_surface.blit(sprite.image, offset_rect)


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Rocket Simulation")
        self.clock = pygame.time.Clock()

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.cloud_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        tmx_map = load_pygame("../Map File/RocketGame.tmx")

        # Normal Tiles without collision
        # layer_list = [
        #     "Ground Collision",
        #     "Ground Non-Collision",
        # ]
        # for layer in layer_list:
        for x, y, surf in tmx_map.get_layer_by_name("Ground Non-Collision").tiles():
            Tile(
                pos=(x * 16, y * 16),
                surf=surf,
                group=self.all_sprites,
                z=LAYERS["Ground Non-Collision"],
            )

        for obj in tmx_map.get_layer_by_name("Clouds"):
            Clouds(
                pos=(obj.x, obj.y),
                surf=obj.image,
                group=[self.all_sprites, self.cloud_sprites],
                z=LAYERS["Ground Objects"],
            )

        for obj in tmx_map.get_layer_by_name("Player"):
            if obj.name == "Player":
                self.player = Player(
                    (obj.x, obj.y),
                    self.all_sprites,
                    "../Player/keyframes",
                )

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Run Delta Time
            dt = self.clock.tick(120) * 0.001
            self.display_surface.fill((100, 100, 100))

            # Update Sprites
            self.all_sprites.update(dt)

            # Drawing

            self.all_sprites.custom_draw(self.player)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
