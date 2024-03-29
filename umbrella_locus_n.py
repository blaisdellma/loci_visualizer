import pygame, sys, random, math

def prob_scale(x,n):
    q = 2
    b = 0.5
    y1 = math.exp(-math.pow(q*x,2*n)) - math.exp(-math.pow(q,2*n))
    y2 = 1 - math.exp(-math.pow(q,2*n))
    y = y1/y2
    return (y+b*(1-x))/(1+b)

W = 800
H = 600
scale = 120
dot_sz = 3

n = 2
scale = 240/n

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
reset = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset = 1
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
            if event.key == pygame.K_6:
                ispeed = -1
            if event.key == pygame.K_PERIOD:
                if n < 6:
                    n += 1
                    scale = 240/n
                    reset = 1
                    print(n)
            if event.key == pygame.K_COMMA:
                if n > 1:
                    n -= 1
                    scale = 240/n
                    reset = 1
                    print(n)

    if reset:
        screen.fill(black)
        pygame.draw.line(screen,white,(int(W/2),H),(int(W/2),0))
        pygame.draw.line(screen,white,(0,int(H/2)),(W,int(H/2)))
        reset = 0

    if add_pt:

        ths = [random.uniform(0,1) for i in range(n)]
        ths = [math.pi*prob_scale(a,n) for a in ths]

        x = sum([math.cos(a) for a in ths])
        y = sum([math.sin(a) for a in ths])

        x = int(W/2 + x*scale)
        y = int(H/2 - y*scale)

        #screen.set_at((x,y),white)
        pygame.draw.circle(screen,white,(x,y),dot_sz)

    pygame.display.flip()

    if ispeed >= 0:
        pygame.time.wait(speeds[ispeed])
