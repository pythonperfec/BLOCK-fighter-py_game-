# enemy.py
import pygame
from constants import ENEMY_SIZE, GROUND_Y
import random

class Enemy:
    def __init__(self, x, y):
        self.width, self.height = ENEMY_SIZE
        self.rect = pygame.Rect(x, y - self.height, self.width, self.height)
        self.color = (220, 90, 70)  # red
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = 200
        self.gravity = 2000
        self.on_ground = False

        # Simple AI
        self.health = 80
        self.max_health = 80
        self.attack_range = 70
        self.attack_cooldown = 0.9
        self.attack_timer = 0.0
        self.attack_duration = 0.15
        self.attack_damage = 10
        self.is_attacking = False
        self.attack_rect = pygame.Rect(0, 0, 48, 26)

        # Facing
        self.facing = -1

    def update(self, dt, player):
        # Move toward player if alive
        if self.health <= 0:
            return

        # simple horizontal AI: move towards player's x unless close
        dx = player.rect.centerx - self.rect.centerx
        dist = abs(dx)
        if dist > self.attack_range:
            dir = 1 if dx > 0 else -1
            self.vel.x = dir * self.speed
            self.facing = 1 if dir > 0 else -1
            # occasionally jump to mix behavior
            if random.random() < 0.001:
                if self.on_ground:
                    self.vel.y = -560
                    self.on_ground = False
        else:
            # in range -> stop and maybe attack
            self.vel.x = 0
            # trigger attack when off cooldown
            if self.attack_timer <= 0:
                self.is_attacking = True
                self.attack_timer = 0.0001

        # Apply gravity
        self.vel.y += self.gravity * dt
        # Integrate
        self.rect.x += int(self.vel.x * dt)
        self.rect.y += int(self.vel.y * dt)

        # Ground collision
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel.y = 0
            self.on_ground = True

        # timers
        if self.is_attacking:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_duration:
                pass
            if self.attack_timer >= self.attack_cooldown:
                self.is_attacking = False
                self.attack_timer = 0.0
        else:
            if self.attack_timer > 0:
                self.attack_timer -= dt

    def get_attack_hitbox(self):
        if not self.is_attacking:
            return None
        if self.attack_timer > self.attack_duration:
            return None
        if self.facing == 1:
            ax = self.rect.right
        else:
            ax = self.rect.left - self.attack_rect.width
        ay = self.rect.centery - self.attack_rect.height // 2
        return pygame.Rect(ax, ay, self.attack_rect.width, self.attack_rect.height)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=6)
        hb = self.get_attack_hitbox()
        if hb:
            pygame.draw.rect(surf, (255, 200, 50), hb)

    def is_alive(self):
        return self.health > 0
