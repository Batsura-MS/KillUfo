
from time import time as timer 
from pygame import *
from random import randint
window = display.set_mode((1930,1000))
display.set_caption('shuter')
background = transform.scale(image.load('galaxy.jpg'),(1930,1000))
clock = time.Clock()
Fps = 60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
game = True
lost = 0
win = 0
killing = 0
class GameSprite(sprite.Sprite):
    def __init__(self,image_file,x,y,speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(image_file),(width,height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y)) 
bullets = sprite.Group()
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 1820:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,5,15,20)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > 1000:
            self.rect.y = 0
            self.rect.x = randint(80,1820)
            lost += 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 1000:
            self.rect.y = 0
            self.rect.x = randint(80,1820)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()
finish = False
font.init()
font1 = font.SysFont('Arial',36)
number = 0
meteors = sprite.Group()
meteor1 = Asteroid('asteroid.png',randint(80,1820),-60,randint(2,3),100,100)
meteor2 = Asteroid('asteroid.png',randint(80,1820),-60,randint(2,3),100,100)
meteor3 = Asteroid('asteroid.png',randint(80,1820),-60,randint(2,3),100,100)
meteors.add(meteor1)
meteors.add(meteor2)
meteors.add(meteor3)
monsters = sprite.Group()
monster1 = Enemy('ufo.png',randint(80,1820),-60,randint(2,3),225,75)
monster2 = Enemy('ufo.png',randint(80,1820),-60,randint(2,3),225,75)
monster3 = Enemy('ufo.png',randint(80,1820),-60,randint(2,3),225,75)
monster4 = Enemy('ufo.png',randint(80,1820),-60,randint(2,3),225,75)
monster5 = Enemy('ufo.png',randint(80,1820),-60,randint(1,3),225,75)
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

player = Player('rocket.png',900,750,15,150,227)
kick = mixer.Sound('fire.ogg')
font.init()
font3 = font.SysFont('Arial',210)
font2  = font.SysFont('Arial',140)
life = 3
timer_gun = font2.render('Перезарядка!',True,(255,0,0))
won = font3.render('YOU WIN!!!',True,(255,215,0))
lose = font3.render('YOU LOSE!!!',True,(255,215,0))
num_fire = 0
rel_time = False
while game:
    #with open('file.txt','a',encoding='utf-8') as file:
        #for i in range(50000):
           #file.write('зарикролен)')
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:

                if num_fire < 7 and rel_time != True:
                    player.fire()
                    kick.play()
                    num_fire += 1
                if num_fire >= 7 and rel_time != True:
                    rel_time = True
                    time_start = timer()

        if e.type==QUIT:
            game = False
    if finish != True:
        window.blit(background,(0,0))
        lifes = font2.render(str(life),True,(0,255,0))
        if life <= 1:
            lifes = font2.render(str(life),True,(255,0,0))
        window.blit(lifes,(1860,0))
        if rel_time == True:
            time_end = timer()
            if time_end-time_start < 2:
                window.blit(timer_gun,(750,0))
            else:
                rel_time = False
                num_fire = 0
        sprite_list = sprite.groupcollide(monsters,bullets,True,True)
        for monster in sprite_list:
            win += 1
            monsters.add(Enemy('ufo.png',randint(80,1820),-60,randint(1,3),225,75))
        if sprite.spritecollide(player,meteors,True):
            life -= 1
            meteors.add(Enemy('asteroid.png',randint(80,620),-60,randint(2,3),100,100))
        txt = font2.render('Пропущено: '+str(lost),1,(255,0,0))
        txt1 = font2.render('Повержено: '+str(win),1,(0,255,0))
        window.blit(txt,(10,10))   
        window.blit(txt1 ,(10,100))     
        player.reset()
        player.update()
        meteors.draw(window)
        meteors.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        if win >= 10:
            window.blit(won,(550,400))
            finish = True
        if lost >= 3 or life == 0:
            window.blit(lose,(550,400))
            finish = True
    clock.tick(Fps)
    display.update()