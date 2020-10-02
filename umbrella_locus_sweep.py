import pygame, sys, random, math

W = 800
H = 600
scale = 120
dot_sz = 3

n = 2
scale = 240/n

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
colors = [red, green, blue]
ncolors = len(colors)

speeds = [10, 25, 50, 100, 200]
ispeed = 2

pygame.init()

screen = pygame.display.set_mode((W,H))
pygame.display.set_caption('Umbrella Locus')

def blank():
    screen.fill(black)
    pygame.draw.line(screen,white,(int(W/2),H),(int(W/2),0))
    pygame.draw.line(screen,white,(0,int(H/2)),(W,int(H/2)))

add_pt = 1
pts = []
indices = [0 for x in range(n)]

def reset():
    pts.clear()
    indices.clear()
    indices.extend([0 for x in range(n)])
    print('RESET')


n_step = 20
th_step = math.pi/n_step
sweep_home = 0

def get_xy(ths):
    x = sum([math.cos(a) for a in ths])
    y = sum([math.sin(a) for a in ths])

    x = int(W/2 + x*scale)
    y = int(H/2 - y*scale)

    return (x,y)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
                add_pt = 1
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
                    reset()
                    print(n)
            if event.key == pygame.K_COMMA:
                if n > 1:
                    n -= 1
                    scale = 240/n
                    reset()
                    print(n)



    blank()

    if add_pt:

        ths = [th_step*a for a in indices]

        (x,y) = get_xy(ths)

        pts.append((x,y))

        if sum(indices) == n_step*n and sweep_home == 0:
            sweep_home = 1
        elif sum(indices) == 0 and sweep_home == 1:
            #reset()
            add_pt = 0
            sweep_home = 0
        elif sweep_home:
            a = indices[0]
            indices.clear()
            indices.extend([a-1 for x in range(n)])
        else:
            ii = 0
            while(indices[ii]==n_step):
                ii += 1
            indices[ii] += 1

    icolor = 0
    for a in range(len(ths)):
        pygame.draw.line(screen,colors[icolor],get_xy(ths[0:a]),get_xy(ths[0:(a+1)]))
        icolor = (icolor + 1) % ncolors

    for a in pts:
        #screen.set_at((x,y),white)
        pygame.draw.circle(screen,white,a,dot_sz)

    pygame.display.flip()




    if ispeed >= 0:
        pygame.time.wait(speeds[ispeed])
