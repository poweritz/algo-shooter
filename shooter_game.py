#Создай собственный Шутер!
from pygame import *
from random import *


lost = 0
sbito = 0

font.init()
font1 = font.SysFont('Arial', 40)
win = font1.render('YOU WIN!', True, (0, 255, 0))
lose = font1.render('YOU LOSE!', True, (255, 0, 0))

class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed
        player_speed = 20
        self.rect = self.image.get_rect() 
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))


#класс спрайта-пули  
class Bullet(GameSprite):
   # движение врага
   def update(self):
       self.rect.y += self.speed 
       # исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()

img_bullet = 'bullet.png'

class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 2:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_w - 80:
            self.rect.x += self.speed

 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
    def update(self):
        self.rect.y += self.speed  
        global lost
        #исчезает, если дойдёт до края экрана
        if self.rect.y > win_h:
            self.rect.x = randint(80, win_w - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteria(GameSprite):
    def update(self):
        self.rect.y += self.speed  
           
goal = 10
max_lost = 5

win_w = 700
win_h = 500

window = display.set_mode((win_w, win_h))
display.set_caption('Maze')

background = transform.scale(image.load('galaxy.jpg'), (700, 500))
hero = Player('rocket.png', 0, win_h - 100, 80, 100, 4)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_w - 80), -50, 80, 50, randint(1,5))
    monsters.add(monster)

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

game = True
finish = False


while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()

    if not finish:
        window.blit(background, (0,0))

        font_lost = font1.render("Пропущено: " + str(lost), 1, (255, 0, 0))
        window.blit(font_lost, (20, 45))

        font_sbito = font1.render("Сбито: " + str(sbito), 1, (0, 255, 0))
        window.blit(font_sbito, (20, 20))   

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            sbito = sbito + 1
            monster = Enemy('ufo.png', randint(80, win_w - 80), -50, 80, 50, randint(1,5))
            monsters.add(monster)

               #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if  lost >= max_lost:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))


       #проверка выигрыша: сколько очков набрали?
        if sbito >= goal:
            finish = True
            window.blit(win, (200, 200))

        hero.update()
        hero.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

    clock.tick(FPS)
    display.update()