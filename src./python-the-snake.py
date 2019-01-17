import pygame
import time
import random
import color

pygame.init()

screen_height = 600
screen_width = 800

gameDisplay = pygame.display.set_mode((screen_width, screen_height))

block_size = 20

apple_size = 20
apple_img = pygame.image.load("apple.jpg")

snake_size = 20
snake_head_img = pygame.image.load("snake_head.jpg")

direction = "right"
FPS = 15

clock = pygame.time.Clock()

default_Font = pygame.font.SysFont("ubuntu", 25)
small_Font = pygame.font.SysFont("ubuntu", 15)
medium_Font = pygame.font.SysFont("ubuntu", 30)
large_Font = pygame.font.SysFont("ubuntu", 50)

def game_intro():
    intro = True

    gameDisplay.fill(color.WHITE)
    display_message(
        "Welcome to Snake Xenzia!",
        color.DARKGREEN,
        y_displace=-120,
        size="large")

    display_message(
        "Eat those red apples and grow bigger as you do so.",
        color.BLACK,
        y_displace=-50)

    display_message(
        "If you try to eat yourself or the edges of the screen, you lose!",
        color.BLACK,
        y_displace=-20)

    pygame.draw.rect(gameDisplay, color.RED , [160, 500, 100, 50])
    pygame.draw.rect(gameDisplay, color.ORANGE, [350, 500, 120, 50])
    pygame.draw.rect(gameDisplay, color.DARKGREEN, [555, 500, 100, 50])

    text_to_button("Quit", color.BLACK, [160, 500, 100, 50], "medium")
    text_to_button("Menu", color.BLACK, [350, 500, 120, 50], "medium")
    text_to_button("Play", color.BLACK, [555, 500, 100, 50], "medium")
    pygame.display.update()

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_h:
                    show_highscores()

            handle_button("Play", color.BLACK, [555, 500, 100, 50],
                          active_color=color.GREEN, inactive_color=color.DARKGREEN, action="play")

            handle_button("Quit", color.BLACK, [160, 500, 100, 50],
                          active_color=color.LIGHTRED, inactive_color=color.RED, action="quit")

            handle_button("Menu", color.BLACK, [350, 500, 120, 50],
                          active_color=color.YELLOW, inactive_color=color.ORANGE, action="menu")

            pygame.display.update()
    clock.tick(5)


def countdown(screen_reset):
    # if screen_reset:
    #    gameDisplay.fill(color.WHITE)
    gameDisplay.fill(color.WHITE)

    for sec in range(3, 0, -1):
        display_message("Starting in: " + str(sec), color.BLUE,
                        y_displace=-100, size="medium")
        pygame.display.update()
        gameDisplay.fill(color.WHITE)
        time.sleep(1)


def show_highscores():
    pass


def game_menu():
    menu = True
    gameDisplay.fill(color.WHITE)

    display_message(
        "Menu",
        color.DARKGREEN,
        y_displace=-120,
        size="large")

    red_btn = [110, 500, 140, 50]
    orange_btn = [350, 500, 120, 50]
    green_btn = [555, 500, 160, 50]
    pygame.draw.rect(gameDisplay, color.RED, red_btn)
    pygame.draw.rect(gameDisplay, color.ORANGE, orange_btn)
    pygame.draw.rect(gameDisplay, color.DARKGREEN, green_btn)

    text_to_button("Settings", color.BLACK, red_btn, "medium")
    text_to_button("Home", color.BLACK, orange_btn, "medium")
    text_to_button("Highscores", color.BLACK, green_btn, "medium")
    pygame.display.update()

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    menu = False
                if event.key == pygame.K_h:
                    show_highscores()

            handle_button("Highscores", color.BLACK, green_btn,
                          active_color=color.GREEN, inactive_color=color.DARKGREEN, action="high_score")

            handle_button("Settings", color.BLACK, red_btn,
                          active_color=color.LIGHTRED, inactive_color=color.RED, action="settings")

            handle_button("Home", color.BLACK, orange_btn,
                          active_color=color.YELLOW, inactive_color=color.ORANGE, action="home")

            pygame.display.update()

        clock.tick(5)


def text_to_button(txt, txt_color, btn_properties, txt_size="default"):
    text_surf, text_rect = text_objects(txt, txt_color, txt_size)
    button_x = btn_properties[0]
    button_y = btn_properties[1]
    button_width = btn_properties[2]
    button_height = btn_properties[3]
    text_rect.center = (button_x + (button_width / 2)
                        ), (button_y + (button_height / 2))
    gameDisplay.blit(text_surf, text_rect)


def handle_button(text, text_color, btn_properties, active_color, inactive_color, action=None):
    button_x = btn_properties[0]
    button_y = btn_properties[1]
    width = btn_properties[2]
    height = btn_properties[3]

    mouse_coord = pygame.mouse.get_pos()
    # clicks = (1,0,0) means that left mouse button was pressed, others at rest
    clicks = pygame.mouse.get_pressed()

    if button_x + width > mouse_coord[0] > button_x and button_y + height > mouse_coord[1] > button_y:
        pygame.draw.rect(gameDisplay, active_color, [
                         button_x, button_y, width, height])
        if clicks[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "menu":
                game_menu()
            if action == "play":
                game_loop()
            if action == "home":
                game_intro()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, [
                         button_x, button_y, width, height])

    text_to_button(text, text_color, [button_x,
                                      button_y, width, height], "medium")


def snake(snake_list, snake_size):

    head = snake_head_img
    if direction == "right":
        head = pygame.transform.rotate(snake_head_img, 270)
    elif direction == "down":
        head = pygame.transform.rotate(snake_head_img, 180)
    elif direction == "left":
        head = pygame.transform.rotate(snake_head_img, 90)
    elif direction == "up":
        head = snake_head_img

    snake_head_x, snake_head_y = snake_list[-1][0], snake_list[-1][1]
    gameDisplay.blit(head, (snake_head_x, snake_head_y))

    for snake_coord in snake_list[:-1]:
        pygame.draw.rect(
            gameDisplay, color.DARKGREEN,
            [snake_coord[0], snake_coord[1], snake_size, snake_size])


def snake_eats_apple(x_coord, y_coord, apple_x_coord, apple_y_coord):
    if x_coord >= apple_x_coord and x_coord <= apple_x_coord + block_size:  # x axis bound crossed
        if y_coord >= apple_y_coord and y_coord <= apple_y_coord + block_size:  # y axis bound crossed
            apple_x_coord, apple_y_coord = generate_random_apple()
            return True

    elif x_coord > apple_x_coord and x_coord < apple_x_coord + apple_size or x_coord + snake_size > apple_x_coord and x_coord + snake_size < apple_x_coord + apple_size:
        if y_coord > apple_y_coord and y_coord < apple_y_coord + apple_size:
            return True

        elif y_coord + snake_size > apple_y_coord and y_coord + snake_size < apple_y_coord + apple_size:
            return True

    return False


def text_objects(text, text_color, size):
    if size == "small":
        text_surface = small_Font.render(text, True, text_color)
    elif size == "medium":
        text_surface = medium_Font.render(text, True, text_color)
    elif size == "large":
        text_surface = large_Font.render(text, True, text_color)
    else:
        text_surface = default_Font.render(text, True, text_color)

    return text_surface, text_surface.get_rect()


def display_message(msg, msg_color, y_displace=0, size="default"):
    text_surface, text_rect = text_objects(msg, msg_color, size)
    text_rect.center = (screen_width / 2), (screen_height / 2) + y_displace
    gameDisplay.blit(text_surface, text_rect)


def generate_random_apple():
    apple_x_coord = random.randrange(0, screen_width - apple_size)
    apple_x_coord = round(apple_x_coord)  # / 10.0) * 10.0

    apple_y_coord = random.randrange(0, screen_height - apple_size)
    apple_y_coord = round(apple_y_coord)  # /10.0) * 10.0

    return apple_x_coord, apple_y_coord


def draw_apple(x, y):
    gameDisplay.blit(apple_img, (x, y))


def is_game_over(x, y):
    if x > screen_width or x < 0 or y > screen_height or y < 0:
        return True
    elif x + snake_size > screen_width or x + snake_size < 0 or y + snake_size > screen_height or snake_size < 0:
        return True


def pause():
    paused = True
    # gameDisplay.fill(color.WHITE)
    display_message("Paused", color.BLACK, y_displace=-180, size="large")
    # display_message("Press C to continue or Q to quit", color.BLACK,y_displace= 25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)


def score(score):
    text = small_Font.render("Score: " + str(score), True, color.BLACK)
    gameDisplay.blit(text, [0, 0])


def upload_high_score(score):
    pass   #file = open("scores.txt", "w")
  ##  highscores = []
   # for line in file:
        #highscores.append(int(line))
    
    #highscores.append(int(score))
    #highscores = sorted(highscores)


def game_loop():
    global direction
    
    gameExit = False
    gameOver = False

    x_coord = screen_width / 2
    y_coord = screen_height / 2
    x_coord_change = snake_size  # snake starts moving as soon as game starts
    y_coord_change = 0

    snake_list = []
    snake_length = 1

    # in case apple starts at screen_width (say 800) then a 20 block_size apple will go till 810 which is out of screen
    # so we restrict it to screen_width -  - apple_size
    apple_x_coord, apple_y_coord = generate_random_apple()

    while not gameExit:

        gameDisplay.fill(color.WHITE)
        draw_apple(apple_x_coord, apple_y_coord)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                upload_high_score(snake_length - 1)
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                # to avoid clashing with oneself by "reverse gearing" direction
                    if direction == "right":
                        continue
                    x_coord_change = -snake_size
                    y_coord_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    if direction == "left":
                        continue
                    x_coord_change = snake_size
                    y_coord_change = 0
                    direction = "right"
                elif event.key == pygame.K_UP:
                    if direction == "down":
                        continue
                    y_coord_change = -snake_size
                    x_coord_change = 0
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    if direction == "up":
                        continue
                    y_coord_change = snake_size
                    x_coord_change = 0
                    direction = "down"
                elif event.key == pygame.K_p:
                    pause()
            

        while gameOver:

            gameDisplay.fill(color.BLACK)
            display_message(
                "Game Over!", color.RED, y_displace=-50, size="large")

            display_message(
                "Press C to Play Again or Q to Quit",
                color.WHITE,
                y_displace=50,
                size="small")

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    upload_high_score(snake_length - 1)
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        upload_high_score(snake_length - 1)
                        pygame.quit()
                        quit()

                    if event.key == pygame.K_c:
                        upload_high_score(snake_length - 1)
                        game_loop()

        gameOver = is_game_over(x_coord, y_coord)

        x_coord += x_coord_change
        y_coord += y_coord_change

        snake_head = []
        snake_head.insert(0, x_coord)
        snake_head.insert(1, y_coord)
        snake_list.append(snake_head)

        # As we add co-ordinates to the snake_list, we allow only a specific number of co-ordinates (=length of snake)
        # If more, delete the first added element in the list
        if len(snake_list) > snake_length:
            del snake_list[0]

        # handle crashing to ourself
        for each_segment in snake_list[:-1]:
            if each_segment == snake_head:
                gameOver = True

        snake(snake_list, snake_size)

        score(snake_length - 1)

        pygame.display.update()

        if snake_eats_apple(x_coord, y_coord, apple_x_coord, apple_y_coord):
            snake_length += 1
            apple_x_coord, apple_y_coord = generate_random_apple()

        # The Frame per seconds
        clock.tick(FPS)

game_intro()
countdown(True)
game_loop()

pygame.quit()
quit()
