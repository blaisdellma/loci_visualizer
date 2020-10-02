import pygame, sys, random, math

W = 800
H = 600
scale = 120
dot_sz = 3

black = (0,0,0)
white = (255,255,255)

speeds = [10, 25, 50, 100, 200]
ispeed = 2

pygame.init()

screen = pygame.display.set_mode((W,H))
pygame.display.set_caption('Umbrella Locus')

screen.fill(black)
pygame.draw.line(screen,white,(int(W/2),H),(int(W/2),0))
pygame.draw.line(screen,white,(0,int(H/2)),(W,int(H/2)))

add_pt = 1

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                screen.fill(black)
                pygame.draw.line(screen,white,(int(W/2),H),(int(W/2),0))
                pygame.draw.line(screen,white,(0,int(H/2)),(W,int(H/2)))
            if event.key == pygame.K_p:
                add_pt = 1-add_pt
            if event.key == pygame.K_1:
                ispeed = 4
            if event.key == pygame.K_2:
                ispeed = 3
            if event.key == pygame.K_3:
                ispeed = 2
            if event.key == pygame.K_4:
                ispeed = 1
            if event.key == pygame.K_5:
                ispeed = 0


    if add_pt:

        th1 = random.uniform(0,math.pi)
        th2 = random.uniform(0,math.pi)

        x = math.cos(th1) + math.cos(th2)
        y = math.sin(th1) + math.sin(th2)

        x = int(W/2 + x*scale)
        y = int(H/2 - y*scale)

        #screen.set_at((x,y),white)
        pygame.draw.circle(screen,white,(x,y),dot_sz)

    pygame.display.flip()

    pygame.time.wait(speeds[ispeed])
