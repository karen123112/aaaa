from pygame import*
from random import randint
class GameSpraite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSpraite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self): 
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top,5,10,15 )
        bullets.add(bullet)



class Enemy(GameSpraite):
    def update(self):
        global lost 
        self.rect.y += self.speed 
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(5,620)
            lost += 1

class Bullet(GameSpraite):
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y == 0:
            self.kill()
bullets  = sprite.Group()



win_width = 700 
win_height = 500


player = Player('rocket.png', 70, 420, 10, 65, 65)
window = display.set_mode((win_width, win_height))
display.set_caption('maze')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(5,620), 0,randint(3,7),65,70)
    monsters.add(monster)

game = True 
clock = time.Clock()
fps = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sounds = mixer.Sound('fire.ogg')
finish = False
font.init()
font = font.Font(None, 36)
killed, lost = 0,0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:  
            if e.key == K_SPACE:
                fire_sounds.play()
                player.fire()

    if not finish:     
        window.blit(background,(0,0))
        win = font.render(
        'повержно' + str(killed), True, (255,255,255)   
        )
        window.blit(win,(10,10))
        lose = font.render(
        'упущено' + str(lost), True, (255,255,255)     
        )
        window.blit(lose,(10,10))
        finish = True    
        sprites_list = sprite.spritecollide(
        player, monsters, False
        )  
        

        window.blit(lose,(10,50))
        player.update()
        player.reset()  
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        display.update()
        clock.tick(fps)
