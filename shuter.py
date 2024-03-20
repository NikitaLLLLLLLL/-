from pygame import *
from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('music-fone.mp3')
mixer.music.play(-1)
mixer.music.set_volume(22)

font.init()
font1 = font.SysFont('Arial', 35)
font2 = font.SysFont('Arial', 80)

lost = 0
score = 0

window = display.set_mode((700,500))
display.set_caption("Шутер")
background = transform.scale(image.load('peace.png'), (700,500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20,10)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80,620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        
    
win_width = 700
win_height = 500
win = font2.render('YOU WIN!', True, (0,255,0))
lose = font2.render('YOU LOSE!', True, (255,0,0))

player = Player('rocket1.png', 5, win_height-100, 80, 100, 7)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80,620), -40, 80,50, randint(1,4))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80,620), -40, 80,50, randint(1,4))
    asteroids.add(asteroid)

game = True
finish = False
fire_sound = mixer.Sound('fire.ogg')

rel_time = False
num_fire = 0
life = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_time != True:
                    fire_sound.play() 
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time != True:
                    rel_time = True 
                    last_time = timer()
    
    if not finish:
        window.blit(background, (0, 0))

        text = font1.render(f'Счёт: {score}', True, (255,255,255))
        window.blit(text, (10,20))

        text_lose = font1.render(F'Пропущено:   {lost}', True, (255, 255, 255))
        window.blit(text_lose, (10,50))

        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        life_text = font1.render(str(life), True, (0,255,0))
        window.blit(life_text,(650,10))

        collides = sprite.groupcollide(bullets, monsters, True, True)
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('ДАЙ ОТДОХНУТЬ', True, (100,200,100))
                window.blit(reload, (250,450))
            else:
                num_fire = 0
                rel_time = False
        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80,620), -40, 80,50, randint(1,4))
            monsters.add(monster)

        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80,620), -40, 80,50, randint(1,4))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(lose, (200,200))
        if sprite.spritecollide(player, asteroids, True):
            life -= 1
            asteroid = Enemy('asteroid.png', randint(80,620), -40, 80,50, randint(1,4))
            asteroids.add(asteroid)

        if score > 9:
            finish = True   
            window.blit(win,(200,200))
        if life < 1:
            finish = True
            window.blit(lose, (200,200))

    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        rel_time = False
        num_fire = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(80,620), -40, 80,50, randint(1,4))
            monsters.add(monster)
        for i in range(3):
            asteroid = Enemy('asteroid.png', randint(80,620), -40, 80,50, randint(1,4))
            asteroids.add(asteroid)

        



    display.update()
    time.delay(20)