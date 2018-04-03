import pygame

#pygame.init()
screen = pygame.display.set_mode((1000, 1000))
done = False
white = (255, 255, 255)
screen.fill(white)



compass = pygame.image.load("compass.png")
lunch = pygame.image.load("1.png")
holidays=pygame.image.load("2.png")
restauranrts=pygame.image.load("3.png")
four=pygame.image.load("4.png")
five=pygame.image.load("5.png")
six=pygame.image.load("6.png")
seven=pygame.image.load("7.png")
eight=pygame.image.load("8.png")
nine=pygame.image.load("9.png")
ten=pygame.image.load("10.png")



pic = pygame.transform.scale(compass, (80, 80))
lunch_box=pygame.transform.scale(lunch,(50,50))
holidays_box=pygame.transform.scale(holidays,(50,50))
restuarants_box=pygame.transform.scale(restauranrts,(50,50))
four_box=pygame.transform.scale(four,(50,50))
five_box=pygame.transform.scale(five,(50,50))
six_box=pygame.transform.scale(six,(50,50))
seven_box=pygame.transform.scale(seven,(50,50))
eight_box=pygame.transform.scale(eight,(50,50))
nine_box=pygame.transform.scale(nine,(50,50))
ten_box=pygame.transform.scale(ten,(50,50))





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
        pygame.draw.line(screen, (0, 0, 0), (0, 250), (800, 250))
        pygame.draw.line(screen, (0, 0, 0), (250, 0), (250, 800))
        screen.blit(pic,(0,500))
        screen.blit(lunch_box,(250,450))
        screen.blit(holidays_box,(250,400))
        screen.blit(restuarants_box,(250,350))
        screen.blit(four_box,(250,300))
        screen.blit(five_box,(250,250))
        screen.blit(six_box,(250,200))
        screen.blit(seven_box,(250,150))
        screen.blit(eight_box,(250,100))
        screen.blit(nine_box,(250,50))
        screen.blit(ten_box,(250,0))
        
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 20, 20))
        
        pygame.display.flip()
        clock.tick(60)
