'''
The idea for this file was to use PyGame to show the user's current location
'''

import pygame
pygame.init()
pygame.display.set_caption('3D Audio for Museum Exhibits - User Location')


screen = pygame.display.set_mode((620, 620))
done = False
white = (255, 255, 255)
screen.fill(white)

compass = pygame.image.load("images/compass.png")
lunch = pygame.image.load("images/1.png")
holidays=pygame.image.load("images/2.png")
restaurants=pygame.image.load("images/3.png")
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

pic = pygame.transform.scale(compass, (80, 80))
lunch_box=pygame.transform.scale(lunch,(20,20))
holidays_box=pygame.transform.scale(holidays,(20,20))
restuarants_box=pygame.transform.scale(restaurants,(20,20))
four_box=pygame.transform.scale(four,(20,20))
five_box=pygame.transform.scale(five,(20,20))
six_box=pygame.transform.scale(six,(20,20))
seven_box=pygame.transform.scale(seven,(20,20))
eight_box=pygame.transform.scale(eight,(20,20))
nine_box=pygame.transform.scale(nine,(20,20))
ten_box=pygame.transform.scale(ten,(20,20))
eleven_box=pygame.transform.scale(eleven,(20,20))
twelve_box=pygame.transform.scale(twelve,(20,20))
thirteen_box=pygame.transform.scale(thirteen,(20,20))
fourteen_box=pygame.transform.scale(fourteen,(20,20))
fifteen_box=pygame.transform.scale(fifteen,(20,20))
entrance_box = pygame.transform.scale(entrance,(20,20))

is_blue = True
x = 350
y = 605

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
        screen.blit(pic,(0,500))
        screen.blit(entrance_box,(300,600))
        screen.blit(lunch_box,(300,560))
        screen.blit(holidays_box,(300,520))
        screen.blit(restuarants_box,(300,480))
        screen.blit(four_box,(300,440))
        screen.blit(five_box,(300,400))
        screen.blit(six_box,(300,360))
        screen.blit(seven_box,(300,320))
        screen.blit(eight_box,(300,280))
        screen.blit(nine_box,(300,240))
        screen.blit(ten_box,(300,200))
        screen.blit(eleven_box,(300,160))
        screen.blit(twelve_box,(300,120))
        screen.blit(thirteen_box,(300,80))
        screen.blit(fourteen_box,(300,40))
        screen.blit(fifteen_box,(300,0))

        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 10, 10))

        pygame.display.flip()
        clock.tick(60)
