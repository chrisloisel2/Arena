import pygame
import random

class AnimatedEntity:
    def __init__(self, x, y, size, sprite_sheet_path, animation_map, default_state="idle", default_direction="bot"):
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size
        self.sprite_sheet_path = sprite_sheet_path
        self.animation_map = animation_map
        self.animations = {}
        self.state = default_state
        self.direction = default_direction
        self.anim_index = 0
        self.anim_timer = 0
        self.load_all_animations()

    def load_all_animations(self):
        sheet = pygame.image.load(self.sprite_sheet_path).convert_alpha()
        for key, (row, num_frames) in self.animation_map.items():
            frames = []
            for i in range(num_frames):
                frame = sheet.subsurface(pygame.Rect(i * 64, row * 64, 64, 64))
                frames.append(pygame.transform.scale(frame, (self.size, self.size)))
            self.animations[key] = frames

    def update_animation(self):
        self.anim_timer += 1
        if self.anim_timer >= 5:
            key = self.state + self.direction if self.state != "death" else "death"
            if key in self.animations:
                self.anim_index = (self.anim_index + 1) % len(self.animations[key])
            self.anim_timer = 0

    def render(self, surface):
        key = self.state + self.direction if self.state != "death" else "death"
        frame = self.animations.get(key, [None])[self.anim_index]
        if frame:
            surface.blit(frame, self.rect)

class ArenaGame:
    WIDTH = 600
    HEIGHT = 600
    PLAYER_SIZE = 20
    PNJ_SIZE = 64
    SPEED = 5

    def __init__(self, render_mode=False):
        self.render_mode = render_mode
        if self.render_mode:
            pygame.init()
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption("Arena Survival")
            self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        self.player = pygame.Rect(100, 100, self.PLAYER_SIZE, self.PLAYER_SIZE)
        enemy_anim_map = {
            "idletop": (0, 6), "idleleft": (1, 6), "idlebot": (2, 6), "idleright": (3, 6),
            "grabtop": (4, 6), "grableft": (5, 6), "grabbot": (6, 6), "grabright": (7, 6),
            "walktop": (8, 6), "walkleft": (9, 6), "walkbot": (10, 6), "walkright": (11, 6),
            "death": (20, 5)
        }
        self.enemy = AnimatedEntity(
            x=400,
            y=400,
            size=self.PNJ_SIZE,
            sprite_sheet_path="./game/sprites/Zombie.png",
            animation_map=enemy_anim_map
        )
        self.hp_player = 100
        self.hp_pnj = 100
        self.timestep = 0

    def get_observation(self):
        return [
            self.enemy.rect.x, self.enemy.rect.y,
            self.player.x, self.player.y,
            self.hp_pnj, self.hp_player
        ]

    def step(self, action):
        reward = 0
        done = False
        self.timestep += 1
        self._move_player()

        if action == 0:
            self.enemy.state = "idle"
        elif action == 1:
            self.enemy.rect.y -= self.SPEED
            self.enemy.state = "walk"
            self.enemy.direction = "top"
        elif action == 2:
            self.enemy.rect.x -= self.SPEED
            self.enemy.state = "walk"
            self.enemy.direction = "left"
        elif action == 3:
            self.enemy.rect.x += self.SPEED
            self.enemy.state = "walk"
            self.enemy.direction = "right"
        elif action == 4:
            self.enemy.state = "grab"
            if self.enemy.rect.colliderect(self.player):
                self.hp_player -= 10
                reward = 1
        elif action == 5:
            self.enemy.state = "walk"
            dx = self.enemy.rect.x - self.player.x
            dy = self.enemy.rect.y - self.player.y
            if abs(dx) > abs(dy):
                self.enemy.direction = "left" if dx > 0 else "right"
            else:
                self.enemy.direction = "top" if dy > 0 else "bot"
            self.enemy.rect.x += self.SPEED if dx >= 0 else -self.SPEED
            self.enemy.rect.y += self.SPEED if dy >= 0 else -self.SPEED

        if self.player.colliderect(self.enemy.rect):
            self.hp_pnj -= 5
            reward -= 1

        reward += 0.1

        if self.hp_player <= 0 or self.hp_pnj <= 0:
            self.enemy.state = "death"
            done = True

        return reward, done

    def _move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.y -= self.SPEED
        if keys[pygame.K_DOWN]:
            self.player.y += self.SPEED
        if keys[pygame.K_LEFT]:
            self.player.x -= self.SPEED
        if keys[pygame.K_RIGHT]:
            self.player.x += self.SPEED

        self.player.x = max(0, min(self.WIDTH - self.PLAYER_SIZE, self.player.x))
        self.player.y = max(0, min(self.HEIGHT - self.PLAYER_SIZE, self.player.y))

    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.enemy.update_animation()

        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (0, 255, 0), self.player)
        self.enemy.render(self.screen)
        pygame.display.flip()
        self.clock.tick(30)

    def close(self):
        if self.render_mode:
            pygame.quit()
