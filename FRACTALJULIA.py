import pygame, math
pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
loop_range = 128

colors = []
for i in range(loop_range):
    colors.append(math.sqrt(i) * 22)

def escape(x, y, x_c, y_c, colors):
    for i in range(1, loop_range):
        old_x = x
        x = x * x - y * y + x_c
        y = 2 * old_x * y + y_c
        if math.sqrt(x * x + y * y) > 2:
            #r = (i & 28) * 8
            #g = (i & 56) * 4.5
            #b = (i & 14) * 17
            #return (r, g, b)
            return(i * 2, 80, colors[i])
    return (255, 255, 255)

FRACTAL_WIDTH = 1000
FRACTAL_HEIGHT = 1000
fractal = pygame.Surface((FRACTAL_WIDTH, FRACTAL_HEIGHT))
xx, yy = (WIDTH - FRACTAL_WIDTH) / 2, (HEIGHT - FRACTAL_HEIGHT) / 2
for y in range(FRACTAL_HEIGHT):
    for x in range(FRACTAL_WIDTH):
        fractal.set_at((x, y),escape((x - FRACTAL_WIDTH / 2) / FRACTAL_WIDTH * 4 ,
                                     (y - FRACTAL_HEIGHT / 2)/ FRACTAL_HEIGHT * 4,  -0.194, 0.6557, colors))
        #screen.blit(fractal, (xx, yy))
        #pygame.display.update()

while True:
    screen.blit(fractal, (xx, yy))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        yy += 1
    if keys[pygame.K_s]:
        yy -= 1
    if keys[pygame.K_a]:
        xx += 1
    if keys[pygame.K_d]:
        xx -= 1

    pygame.display.update()