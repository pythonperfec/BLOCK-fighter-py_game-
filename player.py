# player.py
import pygame
from constants import PLAYER_SIZE, GROUND_Y

class Player:
    def __init__(self, x, y, facing=1):
        self.width, self.height = PLAYER_SIZE
        self.rect = pygame.Rect(x, y - self.height, self.width, self.height)
        self.color = (60, 140, 220)  # blue
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = 320
        self.jump_speed = -620
        self.gravity = 2000
        self.on_ground = False

        # Facing: 1 = right, -1 = left
        self.facing = facing

        # Combat
        self.health = 100
        self.max_health = 100
        self.is_attacking = False
        self.attack_cooldown = 0.38
        self.attack_timer = 0.0
        self.attack_duration = 0.18
        self.attack_damage = 12
        # attack hitbox relative to player
        self.attack_rect = pygame.Rect(0, 0, 48, 24)

        # Simple invulnerability after hit (frames)
        self.hurt_timer = 0.0
        self.hurt_cooldown = 0.6

    def update(self, dt, keys):
        # Horizontal movement
        self.vel.x = 0
        if keys[pygame.K_a]:
            self.vel.x = -self.speed
            self.facing = -1
        if keys[pygame.K_d]:
            self.vel.x = self.speed
            self.facing = 1

        # Jump
        if keys[pygame.K_w] and self.on_ground:
            self.vel.y = self.jump_speed
            self.on_ground = False

        # Dash (quick move)
        if keys[pygame.K_LSHIFT] and self.on_ground:
            self.vel.x *= 1.8

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

        # Attack handling
        if self.is_attacking:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_duration:
                # attack active window ends
                pass
            if self.attack_timer >= self.attack_cooldown:
                self.is_attacking = False
                self.attack_timer = 0.0

        # Hurt timer
        if self.hurt_timer > 0:
            self.hurt_timer -= dt
            if self.hurt_timer < 0:
                self.hurt_timer = 0

    def start_attack(self):
        if not self.is_attacking and self.attack_timer <= 0:
            self.is_attacking = True
            # attack cooldown timer starts from 0
            self.attack_timer = 0.0001  # set tiny to mark started

    def get_attack_hitbox(self):
        # Only active in the early attack_duration window
        if not self.is_attacking:
            return None
        # Determine active window: first attack_duration seconds are active
        if self.attack_timer > self.attack_duration:
            return None

        # position attack_rect relative to facing
        if self.facing == 1:
            ax = self.rect.right
        else:
            ax = self.rect.left - self.attack_rect.width
        ay = self.rect.centery - self.attack_rect.height // 2
        return pygame.Rect(ax, ay, self.attack_rect.width, self.attack_rect.height)

    def take_damage(self, amount):
        # if currently hurt, ignore to prevent instant-kill chains
        if self.hurt_timer > 0:
            return
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.hurt_timer = self.hurt_cooldown

    def draw(self, surf):
        # flash when hurt
        if self.hurt_timer > 0 and int(self.hurt_timer * 10) % 2 == 0:
            color = (255, 200, 200)
        else:
            color = self.color
        pygame.draw.rect(surf, color, self.rect, border_radius=6)

        # draw attack hitbox (debug)
        hb = self.get_attack_hitbox()
        if hb:
            pygame.draw.rect(surf, (255, 200, 50), hb)

    def is_alive(self):
        return self.health > 0
