import random
import math
import time
import pygame
import Target
pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 500
TERGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BG_COLOR = (0, 25, 40)
LIVES = 3
TOP_BAR_HEIGHT = 30

LABEL_FONT = pygame.font.SysFont('comicsans', 24)

def draw(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

def format_time(secs):
    milliseconds = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f'{minutes:02d}:{seconds:02d}.{milliseconds}'

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, 'gray', (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, 'black')
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f'Speed: {speed} t/s', 1, 'black')
    hits_label = LABEL_FONT.render(f'Hits: {targets_pressed}', 1, 'black')
    lives_label = LABEL_FONT.render(f'Lives: {LIVES - misses}', 1, 'black')

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

def end_game(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)

    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, 'white')
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f'Speed: {speed} t/s', 1, 'white')
    hits_label = LABEL_FONT.render(f'Hits: {targets_pressed}', 1, 'white')

    if clicks == 0:
        accuracy = 0
    else:
        accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f'Accuracy: {accuracy}%', 1, 'white')

    win.blit(time_label, (get_middle_position(time_label), 100))
    win.blit(speed_label, (get_middle_position(speed_label), 200))
    win.blit(hits_label, (get_middle_position(hits_label), 300))
    win.blit(accuracy_label, (get_middle_position(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_middle_position(surface):
    return WIDTH / 2 - surface.get_width() / 2

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TERGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_position = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TERGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target.Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_position):
                targets.remove(target)
                targets_pressed += 1

        if misses >= LIVES:
            end_game(WIN, elapsed_time, targets_pressed, clicks) # Game over

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
