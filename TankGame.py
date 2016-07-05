import pygame
import random

pygame.init()
pygame.display.set_caption('Tanks')
clock = pygame.time.Clock()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))

fire_sound = pygame.mixer.Sound('boom1.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')



#menu button,mouse[0] is x, mouse[1] is y
#click[0] == 1 means mouse button was pressed
def button_type(z, color,bright_color,action):
    mouse = pygame.mouse.get_pos()
    #define click
    click = pygame.mouse.get_pressed()

    if z+100 > mouse[0] > z and 520 > mouse[1] > 470:
        #               screen    color          x    y    w    h
        pygame.draw.rect(screen, color, (z, 470, 100, 50))
        #button click set to 1,action for exact button
        if click[0] == 1 and action != None:
            if action == "play":
                game_loop()
            elif action == "play_again":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(screen, bright_color, (z, 470, 100, 50))
#our tank function
def tank(x, y,turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x-27,y-2),
                       (x-26,y-5),
                       (x-25,y-8),
                       (x-23,y-12),
                       (x-21,y-14),
                       (x-20,y-17),
                       (x-18,y-19),
                       (x-16,y-21),
                       (x-14,y-23)
                       ]


    #                                   width  height  radius
    pygame.draw.circle(screen, black, (x,y), tankHeight/2)
    pygame.draw.rect(screen, black, (x-tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(screen, black, (x,y),possibleTurrets[turPos],turretWidth)
    pygame.draw.circle(screen, black, (x, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x+5, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x-5, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x+10, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x-10, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x+15, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x-15, y+23), wheelWidth)

    return possibleTurrets[turPos]


def enemy_tank(x, y, turPos):
    x = int(x)
    y = int(y)

    possibleTurrets = [(x+27,y-2),
                       (x+26,y-5),
                       (x+25,y-8),
                       (x+23,y-12),
                       (x+21,y-14),
                       (x+20,y-17),
                       (x+18,y-19),
                       (x+16,y-21),
                       (x+14,y-23)
                       ]


    #                                   width  height  radius
    pygame.draw.circle(screen, black, (x,y), tankHeight/2)
    pygame.draw.rect(screen, black, (x-tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(screen, black, (x,y),possibleTurrets[turPos],turretWidth)
    pygame.draw.circle(screen, black, (x, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x+5, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x-5, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x+10, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x-10, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x+15, y+23), wheelWidth)
    pygame.draw.circle(screen, black, (x-15, y+23), wheelWidth)

    return possibleTurrets[turPos]


#random barrier near middle
def barrier(xlocation,randomHeight, barrier_width):
        pygame.draw.rect(screen, black, (xlocation, screen_height-randomHeight,barrier_width,randomHeight))

#define explosion
def explosion(x, y):
    pygame.mixer.Sound.play(explosion_sound)
    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        startPoint = x, y

        colorChoices = [red,bright_red,green,bright_green, yellow]

        magnitude = 1
        while magnitude < explosion_size:

            exploding_bit_x = x + random.randrange(-1*magnitude,magnitude)
            exploding_bit_y = y + random.randrange(-1*magnitude,magnitude)
            pygame.draw.circle(screen, colorChoices[random.randrange(0,5)],(exploding_bit_x,exploding_bit_y),random.randrange(1,5))
            magnitude += 1
            pygame.display.update()
            clock.tick(100)
        explode = False
#define a fire function
def fireShell(xy, tankx, tanky, currentTurPos,gun_power,xlocation,barrier_width,randomHeight,enemytankX,enemytankY):
    pygame.mixer.Sound.play(fire_sound)
    fire = True
    damage = 0
    startingShell = list(xy)
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(screen, red,(startingShell[0],startingShell[1]),5)

        startingShell[0] -= (12 - currentTurPos)*2

        # y**2 so x wont be in the negatives
        startingShell[1] += int((((startingShell[0]-xy[0])*0.01/(gun_power/50.0))**2) - (currentTurPos+currentTurPos/(12-currentTurPos)))

        if startingShell[1] > screen_height-ground_height:
            hit_x = int((startingShell[0]*(screen_height-ground_height))/startingShell[1])
            hit_y = int(screen_height-ground_height)
            if enemytankX + 10 > hit_x > enemytankX - 10:
                print "CRITICAL HIT"
                damage = 25
            elif enemytankX + 15 > hit_x > enemytankX - 15:
                print "HARD HIT"
                damage = 18
            elif enemytankX + 25 > hit_x > enemytankX - 25:
                print "MEDIUM HIT"
                damage = 10
            elif enemytankX + 35 > hit_x > enemytankX - 35:
                print "LIGHT HIT"
                damage = 5
            explosion(hit_x,hit_y)
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation

        check_y_1 = startingShell[1] <= screen_height
        check_y_2 = startingShell[1] >= screen_height- randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int((startingShell[0]*screen_height)/startingShell[1])
            hit_y = int(startingShell[1])
            explosion(hit_x,hit_y)
            fire = False

        pygame.display.update()
        clock.tick(60)
    return damage
def e_fireShell(xy, tankx, tanky, currentTurPos,gun_power,xlocation,barrier_width,randomHeight,ptankx,ptanky):
    damage = 0
    currentPower = 1
    power_found = False

    while not power_found:
        currentPower += 1
        if currentPower > 65:
            power_found = True
        fire = True
        startingShell = list(xy)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #pygame.draw.circle(screen, red,(startingShell[0],startingShell[1]),5)

            startingShell[0] += (12 - currentTurPos)*2
            startingShell[1] += int((((startingShell[0]-xy[0])*0.01/(currentPower/50.0))**2) - (currentTurPos+currentTurPos/(12-currentTurPos)))

            if startingShell[1] > screen_height-ground_height:
                hit_x = int((startingShell[0]*(screen_height-ground_height))/startingShell[1])
                hit_y = int(screen_height-ground_height)
                #explosion(hit_x,hit_y)
                if ptankx +15 > hit_x > ptankx - 15:
                    power_found = True
                fire = False

            check_x_1 = startingShell[0] <= xlocation + barrier_width
            check_x_2 = startingShell[0] >= xlocation

            check_y_1 = startingShell[1] <= screen_height
            check_y_2 = startingShell[1] >= screen_height- randomHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int((startingShell[0]*screen_height)/startingShell[1])
                hit_y = int(startingShell[1])
                #explosion(hit_x-barrier_width,hit_y)
                fire = False
        pygame.display.update()
        clock.tick(60)
    pygame.mixer.Sound.play(fire_sound)
    fire = True
    startingShell = list(xy)
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(screen, red,(startingShell[0],startingShell[1]),5)

        startingShell[0] += (12 - currentTurPos)*2

        # y**2 so x wont be in the negatives
        gun_power = random.randrange(int(currentPower*0.90), int(currentPower*1.1))
        startingShell[1] += int((((startingShell[0]-xy[0])*0.01/(gun_power/50.0))**2) - (currentTurPos+currentTurPos/(12-currentTurPos)))

        if startingShell[1] > screen_height-ground_height:
            hit_x = int((startingShell[0]*(screen_height-ground_height))/startingShell[1])
            hit_y = int(screen_height-ground_height)
            if ptankx + 10 > hit_x > ptankx - 10:
                print "CRITICAL HIT"
                damage = 25
            elif ptankx + 15 > hit_x > ptankx - 15:
                print "HARD HIT"
                damage = 18
            elif ptankx + 25 > hit_x > ptankx - 25:
                print "MEDIUM HIT"
                damage = 10
            elif ptankx + 35 > hit_x > ptankx - 35:
                print "LIGHT HIT"
                damage = 5
            explosion(hit_x,hit_y)
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation

        check_y_1 = startingShell[1] <= screen_height
        check_y_2 = startingShell[1] >= screen_height- randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int((startingShell[0]*screen_height)/startingShell[1])
            hit_y = int(startingShell[1])
            explosion(hit_x,hit_y)
            fire = False




        pygame.display.update()
        clock.tick(60)
    return damage
def power(level):
    message_to_screen("Power: " + str(level) + "%",black,25,0,0)

def button_font(value,button_width,button_height):
    small_text = pygame.font.Font('freesansbold.ttf',20)
    text = small_text.render(value,True,(0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = button_width
    textRect.centery = button_height
    screen.blit(text,textRect)

def message_to_screen(msg,color,size,w,h):
    Small_text = pygame.font.Font('freesansbold.ttf',size)
    screen_text = Small_text.render(msg, True, color)
    screen.blit(screen_text,(w,h))

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(white)
        basicfont = pygame.font.Font('freesansbold.ttf', 100)
        text = basicfont.render('Tank Wars', True, (0, 0, 0), (255, 255, 255))
        screen.blit(text,(120,100))
        message_to_screen("Shoot the other tank to survive!",red,25,150,260)
        message_to_screen("Press SPACE to shoot",red,25,150,290)
        message_to_screen("Press Up or Down to move turret!",red,25,150,320)
        message_to_screen("Press Left or Right to move tank!",red,25,150,350)

        mouse = pygame.mouse.get_pos()

        button_type(200,green,bright_green,"play")
        button_font('GO!',250,495)

        button_type(500,red,bright_red,"quit")
        button_font('Quit',550,495)

        pygame.display.update()
        clock.tick(5)

def game_over():
    game_over = True

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(white)
        basicfont = pygame.font.Font('freesansbold.ttf', 100)
        text = basicfont.render('Game Over!', True, (0, 0, 0), (255, 255, 255))
        screen.blit(text,(120,100))
        message_to_screen("",red,25,80,360)

        mouse = pygame.mouse.get_pos()

        button_type(200,green,bright_green,"play_again")
        button_font('Play again',250,495)

        button_type(500,red,bright_red,"quit")
        button_font('Quit',550,495)

        pygame.display.update()
        clock.tick(5)
def game_win():
    game_over = True

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(white)
        basicfont = pygame.font.Font('freesansbold.ttf', 100)
        text = basicfont.render('You Won!', True, (0, 0, 0), (255, 255, 255))
        screen.blit(text,(120,100))
        message_to_screen("",red,25,80,360)

        mouse = pygame.mouse.get_pos()

        button_type(200,green,bright_green,"play_again")
        button_font('Play again',250,495)

        button_type(500,red,bright_red,"quit")
        button_font('Quit',550,495)

        pygame.display.update()
        clock.tick(5)

tankWidth = 40
tankHeight = 20
tank_wheel_fix = 725
turretWidth = 5

wheelWidth = 5

ground_height = 35

red = (255, 0, 0)
green = (0, 255, 0)
bright_green = (0, 200, 0)
bright_red = (200, 0, 0)
yellow = (200, 200, 0)
white = (255, 255, 255)
black = (0, 0, 0)
FPS = 15
explosion_size = 50

def health_bars(player_health, enemy_health):
    if player_health > 75:
        player_health_color = green
    elif player_health >= 50:
        player_health_color = yellow
    else:
        player_health_color = red

    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health >= 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red
    pygame.draw.rect(screen,player_health_color,(680, 25, player_health, 25))
    pygame.draw.rect(screen,enemy_health_color,(20, 25, enemy_health, 25))
    message_to_screen(str(player_health)+"%",black,15,710,32)
    message_to_screen(str(enemy_health)+"%",black,15,50,32)



def game_loop():

    game = True
    maintankX = screen_width * 0.9
    maintankY = screen_height * 0.9
    tankMove = 0
    xlocation = (screen_width/2) + random.randint(-0.1*screen_width,0.1*screen_width)
    randomHeight = random.randrange(screen_height*0.1,screen_height*0.6)

    player_health = 100
    enemy_health = 100

    barrier_width = 50
    # turret current pos and the changetur for key presses
    currentTurPos = 0
    changeTur = 0

    enemytankX = screen_width * 0.1
    enemytankY = screen_height * 0.9

    fire_power = 50
    power_change = 0

    tank_speed = 5

    while game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tankMove -= tank_speed
                elif event.key == pygame.K_RIGHT:
                    tankMove += tank_speed
                elif event.key == pygame.K_UP:
                    changeTur = 1
                elif event.key == pygame.K_DOWN:
                    changeTur = -1
                elif event.key == pygame.K_SPACE:
                    damage = fireShell(gun,maintankX,maintankY,currentTurPos,fire_power,xlocation,barrier_width,randomHeight,enemytankX,enemytankY)
                    enemy_health -= damage

                    possible_movement = ['f','r']
                    move_index = random.randrange(0,2)
                    #random range to be multiplied with random f or r movement
                    #for the tank to move,random range because it's more fun
                    #if you put a number there, the enemy tank will move the
                    #same amount of pixels every freaking time!
                    for x in range(random.randrange(2,10)):

                        if screen_width * 0.3 > enemytankX > screen_width * 0.03:
                            if possible_movement[move_index] == "f":
                                enemytankX += 5
                            elif possible_movement[move_index] == "r":
                                enemytankX -= 5

                            currentTurPos = 0
                            screen.fill(white)
                            health_bars(player_health,enemy_health)
                            gun = tank(maintankX, maintankY, currentTurPos)
                            enemy_gun = enemy_tank(enemytankX, enemytankY, 8)
                            fire_power += power_change
                            barrier(xlocation,randomHeight, barrier_width)
                            screen.fill(green, rect=[0,screen_height-ground_height, screen_width,ground_height])
                            pygame.display.update()
                            clock.tick(FPS)

                    damage = e_fireShell(enemy_gun,enemytankX,enemytankY,8,50,xlocation,barrier_width,randomHeight,maintankX,maintankY)
                    player_health -= damage
                    if player_health <= 0:
                        game_over()
                    elif enemy_health <= 0:
                        game_win()
                elif event.key == pygame.K_a:
                    power_change -= 1
                elif event.key == pygame.K_d:
                    power_change += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0



        maintankX += tankMove
        currentTurPos += changeTur
        #turret error out of range fix
        if currentTurPos > 8:
            currentTurPos = 8
        elif currentTurPos < 0:
            currentTurPos = 0
        screen.fill(white)
        health_bars(player_health,enemy_health)
        #after we added return the turret pos, we put it in the gun in order to fire
        gun = tank(maintankX, maintankY, currentTurPos)
        enemy_gun = enemy_tank(enemytankX, enemytankY, 8)
        fire_power += power_change
        if maintankX - (tankWidth/2) < xlocation+barrier_width:
            maintankX += tank_speed
        if maintankX + (tankWidth/2) > screen_width:
            maintankX -= tank_speed
        if fire_power > 67:
            fire_power = 67
        elif fire_power < 3:
            fire_power = 3
        #display fire power
        power(fire_power)
        #dispaly tank
        barrier(xlocation,randomHeight, barrier_width)
        screen.fill(green, rect=[0,screen_height-ground_height, screen_width,ground_height])
        pygame.display.update()
        clock.tick(FPS)
game_intro()

