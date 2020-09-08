import pygame, math, random

WIDTH = 800 #Window width.
HEIGHT = 600 #Window height.

TITLE = 'Jo The Pyro' #Window title.
FPS = 60 #Game frames per seconds.
    
#Colours
ORANGE = (242,125,12)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (117,118,118)

def rotateImage(original, angle=0):
    new_images = None #Initialize.
    if type(original) == list: #Check if original is passed as a list.
        new_images = [] #Initialize as list.
        for image in original: #For every image in the list.
            new_images.append(pygame.transform.rotate(image, angle)) #Rotate individual image.
    else:
        new_images = pygame.transform.rotate(original, angle) #Rotate image.

    return new_images

def flipImage(original, horizontal=False, vertical=False):
    new_images = None #Initialize.
    if type(original) == list: #Check if original is passed as a list.
        new_images = [] #Initialize as list.
        for image in original: #For every image in the list.
            new_images.append(pygame.transform.flip(image, horizontal, vertical)) #Rotate individual image.
    else:
        new_images = pygame.transform.flip(original, horizontal, vertical) #Rotate image.

    return new_images

class Animation:

    def __init__(self, images=None, speed=1):
        self.images = images
        self.speed = speed
        self.interval_count = 0 #Initialize;
        self.frame = 0 #Initialize; serve as the index of the images list.
        self.complete = False

    def draw(self, screen, position):
        if type(self.images) == list: #If the image is in list format, and therefore has more than one image...
            if self.frame <= (len(self.images) - 1): #If the frame/index is within the bounds of the list...
                screen.blit(self.images[self.frame], (position[0], position[1])) #Display image to screen.
                self.increaseFrame() #Increase frame.
                self.complete = False

            else: #Else; assume that self.frame has exceeded the list size.
                self.frame = 0 #Reset frame.
                screen.blit(self.images[self.frame], (position[0], position[1])) #Display image to screen.
                self.complete = True

        elif type(self.images) == str: #Check if the image is in str format, and therefore only one image.
            screen.blit(self.images, (position[0], position[1])) #Display image to screen.

    def increaseFrame(self):
        self.interval_count += 1 #Automatically increase interval_count.
        if self.interval_count == self.speed: #Check if interval_count has reached the defined speed.
            self.frame += 1 #Increase frame/index
            self.interval_count = 0 #Reset interval_count.
        else: #Else; assume that interval_count is still less than speed.
            self.frame = self.frame #Keep the same frame.

class Consumable:
    def __init__(self, pos_x, pos_y):
        self.image = None
        self.fuel = 0
        self.health = 0

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.width = 0
        self.height = 0

        self.hitbox = None
        self.rect = None

        self.index = None

    def consume(self, player):
        if player.health + self.health > player.maxhealth:
            player.health = player.maxhealth
        else:
            player.health += self.health

        if player.flamethrower.fuel + self.fuel > player.flamethrower.maxfuel:
            player.flamethrower.fuel = player.flamethrower.maxfuel
        else:
            player.flamethrower.fuel += self.fuel

    def draw(self, screen):
        screen.blit(self.image, (self.pos_x - self.width/2, self.pos_y - self.height/2))

    def createHitbox(self):
        self.hitbox = (self.pos_x - self.width/2, self.pos_y - self.width/2, self.width, self.height)
        self.rect = pygame.Rect(self.hitbox)

class Propane(Consumable):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = pygame.image.load('consumables/propane.png')
        self.fuel = 30
        self.width = 32
        self.height = 32
        self.createHitbox()

class Barrel(Consumable):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = pygame.image.load('consumables/barrel.png')
        self.fuel = 75
        self.width = 64
        self.height = 64
        self.createHitbox()

class Bandages(Consumable):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = pygame.image.load('consumables/bandages.png')
        self.health = 25
        self.width = 32
        self.height = 32
        self.createHitbox()

class Medkit(Consumable):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = pygame.image.load('consumables/medkit.png')
        self.health = 50
        self.width = 32
        self.height = 32
        self.createHitbox()

class Pepper(Consumable):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = pygame.image.load('consumables/pepper.png')
        self.width = 32
        self.height = 32
        self.createHitbox()

    def consume(self, player):
        player.fast = True #Activate/re-activate flag.
        player.fastcount = 0 #Reset timer.

class Steak(Consumable):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = pygame.image.load('consumables/steak.png')
        self.width = 32
        self.height = 32
        self.createHitbox()

    def consume(self, player):
        player.strong = True #Activate/re-activate flag.
        player.strongcount = 0 #Reset timer.

class GoldenMask(Consumable):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = pygame.image.load('consumables/golden_mask.png')
        self.width = 32
        self.height = 32
        self.createHitbox()

    def consume(self, player):
        player.invincible = True #Activate/re-activate flag.
        player.invincount = 0 #Reset timer.

class Enemy:
    
    def __init__(self):
        self.image = None
        self.anim_walkingR = None
        self.anim_walkingL = None
        self.anim_current = self.anim_walkingR

        #Enemy position on screen.
        self.pos_x = 0
        self.pos_y = 0

        self.speed = 5 #Enemy movement speed.

        #These variables affect enemy movement; leave 0.
        self.mov_x = 0
        self.mov_y = 0
        
        #Enemy size dimensions
        self.width = 0
        self.height = 0

        self.hitbox = (self.pos_x, self.pos_y, self.width, self.height) #Will define the hitbox of enemy.
        
        self.index = None

        self.damagecount = 0
        self.health = 150

        self.strength = 1

        self.direction = 'RIGHT'
        
    def spawnEnemy(self):
        #NOTE: Don't forget to add/subtract the enemy size so the enemy doesn't spawn on screen.
        self.pos_x = random.randint(-50, 850)
        if self.pos_x >= 0 and self.pos_x <= WIDTH:
            y_chance = random.randint(1,2)
            if y_chance == 1:
                self.pos_y = HEIGHT + 50
            else:
                self.pos_y = -50
        else:
            self.pos_y = random.randint(0, HEIGHT)

    def calculatePosition(self, player):
        rect = pygame.Rect(self.hitbox)
        player_rect = pygame.Rect(player.hitbox)
        if rect.colliderect(player_rect):
            self.mov_x = 0
        elif player.pos_x + player.size/2 > self.pos_x + self.width/2:
            self.mov_x = self.speed
        elif player.pos_x + player.size/2 < self.pos_x + self.width/2:
            self.mov_x = -self.speed

        if rect.colliderect(player_rect):
            self.mov_y = 0
        elif player.pos_y + player.size/2 > self.pos_y + self.height/2:
            self.mov_y = self.speed 
        elif player.pos_y + player.size/2 < self.pos_y + self.height/2:
            self.mov_y = -self.speed

        #Move the enemy
        self.pos_x += self.mov_x
        self.pos_y += self.mov_y
        
    def updateEnHitbox(self):
        self.hitbox = (self.pos_x, self.pos_y, self.width, self.height) #Will define the hitbox of enemy.
        
    def damageEnemy(self, flamethrower, player):
        rect = pygame.Rect(self.hitbox)
        if player.firing == True:
            flamethrower_rect = pygame.Rect(flamethrower.hitbox)
            if rect.colliderect(flamethrower_rect):
                return True

    def calculateDirection(self, player):
        if player.pos_x > self.pos_x:
            self.direction = 'RIGHT'
        elif player.pos_x < self.pos_x:
            self.direction = 'LEFT'

    def draw(self, screen):
        if self.direction == 'LEFT':
            self.anim_current = self.anim_walkingL
        elif self.direction == 'RIGHT':
            self.anim_current = self.anim_walkingR
        self.anim_current.draw(screen, (self.pos_x, self.pos_y))
            
class Rose(Enemy):
    def __init__(self):
        super().__init__()

        self.img_walking1 = pygame.image.load('enemy/rose_walk(1).png') 
        self.img_walking2 = pygame.image.load('enemy/rose_walk(2).png')
        self.img_walking3 = pygame.image.load('enemy/rose_walk(3).png')
        self.img_walking4 = pygame.image.load('enemy/rose_walk(4).png')
        self.img_walking5 = pygame.image.load('enemy/rose_walk(5).png')

        self.anim_walkingL = Animation(images=[self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking4, self.img_walking5], speed=5)
        self.anim_walkingR = Animation(images=flipImage([self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking4, self.img_walking5], horizontal=True), speed=5)
        
        #Get random position for the x and y component for the enemy to spwan on
        self.pos_x = random.randint(-50, 0) or random.randint(800, 850)
        self.pos_y = random.randint(-50, 0) or random.randint(600, 650)
        
        #Determines the enemy's speed
        self.speed = 0.5
        
        #Size dimensions
        self.width = 40
        self.height = 64

        self.health = 80
           
        self.hitbox = (self.pos_x, self.pos_y, self.width, self.height)

class EvilTree(Enemy):
    def __init__(self):
        super().__init__()

        self.img_walking1 = pygame.image.load('enemy/eviltree_walk(1).png') 
        self.img_walking2 = pygame.image.load('enemy/eviltree_walk(2).png')
        self.img_walking3 = pygame.image.load('enemy/eviltree_walk(3).png')
        self.img_walking4 = pygame.image.load('enemy/eviltree_walk(4).png')
        self.img_walking5 = pygame.image.load('enemy/eviltree_walk(5).png')
        self.img_walking6 = pygame.image.load('enemy/eviltree_walk(6).png')

        self.anim_walkingR = Animation(images=[self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking4, self.img_walking5, self.img_walking6], speed=5)
        self.anim_walkingL = Animation(images=flipImage([self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking4, self.img_walking5, self.img_walking6], horizontal=True), speed=5)
        
        #Get random position for the x and y component for the enemy to spwan on
        self.pos_x = random.randint(-50, 0) or random.randint(800, 850)
        self.pos_y = random.randint(-50, 0) or random.randint(600, 650)
        
        #Determines the enemy's speed
        self.speed = 0.1
        
        self.health = 250

        self.strength = 5

        #Size dimensions
        self.width = 90
        self.height = 96
           
        self.hitbox = (self.pos_x, self.pos_y, self.width, self.height)
        
class EvilSunflower(Enemy):
    def __init__(self):
        super().__init__()

        self.img_walking1 = pygame.image.load('enemy/sunflower_walk(1).png') 
        self.img_walking2 = pygame.image.load('enemy/sunflower_walk(2).png')
        self.img_walking3 = pygame.image.load('enemy/sunflower_walk(3).png')
        self.img_walking4 = pygame.image.load('enemy/sunflower_walk(4).png')
        self.img_walking5 = pygame.image.load('enemy/sunflower_walk(5).png')
        self.img_walking6 = pygame.image.load('enemy/sunflower_walk(6).png')
        self.img_walking7 = pygame.image.load('enemy/sunflower_walk(7).png')
        self.img_walking8 = pygame.image.load('enemy/sunflower_walk(8).png')
        self.img_walking9 = pygame.image.load('enemy/sunflower_walk(9).png')

        self.anim_walkingR = Animation(images=[self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking4, self.img_walking5, self.img_walking6, self.img_walking7, self.img_walking8, self.img_walking9], speed=2)
        self.anim_walkingL = Animation(images=flipImage([self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking4, self.img_walking5, self.img_walking6, self.img_walking7, self.img_walking8, self.img_walking9], horizontal=True), speed=2)
        
        #Get random position for the x and y component for the enemy to spwan on
        self.pos_x = random.randint(-50, 0) or random.randint(800, 850)
        self.pos_y = random.randint(-50, 0) or random.randint(600, 650)
        
        #Determines the enemy's speed
        self.speed = 5.5

        self.health = 45

        self.strength = 1.0
        
        #Size dimensions
        self.width = 38
        self.height = 64
           
        self.hitbox = (self.pos_x, self.pos_y, self.width,self.height)

        self.sprint = True
        self.run_count_max = 15
        self.run_count = 0

    def calculatePosition(self, player):
        rect = pygame.Rect(self.hitbox)
        player_rect = pygame.Rect(player.hitbox)
        if self.sprint:
            if rect.colliderect(player_rect):
                self.mov_x = 0
            elif player.pos_x + player.size/2 > self.pos_x + self.width/2:
                self.mov_x = self.speed
            elif player.pos_x + player.size/2 < self.pos_x + self.width/2:
                self.mov_x = -self.speed

            if rect.colliderect(player_rect):
                self.mov_y = 0
            elif player.pos_y + player.size/2 > self.pos_y + self.height/2:
                self.mov_y = self.speed 
            elif player.pos_y + player.size/2 < self.pos_y + self.height/2:
                self.mov_y = -self.speed

        else:
            self.mov_x = 0
            self.mov_y = 0

        if self.run_count >= self.run_count_max:
            if self.sprint == False:
                self.sprint = True
            else:
                self.sprint = False
            self.run_count = 0

        #Move the enemy
        self.pos_x += self.mov_x
        self.pos_y += self.mov_y

        self.run_count += 1

    def draw(self, screen):
        #If sprinting, show run animation.
        if self.sprint:
            if self.direction == 'LEFT':
                self.anim_current = self.anim_walkingL
            elif self.direction == 'RIGHT':
                self.anim_current = self.anim_walkingR
            self.anim_current.draw(screen, (self.pos_x, self.pos_y))
        #If not sprinting, show standing frame.
        else:
            if self.direction == 'LEFT':
                screen.blit(flipImage(self.img_walking5, horizontal=True), (self.pos_x, self.pos_y))
            elif self.direction == 'RIGHT':
                screen.blit(self.img_walking5, (self.pos_x, self.pos_y))

class EvilBox(Enemy):
    def __init__(self):
        super().__init__()

        self.img_walking1 = pygame.image.load('enemy/evilbox_walk(1).png') 
        self.img_walking2 = pygame.image.load('enemy/evilbox_walk(2).png')
        self.img_walking3 = pygame.image.load('enemy/evilbox_walk(3).png')
        self.img_walking4 = pygame.image.load('enemy/evilbox_walk(4).png')
        self.img_walking5 = pygame.image.load('enemy/evilbox_walk(5).png')
        self.img_walking6 = pygame.image.load('enemy/evilbox_walk(6).png')
        self.img_walking7 = pygame.image.load('enemy/evilbox_walk(7).png')
        self.img_walking8 = pygame.image.load('enemy/evilbox_walk(8).png')
        self.img_walking9 = pygame.image.load('enemy/evilbox_walk(9).png')
        self.img_walking10 = pygame.image.load('enemy/evilbox_walk(10).png')

        self.anim_walkingR = Animation(images=[self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking4, self.img_walking5, self.img_walking6, self.img_walking7, self.img_walking8, self.img_walking9, self.img_walking10], speed=1)
        self.anim_walkingL = Animation(images=flipImage([self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking4, self.img_walking5, self.img_walking6, self.img_walking7, self.img_walking8, self.img_walking9, self.img_walking10], horizontal=True), speed=1)

        #Get random position for the x and y component for the enemy to spwan on
        self.pos_x = random.randint(-50, 0) or random.randint(800, 850)
        self.pos_y = random.randint(-50, 0) or random.randint(600, 650)
        
        #Determines the enemy's speed
        self.speed = 7.0

        self.health = 10

        self.strength = 0.1
        
        #Size dimensions
        self.width = 64
        self.height = 50
           
        self.hitbox = (self.pos_x, self.pos_y, self.width,self.height)

class Watermelon(Enemy):
    def __init__(self, parent):
        super().__init__()

        self.img_walking1 = pygame.image.load('enemy/watermelon_walk(1).png') 
        self.img_walking2 = pygame.image.load('enemy/watermelon_walk(2).png')
        self.img_walking3 = pygame.image.load('enemy/watermelon_walk(3).png')
        self.img_walking4 = pygame.image.load('enemy/watermelon_walk(4).png')
        self.img_walking5 = pygame.image.load('enemy/watermelon_walk(5).png')
        self.img_walking6 = pygame.image.load('enemy/watermelon_walk(6).png')
        self.img_walking7 = pygame.image.load('enemy/watermelon_walk(7).png')
        self.img_walking8 = pygame.image.load('enemy/watermelon_walk(8).png')
        self.img_walking9 = pygame.image.load('enemy/watermelon_walk(9).png')
        self.img_walking10 = pygame.image.load('enemy/watermelon_walk(10).png')
        self.img_walking11 = pygame.image.load('enemy/watermelon_walk(11).png')
        self.img_walking12 = pygame.image.load('enemy/watermelon_walk(12).png')
        self.img_walking13 = pygame.image.load('enemy/watermelon_walk(13).png')
        self.img_walking14 = pygame.image.load('enemy/watermelon_walk(14).png')

        self.anim_walkingR = Animation(images=[self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking4, self.img_walking5, self.img_walking6, self.img_walking7, self.img_walking8, self.img_walking9, self.img_walking10, self.img_walking11, self.img_walking12, self.img_walking13, self.img_walking14], speed=3)
        self.anim_walkingL = Animation(images=flipImage([self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking4, self.img_walking5, self.img_walking6, self.img_walking7, self.img_walking8, self.img_walking9, self.img_walking10, self.img_walking11, self.img_walking12, self.img_walking13, self.img_walking14], horizontal=True), speed=3)

        self.img_shoot1 = pygame.image.load('enemy/watermelon_shoot(1).png')
        self.img_shoot2 = pygame.image.load('enemy/watermelon_shoot(2).png')
        self.img_shoot3 = pygame.image.load('enemy/watermelon_shoot(3).png')
        self.img_shoot4 = pygame.image.load('enemy/watermelon_shoot(4).png')
        self.img_shoot5 = pygame.image.load('enemy/watermelon_shoot(5).png')
        self.img_shoot6 = pygame.image.load('enemy/watermelon_shoot(6).png')
        self.img_shoot7 = pygame.image.load('enemy/watermelon_shoot(7).png')
        self.img_shoot8 = pygame.image.load('enemy/watermelon_shoot(8).png')
        self.img_shoot9 = pygame.image.load('enemy/watermelon_shoot(9).png')
        self.img_shoot10 = pygame.image.load('enemy/watermelon_shoot(10).png')
        self.img_shoot11 = pygame.image.load('enemy/watermelon_shoot(11).png')
        
        self.anim_shoot = Animation(images=[self.img_shoot1, self.img_shoot2, self.img_shoot3, self.img_shoot4, self.img_shoot5, self.img_shoot6, self.img_shoot7, self.img_shoot8, self.img_shoot9, self.img_shoot10, self.img_shoot11], speed=2)
        
        self.anim_current = self.anim_walkingR

        #Get random position for the x and y component for the enemy to spwan on
        self.pos_x = random.randint(-50, 0) or random.randint(800, 850)
        self.pos_y = random.randint(-50, 0) or random.randint(600, 650)
        
        #Determines the enemy's speed
        self.speed = 0.5

        self.health = 25

        self.strength = 0.5
        
        #Size dimensions
        self.width = 32
        self.height = 32
           
        self.hitbox = (self.pos_x, self.pos_y, self.width,self.height)

        self.shooting = False #Flag for the shooting animation.
        self.shoot_count = 0
        self.shoot_count_max = 25

        self.direction = None #Initialize; represents direction of firing.

        #Give access to the game functions and lists.
        self.parent = parent

    def calculatePosition(self, player):
        watermelon_axis_x = pygame.Rect(player.pos_x - 220, player.pos_y + player.size/2, 440 + player.size, 1)
        watermelon_axis_y = pygame.Rect(player.pos_x + player.size/2, player.pos_y - 145, 1, 290 + player.size)
        watermelon_rect_x = pygame.Rect(self.pos_x, self.pos_y + self.height/2, self.width, 1)
        watermelon_rect_y = pygame.Rect(self.pos_x + self.width/2, self.pos_y, 1, self.height)
        watermelon_rect = pygame.Rect(self.hitbox)
        player_rect = pygame.Rect(player.hitbox)
        if watermelon_rect_x.colliderect(watermelon_axis_x):
            if self.pos_x > player.pos_x: #Check if enemy is to the right of the player.
                self.direction = 'LEFT' #Set direction of firing; always opposite.
            elif self.pos_x < player.pos_x: #Check if enemy is to the left.
                self.direction  = 'RIGHT'

            self.mov_x = 0
            self.mov_y = 0
            self.shoot_count += 1
            self.shooting = True

        elif watermelon_rect_y.colliderect(watermelon_axis_y):
            if self.pos_y < player.pos_y: #Check if enemy is above the player.
                self.direction = 'DOWN'
            elif self.pos_y > player.pos_y: #Check if enemy is below.
                self.direction  = 'UP'

            self.mov_x = 0
            self.mov_y = 0
            self.shoot_count += 1
            self.shooting = True

        else:
            self.shoot_count = 0 #Reset shoot count.
            self.shooting = False
            if player_rect.colliderect(watermelon_rect):
                self.mov_x = 0
                self.mov_y = 0
            else:
                if player.pos_x + player.size > self.pos_x + self.width:
                    self.mov_x = self.speed
                elif player.pos_x + player.size < self.pos_x + self.width:
                    self.mov_x = -self.speed

                if player.pos_y + player.size > self.pos_y + self.height:
                    self.mov_y = self.speed 
                elif player.pos_y + player.size < self.pos_y + self.height:
                    self.mov_y = -self.speed

        if self.shoot_count >= self.shoot_count_max:
            self.shoot(self.parent)
            self.shoot_count = 0

        #Move the enemy
        self.pos_x += self.mov_x
        self.pos_y += self.mov_y

        #Move the enemy
        self.pos_x += self.mov_x
        self.pos_y += self.mov_y

    def shoot(self, game):
        strong_chance = random.randint(1,15)

        if strong_chance == 15:
            strong = True
        else: 
            strong = False

        x_projectile = Projectile(self.pos_x + self.width/2, self.pos_y + self.width/2, self.direction, strong)
        x_projectile.index = len(game.projectiles)    
        game.projectiles.append(x_projectile)

    def draw(self, screen):
        if self.shooting:
            self.anim_current = self.anim_shoot
        else:
            if self.direction == 'LEFT':
                self.anim_current = self.anim_walkingL
            elif self.direction == 'RIGHT':
                self.anim_current = self.anim_walkingR
        self.anim_current.draw(screen, (self.pos_x, self.pos_y))

class Projectile():
    def __init__(self, pos_x, pos_y, direction, strong=False):
        self.image = None

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.speed = 6
        self.size = 16

        self.index = None

        self.updateHitbox()

        self.direction = direction

        if strong == True:
            self.strength = 6
            self.colour = BLACK
        else:
            self.strength = 3
            self.colour = WHITE

    def move(self):
        if self.direction == 'UP':
            self.pos_y -= self.speed
        elif self.direction == 'DOWN':
            self.pos_y += self.speed
        elif self.direction == 'LEFT':
            self.pos_x -= self.speed
        elif self.direction == 'RIGHT':
            self.pos_x += self.speed

    def checkForCollision(self, player):
        x_rect = pygame.Rect(self.hitbox)
        player_rect = pygame.Rect(player.hitbox)
        if self.pos_x >= WIDTH or self.pos_x <= 0 or self.pos_y <= 0 or self.pos_y >= HEIGHT or x_rect.colliderect(player_rect):
            return True
        else:
            return False

    def draw(self, screen):
        self.updateHitbox()
        if self.image == None:
            pygame.draw.circle(screen, self.colour, (int(self.pos_x), int(self.pos_y)), int(self.size/2), 0)
        else:
            screen.blit(self.image, (self.pos_x, self.pos_y))

    def updateHitbox(self):
        self.hitbox = (self.pos_x - self.size/2, self.pos_y - self.size/2, self.size, self.size)

class Player:
    def __init__(self):
        self.img_standing1 = pygame.image.load('player/player_idle(1).png')
        self.img_standing2 = pygame.image.load('player/player_idle(2).png')
        self.img_standing3 = pygame.image.load('player/player_idle_front(1).png')
        self.img_standing4 = pygame.image.load('player/player_idle_front(2).png')
        self.img_standing5 = pygame.image.load('player/player_idle_back(1).png')
        self.img_standing6 = pygame.image.load('player/player_idle_back(2).png')

        self.img_walking1 = pygame.image.load('player/player_walk(1).png')
        self.img_walking2 = pygame.image.load('player/player_walk(2).png')
        self.img_walking3 = pygame.image.load('player/player_walk(3).png')
        self.img_walking4 = pygame.image.load('player/player_walk_front(1).png')
        self.img_walking5 = pygame.image.load('player/player_walk_front(2).png')
        self.img_walking6 = pygame.image.load('player/player_walk_front(3).png')
        self.img_walking7 = pygame.image.load('player/player_walk_back(1).png')
        self.img_walking8 = pygame.image.load('player/player_walk_back(2).png')
        self.img_walking9 = pygame.image.load('player/player_walk_back(3).png')

        self.anim_standingR = Animation(images=[self.img_standing1, self.img_standing2], speed=10)
        self.anim_standingL = Animation(images=flipImage([self.img_standing1, self.img_standing2], horizontal=True), speed=10)
        self.anim_standingD = Animation(images=[self.img_standing3, self.img_standing4], speed=10)
        self.anim_standingU = Animation(images=[self.img_standing5, self.img_standing6], speed=10)

        self.anim_walkingR = Animation(images=[self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking2], speed=5)
        self.anim_walkingL = Animation(images=flipImage([self.img_walking1, self.img_walking2, self.img_walking3, self.img_walking2], horizontal=True), speed=5)
        self.anim_walkingD = Animation(images=[self.img_walking4, self.img_walking5, self.img_walking6, self.img_walking5], speed=5)
        self.anim_walkingU = Animation(images=[self.img_walking7, self.img_walking8, self.img_walking9, self.img_walking8], speed=5)

        self.anim_current = self.anim_standingR

        #Initialize player position at center of screen.
        self.pos_x = (WIDTH * 0.5)
        self.pos_y = (WIDTH * 0.5)

        self.speed = 5 #Player movement speed.

        self.direction = 'RIGHT' #Initialize direction.
        self.moving = False

        #These variables also affect player movement.
        self.mov_x = 0
        self.mov_y = 0
        
        self.hitbox = (self.pos_x, self.pos_y, 32, 32) # Will define the hitbox of the player
        self.health = 100
        self.maxhealth = 100
        self.flamethrower = Flamethrower(self)
        self.firing = False #Flag for flamethrower

        self.size = 32 #Size in pixels. If it fits in a square than the length and width is the same.

        self.strength = 1

        self.fast = False
        self.strong = False
        self.invincible = False

        self.fastcount = 0
        self.fastcount_max = 300

        self.strongcount = 0
        self.strongcount_max = 200

        self.invincount = 0
        self.invincount_max = 200

    def draw(self, screen):
        self.anim_current.draw(screen, (self.pos_x,self.pos_y))

    def updateHitbox(self):
        self.hitbox = (self.pos_x, self.pos_y, self.size, self.size)

    def updateCurrentAnimation(self):
        if self.direction == 'UP' and self.moving == False:
            self.anim_current = self.anim_standingU
        elif self.direction == 'DOWN' and self.moving == False:
            self.anim_current = self.anim_standingD
        elif self.direction == 'LEFT' and self.moving == False:
            self.anim_current = self.anim_standingL
        elif self.direction == 'RIGHT' and self.moving == False:
            self.anim_current = self.anim_standingR

        elif self.direction == 'UP' and self.moving == True:
            self.anim_current = self.anim_walkingU
        elif self.direction == 'DOWN' and self.moving == True:
            self.anim_current = self.anim_walkingD
        elif self.direction == 'LEFT' and self.moving == True:
            self.anim_current = self.anim_walkingL
        elif self.direction == 'RIGHT' and self.moving == True:
            self.anim_current = self.anim_walkingR
            
    def updateMovement(self):
        #Update player coords; include boundaries.
        if self.pos_x + self.mov_x <= 0:
            self.pos_x = 0
        elif self.pos_x + self.mov_x >= WIDTH - self.size:
            self.pos_x = WIDTH - self.size
        else:
            self.pos_x += self.mov_x

        if self.pos_y + self.mov_y <= 0:
            self.pos_y = 0
        elif self.pos_y + self.mov_y >= HEIGHT - self.size:
            self.pos_y = HEIGHT - self.size
        else: 
            self.pos_y += self.mov_y

class Flamethrower:
    def __init__(self, parent):
        self.img_start1 = pygame.image.load('fire/fire_startup(1).png')
        self.img_start2 = pygame.image.load('fire/fire_startup(2).png')
        self.img_start3 = pygame.image.load('fire/fire_startup(3).png')
        self.img_active1 = pygame.image.load('fire/fire_active(1).png')
        self.img_active2 = pygame.image.load('fire/fire_active(2).png')
        self.img_active3 = pygame.image.load('fire/fire_active(3).png')

        self.anim_startupL = Animation(images=[self.img_start1, self.img_start2, self.img_start3], speed=1)
        self.anim_activeL = Animation(images=[self.img_active1, self.img_active2, self.img_active3], speed=2)

        self.anim_startupR = Animation(images=flipImage([self.img_start1, self.img_start2, self.img_start3], horizontal=True), speed=1)
        self.anim_activeR = Animation(images=flipImage([self.img_active1, self.img_active2, self.img_active3], horizontal=True), speed=2)

        self.anim_startupD = Animation(images=rotateImage([self.img_start1, self.img_start2, self.img_start3], angle=90), speed=1)
        self.anim_activeD = Animation(images=rotateImage([self.img_active1, self.img_active2, self.img_active3], angle=90), speed=2)

        self.anim_startupU = Animation(images=rotateImage([self.img_start1, self.img_start2, self.img_start3], angle=270), speed=1)
        self.anim_activeU = Animation(images=rotateImage([self.img_active1, self.img_active2, self.img_active3], angle=270), speed=2)

        self.anim_current = [self.anim_startupR, self.anim_activeR]

        self.height = 32
        self.width = 96

        self.fuel = 100
        self.maxfuel = 100

        self.active = False

        self.updateHitbox(parent)

    def updateHitbox(self, parent): 
        if parent.direction == 'UP':
            self.hitbox = (parent.pos_x + self.width/4 - 24, parent.pos_y - self.width, self.height, self.width)
            self.anim_current = [self.anim_startupU, self.anim_activeU]
        elif parent.direction == 'DOWN':
            self.hitbox = (parent.pos_x + self.width/4 - 24, parent.pos_y + self.width/2 - 16, self.height, self.width)
            self.anim_current = [self.anim_startupD, self.anim_activeD]
        elif parent.direction == 'LEFT':
            self.hitbox = (parent.pos_x - 95, parent.pos_y + self.height/2 - 13, self.width, self.height)
            self.anim_current = [self.anim_startupL, self.anim_activeL]
        elif parent.direction == 'RIGHT':
            self.hitbox = (parent.pos_x + 32, parent.pos_y + self.height/2 - 13, self.width, self.height)
            self.anim_current = [self.anim_startupR, self.anim_activeR]

    def draw(self,screen):

        if self.anim_current[0].complete == False:
            self.anim_current[0].draw(screen, (self.hitbox[0], self.hitbox[1]))
        else:
            self.anim_current[1].draw(screen, (self.hitbox[0], self.hitbox[1]))

class Game:  
    def __init__(self):
        #Initialize game window, etc.
        pygame.init()
        pygame.mixer.init() #Initialize the mixer for sound loading and playback.
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.start_menu = Menu(self, self.screen)
        self.start_menu.running = True #Activate menu flag.
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.img_background = pygame.image.load('environment/background.gif')
        self.img_treesU = pygame.image.load('environment/bg_treesU.png')
        self.img_treesD = pygame.image.load('environment/bg_treesD.png')
        self.img_treesL = pygame.image.load('environment/bg_treesL.png')
        self.img_treesR = pygame.image.load('environment/bg_treesR.png')

        self.img_tent = pygame.image.load('environment/tent.png')
        self.img_campfire1 = pygame.image.load('environment/campfire1.png')
        self.img_campfire2 = pygame.image.load('environment/campfire2.png')
        self.img_campfire3 = pygame.image.load('environment/campfire3.png')
        self.img_campfire4 = pygame.image.load('environment/campfire4.png')
        self.img_campfire5 = pygame.image.load('environment/campfire5.png')
        self.img_campfire6 = pygame.image.load('environment/campfire6.png')
        self.img_campfire7 = pygame.image.load('environment/campfire7.png')
        self.img_campfire8 = pygame.image.load('environment/campfire8.png')
        self.img_campfire9 = pygame.image.load('environment/campfire9.png')
        self.img_campfire10 = pygame.image.load('environment/campfire10.png')
        self.img_campfire11 = pygame.image.load('environment/campfire11.png')
        self.img_campfire12 = pygame.image.load('environment/campfire12.png')
        self.img_campfire13 = pygame.image.load('environment/campfire13.png')

        self.anim_campfire = Animation(images=[self.img_campfire1, self.img_campfire2, self.img_campfire3, self.img_campfire4, self.img_campfire5, self.img_campfire6, 
            self.img_campfire7, self.img_campfire8, self.img_campfire9, self.img_campfire10, self.img_campfire11, self.img_campfire12, self.img_campfire13], speed=5)

        self.img_grass1 = pygame.image.load('environment/grass1.png')
        self.img_grass2 = pygame.image.load('environment/grass2.png')
        self.img_grass3 = pygame.image.load('environment/grass3.png')
        self.img_grass4 = pygame.image.load('environment/grass4.png')

        self.anim_grass = Animation(images=[self.img_grass1, self.img_grass2, self.img_grass3, self.img_grass4], speed=5)

        self.img_burntstump1 = pygame.image.load('environment/burnt_stump1.png')
        self.img_burntstump2 = pygame.image.load('environment/burnt_stump2.png')

        self.img_healthbar = pygame.image.load('ui/healthbar.png')
        self.img_fuelbar = pygame.image.load('ui/fuelbar.png')
        self.img_score = pygame.image.load('ui/score.png')
        self.music_on = False
 
    def new(self):
        #Create new game, reset variables, etc.
        self.player = Player()
        self.enemies = []
        self.consumables = []
        self.projectiles = []
        self.score = 0 #Initialize.
        self.max_enemies = 10
        self.base_addition = 10
        self.enemy_spawnrate = [1,100]
        self.consum_spawnrate = [1, 2]
        self.score_thousand = 1

        self.killstreak = False
        self.killtime = 0
        self.killtime_limit = 400
        self.killcount = 0
        self.killcount_mark = 5

        self.game_over = False

    def run(self):
        pygame.mixer.music.rewind()
        music = random.randint(1,3)
        music = 'sound/fight' + str(music) + '.mid'
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(loops=-1)
        while self.playing:
            self.events()
            self.clock.tick(FPS)
            self.draw()
            self.update()
        pygame.mixer.music.stop()
            
    def events(self):
        keypresses = {'A':pygame.K_a,
                    'D':pygame.K_d,
                    'W':pygame.K_w,
                    'S':pygame.K_s,
                    'LEFT':pygame.K_LEFT,
                    'RIGHT':pygame.K_RIGHT,
                    'UP':pygame.K_UP,
                    'DOWN':pygame.K_DOWN}

        #Check for each event during game loop.
        for event in pygame.event.get():
            #Check for window exit.
            if event.type == pygame.QUIT:
                #End both game loops
                if self.playing == True:
                    self.playing = False
                self.running = False
            
            #Check for key press.
            if event.type == pygame.KEYDOWN:
                #Check if left key for movement was pressed.
                if event.key == keypresses['A']:
                    self.player.mov_x = -self.player.speed
                #Check if right key for movement was pressed.
                elif event.key == keypresses['D']:
                    self.player.mov_x = self.player.speed
                #Check if up key for movement was pressed.
                if event.key == keypresses['W']:
                    self.player.mov_y = -self.player.speed
                #Check if down key for movement was pressed.
                elif event.key == keypresses['S']:
                    self.player.mov_y = self.player.speed
                #Diagonal movement.
                if self.player.mov_x != 0 and self.player.mov_y != 0:
                    self.player.mov_x = self.player.mov_x*(math.sqrt(2)/2)
                    self.player.mov_y = self.player.mov_y*(math.sqrt(2)/2)

                if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S']:
                    self.player.moving = True

                #Check if left key for direction was pressed.
                if event.key == keypresses['LEFT']:
                    self.player.direction = 'LEFT'
                #Check if right key for direction was pressed.
                elif event.key == keypresses['RIGHT']:
                    self.player.direction = 'RIGHT'
                #Check if up key for direction was pressed.
                if event.key == keypresses['UP']:
                    self.player.direction = 'UP'
                #Check if down for direction key was pressed.
                elif event.key == keypresses['DOWN']:
                    self.player.direction = 'DOWN'

                #Check for any of the directional keypresses; activate the flamethrower.
                if event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                    self.player.firing = True
                
            #Check for key release.
            if event.type == pygame.KEYUP:
                if event.key == keypresses['A'] or event.key == keypresses['D'] or event.key == keypresses['W'] or event.key == keypresses['S']:
                    self.player.mov_x = 0 
                    self.player.mov_y = 0
                    self.player.moving = False

                if event.key == keypresses['LEFT'] or event.key == keypresses['RIGHT'] or event.key == keypresses['UP'] or event.key == keypresses['DOWN']:
                    self.player.firing = False
                    for anim in self.player.flamethrower.anim_current:
                        anim.complete = False

        #Subtract the player fuel    
        if self.player.firing:
            self.subtractFuel()
                    
        if len(self.enemies) > 0:
            for enemy in self.enemies:
                enemy.calculateDirection(self.player)
                #Create a 'pretend' hitbox if the player were to move into their next position
                player_hitbox = (self.player.hitbox[0] + self.player.mov_x, self.player.hitbox[1] + self.player.mov_y, self.player.hitbox[2], self.player.hitbox[3])
                player_rect = pygame.Rect(player_hitbox)
                enemy_rect_top = pygame.Rect(enemy.hitbox[0] + 2, enemy.hitbox[1], enemy.hitbox[2] - 4, 1)
                enemy_rect_bottom = pygame.Rect(enemy.hitbox[0] + 2, enemy.hitbox[1] + enemy.height, enemy.hitbox[2] - 4, 1)
                enemy_rect_left = pygame.Rect(enemy.hitbox[0], enemy.hitbox[1] + 2, 1, enemy.hitbox[3] - 4)
                enemy_rect_right = pygame.Rect(enemy.hitbox[0] + enemy.width, enemy.hitbox[1] + 2, 1, enemy.hitbox[3] - 4)
                if player_rect.colliderect(enemy_rect_bottom) or player_rect.colliderect(enemy_rect_top):
                    self.player.mov_y = 0
                    if self.player.invincible == False:
                        self.player.health -= enemy.strength
                if player_rect.colliderect(enemy_rect_left) or player_rect.colliderect(enemy_rect_right):
                    self.player.mov_x = 0
                    if self.player.invincible == False:
                        self.player.health -= enemy.strength


        if len(self.consumables) > 0:
            for consumable in self.consumables:
                #player_hitbox = (self.player.hitbox[0], self.player.hitbox[1], self.player.hitbox[2], self.player.hitbox[3])
                player_rect = pygame.Rect(self.player.hitbox)

                #Check if player collides with a consumable.
                if player_rect.colliderect(consumable.rect):
                    #Consume consumable and get its fuel + health.
                    consumable.consume(self.player)

                    #Delete consumable.
                    del self.consumables[consumable.index]
            
                #Reset consumables list.
                x_consumables =[]
                for consumable in self.consumables:
                    consumable.index = len(x_consumables)
                    x_consumables.append(consumable)
                    self.consumables = x_consumables


        if self.player.fast and self.player.fastcount < self.player.fastcount_max:
            self.player.speed = 10
            self.player.fastcount += 1
        elif self.player.fastcount >= self.player.fastcount_max:
            self.player.fast = False
            self.player.speed = 5
            self.player.fastcount = 0

        if self.player.strong and self.player.strongcount < self.player.strongcount_max:
            self.player.strength = 10
            self.player.strongcount += 1
        elif self.player.strongcount >= self.player.strongcount_max:
            self.player.strong = False
            self.player.strength = 1
            self.player.strongcount = 0

        if self.player.invincible and self.player.invincount < self.player.invincount_max:
            self.player.invincount += 1
        elif self.player.invincount >= self.player.invincount_max:
            self.player.invincible = False
            self.player.invincount = 0


        self.player.updateMovement()

        #Update player animation.
        self.player.updateCurrentAnimation()

        #Change direction of fire hitbox.
        self.player.flamethrower.updateHitbox(self.player)

        #Check if player dies.
        if self.player.health <= 0:
            self.playing = False
            self.game_over = True
    
        #To determine whether an enemy should be spawned or not. If True, spawn an enemy.
        if self.getSpawnChance(self.enemy_spawnrate[0], self.enemy_spawnrate[1]) == True and len(self.enemies) < self.max_enemies:
            random_enemy = random.randint(1,100)
            if random_enemy >= 1 and random_enemy <= 50: #51 out of 100 chance.
                enemy = Rose()
            elif random_enemy >= 51 and random_enemy <= 66: #16 out of 100 chance.
                enemy = EvilSunflower()
            elif random_enemy >= 67 and random_enemy <= 87: #21 out of 100 chance.
                enemy = Watermelon(self)
            elif random_enemy >= 88 and random_enemy <= 99: #11 out of 100 chance.
                enemy = EvilTree()
            elif random_enemy == 100: #1 out of 100 chance. 
                enemy = EvilBox()
            enemy.spawnEnemy()
            enemy.index = len(self.enemies)
            self.enemies.append(enemy)

        #Calculate the enemy's movement.
        for enemy in self.enemies:
            enemy.calculatePosition(self.player)
            enemy.updateEnHitbox()
            if enemy.damageEnemy(self.player.flamethrower, self.player):
                enemy.damagecount += self.player.strength
                #Check if enemy dies.
                if enemy.damagecount >= enemy.health:
                    self.killcount += 1 #Increase the killstreak count.
                    self.killtime = 0 #Reset/extend the killstreak timer.
                    #Check if a consumable should spawn.
                    if self.getSpawnChance(self.consum_spawnrate[0], self.consum_spawnrate[1]) == True:
                        x_chance = random.randint(1,100)

                        #Determine which consumable to spawn.
                        if x_chance >= 1 and x_chance <= 24: #25% chance for propane to spawn
                            x_consumable = Propane(enemy.pos_x + enemy.width/2, enemy.pos_y + enemy.height/2)
                        elif x_chance >= 25 and x_chance <= 34: #10% chance for barrel to spawn
                            x_consumable = Barrel(enemy.pos_x + enemy.width/2, enemy.pos_y + enemy.height/2)
                        elif x_chance >= 35 and x_chance <= 54: #20% chance for bandages to spawn
                            x_consumable = Bandages(enemy.pos_x + enemy.width/2, enemy.pos_y + enemy.height/2)
                        elif x_chance >= 55 and x_chance <= 64: #10% chance for medkit to spawn
                            x_consumable = Medkit(enemy.pos_x + enemy.width/2, enemy.pos_y + enemy.height/2)
                        elif x_chance >= 65 and x_chance <= 79: #15% chance for pepper to spawn
                            x_consumable = Pepper(enemy.pos_x + enemy.width/2, enemy.pos_y + enemy.height/2)
                        elif x_chance >= 80 and x_chance <= 91: # 12% chance for steak to spawn
                            x_consumable = Steak(enemy.pos_x + enemy.width/2, enemy.pos_y + enemy.height/2)
                        elif x_chance >= 92 and x_chance <= 100: #8% chance for goldenmask to spawn
                            x_consumable = GoldenMask(enemy.pos_x + enemy.width/2, enemy.pos_y + enemy.height/2)

                        #Spawn consumable.
                        x_consumable.index = len(self.consumables)
                        self.consumables.append(x_consumable)

                    #Delete enemy.
                    del self.enemies[enemy.index]

                    #Increase score
                    self.calculateScore(enemy)

                    #Recreate self.enemies list.
                    x_enemies = []
                    for enemy in self.enemies:
                        enemy.index = len(x_enemies) 
                        x_enemies.append(enemy)
                        self.enemies = x_enemies

        #Calculate projectiles' movement.
        for projectile in self.projectiles:
            if projectile.checkForCollision(self.player) and self.player.invincible == False:
                self.player.health -= projectile.strength
                #Delete projectile.
                del self.projectiles[projectile.index]

                #Recreate self.projectiles list.
                x_projectiles = []
                for projectile in self.projectiles:
                    projectile.index = len(x_projectiles) 
                    x_projectiles.append(projectile)
                    self.projectiles = x_projectiles
            else:
                projectile.move()

        #Automatically add fuel to the player.
        self.addFuel()

        #Kill streak checks.
        if self.killstreak == True and self.killtime >= self.killtime_limit:
            self.killstreak = False
            self.base_addition = 10
            self.killtime = 0
            self.killcount = 0
        elif self.killstreak == True:
            self.base_addition = 10 * self.killcount
            self.killtime += 1
        elif self.killstreak == False and self.killcount >= self.killcount_mark:
            self.killstreak = True

    def addFuel(self):
        if self.player.flamethrower.fuel + 1 > self.player.flamethrower.maxfuel and self.player.firing == False:
            self.player.flamethrower.fuel = self.player.flamethrower.maxfuel
        else:
            self.player.flamethrower.fuel += 0.05

    def subtractFuel(self):
        if self.player.flamethrower.fuel <= 0:
            self.player.firing = False    
        if self.player.firing:
            self.player.flamethrower.fuel -= 0.2

    #Calculate if an enemy should spawn.
    def getSpawnChance(self, x_start=1, x_end=100):
        spawn_chance = random.randint(x_start, x_end)
        if spawn_chance == 1:
            return True
        else:
            return False

    #Draw everything during the game loop.
    def draw(self):
        #self.screen.fill(GREEN)

        self.drawBackground()
        
        for consumable in self.consumables:
            consumable.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)
            pygame.draw.rect(self.screen, BLACK, (enemy.hitbox[0], enemy.hitbox[1] - 15, enemy.width, 10)) #Draw black (background) enemy health bar.
            pygame.draw.rect(self.screen, RED, (enemy.hitbox[0], enemy.hitbox[1] - 15, enemy.width - (enemy.width/enemy.health * (enemy.health - (enemy.health - enemy.damagecount))), 10)) #Draw red enemy health bar.

   
        #Will update the hitbox as the player moves.
        self.player.updateHitbox()
        self.player.draw(self.screen)

        for projectile in self.projectiles:
            projectile.draw(self.screen)

        if self.player.firing == True:
            self.player.flamethrower.draw(self.screen)

        self.drawOverlay()

        #Draw player health.
        pygame.draw.rect(self.screen, RED, (40, 24, self.player.health, 20))

        #Draw fuel bar.
        pygame.draw.rect(self.screen, ORANGE, (160, 24, self.player.flamethrower.fuel, 20))
            
        
    def update(self):
        #Update the screen during game loop.
        pygame.display.update()

    def drawBackground(self):
        self.screen.blit(self.img_background, (0,0))
        self.screen.blit(self.img_tent, (400, HEIGHT/2 - 150))
        self.anim_campfire.draw(self.screen, (355, HEIGHT/2 - 85))
        x_grass = [self.anim_grass, self.anim_grass, self.anim_grass, self.anim_grass, self.anim_grass, self.anim_grass, self.anim_grass, self.anim_grass, self.anim_grass, self.anim_grass, self.anim_grass, self.anim_grass, self.anim_grass]
        
        x_grass[0].draw(self.screen, (375, 285))
        x_grass[1].draw(self.screen, (479, 530))
        x_grass[2].draw(self.screen, (256, 189))
        x_grass[3].draw(self.screen, (500, 54))
        x_grass[4].draw(self.screen, (154, 498))
        x_grass[5].draw(self.screen, (700, 500))
        x_grass[6].draw(self.screen, (600, 450))
        x_grass[7].draw(self.screen, (100, 560))
        x_grass[8].draw(self.screen, (217, 110))
        x_grass[9].draw(self.screen, (100, 350))
        x_grass[10].draw(self.screen, (630, 150))
        x_grass[11].draw(self.screen, (300, 300))
        x_grass[12].draw(self.screen, (297, 445))
        
        self.screen.blit(self.img_burntstump1, (50,60))
        self.screen.blit(self.img_burntstump1, (400,350))
        self.screen.blit(self.img_burntstump2, (175,300))
        self.screen.blit(self.img_burntstump2, (550,200))


    def drawOverlay(self):
        self.screen.blit(self.img_treesU, (0, -10))
        self.screen.blit(self.img_treesL, (-22,0))
        self.screen.blit(self.img_treesR, (WIDTH - 32,0))
        self.screen.blit(self.img_treesD, (0, HEIGHT-54))
        #Draw fuel and healthbar.
        self.screen.blit(self.img_healthbar, (-10,0))
        self.screen.blit(self.img_fuelbar, (110,0))
        self.screen.blit(self.img_score, (635,2))

        if self.player.fast:
            x_temp = Pepper(53, 65)
            x_temp.draw(self.screen)
        if self.player.strong:
            x_temp = Steak(88, 65)
            x_temp.draw(self.screen)
        if self.player.invincible:
            x_temp = GoldenMask(123, 65)
            x_temp.draw(self.screen)

        if self.player.fast or self.player.strong or self.player.invincible:
            self.screen.blit(pygame.image.load('ui/emptybar.png'), (34, 50))

        if self.killstreak:
            self.screen.blit(pygame.image.load('ui/killstreak.png'), (647, 50))

        #Display the score.
        self.displayScore()

    def calculateScore(self, enemy):
        self.score += int(self.base_addition + (enemy.health / 2))
        #If enemy limit has not been reached and the player has reached another thousand points, increase difficulty.
        if self.max_enemies < 100 and int(self.score / 500) >= self.score_thousand:
            self.max_enemies += 1
            self.score_thousand += 1
            if self.enemy_spawnrate[1] >= 25:
                self.enemy_spawnrate[1] -= 1
            if self.consum_spawnrate[1] <= 35:
                self.consum_spawnrate[1] += 1

    def displayScore(self):
        font = pygame.font.SysFont('Arial', 23)
        text = font.render(str(self.score), True, WHITE)
        self.screen.blit(text, (WIDTH - 139, 20))

    def getMainMenu(self):
        self.start_menu.run() #Run menu.

    def getGameOver(self):
        img_gameover = pygame.image.load('ui/game_over.png')
        img_player = pygame.image.load('player/player_gameover.png')
        btn_restart = Button(self.screen, image='ui/tryagain.png', position=(150,500))
        btn_mainmenu = Button(self.screen, image='ui/mainmenu.png', position=(450,500))
        buttons = [btn_restart, btn_mainmenu]

        while self.game_over:
            self.screen.fill(BLACK)
            self.screen.blit(img_gameover, (WIDTH/4 + 50, HEIGHT/2 - 100))
            self.screen.blit(img_player, ((WIDTH/4 + 135, HEIGHT/2)))
            font = pygame.font.SysFont('Arial', 30)
            text = font.render('Score: ' + str(self.score), True, WHITE)
            text_width = text.get_width()
            self.screen.blit(text, (WIDTH/2 - text_width/2,430))
            btn_restart.draw()
            btn_mainmenu.draw()

            for event in pygame.event.get():
                self.mouse_pos = pygame.mouse.get_pos() # Get mouse position at time of press.

                #Check for window exit.
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                    self.game_over = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = event.pos  # Get mouse position at time of press.
                    for button in buttons:
                        if button.rect_obj.collidepoint(self.mouse_pos):
                            button.active = True #Activate button.

            #Check if player wants to restart.
            if btn_restart.active == True:
                self.game_over = False #End this while loop.
                self.playing = True #Activate game flag.
                btn_restart.active = False #Deactivate this button.

            #Check if player wants to go back to main menu.
            elif btn_mainmenu.active == True:
                self.game_over = False #End this while loop.
                self.start_menu.running = True #Activate start menu flag.
                btn_restart.active = False

            pygame.display.update()
    
class Menu:
    def __init__(self, parent, screen):
        self.img_logo = pygame.image.load('ui/title_logo.png')
        self.img_company_logo = pygame.image.load('ui/company_logo.png')
        self.start_button = Button(screen, image='ui/start.png', position=(300,350))
        self.help_button = Button(screen, image='ui/help.png', position=(300,425))
        self.quit_button = Button(screen, image='ui/quit.png', position=(300,500))
        self.credit_button = Button(screen, image='ui/credits_button.png', position=(0,550))
        self.parent = parent
        self.buttons = [self.start_button, self.help_button, self.quit_button, self.credit_button]
        self.running = None #Initialize flag.
        self.x_rose = Rose()
        self.x_sunflow = EvilSunflower()
        self.x_tree = EvilTree()
        self.x_melon = Watermelon(parent)
        self.x_box = EvilBox()

    def run(self):
        while self.running:
            self.events()
            self.draw()
            self.update()

    def events(self):
        for event in pygame.event.get():
            self.mouse_pos = pygame.mouse.get_pos() # Get mouse position at time of press.

            #Check for window exit.
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = event.pos  # Get mouse position at time of press.
                for button in self.buttons:
                    if button.rect_obj.collidepoint(self.mouse_pos):
                        button.active = True #Activate button.

        #If the start button has been activated...
        if self.start_button.active == True:
            self.running = False #End menu loop.
            self.parent.playing = True
            self.start_button.active = False #Deactivate button.

        #If the help button has been activated.
        elif self.help_button.active == True:
            self.displayHelp() #Display help menu.
            self.help_button.active = False #Deactivate button.

        #If quit utton has been activated.
        elif self.quit_button.active == True:
            self.quit() #Quit game.
            self.quit_button.active = False #Deactivate button.

        elif self.credit_button.active == True:
            self.displayCredits() #Display credits.
            self.credit_button.active = False #Deactivate button

    def draw(self):
        self.parent.screen.fill(BLACK) #Fill background.
        self.parent.screen.blit(self.img_logo,[100, 50]) #Draw game title logo.
        self.parent.screen.blit(self.img_company_logo, [605, 545])

        for button in self.buttons:
            button.draw() #Draw each button.

    def update(self):
        pygame.display.update() #Update the screen.

    def quit(self):
        self.running = False #End entire application loop.
        self.parent.running = False #End game loop.
        self.parent.game_over = False #End rhe game over loop.

    def displayHelp(self):
        help_flag = True
        help_num = 0
        main_menu_button = Button(self.parent.screen, image='ui/mainmenu.png', position=(300,535))
        next_button = Button(self.parent.screen, image='ui/next.png', position=(550,535))
        back_button = Button(self.parent.screen, image='ui/back.png', position=(50,535))
        img_controls_help = pygame.image.load('ui/controls_help.png')
        img_health_help = pygame.image.load('ui/healthfuelscore_help.png')
        img_enmies_help = pygame.image.load('ui/enemies_help.png')
        img_items_help = pygame.image.load('ui/items_help.png')

        while help_flag == True:
            if help_num == 0:
                self.parent.screen.fill(BLACK)
                self.parent.screen.blit(img_controls_help, (50,20))
                main_menu_button.draw()
                next_button.draw()
                pygame.display.update()
            elif help_num == 1:
                self.parent.screen.fill(BLACK)
                self.parent.screen.blit(img_health_help, (50,20))
                main_menu_button.draw()
                next_button.draw()
                back_button.draw()
                pygame.display.update()
            elif help_num == 2:
                self.parent.screen.fill(BLACK)
                self.parent.screen.blit(img_enmies_help, (50,20))
                self.x_rose.anim_walkingR.draw(self.parent.screen, (116,77))
                self.x_melon.anim_walkingR.draw(self.parent.screen, (247,99))
                self.x_sunflow.anim_walkingR.draw(self.parent.screen, (383,77))
                self.x_tree.anim_walkingR.draw(self.parent.screen, (475,67))
                self.x_box.anim_walkingR.draw(self.parent.screen, (628,87))
                main_menu_button.draw()
                next_button.draw()
                back_button.draw()
                pygame.display.update()
            elif help_num == 3:
                self.parent.screen.fill(BLACK)
                self.parent.screen.blit(img_items_help, (50,20))
                main_menu_button.draw()
                back_button.draw()
                pygame.display.update()
                
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = event.pos  # gets mouse position
                    if main_menu_button.rect_obj.collidepoint(self.mouse_pos):
                        help_flag = False
                    elif back_button.rect_obj.collidepoint(self.mouse_pos):
                        if help_num - 1 <= 0:
                            help_num = 0
                        else:
                            help_num -= 1
                    elif next_button.rect_obj.collidepoint(self.mouse_pos):
                        if help_num + 1 >= 3:
                            help_num = 3
                        else:
                            help_num += 1

                if event.type == pygame.QUIT:
                    help_flag = False
                    self.quit()

    def displayCredits(self):
        credits_flag = True
        main_menu_button = Button(self.parent.screen, image='ui/mainmenu.png', position=(300,535))
        img_credits = pygame.image.load('ui/credits.png')


        while credits_flag == True:
            self.parent.screen.fill(BLACK)
            self.parent.screen.blit(img_credits, (50,20))
            main_menu_button.draw()
            pygame.display.update()
                
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = event.pos  # gets mouse position
                    if main_menu_button.rect_obj.collidepoint(self.mouse_pos):
                        credits_flag = False

                if event.type == pygame.QUIT:
                    credits_flag = False
                    self.quit()

class Button:
    def __init__(self, screen, image='start.png', colour=GREEN, position=(0,0), size=(200,50)):
        self.rect_obj = pygame.Rect((position),(size)) #Button Rect object.
        self.screen = screen #Screen button will be displayed on.
        self.image = pygame.image.load(image) #Button image.
        self.colour = colour #Button colour.
        self.pos_x = position[0] #Button x coord.
        self.pos_y = position[1] #Button y coord.
        self.size = size #Button size.
        self.active = None #Initialize button flag.

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, self.rect_obj)  #Draw button.
        self.screen.blit(self.image, (self.pos_x, self.pos_y)) #Display to screen.
                        
g = Game()
while g.running:
    if g.start_menu.running == True:
        g.getMainMenu()
    if g.playing == True:
        g.new()
        g.run()
    if g.game_over == True:
        g.getGameOver()
pygame.quit()
