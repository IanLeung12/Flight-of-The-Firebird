########################################################################################################################
#  (     (     (                )              )   (                 )        (     (    (              (    (    (
#  )\ )  )\ )  )\ )  (       ( /(   *   )   ( /(   )\ )    *   )  ( /(        )\ )  )\ ) )\ )       (   )\ ) )\ ) )\ )
# (()/( (()/( (()/(  )\ )    )\())` )  /(   )\()) (()/(  ` )  /(  )\()) (    (()/( (()/((()/( (   ( )\ (()/((()/((()/(
#  /(_)) /(_)) /(_))(()/(   ((_)\  ( )(_)) ((_)\   /(_))  ( )(_))((_)\  )\    /(_)) /(_))/(_)))\  )((_) /(_))/(_))/(_))
# (_))_|(_))  (_))   /(_))_  _((_)(_(_())    ((_) (_))_| (_(_())  _((_)((_)  (_))_|(_)) (_)) ((_)((_)_ (_)) (_)) (_))_
# | |_  | |   |_ _| (_)) __|| || ||_   _|   / _ \ | |_   |_   _| | || || __| | |_  |_ _|| _ \| __|| _ )|_ _|| _ \ |   \
# | __| | |__  | |    | (_ || __ |  | |    | (_) || __|    | |   | __ || _|  | __|  | | |   /| _| | _ \ | | |   / | |) |
# |_|   |____||___|    \___||_||_|  |_|     \___/ |_|      |_|   |_||_||___| |_|   |___||_|_\|___||___/|___||_|_\ |___/
########################################################################################################################


#########################################
# File Name: Flight of the Firebird
# Description: Endless scrolling game where you try to get the best score and buy things in the shop
# Author: Ian Leung
# Date: 16/06/2022
#########################################

# Importing
import time
import random
import pygame
import math

# Initializing pygame
pygame.init()
WIDTH = 800
HEIGHT = 600
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
size = (WIDTH, HEIGHT)

# Colours
BLACK     = (0, 0, 0)
RED       = (255, 0, 0)
GREEN     = (0, 255, 0)
BLUE      = (0, 0, 255)
ORANGE    = (255, 127, 0)
CYAN      = (0, 183, 235)
MAGENTA   = (255, 0, 255)
YELLOW    = (255, 255, 0)
WHITE     = (255, 255, 255)
BGCLR_R = 10
BGRincrease = 0.05
BGCLR_G = 20
BGGincrease = 0.2
BGCLR_B = 0
BGBincrease = 0.1
BGCHANGE = pygame.Surface(size)
BGalpha = 50
BGCHANGE.set_alpha(BGalpha)
OUTLINE = 0
BGCHANGE.fill((BGCLR_R, BGCLR_G, BGCLR_B))
slotclrs = [BLACK, RED, ORANGE, BLUE, CYAN, MAGENTA, GREEN, YELLOW, WHITE]

# Opening text (save) file
f = open("save.txt", 'r')
lineR = f.readlines()

# Loading Images
# Backgrounds
startbg0 = pygame.image.load("Pictures/Backgrounds/startbg0.png")
startbg1 = pygame.image.load("Pictures/Backgrounds/startbg1.png")
startbg2 = pygame.image.load("Pictures/Backgrounds/startbg2.png")
eggx = 0

menubg = pygame.image.load("Pictures/Backgrounds/menubg.png")

endingbg = pygame.image.load("Pictures/Backgrounds/endingbg.jpg")

backgroundtemplate = pygame.image.load("Pictures/Backgrounds/background.jpg")
background1 = pygame.transform.scale2x(backgroundtemplate)
background2 = pygame.transform.scale2x(backgroundtemplate)
back1x = 0
back2x = 1440

deathscreen = pygame.image.load("Pictures/Backgrounds/deathscreen.png")

shopscreen = pygame.image.load("Pictures/Backgrounds/shop.png")

skinshopscreen = pygame.image.load("Pictures/Backgrounds/skinshop.png")

# Bird skins and attributes
skin = str(lineR[10].strip("\n"))

if "False" in lineR[11]:
    iceunlock = False
else:
    iceunlock = True

if "False" in lineR[12]:
    deathunlock = False
else:
    deathunlock = True

if "False" in lineR[13]:
    goldunlock = False
else:
    goldunlock = True

bigbird = pygame.image.load("Pictures/Objects/big" + skin + "bird.png")
bigbirdX = -1500

birdpic = [0] * 6
birdpicnum = 0
for i in range(6):
    birdpic[i] = pygame.image.load("Pictures/Objects/bird/" + skin + "bird (" + str(i + 1) + ").png")
birdx = 100
birdy = 200
birdxdirection = 1
birdydirection = 1
birdanimtimer = time.time() + 0.05
birdchange = 0

# Obstacles and Game objects
coinpic = pygame.image.load("Pictures/Objects/coin.png")
bigcoin = pygame.transform.scale2x(coinpic)

transformimage = pygame.image.load("Pictures/Objects/transform.png")

warning = pygame.image.load("Pictures/Objects/warning.png")

angrybird = pygame.image.load("Pictures/Objects/angrybird.png")

lightningh = pygame.image.load("Pictures/Objects/lightningh.png")
lightningv = pygame.image.load("Pictures/Objects/lightningv.png")
lightningup = pygame.image.load("Pictures/Objects/lightningdup.png")
lightningdown = pygame.image.load("Pictures/Objects/lightningddown.png")

# Buttons
continuepic = [0]*2
for i in range(2):
    continuepic[i] = pygame.image.load("Pictures/Buttons/continue" + str(i) + ".png").convert_alpha()

shoppic = [0]*2
for i in range(2):
    shoppic[i] = pygame.image.load("Pictures/Buttons/shop" + str(i) + ".png").convert_alpha()

resetpic = [0]*2
for i in range(2):
    resetpic[i] = pygame.image.load("Pictures/Buttons/reset" + str(i) + ".png").convert_alpha()

playpic = [0]*2
for i in range(2):
    playpic[i] = pygame.image.load("Pictures/Buttons/play" + str(i) + ".png").convert_alpha()

# More opening screen images
exclamation = pygame.image.load("Pictures/Objects/exclamation.png")
exclamation = pygame.transform.scale(exclamation, (50, 50))

ghost = pygame.image.load("Pictures/Objects/ghost.png")
ghostx = 375
ghosty = 650

EGG = pygame.image.load("Pictures/Objects/EGG.png")
EGGanimX = 1000


# Loading Music and SFX
pygame.mixer.music.load("Sound/Music/opening.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

coinsfx = pygame.mixer.Sound("Sound/SFX/coin.wav")
coinsfx.set_volume(0.3)

thud = pygame.mixer.Sound("Sound/SFX/thud.wav")
thud.set_volume(1)

alert = pygame.mixer.Sound("Sound/SFX/alert.mp3")
alert.set_volume(0.5)
playedalert = False

transformsfx = pygame.mixer.Sound("Sound/SFX/transform.flac")
transformsfx.set_volume(0.3)

#####################################
# Classes
#####################################


class Obstacle:
    """ Parent class for all obstacles

    Attributes
        (x) -> float
            X value of obstacle

        (y) -> int
            Y value of obstacle

        (width) -> int
            Width of obstacle

        (height) -> int
            Height of obstacle
    """
    def __init__(self, x: float, y: int, width: float, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class HomingRocket(Obstacle):
    """ Class for rockets that follow the player"""
    def __init__(self, x: float, y: int, width: float, height: int) -> None:
        super().__init__(x, y, width, height)

    # Blits the rockets
    def draw(self):
        # Displays warning for where the rocket will appear from
        if 1500 > self.x > 800:
            gameWindow.blit(warning, (700, self.y))
        gameWindow.blit(angrybird, (self.x, self.y))


class StillRocket(Obstacle):
    """ Class for rockets that do not follow the player"""
    def __init__(self, x: float, y: int, width: float, height: int) -> None:
        super().__init__(x, y, width, height)

    # Blits the rockets
    def draw(self):
        # displays warning for where the rocket will appear from
        if 1500 > self.x > 800:
            gameWindow.blit(warning, (700, self.y))
        gameWindow.blit(angrybird, (self.x, self.y))


class Laser(Obstacle):
    """ Laser class to establish collisions """

    def __init__(self, x: float, y: int, width: int, height: int) -> None:
        super().__init__(x, y, width, height)


class LaserImage:
    """ Laser image class to draw images in the position of lasers

    Attributes
        (type) -> str
            Type (rotation) of the laser

        (x) -> float
            X value of laser

        (y) -> float
            Y value of laser
    """

    def __init__(self, type: str, x: float, y: float):
        self.x = x
        self.y = y
        self.type = type

    # draws lasers based on their type
    def draw(self):
        if self.type == "horizontal":
            gameWindow.blit(lightningh, (self.x, self.y))
        elif self.type == "vertical":
            gameWindow.blit(lightningv, (self.x, self.y))
        elif self.type == "+diagonal":
            gameWindow.blit(lightningup, (self.x, self.y))
        else:
            gameWindow.blit(lightningdown, (self.x, self.y))


class Coin:
    """ Class for coins

    Attributes

        (radius) -> float
            radius of the coin

        (x) -> float
            X value of the coin

        (y) -> float
            Y value of the coin
    """
    def __init__(self, radius: float, x: float, y: float):
        self.radius = radius
        self.x = x
        self.y = y

    # blits the coin
    def draw(self):
        gameWindow.blit(coinpic, (self.x - self.radius, self.y - self.radius))


class PowerUp:
    """ Parent class for powerups
    Attributes

        (clr)
            Colour of the powerup

        (radius) -> float
            radius of the powerup

        (x) -> float
            X value of the powerup

        (y) -> float
            Y value of the powerup
        """
    def __init__(self, clr, radius, x, y):
        self.clr = clr
        self.radius = radius
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(gameWindow, self.clr, (self.x, self.y), self.radius, 3)


class Transform:
    """Class for Transformation spawner

    Attributes
        (x) -> float
            X value of hitbox

        (y) -> int
            Y value of hitbox

        (width) -> int
            Width of hitbox

        (height) -> int
            Height of hitbox"""

    def __init__(self, x: float, y: float, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # blits transform image
    def draw(self):
        gameWindow.blit(transformimage, (self.x, self.y))


class WaveTrail:
    """ Class for trail of wave transformation

    Attributes

        (x) -> float
            X value of trail
        (y) -> float
            Y value of trail
        (radius) -> float
            radius of trail
    """
    def __init__(self, x: float, y: float, radius: float):
        self.x = x
        self.y = y
        self.radius = radius

    # Draws the trail
    def draw(self):
        pygame.draw.circle(gameWindow, BLACK, (self.x, self.y), self.radius, 0)

# ---------------------------------------#
# functions                             #
# ---------------------------------------#


def createLaser():
    # types of laser
    obstacletypes = ["horizontal", "vertical", "+diagonal", "-diagonal"]

    # creates multiple lasers with different x positions
    for x in range(1000, 4000, 500):

        # chooses random from obstacle types and creates the lasers randomly based off of the choice
        type = random.choice(obstacletypes)
        if type == "horizontal":
            y = random.randint(0, 11) * GRIDSIZE
            laser.append(Laser(x, y, 5 * GRIDSIZE, GRIDSIZE))
            laserimages.append(LaserImage(type, x, y))

        elif type == "vertical":
            y = random.randint(0, 7) * GRIDSIZE
            laser.append(Laser(x, y, GRIDSIZE, 5 * GRIDSIZE))
            laserimages.append(LaserImage(type, x, y))

        elif type == "+diagonal":
            inity = random.randint(4, 11) * GRIDSIZE
            for i in range(0, 201, GRIDSIZE):
                laser.append(Laser(x + i, inity - i, GRIDSIZE, GRIDSIZE))
            laserimages.append(LaserImage(type, x, inity - 200))

        else:
            inity = random.randint(0, 7) * GRIDSIZE
            for i in range(0, 201, GRIDSIZE):
                laser.append(Laser(x + i, inity + i, GRIDSIZE, GRIDSIZE))
            laserimages.append(LaserImage(type, x, inity))


def createRocket():
    # types of rockets
    rockettypes = ["homing", "still"]

    # creates multiple rockets with different x positions
    for i in range(1500, 3900, 400):
        type = random.choice(rockettypes)
        y = random.randint(0, 11) * GRIDSIZE

        # rockets are based of the types of rockets
        if type == "homing":
            homingrockets.append(HomingRocket(i, y, GRIDSIZE * 1.5, GRIDSIZE))

        else:
            stillrockets.append(StillRocket(i, y, GRIDSIZE * 1.5, GRIDSIZE))


def createCoins():
    # creates multiple coins spread over the x and y axis
    for x in range(0, 1000, COINGRIDSIZE):
        for y in range(random.randint(2, 5)):
            coins.append(Coin(12.5, 1000 + x, (12.5 + random.randint(0, 28)*COINGRIDSIZE)))


def createPowerUp():
    # chooses random type of powerup to spawn
    type = random.choice(poweruptypes)
    # creates powerup based off of chosen type
    if type == "immunity":
        powerups.append(PowerUp(WHITE, 25, 1000, 25 + random.randint(0, 11)*GRIDSIZE))

    elif type == "magnet":
        powerups.append(PowerUp(RED, 25, 1000, 25 + random.randint(0, 11)*GRIDSIZE))

    elif type == "speedup":
        powerups.append(PowerUp(GREEN, 25, 1000, 25 + random.randint(0, 11)*GRIDSIZE))


def createTransform():
    # creates a transformation spawner with random y position
    y = random.randint(0, 10)*GRIDSIZE
    transforms.append(Transform(1000, y, GRIDSIZE * 2, GRIDSIZE * 2))


def moveSurroundings():
    # moves all objects
    for i in range(len(laser)):
        laser[i].x -= movestep

    for i in range(len(laserimages)):
        laserimages[i].x -= movestep

    for i in range(len(homingrockets)):
        # homing rockets move faster when they are on screen
        if homingrockets[i].x < 800:
            homingrockets[i].x -= movestep * 3

        else:
            homingrockets[i].x -= movestep
        # homing rockets move up and down to follow the player when offscreen
        if homingrockets[i].x > 800 and homingrockets[i].y + homingrockets[i].height/2 < objectY + objectH/2:
            homingrockets[i].y += 2

            if homingrockets[i].y > HEIGHT - homingrockets[i].height:
                homingrockets[i].y = HEIGHT - homingrockets[i].height

        elif homingrockets[i].x > 800 and homingrockets[i].y + homingrockets[i].height/2 > objectY + objectH/2:
            homingrockets[i].y -= 2

            if homingrockets[i].y < 0:
                homingrockets[i].y = 0

    for i in range(len(stillrockets)):
        # still rockets do not follow the player
        if stillrockets[i].x < 800:
            stillrockets[i].x -= movestep * 3

        else:
            stillrockets[i].x -= movestep

    for i in range(len(coins)):
        coins[i].x -= movestep

    for i in range(len(powerups)):
        powerups[i].x -= powerupXVel

        # makes powerups move up and down using acceleration and deceleration
        if powerups[i].y < 100:
            powerupYVel[i] += 1
            powerupmovedown[i] = True

        if powerups[i].y > 500:
            powerupYVel[i] -= 1
            powerupmovedown[i] = False

        elif powerupmovedown[i]:
            powerupYVel[i] += 1

        else:
            powerupYVel[i] -= 1

        if powerupYVel[i] > 10:
            powerupYVel[i] = 10

        if powerupYVel[i] < -10:
            powerupYVel[i] = -10

        powerups[i].y += powerupYVel[i]

    for i in range(len(transforms)):
        transforms[i].x -= movestep

    for i in range(len(wavetrail)):
        wavetrail[i].x -= movestep


def laserCollide():
    # Checks if player collides with a laser and returns the result
    spriterect = pygame.Rect(objectX, objectY, objectW, objectH)
    collide = False

    for i in range(len(laser)):
        laserrect = pygame.Rect(laser[i].x, laser[i].y, laser[i].width, laser[i].height)
        collide = laserrect.colliderect(spriterect)
        if collide:
            break

    # Does not register collision if player has immunity powerup
    if immunitystate:
        collide = False

    return collide


def homingRocketCollide():
    # checks if player collides with a homing rocket and returns the result
    spriterect = pygame.Rect(objectX, objectY, objectW, objectH)
    collide = False

    for i in range(len(homingrockets)):
        rocketrect = pygame.Rect(homingrockets[i].x, homingrockets[i].y,
                                 homingrockets[i].width, homingrockets[i].height)
        collide = rocketrect.colliderect(spriterect)
        if collide:
            break

    # Does not register collision if player has immunity powerup
    if immunitystate:
        collide = False

    return collide


def stillRocketCollide():
    # checks if player collides with a still rocket and returns the result
    spriterect = pygame.Rect(objectX, objectY, objectW, objectH)
    collide = False

    for i in range(len(stillrockets)):
        rocketrect = pygame.Rect(stillrockets[i].x, stillrockets[i].y, stillrockets[i].width, stillrockets[i].height)
        collide = rocketrect.colliderect(spriterect)
        if collide:
            break

    # Does not register collision if player has immunity powerup
    if immunitystate:
        collide = False

    return collide


def coinCollide():
    # checks if player is colliding with a coin
    collectedcoins = 0
    coinscopy = []

    # player hitbox based off of magnets
    if magnetstate:
        spriterect = pygame.Rect(objectX - 50, objectY - 50, objectW + 100, objectH + 100)
    elif permmag:
        spriterect = pygame.Rect(objectX - 30, objectY - 30, objectW + 60, objectH + 60)
    else:
        spriterect = pygame.Rect(objectX, objectY, objectW, objectH)

    for i in range(len(coins)):
        diameter = coins[i].radius * 2
        coinhb = pygame.Rect(coins[i].x - coins[i].radius, coins[i].y - coins[i].radius, diameter, diameter)
        if coinhb.colliderect(spriterect):
            coinsfx.play()
            coinscopy.append(coins[i])
            collectedcoins = collectedcoins + 1
    # returns coinlist without collided coins and amount of coins collected
    return [coin for coin in coins if coin not in coinscopy], collectedcoins


def powerUpCollide():
    # Check if player is colliding with a powerup and return the type of powerup
    spriterect = pygame.Rect(objectX, objectY, objectW, objectH)
    type = "none"
    for i in range(len(powerups)):
        poweruphb = pygame.Rect(powerups[i].x - powerups[i].radius, powerups[i].y - powerups[i].radius,
                                powerups[i].radius * 2, powerups[i].radius * 2)
        # powerup types based off of colour of powerup
        if poweruphb.colliderect(spriterect):
            if powerups[i].clr == WHITE:
                type = "immunity"
            elif powerups[i].clr == RED:
                type = "magnet"
            elif powerups[i].clr == GREEN:
                type = "speedup"
            del powerups[i]
    return type


def transformCollide():
    # checks if player is colliding with a transformation spawner
    spriterect = pygame.Rect(objectX, objectY, objectW, objectH)
    transformation = "none"
    for i in range(len(transforms)):
        transformrect = pygame.Rect(transforms[i].x, transforms[i].y, transforms[i].width, transforms[i].height)
        # chooses randomly from transformation types
        if transformrect.colliderect(spriterect):
            transformsfx.play()
            del transforms[i]
            transformation = random.choice(transformations)
            break
    return transformation


def removeOffscreen():
    # if the object is completely offscreen
    # remove them from their respective list
    for i in reversed(range(len(coins))):
        if coins[i].x < -50:
            coins.pop(i)

    for i in reversed(range(len(laser))):
        if laser[i].x < -300:
            laser.pop(i)

    for i in reversed(range(len(laserimages))):
        if laserimages[i].x < -300:
            laserimages.pop(i)

    for i in reversed(range(len(powerups))):
        if powerups[i].x < -100:
            powerups.pop(i)

    for i in reversed(range(len(homingrockets))):
        if homingrockets[i].x < -200:
            homingrockets.pop(i)

    for i in reversed(range(len(stillrockets))):
        if stillrockets[i].x < -200:
            stillrockets.pop(i)

    for i in reversed(range(len(wavetrail))):
        if wavetrail[i].x < -50:
            wavetrail.pop(i)


def redrawGameWindow():
    # redraws game window
    # bg
    gameWindow.blit(background1, (back1x, 0))
    gameWindow.blit(background2, (back2x, 0))
    gameWindow.blit(BGCHANGE, (0, 0))
    # objects
    for trail in range(len(wavetrail)):
        wavetrail[trail].draw()

    gameWindow.blit(birdpic[birdpicnum], (objectX - 9, objectY - 9))

    if immunitystate:
        pygame.draw.circle(gameWindow, immunityclr, (objectX + objectH/2, objectY + objectH/2), 35, 3)

    for transform in range(len(transforms)):
        transforms[transform].draw()

    for coin in range(len(coins)):
        coins[coin].draw()

    for power in range(len(powerups)):
        powerups[power].draw()

    for lasers in range(len(laserimages)):
        laserimages[lasers].draw()

    for rockets in range(len(homingrockets)):
        homingrockets[rockets].draw()

    for rockets in range(len(stillrockets)):
        stillrockets[rockets].draw()

    # text
    scoregraphic = font.render(("SCORE: " + str(int(score))), True, WHITE)
    highscoregraphic = font.render(("HIGH SCORE: " + str(int(highscore))), True, WHITE)
    coingraphic = font.render(("COINS: " + str(wallet)), True, WHITE)
    powerongraphic = font.render((powerupeffect + " Active: " + str(powertimer)), True, WHITE)
    if poweron:
        gameWindow.blit(powerongraphic, (20, 140))
    gameWindow.blit(scoregraphic, (20, 20))
    gameWindow.blit(highscoregraphic, (20, 60))
    gameWindow.blit(coingraphic, (20, 100))


def redrawButton(image, x, y):
    # function to draw and create functionality of a button
    pos = pygame.mouse.get_pos()
    buttonstate = 0
    clicked = False
    imagehb = gameWindow.blit(image[buttonstate], (x, y))
    # if mouse is hovering over button
    if imagehb.collidepoint(pos):
        # button image is changed to secondary state
        buttonstate = 1
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
    gameWindow.blit(image[buttonstate], (x, y))
    # returns whether or not button is clicked
    return clicked


# ---------------------------------------#
# main program                          #
# ---------------------------------------#

# sprite dimensions
GROUND = HEIGHT
GRAVITY = 0.375
objectW = 30
objectH = 30
objectX = WIDTH / 2 - 200
objectY = GROUND - objectH
objectVx = 0
objectVy = 0

# object lists
laser = []
laserimages = []
coins = []
powerups = []
homingrockets = []
stillrockets = []
powerupmovedown = []
transforms = []
transformations = ["gswitch", "wave", "flappy"]
obstaclesectors = [createLaser, createRocket]

# balance
wallet = 0
bank = int(lineR[1].strip("\n"))
multi1 = float(lineR[2].strip("\n"))
multi2 = float(lineR[3].strip("\n"))
multi3 = float(lineR[4].strip("\n"))
multi4 = float(lineR[5].strip("\n"))
tempcoin = 0
GRIDSIZE = 50
COINGRIDSIZE = 25

# powerups
powerspawn = 0
poweruptypes = ["immunity", "magnet", "speedup"]
COINSPAWNtimer = time.time() + 5
POWERtimer = time.time() + random.randint(15, 45)
immunitytimer = time.time()
immunitystate = False
immunityclr = BLUE
immunityon = 0
magnettimer = time.time()
magnetstate = False
magneton = 0
if "False" in lineR[6]:
    permmag = False
else:
    permmag = True
powerupeffect = "none"
poweron = False
speedon = 0
powertimer = 0

score2coin = float(lineR[7].strip("\n"))

if "False" in lineR[9]:
    freerevives = False
else:
    freerevives = True

# transformations
if "False" in lineR[8]:
    spawntransformed = False
else:
    spawntransformed = True
transformspawn = 0
transformtimer = time.time() + random.randint(30, 60)
transformcount = 0
transformtype = "none"
intransformation = False
gswitch = False
wave = False
flappy = False
wavetrail = []

# Other miscellaneous variables
slotanim = 0
slotresult = 0
payout = "error"
givenreward = False
obstacletimer = time.time() + 2
obstaclesectorinterval = 9
speeduptimer = 0
starttimer = time.time() + 0.7
obstaclespawn = 0
score = 0
scoreincrease = 1
highscore = int(lineR[0].strip("\n"))
movestep = 5
powerupXVel = movestep/1.75
powerupYVel = []
speedtimer = time.time() + 3

# fonts
font = pygame.font.SysFont("IMPACT", 24)
font2 = pygame.font.SysFont("IMPACT", 64)

# Game States and Attributes---------------------------------------#
print("Hit ESC to end the program.")
clock = pygame.time.Clock()
FPS = 60
inStart = True
inblink = True
inGame = True
RESET = True
inOpening = True
openingpart2 = False
inMenu = True
inShop = False
inSkinShop = False
inEggAnim = False
ResetCount = 0

while inGame:
    # Game Loop

    while inStart:
        # Starting screen loop
        # background
        gameWindow.blit(background1, (back1x, 0))
        gameWindow.blit(startbg1, (0, 0))
        gameWindow.blit(startbg2, (eggx, 0))
        gameWindow.blit(startbg0, (0, 0))

        # bird animation
        birdchange = birdanimtimer - time.time()
        if birdchange < 0:
            birdpicnum += 1
            birdanimtimer = time.time() + 0.1
        if birdpicnum > 5:
            birdpicnum = 0
        gameWindow.blit(birdpic[birdpicnum], (birdx, birdy))

        # bird changes direction when it reaches certain x/y coordinates
        birdx += 2 * birdxdirection
        birdy += 0.3 * birdydirection
        if birdx > 300 or birdx < 50:
            birdxdirection *= -1
            for i in range(len(birdpic)):
                birdpic[i] = pygame.transform.flip(birdpic[i], True, False)
        if birdy > 220 or birdy < 180:
            birdydirection *= -1

        # text blinks/ goes on and off periodically
        startblink = starttimer - time.time()
        if startblink < 0:
            inblink = not inblink
            starttimer = time.time() + 0.7

        if inblink:
            startmessage = font2.render("Press Any Button to Start...", True, RED)
            gameWindow.blit(startmessage, (50, 500))

        title = font2.render("FLIGHT OF THE FIREBIRD", True, BLACK)
        gameWindow.blit(title, (110, 50))

        # exits starting screen and plays opening music when button is pressed
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                inStart = False
                pygame.mixer.music.load("Sound/Music/openseq.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(loops=-1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                inStart = False
                pygame.mixer.music.load("Sound/Music/openseq.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(loops=-1)

        pygame.display.update()
        pygame.event.pump()
        clock.tick(FPS)
    while inOpening:
        # opening sequence loop
        # backgrounds
        gameWindow.blit(startbg1, (0, 0))
        gameWindow.blit(ghost, (ghostx, ghosty))
        gameWindow.blit(startbg2, (eggx, 0))
        gameWindow.blit(startbg0, (0, 0))
        gameWindow.blit(bigbird, (bigbirdX, -100))
        skipmessage = font.render("Press again to skip", True, YELLOW)
        gameWindow.blit(skipmessage, (20, 560))

        # bird animation
        birdchange = birdanimtimer - time.time()
        if birdchange < 0:
            birdpicnum += 1
            birdanimtimer = time.time() + 0.1

        if birdpicnum > 5:
            birdpicnum = 0

        gameWindow.blit(birdpic[birdpicnum], (birdx, birdy))
        birdx += 2 * birdxdirection
        birdy += 0.3 * birdydirection

        if birdx > 300 or birdx < 50 and not openingpart2:
            birdxdirection *= -1
            for i in range(len(birdpic)):
                birdpic[i] = pygame.transform.flip(birdpic[i], True, False)

        if birdy > 220 or birdy < 180:
            birdydirection *= -1
        keys = pygame.key.get_pressed()

        # ghost moves in a way that looks like it steals an egg from the bird
        if ghosty > 180:
            ghosty = ghosty - 3

        else:
            ghostx = ghostx + 2.6
            eggx = eggx + 2.6

        # actions of objects are based off of positions of other objects
        if eggx > 526:
            pass

        elif eggx > 525:
            openingpart2 = True
            for i in range(6):
                birdpic[i] = pygame.image.load("Pictures/Objects/bird/" + skin + "bird (" + str(i + 1) + ").png")
            for i in range(len(birdpic)):
                birdpic[i] = pygame.transform.flip(birdpic[i], True, False)
            birdxdirection = -3

        elif eggx > 400:
            # bird is alerted when it realizes its egg has been stolen
            for i in range(6):
                birdpic[i] = pygame.image.load("Pictures/Objects/bird/" + skin + "bird (" + str(i + 1) + ").png")
            if not playedalert:
                playedalert = True
                alert.play()
            birdx -= 2 * birdxdirection
            gameWindow.blit(exclamation, (birdx, birdy - 75))

        if birdx < -100:
            bigbirdX = bigbirdX + 20

        # exits opening sequence
        if bigbirdX > 2000:
            inOpening = False

        # Player can exit game by pressing escape
        if keys[pygame.K_ESCAPE]:
            inGame = False
            inStart = False
            inOpening = False
            inPlay = False
            inDeath = False
            Dead = False
            inMenu = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                inOpening = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                inOpening = False

        pygame.event.pump()
        pygame.display.update()
        clock.tick(FPS)
    for i in range(6):
        birdpic[i] = pygame.image.load("Pictures/Objects/bird/" + skin + "bird (" + str(i + 1) + ").png")

    # plays gameplay music
    pygame.mixer.music.load("Sound/Music/infernaldance.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)
    if RESET:
        # Resets game variables if player did not revive
        movestep = 5
        powerupXVel = movestep / 2
        laser.clear()
        laserimages.clear()
        coins.clear()
        powerups.clear()
        powerupmovedown.clear()
        homingrockets.clear()
        stillrockets.clear()
        transforms.clear()
        score = 0
        ResetCount = 0
        transformcount = 0
        scoreincrease = 1
        BGCLR_R = 10
        BGCLR_G = 20
        BGCLR_B = 0
        inMenu = True

    # resets timers and basic game data
    obstaclesectorinterval = 9
    obstacletimer = time.time() + 2
    speedtimer = time.time() + 3
    COINSPAWNtimer = time.time() + 5
    POWERtimer = time.time() + random.randint(15, 45)
    transformtimer = time.time() + random.randint(30, 60)
    immunitytimer = time.time()
    magnettimer = time.time()
    objectX = WIDTH / 2 - 200
    inPlay = True
    inDeath = True

    while inPlay:
        # bird animation
        birdchange = birdanimtimer - time.time()
        if birdchange < 0:
            birdpicnum += 1
            birdanimtimer = time.time() + 0.1
        if birdpicnum > 5:
            birdpicnum = 0

        keys = pygame.key.get_pressed()
        # Player can exit game by pressing escape key
        if keys[pygame.K_ESCAPE]:
            inGame = False
            inStart = False
            inOpening = False
            inPlay = False
            inDeath = False
            Dead = False
            inMenu = False

        # Movement based on which transformation
        # score increases greater when in transformation
        if gswitch:
            scoreincrease += 0.001
            birdpicnum = 5
            # gravity is reversed and bird is flipped when click
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                        GRAVITY = -GRAVITY
                        birdpic[birdpicnum] = pygame.transform.flip(birdpic[birdpicnum], False, True)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        GRAVITY = -GRAVITY
                        birdpic[birdpicnum] = pygame.transform.flip(birdpic[birdpicnum], False, True)
            objectVy = objectVy + GRAVITY

        elif wave:
            # player moves up when pressed and vice versa. No gravity at play
            scoreincrease += 0.001
            objectVy = 8
            # bird has a trail when in wave transformation
            wavetrail.append(WaveTrail(objectX + objectW/2, objectY + objectH/2, 10))
            birdpicnum = 1
            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                objectVy = -objectVy
                birdpicnum = 5

        elif flappy:
            # player jumps up when click
            scoreincrease += 0.001
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                        objectVy = -10
                        birdpicnum = 3
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        objectVy = -10
                        birdpicnum = 3
            objectVy = objectVy + GRAVITY

        else:
            # player moves up when pressed, but with gravity in effect
            scoreincrease += 0.0001
            GRAVITY = abs(GRAVITY)
            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                objectVy = objectVy - 0.8
            if objectVy < - 30:
                objectVy = -30
            objectVy = objectVy + GRAVITY

        # player can not move offscreen
        objectY = objectY + objectVy
        if objectY + objectH > GROUND:
            objectY = GROUND - objectH
            objectVy = 0
        if objectY < 0:
            objectVy = 0
            objectY = 0

        # score
        score = score + scoreincrease
        if score > highscore:
            highscore = score

        # objects spawn on a timer
        obstaclespawn = obstacletimer - time.time()
        if obstaclespawn < 0:
            obstacletimer = time.time() + obstaclesectorinterval
            random.choice(obstaclesectors)()
        coinspawn = COINSPAWNtimer - time.time()
        if coinspawn < 0:
            createCoins()
            COINSPAWNtimer = time.time() + 5

        # game speeds up over time
        speedup = speedtimer - time.time()
        if speedup < 0:
            speedtimer = time.time() + 3
            movestep = movestep + 0.2
            powerupXVel = movestep / 2
            obstaclesectorinterval -= 0.15
            if obstaclesectorinterval < 4:
                obstaclesectorinterval = 4

        # powerups
        # spawn on a timer
        powerspawn = POWERtimer - time.time()
        if powerspawn < 0:
            createPowerUp()
            powerupYVel.append(2)
            powerupmovedown.append(False)
            POWERtimer = time.time() + random.randint(15, 45)
        # powerups last a set amount of time
        # when they are active, their respective variables are set to their active state
        immunityon = round((immunitytimer - time.time()), 1)
        if immunityon > 0:
            immunitystate = True
            poweron = True
            powertimer = immunityon
            powerupeffect = "immunity"
            immunityclr = BLUE
        else:
            immunitystate = False
            poweron = False
            powerupeffect = "none"

        magneton = round((magnettimer - time.time()), 1)
        if magneton > 0:
            magnetstate = True
            poweron = True
            powertimer = magneton
            powerupeffect = "magnet"
        else:
            magnetstate = False

        speedon = round((speeduptimer - time.time()), 1)
        if speedon > 0:
            immunitystate = True
            immunityclr = GREEN
            # Game moves faster when speed up powerup is active
            for i in range(2):
                back1x = back1x - movestep
                back2x = back2x - movestep
                if back1x <= -1440:
                    back1x = back2x + 1440
                if back2x <= -1440:
                    back2x = back1x + 1440
                moveSurroundings()
                score = score + scoreincrease
        elif speedon > -2:
            immunitystate = True
            immunityclr = GREEN
        else:
            speedstate = False

        # objects are handled (moved and removed)
        moveSurroundings()
        removeOffscreen()

        # transformations
        # are spawned on a timer
        transformspawn = transformtimer - time.time()
        if transformspawn < 0:
            createTransform()
            transformtimer = time.time() + random.randint(30, 60)

        # if player collides with a transformation spawner
        transformtype = transformCollide()  # the type is returned to the player
        if spawntransformed and transformcount < 1:
            # player is automatically transformed if player has spawn transformed powerup
            transformtype = random.choice(transformations)
            transformcount = 1

        if transformtype != "none":
            # visual effects when player gets transformed
            BGCLR_R, BGCLR_G, BGCLR_B = 254, 254, 254
            BGRincrease = -0.25
            BGGincrease = -1
            BGBincrease = -0.5
            BGalpha = 255
            # clears obstacles so player doesn't instantly die
            homingrockets.clear()
            stillrockets.clear()
            laser.clear()
            laserimages.clear()
            intransformation = True

        if transformtype == "gswitch":
            gswitch = True

        if transformtype == "wave":
            wave = True

        if transformtype == "flappy":
            flappy = True

        if intransformation:
            # another transformation spawner can not spawn if player is tranformed
            transformtimer = time.time() + random.randint(30, 60)

        # obstacle collisions
        collide1, collide2, collide3 = laserCollide(), homingRocketCollide(), stillRocketCollide()
        if collide1 or collide2 or collide3:
            if intransformation:
                # Player does not die if it collides and is in tranformation. Rather, it loses its transformation
                birdpic[5] = pygame.image.load("Pictures/Objects/bird/" + skin + "bird (6).png")
                scoreincrease = 1
                # obstacles are cleared so player does not instantly die
                homingrockets.clear()
                stillrockets.clear()
                laser.clear()
                laserimages.clear()
                intransformation = False
                gswitch = False
                wave = False
                flappy = False
                # visuals are reset
                wavetrail.clear()
                BGCLR_R = 10
                BGRincrease = 0.05
                BGCLR_G = 20
                BGGincrease = 0.2
                BGCLR_B = 0
                BGBincrease = 0.1
            else:
                # death
                inPlay = False
        # coins and powerup states
        coins, tempcoin = coinCollide()
        poweruptype = powerUpCollide()
        if poweruptype == "immunity":
            immunitytimer = time.time() + 10
        elif poweruptype == "magnet":
            magnettimer = time.time() + 20
        elif poweruptype == "speedup":
            speeduptimer = time.time() + 5
        wallet = wallet + tempcoin

        # Visuals
        # bg changes colour over time
        if 255 <= BGCLR_R or BGCLR_R <= 0:
            BGRincrease = -BGRincrease
        BGCLR_R = BGCLR_R + BGRincrease

        if 255 <= BGCLR_G or BGCLR_G <= 0:
            BGGincrease = -BGGincrease
        BGCLR_G = BGCLR_G + BGGincrease

        if 255 <= BGCLR_B or BGCLR_B <= 0:
            BGBincrease = -BGBincrease
        BGCLR_B = BGCLR_B + BGBincrease

        if BGalpha > 55:
            BGalpha -= 1
        BGCHANGE.set_alpha(BGalpha)
        BGCHANGE.fill((BGCLR_R, BGCLR_G, BGCLR_B))

        redrawGameWindow()
        # scrolling background
        back1x = back1x - movestep
        back2x = back2x - movestep
        if back1x <= -1440:
            back1x = back2x + 1440
        if back2x <= -1440:
            back2x = back1x + 1440

        clock.tick(FPS)
        pygame.display.update()
        pygame.event.pump()

    Dead = True
    while Dead:
        # death screen
        redrawGameWindow()

        if movestep > 10:
            movestep = 10

        if objectY < 0:
            objectVy = 0
            objectY = 0

        # character bounces forward until it loses its momentum
        objectX = objectX + movestep/2.5
        objectVy = objectVy + GRAVITY
        objectY = objectY + objectVy

        # character can collect coins while bouncing
        coins, tempcoin = coinCollide()
        wallet = wallet + tempcoin

        if objectY + objectH > HEIGHT:
            # bouncing effect
            thud.play()
            objectY = HEIGHT - objectH
            objectVy = objectVy - GRAVITY
            objectVy = -objectVy//2
            if -1.5 < objectVy < 1.5:
                Dead = False

        keys = pygame.key.get_pressed()
        # Player can exit game by pressing escape key
        if keys[pygame.K_ESCAPE]:
            inGame = False
            inStart = False
            inOpening = False
            inPlay = False
            inDeath = False
            Dead = False
            inMenu = False
        pygame.display.update()
        pygame.event.pump()
        clock.tick(FPS)

    # clears objects
    laser.clear()
    laserimages.clear()
    powerups.clear()
    powerupmovedown.clear()
    homingrockets.clear()
    stillrockets.clear()
    coins.clear()
    pygame.event.clear()
    messages = ["Good Job!", "Nice Run!", "Well Done!", "Bad Luck...", "Keep on Going!"]
    deathmessage = random.choice(messages)

    while inDeath:
        # death screen loop
        # backgrounds
        redrawGameWindow()
        gameWindow.blit(deathscreen, (0, 0))

        # text
        deathscoregraphic = font2.render((str(int(score))), True, WHITE)
        coingraphic = font2.render((str(int((wallet + score * score2coin) * multi1 * multi2 * multi3 * multi4))),
                                   True, WHITE)
        message = font2.render(deathmessage, True, WHITE)
        messagerect = message.get_rect(center=(WIDTH/2, 100))
        revivemessage = font.render("press r to revive for 1500 coins", True, WHITE)
        gameWindow.blit(revivemessage, (20, 550))
        gameWindow.blit(message, messagerect)
        gameWindow.blit(deathscoregraphic, (630, 150))
        gameWindow.blit(coingraphic, (550, 260))

        # input functions
        keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()

        continueclick = redrawButton(continuepic, 300, 400)
        if continueclick:
            inDeath = False
            RESET = True

        # Player can exit game by pressing escape key
        if keys[pygame.K_ESCAPE]:
            inGame = False
            inStart = False
            inOpening = False
            inPlay = False
            inDeath = False
            Dead = False
            inMenu = False

        if keys[pygame.K_r] and ResetCount < 1:
            # player can revive once each game
            if freerevives:
                inPlay = True
                RESET = False
                inDeath = False
                inMenu = False

            elif bank >= 1500:
                bank = bank - 1500
                inPlay = True
                RESET = False
                inDeath = False
                inMenu = False
            ResetCount = ResetCount + 1

        pygame.display.update()
        pygame.event.clear()
        clock.tick(FPS)

    if RESET:
        # Continues to menu if player did not revive
        bank = int(bank + ((wallet + score * score2coin) * multi1 * multi2 * multi3 * multi4))
        wallet = 0
        inMenu = True
        pygame.mixer.music.load("Sound/Music/menutheme.mp3")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=-1)

    while inMenu:
        # Menu screen
        # Background
        gameWindow.blit(menubg, (0, 0))
        keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()

        # Player balance text
        gameWindow.blit(bigcoin, (20, 20))
        balance = font2.render(str(bank), True, WHITE)
        gameWindow.blit(balance, (100, 10))

        # buttons
        shopclick = redrawButton(shoppic, 600, 500)
        if shopclick and not inShop and not inSkinShop:
            inShop = True

        playclick = redrawButton(playpic, 200, 400)
        if playclick and not inShop and not inSkinShop:
            inMenu = False
            RESET = True

        resetclick = redrawButton(resetpic, 0, 500)
        if resetclick and not inShop and not inSkinShop:
            # Resets game progress
            confirmmessage = font2.render("Are you sure?", True, RED)
            confirmmessage2 = font2.render("Input \"CONFIRM\" to confirm", True, RED)
            gameWindow.fill(YELLOW)
            gameWindow.blit(confirmmessage, (220, 200))
            gameWindow.blit(confirmmessage2, (50, 300))
            pygame.display.update()
            clock.tick()
            pygame.event.pump()
            confirm = input("TYPE \"CONFIRM\" TO CONFIRM: \n")
            if confirm == "CONFIRM":
                bank = 0
                highscore = 0
                multi1 = 1
                multi2 = 1
                multi3 = 1
                multi4 = 1
                permmag = False
                score2coin = 0
                spawntransformed = False
                freerevives = False
                skin = ''
                iceunlock = False
                deathunlock = False
                goldunlock = False

        if inShop:
            # shop loop
            # background
            gameWindow.blit(shopscreen, (0, 0))
            balance = font.render(str(bank), True, WHITE)
            gameWindow.blit(balance, (50, 25))

            # exit button
            exithb = pygame.Rect(0, 60, 150, 100)
            if exithb.collidepoint(pos):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            inShop = False

            # player can use the shop by inputting numbers
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0 and bank >= 1000 and multi1 < 2:
                        multi1 *= 2
                        bank = bank - 1000

                    elif event.key == pygame.K_1 and bank >= 4000 and multi2 < 2:
                        multi2 *= 2
                        bank = bank - 4000

                    elif event.key == pygame.K_2 and bank >= 10000 and multi3 < 2:
                        multi3 *= 2
                        bank = bank - 10000

                    elif event.key == pygame.K_3 and bank >= 50000 and multi4 < 10:
                        multi4 *= 10
                        bank = bank - 50000

                    elif event.key == pygame.K_4 and bank >= 15000 and not permmag:
                        permmag = True
                        bank = bank - 15000

                    elif event.key == pygame.K_5 and bank >= 25000 and score2coin != 0.01:
                        score2coin = 0.01
                        bank = bank - 25000

                    elif event.key == pygame.K_6 and bank >= 50000 and not spawntransformed:
                        spawntransformed = True
                        bank = bank - 50000

                    elif event.key == pygame.K_7 and bank >= 15000 and not freerevives:
                        freerevives = True
                        bank = bank - 15000

                    elif event.key == pygame.K_8:
                        inSkinShop = True
                        inShop = False

                    elif event.key == pygame.K_9 and bank >= 1000000:
                        bank = bank - 1000000
                        EGGanimX = 1000
                        inEggAnim = True

                    else:
                        print("Invalid/ Not enough money")

        while inEggAnim:
            # Final cutscene loop
            keys = pygame.key.get_pressed()

            # backgrounds
            gameWindow.blit(endingbg, (-100, -50))
            gameWindow.blit(bigbird, (-600, -100))
            gameWindow.blit(EGG, (EGGanimX, 150))

            # egg movement animation
            if EGGanimX > 525:
                EGGanimX -= 2
                Eggmessage = font2.render("And so, the egg was", True, YELLOW)

            elif EGGanimX > 450:
                Eggmessage = font2.render("returned to the Firebird.", True, YELLOW)
                EGGanimX -= 1

            else:
                # Final cutscene frame
                Eggmessage = font2.render("THE END", True, RED)
                endingmessage = font2.render("Thanks for Playing!", True, BLACK)
                exitendingmes = font.render("All multipliers have been multiplied by 1.25x. Press x to exit",
                                            True, WHITE)
                endingpos = endingmessage.get_rect(center=(WIDTH / 2, 550))
                gameWindow.blit(endingmessage, endingpos)
                gameWindow.blit(exitendingmes, (20, 20))

                # Gives player a bonus for completing the game
                if keys[pygame.K_x]:
                    multi1 *= 1.25
                    multi2 *= 1.25
                    multi3 *= 1.25
                    multi4 *= 1.25
                    inEggAnim = False
                # Player can exit game by pressing escape key
                if keys[pygame.K_ESCAPE]:
                    multi1 *= 1.25
                    multi2 *= 1.25
                    multi3 *= 1.25
                    multi4 *= 1.25
                    inGame = False
                    inStart = False
                    inOpening = False
                    inPlay = False
                    inDeath = False
                    Dead = False
                    inMenu = False

            eggpos = Eggmessage.get_rect(center=(WIDTH / 2, 450))
            gameWindow.blit(Eggmessage, eggpos)
            clock.tick(FPS)
            pygame.event.clear()
            pygame.display.update()

        if inSkinShop:
            # skin shop screen
            # background
            gameWindow.blit(skinshopscreen, (0, 0))

            # button to exit skin shop
            exithb = pygame.draw.rect(gameWindow, YELLOW, (10, 205, 130, 75), OUTLINE)
            if exithb.collidepoint(pos):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            inSkinShop = False
                            inShop = True

            slottimer = slotanim - time.time()
            # player can buy things using numbers
            # Ensures that player does not buy the same skin twice when changing skins
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        skin = ''
                        print("default skin equipped")

                    elif event.key == pygame.K_1 and 'i' and not iceunlock and bank >= 10000:
                        skin = 'i'
                        iceunlock = True
                        print("ice skin equipped")
                        bank = bank - 10000

                    elif event.key == pygame.K_1 and iceunlock:
                        skin = 'i'
                        print("ice skin equipped")

                    elif event.key == pygame.K_2 and not deathunlock and bank >= 15000:
                        skin = 'd'
                        deathunlock = True
                        print("death skin equipped")
                        bank = bank - 15000

                    elif event.key == pygame.K_2 and deathunlock:
                        skin = 'd'
                        print("death skin equipped")

                    elif event.key == pygame.K_3 and bank >= 3333 and slottimer < 0:
                        bank = bank - 3333
                        slotanim = time.time() + 5

                    elif event.key == pygame.K_4 and not goldunlock and bank >= 50000:
                        skin = 'g'
                        goldunlock = True
                        print("gold skin equipped")
                        bank = bank - 50000

                    elif event.key == pygame.K_4 and goldunlock:
                        skin = 'g'
                        print("gold skin equipped")

                    else:
                        print("Invalid/ Not enough money")

            # slots functionality
            if slottimer > 0:
                # Slot spinning/ changing animation
                givenreward = False
                slotCLR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                pygame.draw.rect(gameWindow, slotCLR, (320, 220, 170, 170), 0)
                # slot results have different weights/ probabilities
                slotresult = random.choices(slotclrs, weights=(20, 15, 11, 11, 10, 15, 10, 7, 1), k=1)[0]

            elif slottimer > -5:
                # Gives player reward based on the slot result
                pygame.draw.rect(gameWindow, slotresult, (320, 220, 170, 170), 0)
                if not givenreward:
                    if slotresult == BLACK:
                        payout = "nothing"

                    elif slotresult == RED:
                        payout = "250 coins"
                        bank = bank + 250

                    elif slotresult == ORANGE:
                        payout = "1000 coins"
                        bank = bank + 1000

                    elif slotresult == BLUE:
                        payout = "2500 coins"
                        bank = bank + 2500

                    elif slotresult == CYAN:
                        payout = "3333 coins"
                        bank = bank + 3333

                    elif slotresult == MAGENTA:
                        payout = "4500 coins"
                        bank = bank + 4500

                    elif slotresult == GREEN:
                        payout = "5555 coins"
                        bank = bank + 5555

                    elif slotresult == YELLOW:
                        payout = "7777 coins"
                        bank = bank + 7777

                    else:
                        payout = "22222 coins"
                        bank = bank + 22222
                    # player is only given their reward once
                    givenreward = True

                # reward text
                rewardmessage = font.render("You Won " + payout + "!", True, slotresult)
                rewardrect = rewardmessage.get_rect(center=(WIDTH / 2, 500))
                gameWindow.blit(rewardmessage, rewardrect)

            # Skin shop text
            balance = font.render("You have " + str(bank) + " coins - Press a number to buy the item", True, WHITE)
            gameWindow.blit(balance, (20, 175))
            exittext = font2.render("EXIT", True, RED)
            gameWindow.blit(exittext, (20, 200))

        # Player can exit game by pressing escape key
        if keys[pygame.K_ESCAPE]:
            inGame = False
            inStart = False
            inOpening = False
            inPlay = False
            inDeath = False
            Dead = False
            inMenu = False

        pygame.display.update()
        pygame.event.pump()
        clock.tick(FPS)

# saves progress on a text file
bank = int(bank + ((wallet + score * score2coin) * multi1 * multi2 * multi3 * multi4))
lines = [int(highscore), bank, multi1, multi2, multi3, multi4, permmag, score2coin,
         spawntransformed, freerevives, skin, iceunlock, deathunlock, goldunlock]
with open("save.txt", "w") as f:
    for line in lines:
        f.write(str(line))
        f.write("\n")

# Pygame Quitting --------------------------------------------#
pygame.quit()
