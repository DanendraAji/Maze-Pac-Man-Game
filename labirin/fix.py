from pygame import *

BACKGROUND = (173, 216, 230)
window_width = 700
window_height = 500
window = display.set_mode((window_width,window_height))
display.set_caption('Labirint Game')

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        if pacman.rect.x <= window_width-80 and pacman.x_speed > 0 or pacman.rect.x >= 0 and pacman.x_speed < 0:
            self.rect.x += self.x_speed
        
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        if pacman.rect.y <= window_height-80 and pacman.y_speed > 0 or pacman.rect.y >= 0 and pacman.y_speed < 0:
            self.rect.y += self.y_speed
        
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire(self):
        bullet = Bullet('bullet.png', 15, 20, self.rect.right, self.rect.centery, 45)
        bullets.add(bullet)
        
class Enemy(GameSprite):
    side = 'left'
    def __init__(self, picture, w, h, x, y, player_speed):
        super().__init__(picture, w, h, x, y)
        self.speed = player_speed
    
    def update(self):
        #untuk batas maksimal monster bergerak
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= window_width - 85:
            self.side = 'left'
        #untuk pergerakan kekanan dan kekiri
        if self.side == 'left':
            self.rect.x -= self.speed
        if self.side == 'right':
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, player_speed):
        super().__init__(picture, w, h, x, y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > window_width + 10:
            self.kill()

barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

wall_1 = GameSprite('wall2.png', 300, 50, 120, 250)
wall_2 = GameSprite('platform2_v.png', 50, 400, 380, 100)

barriers.add(wall_1)
barriers.add(wall_2)

pacman = Player('hero.png', 65, 65, 30, 100, 0, 0) 
final_sprite = Player('pac-1.png', 65, 65, 600, 400, 0, 0) 

monster1 = Enemy('cyborg.png', 65, 65, 600, 200, 5) 
monster2 = Enemy('cyborg.png', 65, 65, 600, 280, 5) 
monsters.add(monster1)
monsters.add(monster2)

finish = False
run = True
while run:
    time.delay(50)

    for i in event.get():
        if i.type == QUIT:
            run = False

        elif i.type == KEYDOWN:
            if i.key == K_UP:
                pacman.y_speed = -10
            elif i.key == K_DOWN:
                pacman.y_speed = 10
            elif i.key == K_RIGHT:
                pacman.x_speed = 10
            elif i.key == K_LEFT:
                pacman.x_speed = -10
            elif i.key == K_SPACE:
                pacman.fire()

        elif i.type == KEYUP:
            if i.key == K_UP:
                pacman.y_speed = 0
            elif i.key == K_DOWN:
                pacman.y_speed = 0
            elif i.key == K_RIGHT:
                pacman.x_speed = 0
            elif i.key == K_LEFT:
                pacman.x_speed = 0

    if finish != True:
        window.fill(BACKGROUND)

        wall_1.reset()
        wall_2.reset() 

        # monster.reset()
        final_sprite.reset()

        pacman.reset()
        pacman.update()
        
        bullets.update()
        bullets.draw(window)

        monsters.update()
        monsters.draw(window)

        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.spritecollide(pacman, monsters, False):
            finish = True

            img = image.load('game-over_1.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (window_width, window_height)), (0, 0))

        if sprite.collide_rect(pacman, final_sprite):
            finish = True

            img = image.load('thumb.jpg')
            banding = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (window_width, window_height)), (0, 0))


    display.update()