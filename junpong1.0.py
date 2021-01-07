import os
import pygame
import keyboard
import threading
import time

pygame.init()

def musicplay(low, high):
    global music

    current_path = os.path.dirname(__file__)
    sound_path = os.path.join(current_path, "sounds")

    music = pygame.mixer.Sound(os.path.join(sound_path, "music.wav"))
    pygame.mixer.Sound.play(music)
        

def main():
    pygame.init()

    music = threading.Thread(target=musicplay, args=(1, 10000))
    music.start()

    global running

    screen_width = 800
    screen_height = 480

    main_font = pygame.font.Font(None, 60)
    main_font2 = pygame.font.Font(None, 40)

    screen = pygame.display.set_mode((screen_width, screen_height))
    current_path = os.path.dirname(__file__)

    image_path = os.path.join(current_path, "images")
    background = pygame.image.load(os.path.join(image_path, "background.png"))
    mainimage = pygame.image.load(os.path.join(image_path, "main.png"))

    pygame.display.set_icon(mainimage)
    pygame.display.set_caption("junpong1.0")

    running = True

    while running:
        if keyboard.is_pressed('enter'):
            maingame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.set_icon(mainimage)

        main = main_font.render("Press enter key to start", True, (255, 255, 255))
        title = main_font2.render("--JYJUNPONG--", True, (0, 255, 0))

        screen.blit(background, (0, 0))
        screen.blit(mainimage, (300, 0))
        screen.blit(title, (300, 220))
        screen.blit(main, (155, 290))

        pygame.display.update()
        

def maingame():
    pygame.init()

    global running
    global musicplayre

    musicplayre = True
    screen_width = 800 
    screen_height = 480

    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption("junpong1.0")

    clock = pygame.time.Clock()
    
    current_path = os.path.dirname(__file__)
    image_path = os.path.join(current_path, "images")
    sound_path = os.path.join(current_path, "sounds")

    background = pygame.image.load(os.path.join(image_path, "background.png"))

    stage = pygame.image.load(os.path.join(image_path, "ground.png"))
    stage_size = stage.get_rect().size
    stage_height = stage_size[1]

    character = pygame.image.load(os.path.join(image_path, "character.png"))
    character_size = character.get_rect().size
    character_width = character_size[0]
    character_height = character_size[1]
    character_x_pos = (screen_width / 2) - (character_width / 2)
    character_y_pos = screen_height - character_height - stage_height

    weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
    weapon_size = weapon.get_rect().size
    weapon_width = weapon_size[0]
    weapon_height = weapon_size[1]
    weapon_x_pos = character_x_pos
    weapon_y_pos = character_y_pos

    gameoversound = pygame.mixer.Sound(os.path.join(sound_path, "gameover.wav"))
    popsound = pygame.mixer.Sound(os.path.join(sound_path, "Pop.wav"))

    character_to_x = 0

    weapons = []

    weapon_speed = 10

    character_speed = 5

    ball = pygame.image.load(os.path.join(image_path, "ball.png"))

    pos_x = 50 
    pos_y = 50
    to_x = 3 
    to_y = -6
    init_spd_y = -18

    game_font = pygame.font.Font(None, 40)

    score = 0

    dtresult = 30

    while running:
        dt = clock.tick(dtresult)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    character_to_x -= character_speed
                elif event.key == pygame.K_d:
                    character_to_x += character_speed
                elif event.key == pygame.K_SPACE:
                    weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                    weapon_y_pos = character_y_pos
                    weapons.append([weapon_x_pos, weapon_y_pos])
                    if score >= 1:
                        score -= 1
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    character_to_x = 0

        character_x_pos += character_to_x

        if character_x_pos < 0:
            character_x_pos = 0

        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]
        weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
        
        ball_pos_x = pos_x
        ball_pos_y = pos_y

        ball_size = ball.get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            to_x = to_x * -1
            pygame.mixer.Sound.play(popsound)
            score += 1
            dtresult += 0.1

        if ball_pos_y >= screen_height - stage_height - ball_height:
            to_y = init_spd_y
            pygame.mixer.Sound.play(popsound)
            score += 1
            dtresult += 0.1

        else: 
            to_y += 0.5

        pos_x += to_x
        pos_y += to_y

        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        ball_rect = ball.get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        weapon_rect = weapon.get_rect()
        weapon_rect.left = weapon_x_pos
        weapon_rect.top = weapon_y_pos

        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]
            if weapon_rect.colliderect(ball_rect):
                pygame.mixer.Sound.play(popsound)
                to_x = to_x * -1
                to_y = to_y * -1
                score += 6
                del weapons[weapon_idx]

        if character_rect.colliderect(ball_rect):
            pygame.mixer.Sound.stop(music)
            pygame.mixer.Sound.play(gameoversound)

            gameovertext = game_font.render("Game Over", True, (255, 0, 0))
            lastscore = game_font.render("lastscore:" + str(score), True, (255, 0, 0))
            replay = game_font.render("if you want replay press enter", True, (255, 0, 0))

            screen.blit(gameovertext, (320, 220))
            screen.blit(lastscore, (320, 190))
            screen.blit(replay, (210, 250))

            pygame.display.update()
            
            while running:
                if keyboard.is_pressed('enter'):
                    score = 0
                    dtresult = 30
                    pos_x = 3
                    pos_y = -6
                    pygame.mixer.Sound.stop(gameoversound)
                    pygame.mixer.Sound.play(music)
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

        screen.blit(background, (0, 0))
        
        ball_pos_x = pos_x
        ball_pos_y = pos_y

        for weapon_x_pos, weapon_y_pos in weapons:
            screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
        screen.blit(ball, (ball_pos_x, ball_pos_y))
        screen.blit(stage, (0, screen_height - stage_height))
        screen.blit(character, (character_x_pos, character_y_pos))

        scoreboard = game_font.render("score:" + str(score), True, (255, 255, 255))
        speedboard = game_font.render("speed:" + str(int(dtresult)), True, (255, 255, 255))

        screen.blit(scoreboard, (10, 10))

        screen.blit(speedboard, (10, 40))

        if score >= 20:
            ball = pygame.image.load(os.path.join(image_path, "ball.png"))

            ball2 = pygame.image.load(os.path.join(image_path, "ball.png"))
            pos_x2 = 50 
            pos_y2 = 50
            to_x2 = 3 
            to_y2 = -6
            init_spd_y2 = -18

            game_font = pygame.font.Font(None, 40)
            
            running2 = True
            while running2:
                dt = clock.tick(dtresult)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        running2 = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            character_to_x -= character_speed
                        elif event.key == pygame.K_d:
                            character_to_x += character_speed
                        elif event.key == pygame.K_SPACE:
                            weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                            weapon_y_pos = character_y_pos
                            weapons.append([weapon_x_pos, weapon_y_pos])
                            if score >= 1:
                                score -= 1
                            
                    
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a or event.key == pygame.K_d:
                            character_to_x = 0

                character_x_pos += character_to_x

                if character_x_pos < 0:
                    character_x_pos = 0

                elif character_x_pos > screen_width - character_width:
                    character_x_pos = screen_width - character_width

                weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]
                weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
                
                ball_pos_x = pos_x
                ball_pos_y = pos_y

                ball_size = ball.get_rect().size
                ball_width = ball_size[0]
                ball_height = ball_size[1]

                ball2_pos_x = pos_x2
                ball2_pos_y = pos_y2

                ball2_size = ball2.get_rect().size
                ball2_width = ball2_size[0]
                ball2_height = ball2_size[1]

                if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
                    to_x = to_x * -1
                    pygame.mixer.Sound.play(popsound)
                    score += 1
                    dtresult += 0.25

                if ball_pos_y >= screen_height - stage_height - ball_height:
                    to_y = init_spd_y
                    pygame.mixer.Sound.play(popsound)
                    score += 1
                    dtresult += 0.25

                else: 
                    to_y += 0.5

                if ball2_pos_x < 0 or ball2_pos_x > screen_width - ball2_width:
                    to_x2 = to_x2 * -1
                    pygame.mixer.Sound.play(popsound)
                    score += 1
                    dtresult += 0.25

                if ball2_pos_y >= screen_height - stage_height - ball2_height:
                    to_y2 = init_spd_y2
                    pygame.mixer.Sound.play(popsound)
                    score += 1
                    dtresult += 0.25

                else: 
                    to_y2 += 0.5

                pos_x += to_x
                pos_y += to_y

                pos_x2 += to_x2
                pos_y2 += to_y2

                character_rect = character.get_rect()
                character_rect.left = character_x_pos
                character_rect.top = character_y_pos
                
                weapon_rect = weapon.get_rect()
                weapon_rect.left = weapon_x_pos
                weapon_rect.top = weapon_x_pos

                ball_rect = ball.get_rect()
                ball_rect.left = ball_pos_x
                ball_rect.top = ball_pos_y

                ball2_rect = ball2.get_rect()
                ball2_rect.left = ball2_pos_x
                ball2_rect.top = ball2_pos_y

                for weapon_idx, weapon_val in enumerate(weapons):
                    weapon_pos_x = weapon_val[0]
                    weapon_pos_y = weapon_val[1]
                    if weapon_rect.colliderect(ball_rect):
                        pygame.mixer.Sound.play(popsound)
                        to_x = to_x * -1
                        to_y = to_y * -1
                        score += 6
                        del weapons[weapon_idx]
                    elif weapon_rect.colliderect(ball2_rect):
                        pygame.mixer.Sound.play(popsound)
                        to_x2 = to_x2 * -1
                        to_y2 = to_y2 * -1
                        score += 6
                        del weapons[weapon_idx]

                if character_rect.colliderect(ball_rect):
                    pygame.mixer.Sound.stop(music)
                    pygame.mixer.Sound.play(gameoversound)

                    gameovertext = game_font.render("Game Over", True, (255, 0, 0))
                    lastscore = game_font.render("lastscore:" + str(score), True, (255, 0, 0))
                    replay = game_font.render("if you want replay press enter", True, (255, 0, 0))

                    screen.blit(gameovertext, (320, 220))
                    screen.blit(lastscore, (320, 190))
                    screen.blit(replay, (210, 250))

                    pygame.display.update()
                    
                    while running2:
                        if keyboard.is_pressed('enter'):
                            score = 0
                            dtresult = 30
                            pos_x = 3
                            pos_y = -6
                            pos_x2 = 30
                            pos_y2 = -20
                            pygame.mixer.Sound.stop(gameoversound)
                            pygame.mixer.Sound.play(music)
                            running2 = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running2 = False
                                running = False
                
                if character_rect.colliderect(ball2_rect):
                    pygame.mixer.Sound.stop(music)
                    pygame.mixer.Sound.play(gameoversound)

                    gameovertext = game_font.render("Game Over", True, (255, 0, 0))
                    lastscore = game_font.render("lastscore:" + str(score), True, (255, 0, 0))
                    replay = game_font.render("if you want replay press enter", True, (255, 0, 0))

                    screen.blit(gameovertext, (320, 220))
                    screen.blit(lastscore, (320, 190))
                    screen.blit(replay, (210, 250))

                    pygame.display.update()
                    
                    while running2:
                        if keyboard.is_pressed('enter'):
                            score = 0
                            dtresult = 30
                            pos_x = 3
                            pos_y = -6
                            pos_x2 = 30
                            pos_y2 = -20
                            pygame.mixer.Sound.stop(gameoversound)
                            pygame.mixer.Sound.play(music)
                            running2 = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running2 = False
                                running = False

                screen.blit(background, (0, 0))
                
                ball2_pos_x = pos_x2
                ball2_pos_y = pos_y2

                for weapon_x_pos, weapon_y_pos in weapons:
                    screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
                screen.blit(ball, (ball_pos_x, ball_pos_y))
                screen.blit(ball2, (ball2_pos_x, ball2_pos_y))
                screen.blit(stage, (0, screen_height - stage_height))
                screen.blit(character, (character_x_pos, character_y_pos))

                scoreboard = game_font.render("score:" + str(score), True, (255, 255, 255))
                speedboard = game_font.render("speed:" + str(int(dtresult)), True, (255, 255, 255))

                screen.blit(scoreboard, (10, 10))

                screen.blit(speedboard, (10, 40))
            
                pygame.display.update()

                if score >= 60:
                    ball = pygame.image.load(os.path.join(image_path, "ball.png"))

                    ball2 = pygame.image.load(os.path.join(image_path, "ball.png"))

                    ball3 = pygame.image.load(os.path.join(image_path, "ball.png"))
                    
                    pos_x3 = 50 
                    pos_y3 = 50
                    to_x3 = 3 
                    to_y3 = -6
                    init_spd_y3 = -18

                    game_font = pygame.font.Font(None, 40)
                    
                    running3 = True
                    while running3:
                        dt = clock.tick(dtresult)
                        
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False 
                                running2 = False
                                running3 = False

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_a:
                                    character_to_x -= character_speed
                                elif event.key == pygame.K_d:
                                    character_to_x += character_speed
                                elif event.key == pygame.K_SPACE:
                                    weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                                    weapon_y_pos = character_y_pos
                                    weapons.append([weapon_x_pos, weapon_y_pos])
                                    if score >= 1:
                                        score -= 1
                            
                            if event.type == pygame.KEYUP:
                                if event.key == pygame.K_a or event.key == pygame.K_d:
                                    character_to_x = 0

                        character_x_pos += character_to_x

                        if character_x_pos < 0:
                            character_x_pos = 0

                        elif character_x_pos > screen_width - character_width:
                            character_x_pos = screen_width - character_width

                        weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]
                        weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
                        
                        ball_pos_x = pos_x
                        ball_pos_y = pos_y

                        ball_size = ball.get_rect().size
                        ball_width = ball_size[0]
                        ball_height = ball_size[1]

                        ball2_pos_x = pos_x2
                        ball2_pos_y = pos_y2

                        ball2_size = ball2.get_rect().size
                        ball2_width = ball2_size[0]
                        ball2_height = ball2_size[1]

                        ball3_pos_x = pos_x3
                        ball3_pos_y = pos_y3

                        ball3_size = ball3.get_rect().size
                        ball3_width = ball3_size[0]
                        ball3_height = ball3_size[1]

                        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
                            to_x = to_x * -1
                            pygame.mixer.Sound.play(popsound)
                            score += 1
                            dtresult += 0.3

                        if ball_pos_y >= screen_height - stage_height - ball_height:
                            to_y = init_spd_y
                            pygame.mixer.Sound.play(popsound)
                            score += 1
                            dtresult += 0.3

                        else: 
                            to_y += 0.5

                        if ball2_pos_x < 0 or ball2_pos_x > screen_width - ball2_width:
                            to_x2 = to_x2 * -1
                            pygame.mixer.Sound.play(popsound)
                            score += 1
                            dtresult += 0.3

                        if ball2_pos_y >= screen_height - stage_height - ball2_height:
                            to_y2 = init_spd_y2
                            pygame.mixer.Sound.play(popsound)
                            score += 1
                            dtresult += 0.3

                        else: 
                            to_y2 += 0.5

                        if ball3_pos_x < 0 or ball3_pos_x > screen_width - ball3_width:
                            to_x3 = to_x3 * -1
                            pygame.mixer.Sound.play(popsound)
                            score += 1
                            dtresult += 0.3

                        if ball3_pos_y >= screen_height - stage_height - ball3_height:
                            to_y3 = init_spd_y3
                            pygame.mixer.Sound.play(popsound)
                            score += 1
                            dtresult += 0.3

                        else: 
                            to_y3 += 0.5

                        pos_x += to_x
                        pos_y += to_y

                        pos_x2 += to_x2
                        pos_y2 += to_y2

                        pos_x3 += to_x3
                        pos_y3 += to_y3

                        character_rect = character.get_rect()
                        character_rect.left = character_x_pos
                        character_rect.top = character_y_pos

                        ball_rect = ball.get_rect()
                        ball_rect.left = ball_pos_x
                        ball_rect.top = ball_pos_y

                        ball2_rect = ball2.get_rect()
                        ball2_rect.left = ball2_pos_x
                        ball2_rect.top = ball2_pos_y

                        ball3_rect = ball3.get_rect()
                        ball3_rect.left = ball3_pos_x
                        ball3_rect.top = ball3_pos_y
                        
                        weapon_rect = weapon.get_rect()
                        weapon_rect.left = weapon_x_pos
                        weapon_rect.top = weapon_y_pos

                        for weapon_idx, weapon_val in enumerate(weapons):
                            weapon_pos_x = weapon_val[0]
                            weapon_pos_y = weapon_val[1]
                            if weapon_rect.colliderect(ball_rect):
                                pygame.mixer.Sound.play(popsound)
                                to_x = to_x * -1
                                to_y = to_y * -1
                                score += 6
                                del weapons[weapon_idx]
                                

                        for weapon_idx, weapon_val in enumerate(weapons):
                            weapon_pos_x = weapon_val[0]
                            weapon_pos_y = weapon_val[1]
                            if weapon_rect.colliderect(ball2_rect):
                                pygame.mixer.Sound.play(popsound)
                                to_x = to_x * -1
                                to_y = to_y * -1
                                score += 6
                                del weapons[weapon_idx]

                        for weapon_idx, weapon_val in enumerate(weapons):
                            weapon_pos_x = weapon_val[0]
                            weapon_pos_y = weapon_val[1]
                            if weapon_rect.colliderect(ball3_rect):
                                pygame.mixer.Sound.play(popsound)
                                to_x = to_x * -1
                                to_y = to_y * -1
                                score += 6
                                del weapons[weapon_idx]

                        if character_rect.colliderect(ball_rect):
                            pygame.mixer.Sound.stop(music)
                            pygame.mixer.Sound.play(gameoversound)

                            gameovertext = game_font.render("Game Over", True, (255, 0, 0))
                            lastscore = game_font.render("lastscore:" + str(score), True, (255, 0, 0))
                            replay = game_font.render("if you want replay press enter", True, (255, 0, 0))

                            screen.blit(gameovertext, (320, 220))
                            screen.blit(lastscore, (320, 190))
                            screen.blit(replay, (210, 250))

                            pygame.display.update()
                            
                            while running3:
                                if keyboard.is_pressed('enter'):
                                    score = 0
                                    dtresult = 30
                                    pos_x = 3
                                    pos_y = -6
                                    pos_x2 = 30
                                    pos_y2 = -20
                                    pygame.mixer.Sound.stop(gameoversound)
                                    pygame.mixer.Sound.play(music)
                                    running2 = False
                                    running3 = False
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        running3 = False
                                        running2 = False
                                        running = False
                        
                        if character_rect.colliderect(ball2_rect):
                            pygame.mixer.Sound.stop(music)
                            pygame.mixer.Sound.play(gameoversound)

                            gameovertext = game_font.render("Game Over", True, (255, 0, 0))
                            lastscore = game_font.render("lastscore:" + str(score), True, (255, 0, 0))
                            replay = game_font.render("if you want replay press enter", True, (255, 0, 0))

                            screen.blit(gameovertext, (320, 220))
                            screen.blit(lastscore, (320, 190))
                            screen.blit(replay, (210, 250))

                            pygame.display.update()
                            
                            while running3:
                                if keyboard.is_pressed('enter'):
                                    score = 0
                                    dtresult = 30
                                    pos_x = 3
                                    pos_y = -6
                                    pos_x2 = 30
                                    pos_y2 = -20
                                    pygame.mixer.Sound.stop(gameoversound)
                                    pygame.mixer.Sound.play(music)
                                    running2 = False
                                    running3 = False
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        running3 = False
                                        running2 = False
                                        running = False

                        if character_rect.colliderect(ball3_rect):
                            pygame.mixer.Sound.stop(music)
                            pygame.mixer.Sound.play(gameoversound)

                            gameovertext = game_font.render("Game Over", True, (255, 0, 0))
                            lastscore = game_font.render("lastscore:" + str(score), True, (255, 0, 0))
                            replay = game_font.render("if you want replay press enter", True, (255, 0, 0))

                            screen.blit(gameovertext, (320, 220))
                            screen.blit(lastscore, (320, 190))
                            screen.blit(replay, (210, 250))

                            pygame.display.update()
                            
                            while running3:
                                if keyboard.is_pressed('enter'):
                                    score = 0
                                    dtresult = 30
                                    pos_x = 3
                                    pos_y = -6
                                    pos_x2 = 30
                                    pos_y2 = -20
                                    pygame.mixer.Sound.stop(gameoversound)
                                    pygame.mixer.Sound.play(music)
                                    running2 = False
                                    running3 = False
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        running3 = False
                                        running2 = False
                                        running = False

                        screen.blit(background, (0, 0))
                        
                        ball2_pos_x = pos_x2
                        ball2_pos_y = pos_y2

                        ball3_pos_x = pos_x3
                        ball3_pos_y = pos_y3
                        
                        for weapon_x_pos, weapon_y_pos in weapons:
                            screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
                        screen.blit(ball, (ball_pos_x, ball_pos_y))
                        screen.blit(ball2, (ball2_pos_x, ball2_pos_y))
                        screen.blit(ball3, (ball3_pos_x, ball3_pos_y))
                        screen.blit(stage, (0, screen_height - stage_height))
                        screen.blit(character, (character_x_pos, character_y_pos))

                        scoreboard = game_font.render("score:" + str(score), True, (255, 255, 255))
                        speedboard = game_font.render("speed:" + str(int(dtresult)), True, (255, 255, 255))

                        screen.blit(scoreboard, (10, 10))

                        screen.blit(speedboard, (10, 40))
                    
                        pygame.display.update()
    
        pygame.display.update()

main()

pygame.quit()