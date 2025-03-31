import pygame
from pygame.locals import *
import ctypes
import sys
import random
import math
import pyttsx3

class Block(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        super().__init__()
        self.original_image = pygame.Surface([width, height])
        self.original_image.fill(colour)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.x_speed = 0
        self.y_speed = 0
        self.last_shot = 0  
    def update(self):
        # Required for automatic sprite updates
        
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        # Rotation logic
        if hasattr(self, 'x_speed') and (self.x_speed != 0 or self.y_speed != 0):
            self.angle = math.degrees(math.atan2(-self.y_speed, self.x_speed))
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)



        
    
enemy_bullets = pygame.sprite.Group()
ENEMY_SHOOT_COOLDOWN = 1000 
flame_list = pygame.sprite.Group()
rockets_list = pygame.sprite.Group()
enemy1_list = pygame.sprite.Group()
enemy2_list = pygame.sprite.Group()
e1bullet = pygame.sprite.Group()
e2bullet = pygame.sprite.Group()
rocket_count = 50
flame_count = 50
enemy1weapon_count = 50
enemy2weapon_count = 50
mixiaoquan_life = 10
tietou_life = 10

pygame.init()
screen = pygame.display.set_mode((1500, 750))
ENEMY_SHOOT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_SHOOT_EVENT, 1000)  
# --- Color Definitions ---
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
STUFF = (190, 190, 190)
PURPLE = (128, 0, 128)
BLUE=(123,234,111)
GREEN=(0, 255, 0)# Add this with other color definitions      
screen.fill(YELLOW)
pygame.display.set_caption("米小圈 streetfighter")
clock = pygame.time.Clock()

start_time = pygame.time.get_ticks() 

try:
    mixiaoquan = pygame.image.load("C:/Users/PC/Pictures/Screenshots/Screenshot 2025-03-17 152004.png").convert_alpha()
    tietou = pygame.image.load("C:/Users/PC/Pictures/Screenshots/Screenshot 2025-03-17 155457.png").convert_alpha()
    
except pygame.error as e:
    print(f"图片加载失败: {e}")
    pygame.quit()
    sys.exit()

screen.blit(mixiaoquan, (100, 0))
screen.blit(tietou, (1100, 0))
# --- Define Rectangles ---
flame_unit_rect = pygame.Rect(500, 0, 100, 100)
rocket_rect = pygame.Rect(800, 0, 100, 100)

flame_unit = pygame.draw.rect(screen, GRAY, flame_unit_rect)
rocket = pygame.draw.rect(screen, WHITE, rocket_rect)
font = pygame.font.SysFont("courier", 15, bold=True)
tsurf = font.render("Press to shoot flame unit", True, ORANGE)
screen.blit(tsurf, (450, 0))
tsurf2 = font.render("Press to shoot rockets", True, STUFF)
screen.blit(tsurf2, (750, 0))
pygame.mouse.set_cursor(pygame.cursors.broken_x)
done = False

enemy1 = Block(GRAY, 100, 100)
enemy1_list.add(enemy1)
enemy1.rect.x = 300
enemy1.rect.y = 500
enemy1.life = 10

enemy2 = Block(GRAY, 100, 100)
enemy2.rect.x = 1100
enemy2.rect.y = 500
enemy2.life = 10
enemy2_list.add(enemy2)

while not done:
    
    for event in pygame.event.get():
        current_time = pygame.time.get_ticks()
        if event.type == QUIT:
            
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                # Inside your MOUSEBUTTONDOWN event handler
                if flame_unit_rect.collidepoint(pos):
                    bullet = Block(RED, 20, 15)
                    bullet.rect.center = (100 + mixiaoquan.get_width()//2,
                                          mixiaoquan.get_height()//2)

                    # Random direction with random speeds
                    bullet.x_speed = random.randint(-10, 10)
                    bullet.y_speed = random.randint(-10, 10)

                    # Ensure minimum movement
                    if bullet.x_speed == 0 and bullet.y_speed == 0:
                        bullet.x_speed = 5

                    flame_list.add(bullet)

        
             # Numeric keypad 1
                # Create rocket projectile              
                elif rocket_rect.collidepoint(pos):
                    
                    rocket = Block(PURPLE, 30, 10)
                    # Set start position at player's center
                    rocket.rect.centerx = 100 + mixiaoquan.get_width()//2
                    rocket.rect.centery = mixiaoquan.get_height()//2
                    # Set trajectory with slight random spread
                    rocket.x_speed = 10  # Base forward speed
                    rocket.y_speed = random.randint(-5, 5)  # Vertical variation
                    rockets_list.add(rocket)

        
    current_time = pygame.time.get_ticks()
    elapsed_ms = current_time - start_time
    remaining_seconds = max(60 - (elapsed_ms // 1000), 0)  # 2-minute countdown

    if remaining_seconds <= 0:
        screen.fill(YELLOW)
        game_over_text = font.render("TIME UP!", True, RED)
        screen.blit(game_over_text, (650, 375))
        pygame.display.flip()
        pygame.time.wait(3000)
        
        pygame.quit()  # Add this
        sys.exit()  
        done = True
        continue# Skip the rest of the loop
    if remaining_seconds <= 30 and(enemy1.life >= 4 or enemy2.life >= 4) :
        count = 0
        pygame.display.iconify()  # Minimizes the window (still running in background)
        q = ["猫先生写的第一个童话故事叫什么","李黎的作品刊登在了哪个杂志上","猫先生第一个辅导米小圈的作文叫什么"]
        a = random.choice(q)
        x = input(a)
        if a == "猫先生写的第一个童话故事叫什么":
            if x == "猴棒棒与熊胖胖":
                
                print("you win")
                pygame.quit()
                sys.exit()
            else:
                
                print("you lose")
                pygame.quit()
                sys.exit()
                
        elif a == "李黎的作品刊登在了哪个杂志上":
            if x == "红领巾":
                
                print("you win")
                pygame.quit()
                sys.exit()
            else:
                print("you lose")
                pygame.quit()
                sys.exit()
        elif a == "猫先生第一个辅导米小圈的作文叫什么":
            if x == "十岁的画":
                print("you win")
                pygame.quit()
                sys.exit()
            else:
                print("you lose")
                pygame.quit()
                sys.exit()
        
            
                        
            


        
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    time_text = f"Time: {minutes:02}:{seconds:02}"
           

    flame_list.update()
    rockets_list.update()
    
   
    # Inside the game loop (after event handling)
    
    # Inside your main game loop (after event handling)
    for rocket in rockets_list:
        # Update position
        rocket.rect.x += rocket.x_speed
        rocket.rect.y += rocket.y_speed

        # Remove rockets that leave screen                                               
        if rocket.rect.left > 1500:  # Right edge of screen
            rockets_list.remove(rocket)
        if rocket.rect.top > 750 or rocket.rect.bottom < 0:  # Vertical bounds
            rockets_list.remove(rocket)

    # Check rocket-enemy collisions
    enemy1f_hits = pygame.sprite.groupcollide(
        flame_list, enemy1_list, True, False  # Remove both on collision
    )

    # Handle enemy damage
    for b, enemies in enemy1f_hits.items():
        for enemy in enemies:
            enemy.life -= 1
            if enemy.life <= 0:
                enemy1_list.remove(enemy)
    # Check rocket-enemy collisions
    enemy2f_hits = pygame.sprite.groupcollide(
        flame_list, enemy2_list, True, False  # Remove both on collision
    )

    # Handle enemy damage
    for bullet, enemies in enemy2f_hits.items():
        for enemy in enemies:
            enemy.life -= 1
            if enemy.life <= 0:
                enemy2_list.remove(enemy)
    enemy1r_hits = pygame.sprite.groupcollide(
        rockets_list, enemy1_list, True, False  # Remove both on collision
    )

    # Handle enemy damage
    for b, enemies in enemy1r_hits.items():
        for enemy in enemies:
            enemy.life -= 1
            if enemy.life <= 0:
                enemy1_list.remove(enemy)
    # Check rocket-enemy collisions
    enemy2r_hits = pygame.sprite.groupcollide(
        rockets_list, enemy2_list, True, False  # Remove both on collision
    )

    # Handle enemy damage
    for bullet, enemies in enemy2r_hits.items():
        for enemy in enemies:
            enemy.life -= 1
            if enemy.life <= 0:
                enemy2_list.remove(enemy)

   


    screen.fill(YELLOW)
    screen.blit(mixiaoquan, (100, 0))
    screen.blit(tietou, (1100, 0))
            
    pygame.draw.rect(screen, (0,255,0), (300, 500, 100, 100))  # Enemy1 area
    pygame.draw.rect(screen, (0,255,0), (1100, 500, 100, 100))  # Enemy2 area
    
    flame_unit_rect = pygame.Rect(500, 0, 100, 100)
    rocket_rect = pygame.Rect(800, 0, 100, 100)
    pygame.draw.rect(screen, GRAY, flame_unit_rect)
    pygame.draw.rect(screen, WHITE, rocket_rect)
    font = pygame.font.SysFont("courier", 15, bold=True)
    tsurf = font.render("Press to shoot flame unit", True, ORANGE)
    screen.blit(tsurf, (450, 0))
    tsurf2 = font.render("Press to shoot rockets", True, STUFF)
    screen.blit(tsurf2, (750, 0))
    
    # --- Define Rectangles ---
    flame_list.draw(screen)
    rockets_list.draw(screen)
    enemy1_list.draw(screen)
    enemy2_list.draw(screen)
    
    
    pygame.mouse.set_cursor(pygame.cursors.broken_x)
    
    # Render and display the timer
    timer_surface = font.render(time_text, True, BLACK)  # Use gold color
    screen.blit(timer_surface, (700, 300))  # Position at top center
    
    # 绘制敌人 1 的生命值
    for enemy in enemy1_list:
        life_text = font.render(f"Enemy 1 HP: {enemy.life}", True, RED)
        screen.blit(life_text, (enemy.rect.x - 50, enemy.rect.y - 40))

    # 绘制敌人 2 的生命值
    for enemy in enemy2_list:
        life_text = font.render(f"Enemy 2 HP: {enemy.life}", True, RED)
        screen.blit(life_text, (enemy.rect.x - 50, enemy.rect.y - 40))

    if len(enemy1_list) == 0 and len(enemy2_list) == 0:
        msg = font.render("you win!", True, PURPLE)
        screen.blit(msg, (300, 300))
        pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    

    pygame.display.flip()
              
