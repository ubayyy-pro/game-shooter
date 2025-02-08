#Create your own shooter
from pygame import *
from random import randint
from time import time as timer

#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.Font(None, 36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
lost = 0 #penghitung jumlah monster yang terlewat
score = 0 #Menghitung score
life = 3
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, asteroid=False):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.asteroid = asteroid
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            if self.asteroid == False:
                lost = lost + 1

# bullet sprite class   
class Bullet(GameSprite):
    # enemy movement
    def update(self):
        self.rect.y += self.speed
        # disappears if it reaches the edge of the screen
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group() #Tambahan


asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7), True)
    asteroids.add(asteroid)

finish = False
run = True
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
rel_time = False #flag in charge of reload
num_fire = 0  #variable to count shots    
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
        # if e.type == MOUSEBUTTONDOWN:
        #     if mouse.get_pressed()[0]: #left
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                     
                if num_fire  >= 5 and rel_time == False : #if the player fired 5 shots
                    last_time = timer() #record time when this happened
                    rel_time = True #set the reload flag
        
    if finish != True:
        window.blit(background, (0,0))
        


        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()#Tambahan

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)#Tambahan

        if rel_time == True:
           now_time = timer() #read time
       
           if now_time - last_time < 3: #before 3 seconds are over, display reload message
               reload = font2.render('Wait, reload...', 1, (150, 0, 0))
               window.blit(reload, (260, 460))
           else:
               num_fire = 0   #set the bullets counter to zero
               rel_time = False #reset the reload flag

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #this loop will repeat as many times as the number of monsters hit
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        sprite.groupcollide(asteroids, bullets, False, True)

        #possible lose: missed too many monsters or the character collided with an enemy
        if sprite.spritecollide(ship, monsters, True):
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            life -= 1
        
        if sprite.spritecollide(ship, asteroids, True):
            asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7), True)
            asteroids.add(asteroid)
            life -= 1

        if lost >= 3 or life < 1:
            finish = True #lose, set the background and no longer control the sprites.
            window.blit(lose, (200, 200))

        text_life = font2.render('Life:' + str(life), 1, (0,255,0))
        window.blit(text_life, (win_width - 80,20))
        
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render('Score:' + str(score), 1, (255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render('Missed:' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 50))

    display.update()
    time.delay(50) 

        