import pygame
import random
import sys, time


pygame.init()

# Ekran ólshemi
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Game") 

# Fon túsi
BACKGROUND_COLOR = (255, 255, 255)

FONT = pygame.font.Font(None, 36)
Green = (0, 255, 0)
Black = (0, 0, 0)

# Ár elementke sýretter qoiu
ROCK_IMG = pygame.image.load('Tas.png')
PAPER_IMG = pygame.image.load('Qagaz.png')
SCISSORS_IMG = pygame.image.load('Qaishy.png')

new_size = (20, 20)

ROCK_IMG = pygame.transform.scale(ROCK_IMG, new_size)
PAPER_IMG = pygame.transform.scale(PAPER_IMG, new_size)
SCISSORS_IMG = pygame.transform.scale(SCISSORS_IMG, new_size)

# Elementterdiń olshemi
OBJECT_SIZE = 20

# Qaýipsiz aımaq
SAFE_AREA_LEFT = 10
SAFE_AREA_RIGHT = WINDOW_WIDTH - 10
SAFE_AREA_TOP = 10
SAFE_AREA_BOTTOM = WINDOW_HEIGHT - 10

# Elementterdin kezdeisoq sany
ROCK_COUNT = random.randint(5, 10)
PAPER_COUNT = random.randint(5, 10)
SCISSORS_COUNT = random.randint(5, 10)

# Elementterdiń ornalasýy
ROCK_POSITIONS = []
PAPER_POSITIONS = []
SCISSORS_POSITIONS = []


# Oıyndy aıaqtaý fýnksıasy
def game_over(winner):
    time.sleep(1)
    pygame.mixer.music.stop()
    pygame.mixer.Sound('winner_sound.mp3').play()
    font = pygame.font.SysFont("comicsansms", 40)
    text = font.render('Oiyn aiaqtaldy', True, Green)
    WINDOW.blit(text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 200))

    font2 = pygame.font.SysFont("comicsansms", 40)
    text2 = font2.render(f'Jeńimpaz: {winner}', True, Green)
    WINDOW.blit(text2, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 150))

    winner_image = pygame.image.load(f'{winner}.png')
    original_size = winner_image.get_size()
    scaled_size = (200, 200)
    scale_increment = 2
    current_size = (0, 0)

    while current_size[0] < scaled_size[0]:
        current_size = (current_size[0] + scale_increment, current_size[1] + scale_increment)
        scaled_image = pygame.transform.smoothscale(winner_image, current_size)
        scaled_rect = scaled_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        WINDOW.blit(scaled_image, scaled_rect)
        pygame.display.update()

    pygame.display.update()
    time.sleep(4)
    pygame.quit()


# Oıyn nysandaryn qurý
for i in range(ROCK_COUNT):
    x = random.randint(0, WINDOW_WIDTH - ROCK_IMG.get_width())
    y = random.randint(0, WINDOW_HEIGHT - ROCK_IMG.get_height())
    ROCK_POSITIONS.append(pygame.Rect(x, y, OBJECT_SIZE, OBJECT_SIZE))

for i in range(PAPER_COUNT):
    x = random.randint(0, WINDOW_WIDTH - PAPER_IMG.get_width())
    y = random.randint(0, WINDOW_HEIGHT - PAPER_IMG.get_height())
    PAPER_POSITIONS.append(pygame.Rect(x, y, OBJECT_SIZE, OBJECT_SIZE))

for i in range(SCISSORS_COUNT):
    x = random.randint(0, WINDOW_WIDTH - SCISSORS_IMG.get_width())
    y = random.randint(0, WINDOW_HEIGHT - SCISSORS_IMG.get_height())
    SCISSORS_POSITIONS.append(pygame.Rect(x, y, OBJECT_SIZE, OBJECT_SIZE))


# Jyldamdyq
SPEED = 1

ROCK_DIRECTIONS = [(random.randint(-SPEED, SPEED), random.randint(-SPEED, SPEED)) for _ in range(ROCK_COUNT)]
PAPER_DIRECTIONS = [(random.randint(-SPEED, SPEED), random.randint(-SPEED, SPEED)) for _ in range(PAPER_COUNT)]
SCISSORS_DIRECTIONS = [(random.randint(-SPEED, SPEED), random.randint(-SPEED, SPEED)) for _ in range(SCISSORS_COUNT)]


FPS = 60

clock = pygame.time.Clock()
# pygame.mixer.Sound('music/piano_music.mp3').play()
pygame.mixer.music.load('piano_music.mp3')
pygame.mixer.music.play()

# Oıyn sıkli
while True:
    clock.tick(FPS)
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Nysandardy kezdeısoq jyljytamyz jáne soqtyǵystardy tekseremiz
    for i, rock in enumerate(ROCK_POSITIONS):
        dx, dy = ROCK_DIRECTIONS[i]
        rock.move_ip(dx, dy)
        Checker = True
        if rock.left < SAFE_AREA_LEFT or rock.right > SAFE_AREA_RIGHT:
            dx = -dx
            ROCK_DIRECTIONS[i] = (dx, dy)
        if rock.top < SAFE_AREA_TOP or rock.bottom > SAFE_AREA_BOTTOM:
            dy = -dy
            ROCK_DIRECTIONS[i] = (dx, dy)
        if(Checker):
            for j, paper in enumerate(PAPER_POSITIONS):
                if rock.colliderect(paper) and Checker:
                    ROCK_COUNT -= 1
                    PAPER_COUNT += 1
                    PAPER_POSITIONS.append(pygame.Rect(rock[0],rock[1], rock[2], rock[3]))
                    dx1, dy1 = PAPER_DIRECTIONS[j]
                    PAPER_DIRECTIONS[j] = ([dx, dy])
                    PAPER_DIRECTIONS.append([dx1, dy1])
                    ROCK_POSITIONS.pop(i)
                    ROCK_DIRECTIONS.pop(i)
                    i -= 1
                    Checker = False
                    break
        if(Checker):
            for j, scissors in enumerate(SCISSORS_POSITIONS):
                if rock.colliderect(scissors) and Checker:
                    ROCK_COUNT += 1
                    SCISSORS_COUNT -= 1
                    ROCK_POSITIONS.append(pygame.Rect(scissors[0],scissors[1], scissors[2], scissors[3]))
                    dx1, dy1 = SCISSORS_DIRECTIONS[j]
                    ROCK_DIRECTIONS[i] = ([dx1, dy1])
                    ROCK_DIRECTIONS.append([dx, dy])
                    SCISSORS_POSITIONS.pop(j)
                    SCISSORS_DIRECTIONS.pop(j)
                    j -= 1
                    Checker = False
                    break
        if(Checker):
            for i2, rock2 in enumerate(ROCK_POSITIONS):
                if(i != i2):
                    if rock.colliderect(rock2):
                        dx1, dy1 = ROCK_DIRECTIONS[i2]
                        ROCK_DIRECTIONS[i] = ([dx1, dy1])
                        ROCK_DIRECTIONS[i2] = ([dx, dy])
                        break
    for i, paper in enumerate(PAPER_POSITIONS):
        dx, dy = PAPER_DIRECTIONS[i]
        paper.move_ip(dx, dy)
        Checker = True
        if paper.left < SAFE_AREA_LEFT or paper.right > SAFE_AREA_RIGHT:
            dx = -dx
            PAPER_DIRECTIONS[i] = (dx, dy)
        if paper.top < SAFE_AREA_TOP or paper.bottom > SAFE_AREA_BOTTOM:
            dy = -dy
            PAPER_DIRECTIONS[i] = (dx, dy)
        if(Checker):
            for j, scissors in enumerate(SCISSORS_POSITIONS):
                if paper.colliderect(scissors) and Checker:
                    PAPER_COUNT -= 1
                    SCISSORS_COUNT += 1
                    SCISSORS_POSITIONS.append(pygame.Rect(paper[0],paper[1], paper[2], paper[3]))
                    dx1, dy1 = PAPER_DIRECTIONS[i]
                    SCISSORS_DIRECTIONS[j] = ([dx1, dy1])
                    SCISSORS_DIRECTIONS.append([dx, dy])
                    PAPER_POSITIONS.pop(i)
                    PAPER_DIRECTIONS.pop(i)
                    i -= 1
                    Checker = False
                    break
        if(Checker):
            for j, rock in enumerate(ROCK_POSITIONS):
                if paper.colliderect(rock) and Checker:
                        ROCK_COUNT -= 1
                        PAPER_COUNT += 1
                        PAPER_POSITIONS.append(pygame.Rect(rock[0],rock[1], rock[2], rock[3]))
                        dx1, dy1 = ROCK_DIRECTIONS[j]
                        PAPER_DIRECTIONS[i] = ([dx1, dy1])
                        PAPER_DIRECTIONS.append([dx, dy])
                        ROCK_POSITIONS.pop(j)
                        ROCK_DIRECTIONS.pop(j)
                        j -= 1
                        Checker = False
                        break
        if(Checker):
            for i2, paper2 in enumerate(PAPER_POSITIONS):
                if(i != i2):
                    if paper.colliderect(paper2):
                        dx1, dy1 = PAPER_DIRECTIONS[i2]
                        PAPER_DIRECTIONS[i] = ([dx1, dy1])
                        PAPER_DIRECTIONS[i2] = ([dx, dy])
                        break
    for i, scissors in enumerate(SCISSORS_POSITIONS):
        dx, dy = SCISSORS_DIRECTIONS[i]
        scissors.move_ip(dx, dy)
        Checker = True
        if scissors.left < SAFE_AREA_LEFT or scissors.right > SAFE_AREA_RIGHT:
            dx = -dx
            SCISSORS_DIRECTIONS[i] = (dx, dy)
        if scissors.top < SAFE_AREA_TOP or scissors.bottom > SAFE_AREA_BOTTOM:
            dy = -dy
            SCISSORS_DIRECTIONS[i] = (dx, dy)
        if(Checker):
            for j, paper in enumerate(PAPER_POSITIONS):
                if scissors.colliderect(paper) and Checker:
                    PAPER_COUNT -= 1
                    SCISSORS_COUNT += 1
                    SCISSORS_POSITIONS.append(pygame.Rect(paper[0],paper[1], paper[2], paper[3]))
                    dx1, dy1 = PAPER_DIRECTIONS[j]
                    SCISSORS_DIRECTIONS[i] = ([dx1, dy1])
                    SCISSORS_DIRECTIONS.append([dx, dy])
                    PAPER_POSITIONS.pop(j)
                    PAPER_DIRECTIONS.pop(j)
                    j -= 1
                    Checker = False
                    break
        if(Checker):
            for j, rock in enumerate(ROCK_POSITIONS):
                if scissors.colliderect(rock) and Checker:
                    ROCK_COUNT += 1
                    SCISSORS_COUNT -= 1
                    ROCK_POSITIONS.append(pygame.Rect(scissors[0],scissors[1], scissors[2], scissors[3]))
                    dx1, dy1 = SCISSORS_DIRECTIONS[i]
                    ROCK_DIRECTIONS[j] = ([dx1, dy1])
                    ROCK_DIRECTIONS.append([dx, dy])
                    SCISSORS_POSITIONS.pop(i)
                    SCISSORS_DIRECTIONS.pop(i)
                    i -= 1
                    Checker = False
                    break
        if(Checker):
            for i2, scissors2 in enumerate(SCISSORS_POSITIONS):
                if(i != i2):
                    if scissors.colliderect(scissors2):
                        dx1, dy1 = SCISSORS_DIRECTIONS[i2]
                        SCISSORS_DIRECTIONS[i] = ([dx1, dy1])
                        SCISSORS_DIRECTIONS[i2] = ([dx, dy])
                        break


    # Oıynnyń aıaqtalǵanyn tekseremiz
    if ROCK_COUNT == 0 and PAPER_COUNT == 0:
        game_over('Qaishy')
        print("Qaishy jeńdi!")
        break
    elif ROCK_COUNT == 0 and SCISSORS_COUNT == 0:
        game_over('Qagaz')
        print("Qagaz jeńdi!")
        break
    elif PAPER_COUNT == 0 and SCISSORS_COUNT == 0:
        game_over('Tas')
        print("Tas jeńdi!")
        break

    # Nysandardy ekranga shygaramyz
    WINDOW.fill(BACKGROUND_COLOR)
    for rock in ROCK_POSITIONS:
        WINDOW.blit(ROCK_IMG, rock)
    for paper in PAPER_POSITIONS:
        WINDOW.blit(PAPER_IMG, paper)
    for scissors in SCISSORS_POSITIONS:
        WINDOW.blit(SCISSORS_IMG, scissors)
    rock_text = FONT.render(f"Tas: {ROCK_COUNT}", True, Black)
    WINDOW.blit(rock_text, (10, 10))

    paper_text = FONT.render(f"Qagaz: {PAPER_COUNT}", True, Black)
    WINDOW.blit(paper_text, (10, 40))

    scissors_text = FONT.render(f"Qaishy: {SCISSORS_COUNT}", True, Black)
    WINDOW.blit(scissors_text, (10, 70))
    pygame.display.update()
    

