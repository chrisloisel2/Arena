import os
import random
import pygame


class MapGenerator:
    """Generate a random isometric tile map used as background."""

    def __init__(self, width: int, height: int, terrain_folder: str):
        self.width = width
        self.height = height
        self.terrain_folder = terrain_folder
        self.tiles = self._load_tiles()
        if not self.tiles:
            self.tile_width = 0
            self.tile_height = 0
        else:
            self.tile_width = self.tiles[0].get_width()
            self.tile_height = self.tiles[0].get_height()
        self.map = []

    def _load_tiles(self):
        tiles = []
        for name in os.listdir(self.terrain_folder):
            if name.endswith(".png"):
                path = os.path.join(self.terrain_folder, name)
                image = pygame.image.load(path).convert_alpha()
                tiles.append(image)
        return tiles

    def generate(self):
        if not self.tiles:
            self.map = []
            return
        cols = self.width // self.tile_width + 1
        rows = self.height // self.tile_height + 1
        self.map = [
            [random.choice(self.tiles) for _ in range(cols)] for _ in range(rows)
        ]

    def render(self, surface):
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                surface.blit(tile, (x * self.tile_width, y * self.tile_height))
