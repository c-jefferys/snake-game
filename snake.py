import pygame
import time
import random

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.update()
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 102)

snake_size = 10  # size of snake blocks
snake_speed = 30

score_font = pygame.font.SysFont(None, 25)
msg_font = pygame.font.SysFont(None, 50)


# draw the snake
def snake(block_size, snake_list):
    for loc in snake_list:
        pygame.draw.rect(screen, green, [loc[0], loc[1], block_size, block_size])


# show score in top left of window
def show_score(score):
    value = score_font.render('Score: ' + str(score), True, yellow)
    screen.blit(value, [0, 0])


# show other messages (game over, etc.)
def message(msg, color):
    mesg = msg_font.render(msg, True, color)
    screen.blit(mesg, mesg.get_rect(center=screen.get_rect().center))


def game_loop():
    # starting snake values
    x = screen_width / 2
    y = screen_height / 2

    # values for changes based on movement key
    x_change = 0
    y_change = 0

    # randomly generated food placement
    food_x = round(random.randrange(0, screen_width - snake_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, screen_height - snake_size) / 10.0) * 10.0

    snake_list = []  # stores snake body blocks
    snake_length = 1

    running = True
    game_over = False

    while running:
        # waits for user at game over screen
        while game_over:
            screen.fill(black)
            message('You Lost! Press Q-Quit or C-Play Again', red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # exit game
                        running = False
                        game_over = False
                    elif event.key == pygame.K_c:  # start a new game
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    x_change = 0
                    y_change = -snake_size
                elif event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = snake_size

        # snake hit the edge of screen
        if x >= screen_width or x < 0 or y >= screen_height or y < 0:
            game_over = True

        x += x_change
        y += y_change

        screen.fill(black)

        # draw food
        pygame.draw.rect(screen, red, [food_x, food_y, snake_size, snake_size])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]  # don't increase snake size

        for block in snake_list[:-1]:
            if block == snake_head:  # snake hit itself
                game_over = True

        snake(snake_size, snake_list)
        show_score(snake_length - 1)

        pygame.display.update()

        # food has been eaten
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, screen_width - snake_size) / 10.0) * 10.0  # get rand x for food
            food_y = round(random.randrange(0, screen_height - snake_size) / 10.0) * 10.0  # get rand y for food
            snake_length += 1  # increase snake length on next frame

        clock.tick(snake_speed)

    pygame.quit()
    quit()


game_loop()
