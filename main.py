import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EcoSort Adventure")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 30)
small_font = pygame.font.SysFont("Comic Sans MS", 22)
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 50, 50)
TEAL = (0, 150, 136)

# Load assets
bin_img = pygame.image.load("assets/trashbin.png")
bin_img = pygame.transform.scale(bin_img, (120, 120))
correct_sound = pygame.mixer.Sound("sounds/correct.wav")
wrong_sound = pygame.mixer.Sound("sounds/wrong.wav")

# Trash images
recyclable_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets/recycleable", f)), (80, 80))
                   for f in os.listdir("assets/recycleable")]
unrecyclable_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("assets/unrecycleable", f)), (80, 80))
                     for f in os.listdir("assets/unrecycleable")]

recycle_bin_rect = bin_img.get_rect(topleft=(100, HEIGHT - 140))
unrecycle_bin_rect = bin_img.get_rect(topleft=(WIDTH - 220, HEIGHT - 140))

# Game state
score = 0
high_score = 0
timer = 30
start_ticks = None
game_state = "start"
dragging = False
selected_trash = None

class Trash:
    def __init__(self):
        if random.random() > 0.5:
            self.image = random.choice(recyclable_imgs)
            self.type = "recyclable"
        else:
            self.image = random.choice(unrecyclable_imgs)
            self.type = "unrecycleable"
        self.rect = self.image.get_rect(center=(random.randint(250, 750), random.randint(100, 400)))

    def draw(self):
        screen.blit(self.image, self.rect)

def draw_text(text, x, y, color=BLACK, size=30, center=False):
    f = pygame.font.SysFont("Comic Sans MS", size)
    t = f.render(text, True, color)
    if center:
        rect = t.get_rect(center=(x, y))
        screen.blit(t, rect)
    else:
        screen.blit(t, (x, y))

def draw_start_screen():
    screen.fill(WHITE)
    draw_text("♻️ EcoSort Adventure ♻️", WIDTH//2, 120, TEAL, 42, center=True)
    draw_text("Click anywhere to start!", WIDTH//2, 220, RED, 28, center=True)

def draw_game(trash_item):
    screen.fill((230, 255, 230))
    screen.blit(bin_img, recycle_bin_rect.topleft)
    screen.blit(bin_img, unrecycle_bin_rect.topleft)

    draw_text("Recycle", recycle_bin_rect.centerx, recycle_bin_rect.top - 30, TEAL, 24, center=True)
    draw_text("Trash", unrecycle_bin_rect.centerx, unrecycle_bin_rect.top - 30, TEAL, 24, center=True)

    trash_item.draw()

    time_left = max(0, timer - (pygame.time.get_ticks() - start_ticks) // 1000)
    draw_text(f"Time: {time_left}s", 20, 20, RED if time_left <= 5 else BLACK)
    draw_text(f"Score: {score}", WIDTH - 180, 20)

    return time_left > 0

def draw_end_screen():
    screen.fill((255, 245, 230))

    draw_text("⏱ Time's Up!", WIDTH // 2, 100, RED, 42, center=True)
    draw_text(f"Your Score: {score}", WIDTH // 2, 170, BLACK, 30, center=True)
    draw_text(f"Highest Score: {high_score}", WIDTH // 2, 220, TEAL, 28, center=True)

    draw_text("Play Again?", WIDTH // 2, 290, BLACK, 28, center=True)

    yes_rect = pygame.Rect(WIDTH//2 - 120, 330, 100, 50)
    no_rect = pygame.Rect(WIDTH//2 + 20, 330, 100, 50)
    pygame.draw.rect(screen, (200, 255, 200), yes_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 200, 200), no_rect, border_radius=12)

    draw_text("Yes", yes_rect.centerx, yes_rect.centery, BLACK, 26, center=True)
    draw_text("No", no_rect.centerx, no_rect.centery, BLACK, 26, center=True)

    return yes_rect, no_rect

def reset_game():
    global score, start_ticks, trash_item
    score = 0
    start_ticks = pygame.time.get_ticks()
    return Trash()

# Main loop
trash_item = Trash()
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "start":
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "playing"
                trash_item = reset_game()

        elif game_state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN and trash_item.rect.collidepoint(event.pos):
                dragging = True
                selected_trash = trash_item
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                dragging = False
                if selected_trash.rect.colliderect(recycle_bin_rect) and selected_trash.type == "recyclable":
                    correct_sound.play()
                    score += 1
                elif selected_trash.rect.colliderect(unrecycle_bin_rect) and selected_trash.type == "unrecycleable":
                    correct_sound.play()
                    score += 1
                else:
                    wrong_sound.play()
                trash_item = Trash()

        elif game_state == "end":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if yes_rect.collidepoint(mx, my):
                    game_state = "playing"
                    trash_item = reset_game()
                elif no_rect.collidepoint(mx, my):
                    game_state = "start"

    if dragging and selected_trash:
        selected_trash.rect.center = pygame.mouse.get_pos()

    if game_state == "start":
        draw_start_screen()

    elif game_state == "playing":
        still_time = draw_game(trash_item)
        if not still_time:
            game_state = "end"
            if score > high_score:
                high_score = score

    elif game_state == "end":
        yes_rect, no_rect = draw_end_screen()

    pygame.display.update()

pygame.quit()
