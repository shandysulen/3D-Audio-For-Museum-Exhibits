import pygame

#pygame.init()
screen = pygame.display.set_mode((600, 600))
done = False
white = (255, 255, 255)
screen.fill(white)
compass = pygame.image.load("compass.png")
pic = pygame.transform.scale(compass, (80, 80))
is_blue = True
x = 10
y = 10

clock = pygame.time.Clock()

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        is_blue = not is_blue
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: y -= 1
        if pressed[pygame.K_DOWN]: y += 1
        if pressed[pygame.K_LEFT]: x -= 1
        if pressed[pygame.K_RIGHT]: x += 1
        
        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (0, 300), (600, 300))
        pygame.draw.line(screen, (0, 0, 0), (300, 0), (300, 600))
        screen.blit(pic,(0,500))
        
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 20, 20))
        
        pygame.display.flip()
        clock.tick(60)
