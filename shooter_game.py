from pygame import *
from random import *
import time as tm

class GameSprite(sprite.Sprite):
    def __init__(self, player_sprite_loader, x_sprite, y_sprite,player_speed, x_size,y_size):
        super().__init__()
        self.image = transform.scale(image.load(player_sprite_loader),(x_size,y_size))
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x =x_sprite
        self.rect.y = y_sprite
    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))
class player(GameSprite):
    def update(self):
        if kp[K_d]and self.rect.x < 600:
            self.rect.x +=self.speed
        if kp[K_a] and self.rect.x > 100:
            self.rect.x -=self.speed
class monster(GameSprite):
    def update(self):
        global count2
        if self.rect.y != 500:
            self.rect.y +=self.speed
        elif self.rect.y == 500:
            count2 += 1
            self.rect.y = 0 
            self.rect.x = randint(100,600)
class bullet(GameSprite):
    def update(self):
        if self.rect.y > -10:
            self.rect.y -= self.speed
        elif self.rect.y < 0:
            self.kill()
        
num_bullets = 0
rel_time =False
sprites_list = list()
sprites_list2 = list()
count1 = 0
count2=0
font.init()
mixer.init()
win = display.set_mode((700,500))
FPS = 60
background = transform.scale(image.load('galaxy.jpg'), (700,500))
player = player('rocket.png', 350,400,5,80,80)
monster1 = monster('ufo.png', randint(100,600), 0, 1, 80, 40)
monster2 = monster('ufo.png', randint(100,600), 0, 3, 80, 40)
monster3 = monster('ufo.png', randint(100,600), 0, 5, 80, 40)
monster4 = monster('ufo.png', randint(100,600), 0, 2, 80, 40)
monster5 = monster('ufo.png', randint(100,600), 0, 2, 80, 40)
run = True
clock = time.Clock()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
font = font.SysFont('Arial', 40)
ccc = font.render('Счет: ' + str(count1), True, (255, 215, 0))
r = font.render('Пропущено: ' + str(count2), True, (255, 215, 0))
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
win2 = font.render('YOU WIN!', True, (255, 255, 0))
loss = font.render('YOU LOSE!', True, (255, 255, 0))
reload_text = font.render('Wait, reload...', True, (255, 255, 0))
question = font.render('Вы хотите возобновить игру?', True, (255, 255, 0))
answer = font.render('Да - E   Нет(выйти из игры) - Q', True, (255, 255, 0))
game = True
for i in range(3):
            asteroids.add(monster('asteroid.png', randint(100,600), 0, 1, 80,80))
while run:
    kp = key.get_pressed()
    win.blit(background, (0,0))
    for e in event.get():
            if e.type == QUIT:
                run = False
    if game == True:
        ccc = font.render('Счет: ' + str(count1), True, (255, 215, 0))
        r = font.render('Пропущено: ' + str(count2), True, (255, 215, 0))
        win.blit(ccc, (30,30))
        win.blit(r, (30,70))
        player.update()
        player.reset()
        if kp[K_SPACE]:
            if num_bullets < 100:
                bullets.add(bullet('bullet.png', player.rect.centerx, player.rect.y, 5, 10,10))
                num_bullets +=1
        if num_bullets >= 100 and not rel_time:
            rel_time = True
            t = tm.time()
        if rel_time:
            n = tm.time()
            if n-t < 3:
                win.blit(reload_text, (30,110))
            else:
                rel_time = False
                num_bullets = 0
        bullets.draw(win)
        bullets.update()
        monsters.draw(win)
        monsters.update()
        asteroids.draw(win)
        asteroids.update()
        sprites_list = sprite.groupcollide(monsters, bullets, False, True)
        sprites_list2 = sprite.groupcollide(asteroids, bullets, False, True)
        for f in sprites_list:
            count1 += 1
            f.rect.x, f.rect.y = randint(100,600), 0
    if count1 == 100:
        win.blit(win2, (320,250))
        game = False
    if count2 == 10:
        win.blit(loss, (320,250))
        game = False
    if game == False:
        win.blit(question, (100,350))
        win.blit(answer, (150,420))
        if kp[K_e]:
            game = True
            count1, count2 = 0,0
        elif kp[K_q]:
            run = False
    clock.tick(FPS)
    display.update()