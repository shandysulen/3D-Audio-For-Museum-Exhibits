import pygame

pygame.init()
screen = pygame.display.set_mode((620, 620))
pygame.display.set_caption('3D Audio for Museum Exhibits - User Location')
done = False
white = (255, 255, 255)
screen.fill(white)



compass = pygame.image.load("images/compass.png")
lunch = pygame.image.load("images/1.png")
holidays=pygame.image.load("images/2.png")
restauranrts=pygame.image.load("images/3.png")
four=pygame.image.load("images/4.png")
five=pygame.image.load("images/5.png")
six=pygame.image.load("images/6.png")
seven=pygame.image.load("images/7.png")
eight=pygame.image.load("images/8.png")
nine=pygame.image.load("images/9.png")
ten=pygame.image.load("images/10.png")
eleven = pygame.image.load("images/11.png")
twelve=pygame.image.load("images/12.png")
thirteen=pygame.image.load("images/13.png")
fourteen=pygame.image.load("images/14.png")
fifteen=pygame.image.load("images/15.png")
entrance = pygame.image.load("images/entrance.png")
map1 = pygame.image.load("images/map_entrance.png")



pic = pygame.transform.scale(compass, (80, 80))
#map_pic = pygame.transform.scale(map1,(500,500))
lunch_box=pygame.transform.scale(lunch,(10,10))
holidays_box=pygame.transform.scale(holidays,(10,10))
restuarants_box=pygame.transform.scale(restauranrts,(10,10))
four_box=pygame.transform.scale(four,(10,10))
five_box=pygame.transform.scale(five,(10,10))
six_box=pygame.transform.scale(six,(10,10))
seven_box=pygame.transform.scale(seven,(10,10))
eight_box=pygame.transform.scale(eight,(10,10))
nine_box=pygame.transform.scale(nine,(10,10))
ten_box=pygame.transform.scale(ten,(10,10))
eleven_box=pygame.transform.scale(eleven,(10,10))
twelve_box=pygame.transform.scale(twelve,(10,10))
thirteen_box=pygame.transform.scale(thirteen,(10,10))
fourteen_box=pygame.transform.scale(fourteen,(10,10))
fifteen_box=pygame.transform.scale(fifteen,(10,10))
entrance_box = pygame.transform.scale(entrance,(10,10))

is_blue = True
x = 317
y = 533

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
        pygame.draw.line(screen, (0, 0, 0), (0, 300), (800, 300))
        pygame.draw.line(screen, (0, 0, 0), (300, 0), (300, 800))
        
        screen.blit(pic,(50,500))
        
        screen.blit(entrance_box,(300,530))
        screen.blit(lunch_box,(300,500))
        screen.blit(holidays_box,(300,470))
        screen.blit(restuarants_box,(300,440))
        screen.blit(four_box,(300,410))
        screen.blit(five_box,(300,380))
        screen.blit(six_box,(300,350))
        screen.blit(seven_box,(300,320))
        screen.blit(eight_box,(300,290))
        screen.blit(nine_box,(300,260))
        screen.blit(ten_box,(300,230))
        screen.blit(eleven_box,(300,200))
        screen.blit(twelve_box,(300,170))
        screen.blit(thirteen_box,(300,140))
        screen.blit(fourteen_box,(300,110))
        screen.blit(fifteen_box,(300,80))
        
        screen.blit(map1,(100,0))
        
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 5,5))
        
        pygame.display.flip()
        clock.tick(60)
