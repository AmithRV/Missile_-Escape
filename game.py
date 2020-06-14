import pygame
import random
import winsound
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 500

# Define the Player object by extending pygame.sprite.Sprite, Instead of a surface, use an image for a better-looking sprite

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert() # pygame.image.load() loads an image from the disk. It returns a Surface, and the .convert() call optimizes the Surface, making future .blit() calls faster.
        self.surf.set_colorkey((255, 255, 255))            # set_colorkey() to indicate the color pygame will render as transparent. In this case, you choose white, because that’s the background color of the jet image. 
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen, without this line the player migh moves outside the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect(         # The starting position of enemy is randomly generated
            center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                   )
        )
        self.speed =2       #This specifies how fast this enemy moves towards the player.

    # Move the sprite based on speed, and Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)       # moves the enemy toward the left side of the screen at the .speed defined when it was created.
        if self.rect.right < 0:                 # Once the enemy is off-screen, you call .kill() to prevent it from being processed further.
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0))   # set_colorkey() to indicate the color pygame will render as transparent. In this case, you choose black, because that’s the background color of the cloud image. 

        # The starting position is randomly generated
        self.rect = self.surf.get_rect( center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),random.randint(0, SCREEN_HEIGHT)))

    # Move the cloud based on a constant speed, and Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()



clock = pygame.time.Clock()     # Setup the clock for a decent framerate

pygame.mixer.init()     # Setup for sounds. Defaults are good.

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

# Create custom events for adding a new enemy and a cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,250)     # This says to wait 250 milliseconds, before creating the next enemy.

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)   # This says to wait 1000 milliseconds, or one second, before creating the next cloud.      

player = Player()  # Create our 'player'


# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

all_sprites.add(player)


# Load and play background music
pygame.mixer.music.load("airplane.mp3")
pygame.mixer.music.play(loops=-1)


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)


        elif event.type == ADDCLOUD:            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()     # If so, then remove the player
            running = False   # Stop the loop




    pressed_keys = pygame.key.get_pressed()     # Get the set of keys pressed and check for user input
    
    player.update(pressed_keys)                 # Update the player sprite based on user keypresses
    
    # Update the position of enemies and clouds
    enemies.update()
    clouds.update()

    screen.fill((135, 206, 250))        # Fill the screen with sky blue

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):   # If so, then remove the player and stop the loop
        player.kill()
        running = False
    
    screen.blit(player.surf, player.rect)       # Draw the player on the screen
    pygame.display.flip()
    clock.tick(100)        # Ensure program maintains a rate of 30 frames per second

pygame.mixer.music.stop()
pygame.mixer.quit()    

pygame.quit()
    
