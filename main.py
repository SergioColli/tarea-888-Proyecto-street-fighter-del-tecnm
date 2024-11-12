import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Luchas en el Tecnm de Cancún")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
match_winner = None

# Define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# Load background images
backgrounds = [
    pygame.image.load("assets/images/background/fuenteplacas.jpg").convert_alpha(),
    pygame.image.load("assets/images/background/letrastec.jpg").convert_alpha(),
    pygame.image.load("assets/images/background/canchabeisbol.jpg").convert_alpha(),
    pygame.image.load("assets/images/background/placaarca.jpg").convert_alpha()
]
bg_index = 0

# Load menu background image
menu_bg_image = pygame.image.load("assets/images/background/itcentrada.jpg").convert_alpha()

# Load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Define fonts
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(backgrounds[bg_index], (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, [10, 8, 1, 7, 7, 3, 7], sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, [8, 8, 1, 8, 8, 3, 7], magic_fx)

# Game loop
run = True
menu = True
paused = False

while run:

    clock.tick(FPS)

    if menu:
        scaled_menu_bg = pygame.transform.scale(menu_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_menu_bg, (0, 0))
        draw_text("Elije escenario", count_font, RED, SCREEN_WIDTH / 2 - 300, SCREEN_HEIGHT / 2 - 100)
        draw_text("Presiona ESPACIO para cambiar el escenario", score_font, RED, SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2)
        draw_text("Presiona ENTER para empezar", score_font, RED, SCREEN_WIDTH / 2 - 180, SCREEN_HEIGHT / 2 + 50)
        scaled_bg = pygame.transform.scale(backgrounds[bg_index], (300, 150))
        screen.blit(scaled_bg, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 + 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bg_index = (bg_index + 1) % len(backgrounds)
                if event.key == pygame.K_RETURN:
                    menu = False
                    match_winner = None
                    score = [0, 0]  # reset scores for a new match

    elif match_winner:
        screen.fill(BLACK)
        winner_text = f"Gana {match_winner}"
        draw_text(winner_text, count_font, YELLOW, SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 40)
        draw_text("Presiona ENTER para volver al menu", score_font, YELLOW, SCREEN_WIDTH / 2 - 180, SCREEN_HEIGHT / 2 + 60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = True
                    match_winner = None

    else:
        draw_bg()
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("Espadachin del TecNM: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("Hechicero del TecNM: " + str(score[1]), score_font, RED, 580, 60)

        if intro_count <= 0:
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        fighter_1.update()
        fighter_2.update()
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                if score[0] >= 2:
                    match_winner = "Espadachin"
                elif score[1] >= 2:
                    match_winner = "Hechicero"
                else:
                    round_over = False
                    intro_count = 3
                    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, [10, 8, 1, 7, 7, 3, 7], sword_fx)
                    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, [8, 8, 1, 8, 8, 3, 7], magic_fx)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        if paused:
            screen.fill(BLACK)
            draw_text("PAUSA", count_font, WHITE, SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 40)
            draw_text("Pulsa ESC para reanudar", score_font, WHITE, SCREEN_WIDTH / 2 - 140, SCREEN_HEIGHT / 2 + 40)

    pygame.display.update()

pygame.quit()