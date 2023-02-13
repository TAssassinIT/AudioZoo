import sys
import os
import pygame
import random
import tkinter.filedialog
import audio_functions

#pygame Initialization
pygame.init()
pygame.mixer.init()
pygame.font.init()
game_font=pygame.font.SysFont("Times New Roman",30)

#Class definitions
class sprite():
    def __init__(self, image="Sprites/sprite0.gif", sound_file="Sounds/metalgear.wav", width = 90, height = 90, initPos=(100,200)):
        self.initPos = initPos
        self.width = width
        self.height = height
        
        self.image = pygame.transform.scale(pygame.image.load(image), (self.width, self.height))
        self.rect = self.image.get_rect()

        self.orig_sound_file = sound_file
        self.mod_sound_file = sound_file

        self.volume = 0.5
        self.pitch = 0.5
        self.pitch = 0.5
        self.speed = 0.5

        def __del__(self):
            print("deleted sprite with audio file: " + str(self.orig_sound_file))

class slider():
    def __init__(self, minX=200, maxX=600, y=700):
        if minX > maxX or minX < 0 or maxX > 900:
            ValueError
        self.y = y
        self.minX = minX
        self.maxX = maxX
        self.x = minX + (maxX - minX) / 2

    def get_level(self):
        #return (self.x - self.minX) / ((self.maxX-self.minX )/ self.levels[1]) + self.levels[0]
        return (self.x - self.minX) / ((self.maxX-self.minX ))

    def set_level(self, val):
        if val > 1 or val < 0:
            ValueError
        self.x = (val * (self.maxX - self.minX)) + self.minX

    def draw(self):
        pygame.draw.rect(screen, "Black", (self.minX-2, self.y-12, self.maxX - self.minX+4, 24) )
        pygame.draw.rect(screen, "Grey", (self.minX, self.y-10, self.maxX - self.minX, 20) )
        pygame.draw.rect(screen, "Black", (self.minX+10, self.y-1, self.maxX - self.minX -20 , 1) )
        self.rect = pygame.draw.circle(screen, "Black", (self.x, self.y), 10)
        pygame.draw.circle(screen, "Red", (self.x, self.y), 9)

class textBox():
    def __init__(self, x=0, y=0, width=100, height=20, text="", background_color=(255,255,255),border_color=(0,0,0),text_color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height #location and size

        self.text=text #text

        self.background_color=background_color
        self.border_color=border_color
        self.text_color=text_color #colors
    def draw(self):
        self.rect = pygame.draw.rect(screen,self.background_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen,self.border_color, (self.x, self.y, self.width, self.height) ,width=1)
        text_surface=game_font.render(self.text,False,self.text_color)
        screen.blit(text_surface,(self.x,self.y))
    def within(self,x,y):
        return x>=self.x and x<=self.x+self.width and y>=self.y and y<=self.y+self.height

#Screen setup
size = width, height = 1400, 801
screen = pygame.display.set_mode(size)
BG = pygame.transform.scale(pygame.image.load("./Background\Island1.png"), (1400,800))


sprites = [sprite("Sprites/baloon.png", "Sounds/bruh.wav"), sprite("Sprites/Cactus.png", "Sounds/emergency.wav")]
dragging_sprite = False
dragging_slider = None
initmousepos=[0,0]#initial position of mouse when clicking on sprite, used to calculate where the sprite should be
initspritepos=[0,0]#initial position of sprite when clicking on sprite

#Create widgets

#Buttons
addSpriteButton = textBox(100,height-50,250,50, text="Add a sprite")
removeSpriteButton = textBox(500,height-50,250,50,text="Remove a sprite")

#Sliders
volume_slider = slider(300, 700, 600)

buttons = [addSpriteButton, removeSpriteButton]
sliders = [volume_slider]

selected_sprite = sprites[0]


#loops through sprites, if a sprite is clicked on we return that sprite and set initspritepos and initmousepos apprpriately
def check_drag_sprite(): 
    global sprites, dragging_sprite, initmousepos, initspritepos
    tmp = None
    for i in range(len(sprites)-1,-1,-1):#play corresponding sound to sprite clicked on, prioritize sprites displayed last/on top
        if sprites[i].rect.collidepoint(pygame.mouse.get_pos()):
            dragging_sprite = True
            initmousepos=[event.pos[0],event.pos[1]]
            initspritepos=[sprites[i].rect.x,sprites[i].rect.y]
            tmp=sprites[i] #give the object clicked on top priority
            sprites.remove(tmp)
            sprites.append(tmp)
            break #only interact with the first sprite found
    return tmp

#loops through sliders, if a slider is clicked on, we return that slider and set initsliderpos and initmousepos appropriately
def check_drag_slider():
    global sliders, dragging_slider, initmousepos, initsliderpos
    tmp = None
    for i in range(len(sliders)-1,-1,-1):
        if sliders[i].rect.collidepoint(pygame.mouse.get_pos()):
            dragging_slider = sliders[i]
            initmousepos=[event.pos[0],event.pos[1]]
            initsliderpos=[sliders[i].rect.x,sliders[i].rect.y]
            tmp=sliders[i] #give the object clicked on top priority
            sliders.remove(tmp)
            sliders.append(tmp)
            break #only interact with the first sprite found
    return tmp

def drag_sprite(mouse_x, mouse_y):
    sprites[len(sprites)-1].rect.x = initspritepos[0]+mouse_x-initmousepos[0]
    sprites[len(sprites)-1].rect.y = initspritepos[1]+mouse_y-initmousepos[1]

def drag_slider(mouse_x):
    if mouse_x > sliders[len(sliders)-1].maxX:
        sliders[len(sliders)-1].x = sliders[len(sliders)-1].maxX
    elif mouse_x < sliders[len(sliders)-1].minX:
        sliders[len(sliders)-1].x = sliders[len(sliders)-1].minX
    else:
        sliders[len(sliders)-1].x = initsliderpos[0]+mouse_x-initmousepos[0]

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: 

            #SUPER IMPORTANT
            #selected sprite stores the last sprite clicked on. Nonetype if the background was clicked or selected_sprite got deleted
            #dragging_slider stores the slider currently being dragged
            if (check_drag_slider() == None):
                selected_sprite = check_drag_sprite()
            if selected_sprite == None:
                dragging_slider = None # !! if we try to drag a slider with no current selected_sprite, we do not allow the drag. Slider default to 0.5 !!
            
            # There are 3 steps to dragging. 
            # 1. on MOUSEBUTTONDOWN, set selected_sprite/dragging_slider to what was clicked
            # 2. on MOUSEMOTION, if dragging then drag selected_sprite/dragging_slider from their inital positions (initspritepos/initsliderpos)
            # 3. on MOUSEBUTTONUP, we drop them into place and apply any effects from the drag (like removing sprites, changing volumes, etc)
            
            #If add-a-sprite button is clicked
            if addSpriteButton.within(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                potentialsprites=os.listdir("Sprites")
                potentialsounds=os.listdir("Sounds")
                image = tkinter.filedialog.askopenfilename(initialdir = os.getcwd()+"\\Sprites\\")
                sound = tkinter.filedialog.askopenfilename(initialdir = os.getcwd()+"\\Sounds\\")
                sprites.append(sprite(image, sound))
        elif event.type == pygame.MOUSEBUTTONUP: 

            #If we dragged a sprite
            if dragging_sprite:
                #If the sprite is over the remove button, delete it. Set selected_sprite to Nonetype
                if removeSpriteButton.within(selected_sprite.rect.x, selected_sprite.rect.y):
                    del selected_sprite
                    sprites.remove(sprites[len(sprites)-1])
                    selected_sprite = None
                dragging_sprite = False

            #If we dragged a slider
            if dragging_slider != None:
                # set the selected_sprite's attributes to the dragged slider's position
                if dragging_slider == volume_slider:
                    selected_sprite.volume = dragging_slider.get_level()
                    selected_sprite.mod_sound_file = audio_functions.changeVolume(selected_sprite.orig_sound_file, selected_sprite.volume)
                dragging_slider = None
            #if we did not click on a slider, and we did not drag our mouse since the last MOUSEBUTTONDOWN, and selected_sprite exists, play the sound
            elif abs(event.pos[0]-initmousepos[0]) < 5 and abs(event.pos[1]-initmousepos[1]) < 5 and selected_sprite != None: #if the sprite was not dragged
                #play the sprite sound
                pygame.mixer.Sound(sprites[len(sprites)-1].mod_sound_file).play()
                sprites[len(sprites)-1].rect.x = initspritepos[0]
                sprites[len(sprites)-1].rect.y = initspritepos[1] 

        elif event.type == pygame.MOUSEMOTION:
            #If we are currently dragging something, drag it
            if dragging_sprite:
                drag_sprite(event.pos[0], event.pos[1])
            if dragging_slider != None:
                drag_slider(event.pos[0])

    #If a slider is not currently being dragged, set slider levels to that of the currently selected sprite
    if selected_sprite != None and dragging_slider == None:
        for i in sliders:
            if i == volume_slider:
                i.set_level(selected_sprite.volume)

    #If selected_sprite goes to None, default all sliders to 0.5
    if selected_sprite == None:
        for i in sliders:
            i.set_level(0.5)
            
    screen.fill((0,0,0))
    screen.blit(BG, (0,0))
    
    #Draw Sprites
    for i in range(len(sprites)):
        screen.blit(sprites[i].image, sprites[i].rect)
    
    #Draw Buttons
    for button in buttons:
        button.draw()
        
    #Draw Sliders
    for slider in sliders:
        slider.draw()
        #print(slider.get_level())

    pygame.display.flip()
