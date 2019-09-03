#Importing required modules

import pygame
import random
import os

#initializing pygame
pygame.init()

#initializing mixer,for music
pygame.mixer.init()

#defining colors
green=(153,255,51)
red=(255,0,0)
black=(0,0,0)
white=(255,255,255)
purple=(128,0,128)


#display settings

#1.creating window
screen_height=600
screen_width=900
gameWindow=pygame.display.set_mode((screen_width,screen_height))
#2.setting caption
pygame.display.set_caption("SNAKE GAME")

#image settings
bgimg=pygame.image.load('bg_image.jpg')
bgimg=pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

#clock initializing
clock = pygame.time.Clock()

#font setting for writing text to the screen
font = pygame.font.SysFont(None, 55)
font2 = pygame.font.SysFont(None, 25)
font3 = pygame.font.SysFont(None, 105)


def paused():
    ''' function to pause the game'''
    pause=True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                if event.key == pygame.K_c:
                    pygame.mixer.music.unpause()
                    pause=False


#writing text to the screen
def text_screen(text,color,x,y):
    '''function to pause the game'''
    screen_text=font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def text_screen_2(text,color,x,y):
    '''function to pause the game'''
    screen_text=font2.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def text_screen_3(text,color,x,y):
    '''function to pause the game'''
    screen_text=font3.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

#defining function to plot snake
def plot_snake(gameWindow,color,snk_lst,snake_size):
    ''' function to  plot snake'''
    for x,y in snk_lst:
        pygame.draw.rect(gameWindow, green, [x,y, snake_size, snake_size])

#the function which executes at the beginning of the loop
def welcome():
    exit_game=False
    pygame.mixer.music.load('back.mp3')
    pygame.mixer.music.play()
    while not exit_game:
            gameWindow.fill(purple)
            gameWindow.blit(bgimg, [0,0])
            text_screen("Press Enter",black,350,330)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:

                        gameloop()

            pygame.display.update()
            clock.tick(60)

#starting the game loop
def gameloop():
    # initializing game variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 4
    velocity_y = 4
    snake_size = 20
    init_size=5
    food_x = random.randint(50, screen_width / 2)
    food_y = random.randint(100, screen_height / 2)
    fps = 40
    score = 0
    snk_lst = []
    snk_len = 1


    #Creating the file hiscore.txt if not present and initializing the hiscore to 0
    if not os.path.exists('hiscore.txt'):
        with open('hiscore.txt', 'w') as f:
             f.write('0')

    #The content of the file hiscore.txt is read
    with open ('hiscore.txt','r') as f:
        hiscore=f.read()

    #Beginning of game loop
    while not exit_game:

        if game_over:
            with open('hiscore.txt','w') as f:
                f.write(str(hiscore))
            gameWindow.fill(black)
            text_screen_3("GAME  OVER",red,230,100)
            text_screen("Your Score: " + str(score), white, 350, 300)
            text_screen("Press ENTER to continue....",white,230,450)
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('back.mp3')
                        pygame.mixer.music.play()
                        gameloop()
        else:


            #Checking the key pressed by user

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game=True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_size
                        velocity_y=0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_size
                        velocity_y=0
                    if event.key == pygame.K_UP:
                        velocity_y = - init_size
                        velocity_x=0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_size
                        velocity_x=0

                    if event.key == pygame.K_p:
                        pygame.mixer.music.pause()
                        paused()
        #Updating the position of the snake based on the key pressed(taking velocity into consideration)

            snake_x+=velocity_x
            snake_y+=velocity_y

        #Getting new food to snake if the position of snake and food mathches approximately

            if abs(snake_x - food_x) <15 and  abs(snake_y - food_y) <15 :
                score+=10
                food_x = random.randint(50, screen_width * 3 /4 )
                food_y = random.randint(200, screen_height * 3 / 4)
                snk_len+=5
                if score> int(hiscore) :
                    hiscore=score

        #Updating the game window to white color and writing the parameters into the screen
            gameWindow.fill(white)
            # SCREEN FIELD WITH BORDER 3
            pygame.draw.rect(gameWindow, black, [0,60, 900, 540], 6)
            text_screen("Score: " + str(score)+" Hiscore: "+str(hiscore) , black, 5, 5)
            text_screen_2("p = pause", green, 750, 5)
            text_screen_2("c = continue", green, 750, 30)

        #Positioning of new food to snake
            pygame.draw.rect(gameWindow, red, [food_x, food_y, 15, 15])

        #Creating a temporary list and appending to snk_lst to position the growing snake
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_lst.append(head)

        #Maintaining the height of the snake
            if len(snk_lst) >snk_len:
                del snk_lst[0]

        #Boundary condition for game over
            if snake_x<10 or snake_y<59 or snake_x>screen_width-25 or snake_y>screen_height-25:
                game_over=True
                pygame.mixer.music.load('explo.mp3')
                pygame.mixer.music.play()

        #Condition for game over,if snake collids to itself
            if head in snk_lst[:-1]:
                game_over=True
                pygame.mixer.music.load('explo.mp3')
                pygame.mixer.music.play()

        #Calling the plot function to plot the updated snake
            plot_snake(gameWindow,red,snk_lst,snake_size)

        #Updating the display ,to notice the changes
        pygame.display.update()
        clock.tick(fps)

    #Loop exit condition
    pygame.quit()
    quit()

if __name__ == '__main__':
    welcome()






