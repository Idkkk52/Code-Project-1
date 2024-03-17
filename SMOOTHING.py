import pygame, random
pygame.init()
WIDTH = 200
HEIGHT = 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 5
color_list = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

#pygame.draw.rect(screen, (255, 255, 255), (100, 100, 50, 50))

while True:
    clock.tick(FPS)
    pygame.display.set_caption(str(clock.get_fps()))
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
    for x in range(0, WIDTH - 1):
        for y in range(0, HEIGHT - 1):
            red = 0
            green = 0
            blue = 0
            if x > 0:
                color_list[0] = screen.get_at((x - 1, y))[:3]
            if x > 0 and y > 0:
                color_list[1] = screen.get_at((x - 1, y - 1))[:3]
            if y > 0:
                color_list[2] = screen.get_at((x, y - 1))[:3]
            if x < WIDTH and y > 0:
                color_list[3] = screen.get_at((x + 1, y - 1))[:3]
            if x < WIDTH:
                color_list[4] = screen.get_at((x + 1, y))[:3]
            if x < WIDTH and y < HEIGHT:
                color_list[5] = screen.get_at((x + 1, y + 1))[:3]
            if y < HEIGHT:
                color_list[6] = screen.get_at((x, y + 1))[:3]
            if x > 0 and y < HEIGHT:
                color_list[7] = screen.get_at((x - 1, y + 1))[:3]
            #print(color_list)
            for i in color_list:
                red += i[0]
                green += i[1]
                blue += i[2]
            num = len(color_list)
            red /= num
            green /= num
            blue /= num
            red += random.randint(-round(red), 255 - round(red)) / 50
            green += random.randint(-round(green), 255 - round(green)) / 50
            blue += random.randint(-round(blue), 255 - round(blue)) / 50
            screen.set_at((x, y), (red, green, blue))
    pygame.display.update()