import pygame, sys, random, math

# adjust probability to better fill space depending on n
# needs work
def prob_scale(x,n):
    q = 2
    b = 0.5
    y1 = math.exp(-math.pow(q*x,2*n)) - math.exp(-math.pow(q,2*n))
    y2 = 1 - math.exp(-math.pow(q,2*n))
    y = y1/y2
    return (y+b*(1-x))/(1+b)

W = 800
H = 600
mscale = 300
scale = 150
dot_sz = 3
font_family = "Consolas"

max_sweep = 30;

black = (0,0,0)
white = (255,255,255)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
colors = [red, green, blue]
ncolors = len(colors)

speeds = [10, 25, 50, 100, 200]

fonts = []

def get_xy(ths):
    x = sum([math.cos(a) for a in ths])
    y = sum([math.sin(a) for a in ths])

    x = int(W/2 + x*scale)
    y = int(H*3/4 - y*scale)

    return (x,y)

def draw_axes(surf):
    pygame.draw.line(surf,white,(int(W/2),H),(int(W/2),0))
    pygame.draw.line(surf,white,(0,int(H*3/4)),(W,int(H*3/4)))

def init_fonts():
    fonts.append(pygame.font.SysFont(font_family,16))
    fonts.append(pygame.font.SysFont(font_family,30))

def draw_text_center(msg,surf,ifont,color,py):
    (x,y) = fonts[ifont].size(msg)
    surf.blit(fonts[ifont].render(msg,1,color),(int(W/2-x/2),int(H/2-y/2-py)))

def draw_text_left(msg,surf,ifont,color,px,py):
    surf.blit(fonts[ifont].render(msg,1,color),(int(px),int(py)))

def draw_text_right(msg,surf,ifont,color,px,py):
    (x,y) = fonts[ifont].size(msg)
    surf.blit(fonts[ifont].render(msg,1,color),(int(W-px-x),int(py)))

# display splash screen and wait for keypress
def splash(screen):

    draw_text_center("Welcome to",screen,0,white,60)
    draw_text_center("Loci Visualizer",screen,1,white,25)
    draw_text_center("Press any key to continue ...",screen,0,white,-25)

    pygame.display.flip()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                done = True;

        pygame.time.wait(100)

def get_next_point(n_lines,sweep):
    lines_surf = pygame.Surface((W,H),pygame.SRCALPHA)

    if sweep == -1:
        ths = [random.uniform(0,1) for i in range(n_lines)]
        # ths = [math.pi*prob_scale(a,n_lines) for a in ths]
        ths = [math.pi*a for a in ths]
    else:
        if sweep > 0.5:
            ths = [math.pi*(2-2*sweep) for i in range(n_lines)]
        else:
            ths = [0 for i in range(n_lines)]
            i = 0
            while 2*n_lines*sweep > i+1:
                ths[i] = math.pi
                i += 1

            ths[i] = (2*n_lines*sweep-i)*math.pi

    icolor = 0
    for a in range(len(ths)):
        pygame.draw.line(lines_surf,colors[icolor],get_xy(ths[0:a]),get_xy(ths[0:(a+1)]),3)
        icolor = (icolor + 1) % ncolors

    return (get_xy(ths),lines_surf)

# main program
def main():

    global scale

    n_lines = 2
    scale = mscale/n_lines

    ispeed = 2

    add_pt = 1
    reset = 0
    mode = 0
    show_lines = 1

    sweep = 0

    n_pts = 0

    pygame.init()

    init_fonts()

    screen = pygame.display.set_mode((W,H))
    pygame.display.set_caption('Umbrella Locus')

    screen.fill(black)

    pts_surf = pygame.Surface((W,H));
    draw_axes(pts_surf)

    splash(screen)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
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
                if event.key == pygame.K_UP:
                    if n_lines < 6:
                        n_lines += 1
                        scale = mscale/n_lines
                        reset = 1
                if event.key == pygame.K_DOWN:
                    if n_lines > 1:
                        n_lines -= 1
                        scale = mscale/n_lines
                        reset = 1
                if event.key == pygame.K_m:
                    mode = 1-mode
                if event.key == pygame.K_l:
                    show_lines = 1-show_lines

        if reset:
            pts_surf.fill(black)
            draw_axes(pts_surf)
            n_pts = 0
            reset = 0

        if add_pt:

            (xy,lines_surf) = get_next_point(n_lines,sweep if mode else -1)
            (x,y) = xy

            if mode:
                sweep = sweep + 0.051;
                while sweep > 1:
                    sweep -= 1;

            n_pts += 1

            pygame.draw.circle(pts_surf,white,(x,y),dot_sz)

        screen.blit(pts_surf,(0,0))


        if show_lines and not n_pts == 0:
            screen.blit(lines_surf,(0,0))

        draw_text_left("N:     {}".format(n_lines),screen,0,white,10,10)
        draw_text_left("Mode:  {}".format("Sweep" if mode else "Random"),screen,0,white,10,30)
        draw_text_left("Speed: {}".format(5-ispeed),screen,0,white,10,50)

        draw_text_right("Pause:           P",screen,0,white,10,10)
        draw_text_right("Reset:           R",screen,0,white,10,30)
        draw_text_right("Change Mode:     M",screen,0,white,10,50)
        draw_text_right("Toggle Lines:    L",screen,0,white,10,70)
        draw_text_right("Increase N:      \u2191",screen,0,white,10,90)
        draw_text_right("Decrease N:      \u2193",screen,0,white,10,110)
        draw_text_right("Change Speed:  1-6",screen,0,white,10,130)

        pygame.display.flip()

        if ispeed >= 0:
            pygame.time.wait(speeds[ispeed])

if __name__ == "__main__":
    main()
