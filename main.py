# main.py
import pygame
import sys
from constants import *
from player import Player
from enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame 2D Fighter (mini)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)


def draw_ground(surf):
    # simple ground line
    pygame.draw.rect(surf, (28, 30, 33), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))

def draw_health_bar(surf, x, y, w, h, current, maximum):
    pygame.draw.rect(surf, HEALTH_BG, (x, y, w, h))
    ratio = max(0, current) / maximum
    inner_w = int((w - 4) * ratio)
    pygame.draw.rect(surf, HEALTH_RED if ratio < 0.3 else HEALTH_GREEN, (x + 2, y + 2, inner_w, h - 4))

def main():
    # Entities
    player = Player(160, GROUND_Y)
    enemy = Enemy(WIDTH - 240, GROUND_Y)

    # simple camera offset (screen centered on mid)
    running = True
    paused = False
    round_over = False
    winner_text = ""

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # attack pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    player.start_attack()
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        if not paused and not round_over:
            keys = pygame.key.get_pressed()
            player.update(dt, keys)
            enemy.update(dt, player)

            # collision: player's attack hits enemy
            p_hb = player.get_attack_hitbox()
            if p_hb and enemy.is_alive():
                if p_hb.colliderect(enemy.rect):
                    enemy.take_damage(player.attack_damage)
            # collision: enemy attack hits player
            e_hb = enemy.get_attack_hitbox()
            if e_hb and player.is_alive():
                if e_hb.colliderect(player.rect):
                    player.take_damage(enemy.attack_damage)

            # check death
            if not player.is_alive():
                round_over = True
                winner_text = "Enemy Wins! Press R to Restart"
            elif not enemy.is_alive():
                round_over = True
                winner_text = "Player Wins! Press R to Restart"

        # render
        screen.fill(BG_COLOR)
        draw_ground(screen)

        # Draw entities
        enemy.draw(screen)
        player.draw(screen)



        # Draw HUD (health bars)
        draw_health_bar(screen, 20, 20, 360, 24, player.health, player.max_health)
        draw_health_bar(screen, WIDTH - 380, 20, 360, 24, enemy.health, enemy.max_health)

        # instructions
        inst = font.render("A/D move  W jump  Shift dash  J attack  Esc pause", True, (200,200,200))
        screen.blit(inst, (WIDTH//2 - inst.get_width()//2, HEIGHT - 40))

        if paused:
            pmsg = font.render("PAUSED - press Esc to resume", True, (240,240,240))
            screen.blit(pmsg, (WIDTH//2 - pmsg.get_width()//2, HEIGHT//2 - 12))

        if round_over:
            t = font.render(winner_text, True, (255,255,255))
            screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 12))
            # Restart option
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # reset
                player = Player(160, GROUND_Y)
                enemy = Enemy(WIDTH - 240, GROUND_Y)
                round_over = False
                winner_text = ""

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
