#tap tap basketball
import pygame, sys, random   


pygame.init()  
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption('Tap Tap Basketball')
clock = pygame.time.Clock()

ball_acceleration = 0

ball_forward = 5
score = 0
ball_hooped = False

#LOADING IMAGES
#y is the hoop rim
y = random.randint(200, 400)
hoop = pygame.transform.scale(pygame.image.load('hoop.png').convert_alpha(), (150, 150))
hoop_rect = hoop.get_rect(topright=(600,y-20))
ball = pygame.transform.scale(pygame.image.load('ball.png').convert_alpha(), (70,70))
ball_rect = ball.get_rect(midbottom=(300, 800))
slamDunk = pygame.image.load('slam dunk.jpg').convert_alpha()

#LOADING TEXT
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)

#LOADING SOUND EFFECT
start = pygame.mixer.Sound('audio/start.wav')
tap = pygame.mixer.Sound('audio/tap.wav')
hooped = pygame.mixer.Sound('audio/hooped.wav')
hit = pygame.mixer.Sound('audio/hit.wav')
game_over =  pygame.mixer.Sound('audio/game over.wav')

time_before = 0
scores = list()
gameRunning = False
while True:
    current_time = pygame.time.get_ticks() 
                           
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if gameRunning:
            if event.type == pygame.MOUSEBUTTONDOWN:
                tap.play()
                if score%2==0:
                    ball_forward = 5
                else:
                    ball_forward = -5

                ball_acceleration = -25
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    time_before = pygame.time.get_ticks()
                    score = 0
                    start.play()
                    #move hoop to the right hand side
                    hoop = pygame.transform.scale(pygame.image.load('hoop.png').convert_alpha(), (150, 150))
                    hoop_rect = hoop.get_rect(topright=(600,y-20))
                    gameRunning = True
                    
          
    if gameRunning:
        screen.fill("Grey")
        
        screen.blit(ball, ball_rect)                 
        screen.blit(hoop, hoop_rect)

        #time management
        countdown = 5-(int((current_time - time_before)/1000))
        countdown_surf = text_font.render(f"countdown:{countdown}", True, "Red")
        countdown_rect = countdown_surf.get_rect(center=(500, 20))
        pygame.draw.rect(screen, "Yellow", countdown_rect)
        pygame.draw.rect(screen, "Yellow", countdown_rect, 2)
        screen.blit(countdown_surf, countdown_rect)
        #draw hoop board
        if score%2==0: pygame.draw.line(screen, (255,127,80), (585, y), (585, y-100), width=15)
        else: pygame.draw.line(screen, (255,127,80), (15, y), (15, y-100), width=15)
        #displaying current score
        score_surf = text_font.render(f"score:{score}", True, "Blue")
        score_rect = score_surf.get_rect(center=(100, 20))
        pygame.draw.rect(screen, "Orange", score_rect)
        pygame.draw.rect(screen, "Orange", score_rect, 2)
        screen.blit(score_surf, score_rect)
        
        #ball movement
        ball_acceleration += 1
        ball_rect.x += ball_forward
        ball_rect.y += ball_acceleration
        #ball touching the ground
        if ball_rect.bottom >= 800:
            ball_rect.bottom = 800
            #checks ball movement direction
            if score%2==0 : ball_forward = 1
            elif score%2==1: ball_forward = -1
        #ball touches the left or right side
        if ball_rect.right > 600: ball_rect.left = 1
        if ball_rect.left < 0: ball_rect.right = 599

        #check touching board
        if ((score%2==0) and (ball_rect.right >= 585) and (ball_rect.bottom>y-100 and ball_rect.top<y)) or ((score%2==1) and (ball_rect.left <= 15) and (ball_rect.bottom>y-100 and ball_rect.top<y)):
                ball_forward *= -1
                hit.play()
        
        #check enterring hoop
        if ball_acceleration > 0:
            if ((ball_rect.left>0 and ball_rect.right<150 and ball_rect.top>y and ball_rect.bottom<y+100) and (score%2==1)) or ((ball_rect.left>450 and ball_rect.right<600 and ball_rect.top>y and ball_rect.bottom<y+100) and (score%2==0)):
                if ball_hooped == False:
                    #moves hoop to the other side
                    hoop = pygame.transform.flip(hoop, True, False)
                    y = random.randint(200, 400)
                    if score%2==0: hoop_rect = hoop.get_rect(topleft=(0,y-20))
                    else: hoop_rect = hoop.get_rect(topright=(600,y-20))
                    
                    score += 1
                    hooped.play()
                    ball_hooped = True

                    time_before = pygame.time.get_ticks()
        if ball_acceleration < 0 or ball_rect.bottom >= 800:
            ball_hooped=False

        #check timeout
        if countdown==0:
            scores.append(score)
            game_over.play()
            gameRunning = False

        #move down vertically after enterring hoop
        if ball_hooped and ball_acceleration > 0:
            ball_forward = 0
    else:
        screen.fill((128, 128, 128))
        #display game name
        game_name = text_font.render("Tap Tap Basketball", True, "Green")
        game_rect = game_name.get_rect(center=(300, 50))
        screen.blit(game_name, game_rect)
        #slam dunk image
        slamDunk_rect = slamDunk.get_rect(midtop=(300, 100))
        screen.blit(slamDunk, slamDunk_rect)
                                          
        if time_before == 0:
            instructions = text_font.render("Tap to throw basketball into the hoop!", True, "Purple")
            instructions_rect = instructions.get_rect(center=(300, 550))
            pygame.draw.rect(screen, "Yellow", instructions_rect)
            pygame.draw.rect(screen, "Yellow", instructions_rect, 2)
            screen.blit(instructions, instructions_rect)
        else:
            score_msg = text_font.render(f"Score:{score}", True, "Purple")
            score_msg_rect = score_msg.get_rect(center=(300, 550))
            screen.blit(score_msg, score_msg_rect)
            high_score = text_font.render(f"Best:{max(scores)}", True, "Orange")
            high_score_rect = high_score.get_rect(center=(300, 600))
            screen.blit(high_score, high_score_rect)

    clock.tick(60)
    pygame.display.update()
    
