import pygame
import sys
import os
from pygame.locals import *
from pygame import mixer

#For use music into the game
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#Screen sizes dimensions
screen_width = 1800
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fantasy Pygame 8 Bits")

#define game variables
tile_size = 50
game_over = 0
main_menu = True
score = 0

#Definig the font for the game
font = pygame.font. SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

#Defining the font colors for the game
white = (255, 255, 255)
blue = (0, 0, 255)

#loading images for the main menu
bg_img = pygame.image.load('img/background.jpg')
restart_img = pygame.image.load('img/restart_button.png')
restart_img = pygame.transform.scale(restart_img, (60, 60))
start_img = pygame.image.load('img/play-button.png')
start_img= pygame.transform.scale(start_img, (300, 150))
exit_img = pygame.image.load('img/exit-button.png')
exit_img = pygame.transform.scale(exit_img, (300, 150))

#Adding sound to the game
pygame.mixer.music.load('img/sound/background.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('img/sound/coin.mp3')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/sound/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/sound/game_over.mp3')

#Function to draw text in the screen player
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#This grid help you to reference where do you want to put some art for the game
def draw_grid():
    for line in range(0, 40):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #Get the mouse position in the screen
        pos = pygame.mouse.get_pos()

        #Checking mouseover and if clicked conditions is true
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #Drawing a button for the game
        screen.blit(self.image, self.rect)

        return action


 #This is class if or control the  player movement and more
class Player():
    def __init__(self, x, y):
        self.reset_game(x, y)
        
    def update(self, game_over):
        dx = 0
        dy = 0
        walk_nice = 1

        if game_over == 0:
            #When the user get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 3 #If we increase the number, the sprite will move "more fast"
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 3 #If we increase the number, the sprite will move "more fast"
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            
            #Handling animation into the character
            if self.counter > walk_nice:
                self.counter = 0
                self.index += 1
            if self.index >= len(self.images_right):
                    self.index = 0
            if self.direction == 1:
                    self.image = self.images_right[self.index]
            if self.direction == -1:
                    self.image = self.images_left[self.index]
                

            #Adding some gravity to the player
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #Checking for some collision
            for tile in world.tile_list:
                #Checking collision in X axe
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0        

                #Checking collision in Y axe
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            #Checking for collision with the enemies in the game
            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1
            #Play sound when the player died
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, spike_invert_y_group, False):
                game_over = -1
            #Play sound when the player died
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, spike_invert_group, False):      
                game_over = -1
            #Play sound when the player died
                game_over_fx.play()

            #Checking for collision with the fire
            if pygame.sprite.spritecollide(self, dang_group, False):
                game_over = -1
            #Play sound when the player died
                game_over_fx.play() 
                

            #For update the player coordinates
            self.rect.x += dx
            self.rect.y += dy
        
        elif game_over == -1:
        
            for num in range(1, 15):
                self.dead_image = pygame.image.load(f'img/hero_death/hero_death{num}.png')
                #dead_image = pygame.transform.scale(dead_image, (60, 90))
                self.image = self.dead_image
                

            draw_text('You cant beat the Pygame Challenge. Try again..!', font, blue, (screen_width // 2) - 700, screen_height // 2 )
           

            if self.rect.y > 50:
                    self.rect.y -= 1
        

        #Draw the player onto images
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
         
        return game_over

    def reset_game(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 24):            
            img_RIGHT = pygame.image.load(f'img/hero/hero{num}.png')
            img_RIGHT = pygame.transform.scale(img_RIGHT, (60, 90))
            img_LEFT = pygame.transform.flip(img_RIGHT, True, False)
            self.images_right.append(img_RIGHT)
            self.images_left.append(img_LEFT)
           
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()    
        self.vel_y = 0
        self.jumped = False
        self.direction = 0



#This is a class to draw into the world
class World():
    def __init__(self, data):
        self.tile_list = []
        
        #Loading images to be put it into the world
        dirt_img = pygame.image.load('img/dirt.png')
        dirt1_img = pygame.image.load('img/dirt1.png')
        dirt2_img = pygame.image.load('img/dirt2.png')
        ground_img = pygame.image.load('img/ground0.png')
        ground1_img = pygame.image.load('img/ground1.png')
        ground2_img = pygame.image.load('img/ground2.png')
        elevate_img = pygame.image.load('img/elevate.png')
        elevate_img1 = pygame.image.load('img/elevate1.png')
        elevate_img2 = pygame.image.load('img/elevate2.png')
        plat_img1 = pygame.image.load('img/plat_1.png')
        plat_img2 = pygame.image.load('img/plat_2.png')
        plat_img3 = pygame.image.load('img/plat_3.png')
        plat_img4 = pygame.image.load('img/plat_4.png')
        plat_img5 = pygame.image.load('img/plat_5.png')
        goal_img = pygame.image.load('img/goal.png')
        indi_plat = pygame.image.load('img/indi_plat.png')
        indi_plat1 = pygame.image.load('img/indi_plat1.png')
        

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(dirt1_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 28: #This is for the goal of the game
                    img = pygame.transform.scale(goal_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 29:
                    img = pygame.transform.scale(indi_plat, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 30:
                    img = pygame.transform.scale(indi_plat1, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(dirt2_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    spike = Enemy(col_count * tile_size, row_count * tile_size - 15)
                    spike_group.add(spike)
                if tile == 100:
                    spike_invert = Enemy_invert(col_count * tile_size, row_count * tile_size - 15)
                    spike_invert_group.add(spike_invert)
                if tile == 101:
                    spike_invert_y = Enemy_invert_y(col_count * tile_size, row_count * tile_size -15, 0, 1)
                    spike_invert_y_group.add(spike_invert_y)
                if tile == 102:
                    spike_invert_y_opposite = Enemy_invert_y_opposite(col_count * tile_size, row_count * tile_size - 15, 0, 1)
                    spike_invert_y_opposite_group.add(spike_invert_y_opposite)
                if tile == 5:
                    img = pygame.transform.scale(ground1_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 44:
                    img = pygame.transform.scale(elevate_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 45:
                    img = pygame.transform.scale(elevate_img1, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 46:
                    img = pygame.transform.scale(elevate_img2, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 775:
                    img = pygame.transform.scale(ground_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 776:
                    img = pygame.transform.scale(ground1_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 777:
                    img = pygame.transform.scale(ground2_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 333:
                    img = pygame.transform.scale(plat_img1, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 334:
                    img = pygame.transform.scale(plat_img2, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 335:
                    img = pygame.transform.scale(plat_img3, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 336:
                    img = pygame.transform.scale(plat_img4, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile) 
                if tile == 337:
                    img = pygame.transform.scale(plat_img5, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                
                if tile == 8:
                    dang = danger(col_count * tile_size, row_count * tile_size + 1)
                    dang_group.add(dang)
                if tile == 9:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 1)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spike_img = pygame.image.load('img/Spikes.png')
        self.image = pygame.transform.scale(spike_img, (60, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    
    #This function provide movement direction for the spikes onto the screen
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Enemy_invert(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spike_img = pygame.image.load('img/Spikes_invert.png')
        self.image = pygame.transform.scale(spike_img, (60, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
            
    #This function provide movement direction for the spikes onto the screen
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1

class Enemy_invert_y(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        spike_img = pygame.image.load('img/Spikes_invert_y.png')
        self.image = pygame.transform.scale(spike_img, (60, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.move_x = move_x
        self.move_y = move_y
    
    #This function provide movement direction for the spikes onto the screen
    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 25:
            self.move_direction *= -1
            self.move_counter *= -1

class Enemy_invert_y_opposite(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        spike_img = pygame.image.load('img/Spikes_invert_y_opposite.png')
        self.image = pygame.transform.scale(spike_img, (60, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.move_x = move_x
        self.move_y = move_y
    
    #This function provide movement direction for the spikes onto the screen
    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 25:
            self.move_direction *= -1
            self.move_counter *= -1

class danger(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/dangerous.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coins/coins0.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        

#Building the world data to put some elements for the game
world_data = [
[0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 9, 9, 9, 0, 0, 100, 0, 9, 9, 0, 100, 0, 9, 9, 0, 100, 0, 0, 9, 9, 0, 100, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 9, 4, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 102], 
[101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 100, 100, 100, 0, 0, 0, 0, 0, 0, 0, 44, 45, 46, 0, 0, 0, 9, 9, 9, 9, 9, 0, 0], 
[0, 0, 9, 0, 0, 44, 45, 46, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 333, 334, 335, 336, 337, 0, 0, 102], 
[0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 776, 9, 0, 0, 0, 0], 
[0, 0, 9, 0, 0, 0, 0, 0, 0, 29, 9, 9, 9, 9, 30, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 9, 776, 9, 9, 0, 0, 0], 
[101, 1, 2, 3, 0, 0, 0, 0, 0, 29, 776, 776, 776, 776, 30, 0, 0, 0, 0, 333, 334, 335, 336, 337, 0, 4, 4, 4, 0, 0, 776, 776, 776, 0, 0, 102], 
[0, 0, 776, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 776, 9, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 776, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 776, 776, 776, 9, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 102], 
[0, 9, 0, 0, 0, 0, 0, 1, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 1,2,3, 0, 0, 0, 0, 0, 0, 0, 0], 
[101, 2, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 29, 9, 9, 29, 0, 0, 0, 29, 0, 0, 0, 0, 0, 0, 0, 0, 776, 776, 776, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 776, 0, 28, 0], 
[0, 9, 0, 0, 9, 0, 0, 0, 0, 4, 9, 0, 4, 0, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 776, 776, 776, 776], 
[9, 29, 9, 9, 29, 9, 9, 1, 2, 2, 2, 2, 2, 2, 3, 8, 8, 8, 1, 2, 3, 9, 9, 9, 333, 334, 335, 336, 337, 9, 9, 9, 0, 0, 0, 0], 
[8, 8, 8, 8, 8, 8, 8, 775, 776, 776, 776, 776, 776, 776, 776, 776, 776, 776, 777, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
]

player = Player(100, screen_height - 500)

spike_group = pygame.sprite.Group()

spike_invert_group = pygame.sprite.Group()

spike_invert_y_group = pygame.sprite.Group()

spike_invert_y_opposite_group = pygame.sprite.Group()

dang_group = pygame.sprite.Group()

coin_group = pygame.sprite.Group()

world = World(world_data)

#Creating dummy coin for showing the score in the screen player
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#Creating Buttons for the Main Menu
restart_button = Button(screen_width // 2, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 350, screen_height // 2, exit_img)

run = True

while run:

    clock.tick(FPS)
    
    screen.blit(bg_img, (0, 0))

    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
    
        if game_over == 0:
            spike_group.update()
            spike_invert_group.update()
            spike_invert_y_group.update()
            #Update the score of the player
            #Checking if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            
            draw_text(' ' + str(score), font_score, white, tile_size - 10, 10)
        
        spike_group.draw(screen)
        spike_invert_group.draw(screen)
        spike_invert_y_group.draw(screen)
        spike_invert_y_opposite_group.draw(screen)
        dang_group.draw(screen)
        coin_group.draw(screen)
        world.draw()

        draw_grid()    
        
        game_over = player.update(game_over)


        #If the player has died, which I expected happen :=)
        if game_over == -1:
            if restart_button.draw():
                player = Player(100, screen_height - 500)
                game_over = 0
                score = 0

        #If the player completed the level
        if game_over == 1:
            draw_text('YOU ARE THE MASTER OF THE PYGAME CHALLENGE', font, blue, (screen_width // 2) - 140, screen_height // 2)
        

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # create the credit button rectangle
        credit_button_width = 100
        credit_button_height = 50
        credit_button = pygame.Rect(screen_width - credit_button_width - 10, 10, credit_button_width, credit_button_height)

    # set up the font for displaying the message
        font = pygame.font.SysFont('Arial', 30)

    # draw the credit button
        pygame.draw.rect(screen, (0, 255, 0), credit_button)
        credit_message = font.render('Credits', True, (255, 255, 255))
        credit_message_rect = credit_message.get_rect(center=credit_button.center)
        screen.blit(credit_message, credit_message_rect)    
    
    # check for mouse clicks on the credit button
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()
    if credit_button.collidepoint(mouse_pos) and mouse_clicked[0]:
        # display the credit message
        message1 = font.render('This game was created by Danny Chavez', True, (0, 0, 0))
        message2 = font.render('using Pygame.', True, (0, 0, 0))
        message1_rect = message1.get_rect(center=(screen_width/2, screen_height/2-20))
        message2_rect = message2.get_rect(center=(screen_width/2, screen_height/2+20))
        screen.blit(message1, message1_rect)
        screen.blit(message2, message2_rect)
        pygame.display.update()
        pygame.time.wait(3000) # wait for 3 seconds before clearing the message
        screen.fill((0, 0, 0)) # clear the screen
    
    # draw the credit button again (in case it was covered by the credit message)
    pygame.draw.rect(screen, (95, 150, 179), credit_button)
    screen.blit(credit_message, credit_message_rect)

    pygame.display.update()

pygame.quit()