import pygame
import random

pygame.init()

display_w = 800
display_h = 600

display = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption("Game")


prizeml_sound = pygame.mixer.Sound('tr.wav')

pygame.mixer.music.load('jk.wav')
pygame.mixer.music.set_volume(0.05)


icon = pygame.image.load("ge.png")
pygame.display.set_icon(icon)

cactus_img = [pygame.image.load("99.png"), pygame.image.load("122.png"), pygame.image.load("100.png")]
cactus_options = [27, 450, 27, 450, 27, 450]

golem_img = [pygame.image.load("1.png"), pygame.image.load("2.png"), pygame.image.load("3.png"),
             pygame.image.load("4.png"), pygame.image.load("5.png")]

img_counter = 0


class Cactus:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.w = width
        self.image = image
        self.s = speed

    def move(self):
        if self.x >= self.w:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.s
            return True
        else:
            self.x = display_w + 100 + random.randrange(-80, 60)
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.w = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


user_w = 60
user_h = 100
user_x = display_w // 3
user_y = display_h - user_h - 74

cactus_w = 20
cactus_h = 70
cactus_x = display_w - 100
cactus_y = display_h - cactus_h - 100
clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0
abv_cactus = False
max_scores = 0


def run_game():
    global make_jump
    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    fon = pygame.image.load("fon.png")

    pygame.mixer.music.play(-1)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        count_scores(cactus_arr)

        if check_crash(cactus_arr):
            pygame.mixer.music.stop()
            game = False



        display.blit(fon, (0, 0))
        print_text('Scores: ' + str(scores), 300, 100 )
        draw_array(cactus_arr)

        draw_golem()
        pygame.display.update()
        clock.tick(60)
    return game_over()


def jump():
    global user_y, make_jump, jump_counter
    if jump_counter >= -30:
        if jump_counter == -25:
            pygame.mixer.Sound.play(prizeml_sound)
        user_y -= jump_counter / 3
        jump_counter -= 1


    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Cactus(display_w + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Cactus(display_w + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Cactus(display_w + 600, height, width, img, 4))


def find_radius(array):
    limit = max(array[0].x, array[1].x, array[2].x)

    if limit < display_w:
        radius = display_w
        if radius - limit < 50:
            radius += 150
    else:
        radius = limit

    choice = random.randrange(0, 3)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 350)

    return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]

            cactus.return_self(radius, height, width, img)


def draw_golem():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    display.blit(golem_img[img_counter // 5], (user_x, user_y))
    img_counter += 1


def print_text(message, x, y, font_color = (0, 0, 225), font_type = "gh.ttf", font_size = 33):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    pygame.mixer.music.pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text("Пауза. ENTER для продолжения", 60, 150)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()
        clock.tick(20)

    pygame.mixer.music.unpause()


def check_crash(barriers):
    for barrier in barriers:
        if barrier.y == 450:
            if not make_jump:
                if barrier.x <= user_x + user_w - 5 <= barrier.x + barrier.w:
                    return True
            elif jump_counter >= 0:
                if user_y + user_h - 5 >= barrier.y:
                    if barrier.x <= user_x + user_w - 5 <= barrier.x + barrier.w:
                        return True
            else:
                if user_y + user_h - 10 >= barrier.y:
                    if barrier.x <= user_x <= barrier.x + barrier.w:
                        return True
        else:
            if not make_jump:
                if barrier.x <= user_x + user_w - 5 <= barrier.x + barrier.w:
                    return True
            elif jump_counter == 10:
                if user_y + user_h - 5 >= barrier.y:
                    if barrier.x <= user_x + user_w - 5 <= barrier.x + barrier.w:
                        return True
            elif jump_counter >= -1:
                if user_y + user_h - 5 >= barrier.y:
                    if barrier.x <= user_x + user_w - 5 <= barrier.x + barrier.w:
                        return True
                else:
                    if user_y + user_h - 10 >= barrier.y:
                        if barrier.x <= user_x + 5 <= barrier.x + barrier.w:
                            return True
    return False


def count_scores(barriers):
    global scores, abv_cactus

    if not abv_cactus:
        for barrier in barriers:
            if barrier.x <= user_x + user_w / 2 <= barrier.x + barrier.w:
                if user_y + user_h - 5 <= barrier.y:
                    abv_cactus = True
                    break
    else:
        if jump_counter == -30:
            scores += 1
            abv_cactus = False






def game_over():
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text("GAME OVER.", 60, 150)
        print_text('Max scores: ' + str(max_scores), 60, 200)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(20)


while run_game():
    scores = 0
    make_jump = False
    jump_counter = 30
    user_y = display_h - user_h - 74
pygame.quit()
quit()