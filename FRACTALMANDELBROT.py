import pygame, math
pygame.init()
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
loop_range = 128

colors = []
for i in range(loop_range):
    colors.append(math.sqrt(i) * 22)

def escape(x_c , y_c ):
    x = 0
    y = 0
    for i in range(1, loop_range):
        old_x = x
        x = x * x - y * y + x_c
        y = 2 * old_x * y + y_c
        if abs(x) > 2000:
            #r = i * 2
            #r = (i & 28) * 8
            #g = (i & 56) * 4.5
            #b = (i & 14) * 17
            #return (r, g, b)
            return(40 + i * 1.7, colors[i], 70)
            #color = 1 / i * 200
            #return(color, color, color)
    return (255, 255, 255)

FRACTAL_WIDTH = 600
FRACTAL_HEIGHT = 600
fractal = pygame.Surface((FRACTAL_WIDTH, FRACTAL_HEIGHT))
for y in range(FRACTAL_HEIGHT):
    for x in range(FRACTAL_WIDTH):
        fractal.set_at((x, y),escape((x - FRACTAL_WIDTH / 2) / FRACTAL_WIDTH * 4 ,
                                     (y - FRACTAL_HEIGHT / 2)/ FRACTAL_HEIGHT * 4))
x, y = ((WIDTH - FRACTAL_WIDTH) / 2, (HEIGHT - FRACTAL_HEIGHT) / 2)

while True:
    screen.fill((40, 0, 70))
    screen.blit(fractal, (x, y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        y += 1
    if keys[pygame.K_s]:
        y -= 1
    if keys[pygame.K_a]:
        x += 1
    if keys[pygame.K_d]:
        x -= 1

    pygame.display.update()