import pygame
import random
import time

pygame.init()

bounce_sound = pygame.mixer.Sound("bounce.ogg")
dead_sound = pygame.mixer.Sound("woosh.ogg")

# colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,128,0)
sky = (0,191,255)
gold = (255,215,0)
golden_yellow = (255,223,0)

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

flag = True
started = False
gameOver = False
gameExit = False

ball_pos = [int(WIDTH / 2), int(HEIGHT / 2)]
ball_vel = [0,0]

paddle1_pos = [0, int(HEIGHT / 2)]
paddle2_pos = [0, int(HEIGHT / 2)]

paddle1_vel = 0
paddle2_vel = 0


score1 = 0
score2 = 0

final_score = 10

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Go PONG!')

icon = pygame.image.load('pong.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

def text_objects(text, color, text_font):
    textSurface = text_font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, button_x, button_y, button_width, button_height, font, text_size):
    text_font = pygame.font.SysFont(font, text_size)
    textSurf, textRect = text_objects(msg , color, text_font)
    textRect.center = ((button_x + (button_width / 2)), button_y + (button_height / 2))
    gameDisplay.blit(textSurf, textRect)

def message_to_screen(msg, color, pos1, pos2, font, text_size):
    text_font = pygame.font.SysFont(font, text_size)
    textSurf, textRect = text_objects(msg, color, text_font)
    textRect.center = pos1, pos2
    gameDisplay.blit(textSurf, textRect)

def button(text, x, y, width, height, font, text_size, color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        text_to_button(text, color, x, y, width, height, font, text_size + 5)
        if click[0] == 1 and action != None:
            if action == "intro":
                game_intro()
                
            if action == "quit":
                pygame.quit()
                quit()
                
            if action == "about":
               game_about()
               
            if action == "play":
                game_loop()
    else:
        text_to_button(text, color, x, y, width, height, font, text_size)

    


def game_intro():
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(black)
        message_to_screen("GO PONG!", golden_yellow, WIDTH / 2, HEIGHT / 2 - HEIGHT / 8, 'comicsansms', 100)


        button("NEW GAME", WIDTH / 2 - WIDTH / 12, HEIGHT / 2 + HEIGHT / 6, 100, 20, "sans-serif", 30, green, action="play")
        button("ABOUT", WIDTH / 2 - WIDTH / 12, HEIGHT / 2 + HEIGHT / 4, 100, 20, "sans-serif", 30, green, action="about")
        button("QUIT", WIDTH / 2 - WIDTH / 12, HEIGHT / 2 + HEIGHT / 3, 100, 20, "sans-serif", 30, red, action="quit")
        
        pygame.display.update()
        clock.tick(15)

def game_about():
    about = True

    while about:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black)
        message_to_screen("ABOUT", golden_yellow, WIDTH / 2, HEIGHT / 2 - HEIGHT / 4, 'comicsansms', 100)

        message_to_screen("This game is another version of the famous ARCADE game PONG!", sky, WIDTH / 2, HEIGHT / 2, 'times new roman', 15)
        message_to_screen("This is a TWO-PLAYER Game!", sky, WIDTH / 2, HEIGHT / 2 + HEIGHT / 12, 'times new roman', 15)
        message_to_screen("Use 'w' & 's' to control the paddle on the left, 'up_arrow' & 'down_arrow' to control the right.",
                          sky, WIDTH / 2, HEIGHT / 2 + HEIGHT / 6, 'times new roman', 15)
        message_to_screen("The player who misses 10 balls first loses.",sky, WIDTH / 2, HEIGHT / 2 + HEIGHT / 4, 'times new roman', 15)
            

        button("MAIN MENU", WIDTH / 2 - WIDTH / 12, HEIGHT / 2 + HEIGHT / 2.5, 100, 20, "sans-serif", 30, green, action="intro")

        pygame.display.update()
        clock.tick(15)

def game_play():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global ball_pos, ball_vel
    global flag

    # update ball position
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # update paddle position
    
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    
    if paddle1_pos[1] <= 40:
        paddle1_pos[1] = 40
    if paddle2_pos[1] <= 40:
        paddle2_pos[1] = 40
    if paddle1_pos[1] >= HEIGHT - 40:
        paddle1_pos[1] = HEIGHT - 40
    if paddle2_pos[1] >= HEIGHT - 40:
        paddle2_pos[1] = HEIGHT - 40

    # determine whether paddle and ball collide
    # also handles ball and wall collision 
        
    if ball_pos[1]-BALL_RADIUS<=0 or ball_pos[1]+BALL_RADIUS>=HEIGHT:
        ball_vel[1] *= -1
        pygame.mixer.Sound.play(bounce_sound)
    if ball_pos[0]-BALL_RADIUS<=PAD_WIDTH and ball_pos[1]>=(paddle1_pos[1] - 40) and ball_pos[1]<=paddle1_pos[1] + 40:
        ball_vel[0] *= -1
        ball_vel[0] += 1
        flag = True
        pygame.mixer.Sound.play(bounce_sound)
    elif ball_pos[0]+BALL_RADIUS>=WIDTH-PAD_WIDTH and ball_pos[1]>=(paddle2_pos[1] - 40) and ball_pos[1]<=paddle2_pos[1] + 40:
        ball_vel[0] *= -1
        ball_vel[0] -= 1
        flag = False
        pygame.mixer.Sound.play(bounce_sound)
    elif ball_pos[0]-BALL_RADIUS<=PAD_WIDTH or ball_pos[0]+BALL_RADIUS>=WIDTH-PAD_WIDTH:
        spawn_ball(flag)
        pygame.mixer.Sound.play(dead_sound)

def reset():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global ball_pos, ball_vel
    global started
    
    ball_vel = [0,0]
    ball_pos = [int(WIDTH / 2), int(HEIGHT / 2)]
    paddle1_pos = [0, int(HEIGHT / 2)]
    paddle2_pos = [0, int(HEIGHT / 2)]

    started = False

def spawn_ball(direction):
    global ball_pos, ball_vel
    global flag
    global score1, score2
    global gameOver
    ball_pos = [int(WIDTH / 2), int(HEIGHT / 2)]

    # changes direction if ball goes out of bound
    
    if direction == True:
        ball_vel[0] = -random.randrange(3,6)
        flag = False
        score1 += 1
        if score1 == final_score:
            gameOver = True
    else:
        ball_vel[0] = random.randrange(3,6)
        flag = True
        score2 += 1
        if score2 == final_score:
            gameOver = True
    
    if random.randrange(0,2) == 0:    
        ball_vel[1] = -random.randrange(2,5)
    else:
        ball_vel[1] = random.randrange(2,5)

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global ball_pos, ball_vel
    global flag
    global score1, score2
    global gameOver
    ball_pos = [int(WIDTH / 2), int(HEIGHT / 2)]
    paddle1_pos = [0, int(HEIGHT / 2)]
    paddle2_pos = [0, int(HEIGHT / 2)]

    # random ball velocity
    if random.randrange(0,2) == 0:
        ball_vel[0] = random.randrange(3,6)
        flag = True
    else:
        ball_vel[0] = -random.randrange(3,6)
        flag = False

    if random.randrange(0,2) == 0:    
        ball_vel[1] = -random.randrange(2,5)
    else:
        ball_vel[1] = random.randrange(2,5)

    gameOver = False
    score1 = 0
    score2 = 0

def draw():
    pygame.draw.line(gameDisplay, white, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1)
    pygame.draw.line(gameDisplay, white, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(gameDisplay, white, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(gameDisplay, red, ball_pos, 20, 0)
    pygame.draw.line(gameDisplay, white, [4, paddle1_pos[1] - 40],[4, paddle1_pos[1] + 40], PAD_WIDTH)
    pygame.draw.line(gameDisplay, white, [WIDTH - PAD_WIDTH + 4, paddle2_pos[1] - 40],[WIDTH - PAD_WIDTH + 4, paddle2_pos[1] + 40], PAD_WIDTH)

def key_event():

    global paddle1_vel, paddle2_vel
    global paddle1_pos, paddle2_pos

    global gameExit
    global started
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not started:
                started = True
                new_game()
            if event.key == pygame.K_w:
                paddle1_vel -= 4
            elif event.key == pygame.K_s:
                paddle1_vel += 4
            elif event.key == pygame.K_UP:
                paddle2_vel -= 4
            elif event.key == pygame.K_DOWN:
                paddle2_vel += 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                paddle1_vel = 0
            elif event.key == pygame.K_s:
                paddle1_vel = 0
            elif event.key == pygame.K_UP:
                paddle2_vel = 0
            elif event.key == pygame.K_DOWN:
                paddle2_vel = 0

def show_score():
    message_to_screen(str(score1), green, WIDTH / 2 - WIDTH / 4, HEIGHT / 4, "sans-serif", 50)
    message_to_screen(str(score2), green, WIDTH / 2 + WIDTH / 4, HEIGHT / 4, "sans-serif", 50)


def game_loop():

    while not gameExit:
        gameDisplay.fill(black)
        
        if gameOver:
            reset()
            if score1 == final_score:
                message_to_screen("Player 1", gold, WIDTH / 2 - WIDTH / 4, HEIGHT / 2 - 30, 'comicsansms', 70)
                message_to_screen("Wins!", gold, WIDTH / 2 - WIDTH / 4, HEIGHT / 2 + 30, 'comicsansms', 50)
            if score2 == final_score:
                message_to_screen("Player 2", gold, WIDTH / 2 + WIDTH / 4, HEIGHT / 2 - 30, 'comicsansms', 70)
                message_to_screen("Wins!", gold, WIDTH / 2 + WIDTH / 4, HEIGHT / 2 + 30, 'comicsansms', 50)
            
        
        if not started:
            message_to_screen("Press SPACE to start the game", sky, WIDTH / 2, HEIGHT / 12, "sans-serif", 30)
            
        key_event()
        
        game_play()
        draw()

        show_score()
        
        pygame.display.update()

        clock.tick(60)
        

    pygame.quit()
    quit()
    
game_intro()
game_loop()
