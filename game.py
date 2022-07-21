import pygame
import random
import os
FPS=60
WIDTH=500
HEIGHT=600

BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
YELLOW=(255,255,0)
#遊戲初始化& 創建視窗
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("太空戰爭")

clock=pygame.time.Clock()

#載入圖片
background_img=pygame.image.load(os.path.join("background.png")).convert()
player_img=pygame.image.load(os.path.join("player.png")).convert()
player_mini_img=pygame.transform.scale(player_img,(25,19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
bullet_img=pygame.image.load(os.path.join("bullet.png")).convert()
# rock_img=pygame.image.load(os.path.join("rock.png")).convert()
rock_imgs =[]
for i in range(6):
    rock_imgs.append(pygame.image.load(os.path.join(f"rock{i}.png")).convert())
expl_anim={}
expl_anim["lg"]=[]
expl_anim["sm"]=[]
expl_anim["player"]=[]
for i in range(8):
    expl_img=pygame.image.load(os.path.join(f"expl{i}.png")).convert()
    expl_img.set_colorkey(WHITE)
    expl_anim["lg"].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim["sm"].append(pygame.transform.scale(expl_img,(30,30)))
    player_expl_img=pygame.image.load(os.path.join(f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(WHITE)
    expl_anim["player"].append(pygame.transform.scale(player_expl_img,(75,75)))
power_imgs={}
power_imgs["hp+"]=pygame.image.load(os.path.join("hp+.png")).convert()
power_imgs["weapon"]=pygame.image.load(os.path.join("weapon.png")).convert()


#載入音樂、音效
shoot_sound=pygame.mixer.Sound(os.path.join("shoot.mp3"))
pw1_sound=pygame.mixer.Sound(os.path.join("pw0.mp3"))
pw2_sound=pygame.mixer.Sound(os.path.join("pw1.mp3"))
expl_sound=pygame.mixer.Sound(os.path.join("expl.mp3"))
pygame.mixer.music.load(os.path.join("background.mp3"))
player_expl_sound=pygame.mixer.Sound(os.path.join("player_expl.mp3"))

font_name=os.path.join("font.ttf")
def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,WHITE)
    text_rect=text_surface.get_rect() #定位
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)
def newrock():
    r=Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf,hp,x,y):
    if hp<0:
        hp=0
    BAR_LENGTH=100
    BAR_HEIGHT=10
    fill=(hp/100)*BAR_LENGTH
    outline_rect=pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)       #畫裡面填滿的方形
    pygame.draw.rect(surf,WHITE,outline_rect,2)  #畫外框

def draw_lives(surf,lives,img,x,y):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+30*i      #避免小圖示重疊
        img_rect.y=y
        surf.blit(img,img_rect)

def draw_init():
    screen.blit(background_img,(0,0))
    draw_text(screen,"太空生存戰",64,WIDTH/2,HEIGHT/4)
    draw_text(screen,"← → 移動飛船 空白鍵發射子彈",22,WIDTH/2,HEIGHT/2)
    draw_text(screen,'按任意鍵開始遊戲',18,WIDTH/2,HEIGHT*3/4)
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                return True
            elif event.type==pygame.KEYUP:  #key down 按下鍵盤又鬆開後
                waiting=False
                return False




class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        # self.image.fill(GREEN)
        self.rect=self.image.get_rect()   #定位
        self.radius=20
        # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.bottom=HEIGHT-10
        self.rect.centerx=WIDTH/2  #self.rect.x=200 
                                   #self.rect.y=200
        self.speedx=20
        self.health=100
        self.lives=3
        self.hidden=False
        self.hide_time=0
        self.weapon=1
        self.weapon_time=0

    def update(self):
        now=pygame.time.get_ticks()
        if self.weapon>1 and now-self.weapon_time>3000:  #武器升級3秒
            self.weapon-=1
            self.weapon_time=now
        if self.hidden and now-self.hide_time>1000:
            self.hidden=False
            self.rect.centerx=WIDTH/2
            self.rect.bottom=HEIGHT-10

        key_pressed=pygame.key.get_pressed()   #回傳案件布林值
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x+=self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x-=self.speedx
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0
        # self.rect.x+=2
        # if self.rect.left>WIDTH:
        #     self.rect.right=0
    def shoot(self):
        if not(self.hidden):
            if self.weapon==1:
                bullet=Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.weapon>=2:
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()


    def hide(self):
        self.hidden=True
        self.hide_time=pygame.time.get_ticks()
        self.rect.center=(WIDTH/2,HEIGHT+500)  #把飛船移出畫面外就好

    def weaponup(self):
        self.weapon+=1
        self.weapon_time=pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori=random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image=self.image_ori.copy()
        self.rect=self.image.get_rect()   #定位  
        self.radius=int(self.rect.width*0.85/2)
        # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.x=random.randrange(0,WIDTH-self.rect.width)
        self.rect.y=random.randrange(-180,-100)
        self.speedy=random.randrange(2,5)
        self.speedx=random.randrange(-3,3)
        self.total_degree=0
        self.rot_degree=random.randrange(-3,3)

    def rotate(self):
        self.total_degree+=self.rot_degree
        self.total_degree=self.total_degree%360
        self.image=pygame.transform.rotate(self.image_ori,self.total_degree)
        center=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center=center


    def update(self):
        self.rotate()
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top>HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x=random.randrange(0,WIDTH-self.rect.width)
            self.rect.y=random.randrange(-100,-40)
            self.speedy=random.randrange(2,10)
            self.speedx=random.randrange(-3,3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=bullet_img
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()   #定位
        self.rect.centerx=x
        self.rect.bottom=y
        self.speedy=-10

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=size
        self.image=expl_anim[self.size][0]
        # self.image.set_colorkey(BLACK)  前面載入圖片那裏已經設定好了
        self.rect=self.image.get_rect()   #定位
        self.rect.center=center
        self.frame=0
        self.last_update=pygame.time.get_ticks()
        self.frame_rate=30


    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>self.frame_rate:
            self.last_update=now
            self.frame+=1
            if self.frame==len(expl_anim[self.size]):  #檢查是否到最後一張了
                self.kill()
            else :
                self.image=expl_anim[self.size][self.frame]
                center=self.rect.center
                self.rect=self.image.get_rect()    #定位
                self.rect.center=center

class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type=random.choice(["hp+","weapon"])
        self.image=power_imgs[self.type]
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()   #定位
        self.rect.center=center
        self.speedy=4

    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top>HEIGHT:
            self.kill()
all_sprites=pygame.sprite.Group()
rocks=pygame.sprite.Group()
bullets=pygame.sprite.Group()
powers=pygame.sprite.Group()
player=Player()
all_sprites.add(player)
for i in range(8):
    newrock()
score=0
pygame.mixer.music.play(-1)
#遊戲迴圈
show_init=True
running=True
while running:
    if show_init:
        close= draw_init()
        if close:
            break
        show_init=False
        all_sprites=pygame.sprite.Group()
        rocks=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        powers=pygame.sprite.Group()
        player=Player()
        all_sprites.add(player)
        for i in range(8):
            newrock()
        score=0
    clock.tick(FPS) #一秒之內最多只能執行FPS次
    #取得輸入
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:  #key down 按下鍵盤建
            if event.key==pygame.K_SPACE:
                player.shoot()



    #更新遊戲
    all_sprites.update()  #執行群組裡面每個物件的update函式
    #判斷子彈 石頭碰撞
    hits=pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        expl_sound.play()
        score +=hit.radius
        expl=Explosion(hit.rect.center,"lg")
        all_sprites.add(expl)
        newrock()
        if random.random()>0.9:
            pow=Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
    #判斷石頭 飛船碰撞
    hits=pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)
    for hit in hits:
        player_expl_sound.play()
        newrock()
        player.health-=hit.radius
        expl=Explosion(hit.rect.center,"sm")
        all_sprites.add(expl)
        if player.health<=0:
            player_expl=Explosion(player.rect.center,"player")
            all_sprites.add(player_expl)
            player_expl_sound.play()
            player.lives-=1
            player.health=100
            player.hide()
    #判斷寶物 飛船碰撞
    hits=pygame.sprite.spritecollide(player,powers,True)
    for hit in hits:
        if hit.type=="hp+":
            player.health+=20      
            if player.health>100:
                player.health=100 
            pw1_sound.play()
        if hit.type=="weapon":
            player.weaponup()
            pw2_sound.play()
    if player.lives==0 and not (player_expl.alive()):
        show_init=True
    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,player.health,5,15)
    draw_lives(screen,player.lives,player_mini_img,WIDTH-100,15)
    pygame.display.update()
pygame.quit()