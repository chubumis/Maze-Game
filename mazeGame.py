import sys, pygame, random, time
#-----Variables For Colours, screen, animations, gamestates, framerate-----#
pygame.init()
# Display
dark_red = 180, 0, 0
light_red = 230, 0, 0
black = 0, 0, 0
yellow = 255,140,0
gold = 211, 175, 55
orange = 255,165,0
white = 255, 255, 255
display_w = 800
display_h = 800
screen = pygame.display.set_mode((display_w, display_h))
frameCount = 0
spriteSheet = pygame.image.load("new.png")
spriteSheet = pygame.transform.scale2x(spriteSheet)
color = (255,255,255)
brown = (100,50,50)
gameState = 'start'
circSize = 1
sizeW = 0
sizeH = 0
keyBonus = 0


#---Fonts and texts for various gamestates---#
title = pygame.font.SysFont("comicsansms", 62)
font = pygame.font.SysFont("comicsansms", 62)
font_2 = pygame.font.SysFont("comicsansms", 52)
helpFont = pygame.font.SysFont("comicsansms", 30)

#Font for title
startText = font.render("Maze Wanderer", True, (255, 0, 0))
#font for lose screen
loseText = font.render("You Lose !", True, (0, 0, 0))
#font for win screen
winText = font.render("You Win !", True, (0, 0, 0))
#font for start screen
text = font.render("Start", True, (255, 0, 0))
#font for play again
text_2 = font_2.render("Play Again", True, (255, 0, 0))
#font instuction
text_3 = font_2.render("How to play", True, (255, 0, 0))
#font back
text_4 = font.render("Back", True, (255, 0, 0))
#font for instructions
helpText = helpFont.render("Explore the map going to different rooms through", True, (255, 0, 0))
helpText1 = helpFont.render("a maze until you reach your final destination.", True, (255, 0, 0))
helpText2 = helpFont.render("Make sure not to hit the black walls, or else", True, (255, 0, 0))
helpText3 = helpFont.render("you'll restart from the beginning of the game.", True, (255, 0, 0))
helpTextFix = helpFont.render("Entering one wrong room will cost you the game!", True, (255, 0, 0))
helpText4 = helpFont.render("Use the arrow keys to move around. Good Luck!!!", True, (255, 0, 0))


#Mouse Cursor
class Mouse(pygame.sprite.Sprite):
    '''
    Makes a rect for the mouse

    Takes in cordinate of the cursor and follows
    it so it can click various of buttons.

    Parameters
    ----------
    pygame.sprite.Sprite = image
    Takes an image and makes it into a
    sprite.

    returns
    -------
    None
    '''
    def __init__(self,picture_path):
        '''
        Add the picture to the object

        Loads an image and puts it in obect.

        Parameters
        ----------
        self = self represents the instance of the class
        picture_path = loads the image

        returns
        -------
        None
        '''
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()


    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        '''
        Adds cordinates

        Gives cursor mouse cordinates.

        Parameters
        ----------
        self = self represents the instance of the class

        returns
        -------
        None
        '''

#Cursor image
cursor = Mouse("cursor.png")
#Makes a sprite group
cursor_group = pygame.sprite.Group()
#Adds image to group
cursor_group.add(cursor)

#Button Class
class Button(pygame.sprite.Sprite):
    '''
    Makes sprite for buttons

    Creates various templates for
    different buttons.

    Parameters
    ----------
    pygame.sprite.Sprite = image
    Takes an image and makes it into a
    sprite.

    returns
    -------
    None
    '''
    def __init__(self,picture_path,pos_x,pos_y):
        '''
        Add the picture to the object

        Loads an image and puts it in obect
        and gives cordinates.

        Parameters
        ----------
        self = self represents the instance of the class
        picture_path = loads the image
        pos_x,pos_y = Gives sprites cordinates

        returns
        -------
        None
        '''
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]

#---Button for start---#
button = Button("start.png",410,315)
button_group = pygame.sprite.Group()
button_group.add(button)
#---Button for restart---#
restart = Button("restart.png",410,315)
restart_group = pygame.sprite.Group()
restart_group.add(restart)
#---Button for instructions---#
How = Button("How.png",410,455)
How_group = pygame.sprite.Group()
How_group.add(How)
#---Button for back to main screen---#
Back = Button("back.png",585,710)
Back_group = pygame.sprite.Group()
Back_group.add(Back)

class Hidden(pygame.sprite.Sprite):
    '''
    Makes sprite for easter egg

    Can only be found in the bonus
    room where the player can onl find
    through exploring

    Parameters
    ----------
    pygame.sprite.Sprite = image
    Takes an image and makes it into a
    sprite.

    returns
    -------
    None
    '''
    def __init__(self,picture_path,pos_x,pos_y):
        '''
        Add the picture to the object

        Loads an image and puts it in obect
        and gives cordinates.

        Parameters
        ----------
        self = self represents the instance of the class
        picture_path = loads the image
        pos_x,pos_y = Gives sprites cordinates

        returns
        -------
        None
        '''
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]

#---Hidden text for bonus room---#
hidden = Hidden("hidden.png",400,400)
hidden_group = pygame.sprite.Group()
hidden_group.add(hidden)


#animation variables
ghoulPos = [360, 60]
ghoulRect = [78, 2, 44, 72]
ghoulPatchNumber = 0
ghoulNumPatches = 8
ghoulFrameRate = 70

#The animations of the Sprite
def animate():
    '''
    Animation

    Makes it so the character moves

    Parameters
    ----------
    None

    returns
    -------
    None
    '''
    global ghoulPatchNumber
    if frameCount % ghoulFrameRate == 0:
        if ghoulPatchNumber < ghoulNumPatches - 1:
            ghoulPatchNumber += 1
            ghoulRect[0] += 64
        else:
            ghoulPatchNumber = 0
            ghoulRect[0] = 78

#Rooms that the player will be in

def rooms():
    '''
    Rooms through out the maze

    This function is pretty much
    different gamestates that the player goes through
    from start screen, game rooms, end screen, instructions.

    Parameters
    ----------
    None

    returns
    -------
    None
    '''
    global gameState
    global tempSurface
    global ghoulPos
    global yellow
    global sizeH
    global sizeW
    global orange
    if gameState == 'help':
        screen.fill((100, 25, 100))
        screen.blit(helpText,(25,140))
        screen.blit(helpText1,(25,180))
        screen.blit(helpText2,(25,220))
        screen.blit(helpText3,(25,260))
        screen.blit(helpTextFix,(25,300))
        screen.blit(helpText4,(25,340))
        back = pygame.draw.rect(screen, yellow, pygame.Rect(440, 673, 290, 75))
        cursor_group.draw(screen)
        Back_group.draw(screen)
        cursor_group.update()
        screen.blit(text_4,(500,660))
        if event.type == pygame.MOUSEBUTTONDOWN:
            #time.sleep(0.2)
            if pygame.sprite.spritecollide(cursor,Back_group,False):
                pygame.mixer.Sound("click.wav")
                gameState = 'start'
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] in list(range(437, 727)) and mouse_pos[1] in list(range(673, 753)):
                yellow = 255,165,0
            else:
                yellow = 255,140,0
    if gameState == 'start':
        screen.fill((100, 25, 50))
        play = pygame.draw.rect(screen, yellow, pygame.Rect(265, 275, 290, 75))
        play2 = pygame.draw.rect(screen, orange, pygame.Rect(265, 415, 290, 75))
        cursor_group.draw(screen)
        button_group.draw(screen)
        How_group.draw(screen)
        cursor_group.update()
        screen.blit(text,(320,265))
        screen.blit(text_3,(268,415))
        screen.blit(startText,(200,100))


        if event.type == pygame.MOUSEBUTTONDOWN:
            #time.sleep(0.2)
            if pygame.sprite.spritecollide(cursor,button_group,False):
                gameState = 'room_1'
                ghoulPos = [360, 60]
        if event.type == pygame.MOUSEBUTTONDOWN:
            #time.sleep(0.2)
            if pygame.sprite.spritecollide(cursor,How_group,False):
                gameState = 'help'
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] in list(range(260, 555)) and mouse_pos[1] in list(range(275, 355)):
                yellow = 255,165,0
            else:
                yellow = 255,140,0
            if mouse_pos[0] in list(range(260, 555)) and mouse_pos[1] in list(range(420, 490)):
                orange = 255,165,0
            else:
                orange = 255,140,0


    if gameState == 'room_1':
#------------------Various Game Rooms-------------------------------#
        '''Every game room has the word room in the gameState so you know which one are
        in use when playing the game. Every rectangle in each room that has the name
        border makes you restart in a certain posistion if you hit it.
        If it has the word enter it means go to the next room. Each room redraws the character
        with a hitbox and various of variables for the character.
        '''
        global gold
        global keyBonus
        global remake
        global circSize
        circSize = 1
        gold = 211, 175, 55
        remake = False
        keyBonus = 0
        sizeW = 0
        sizeH = 0
        #print(ghoulPos)
        ghoulHitbox = pygame.Rect(ghoulPos[0], ghoulPos[1], 44, 72)
        screen.fill(light_red)
        #pygame.draw.rect(screen,(0,0,0), ghoulHitbox, 2)
        cant = pygame.draw.rect(screen, dark_red, pygame.Rect(200, 0, 400, 10))
        border = pygame.draw.rect(screen, black, pygame.Rect(0, 0, 200, 800))
        border2 = pygame.draw.rect(screen, black, pygame.Rect(600, 0, 200, 800))
        enter = pygame.draw.rect(screen, dark_red, pygame.Rect(200, 790, 400, 10))
        tempSurface = pygame.Surface((ghoulRect[2], ghoulRect[3]))
        tempSurface.fill((1, 1, 1))
        tempSurface.set_colorkey((1, 1, 1))
        tempSurface.blit(spriteSheet, (0, 0), ghoulRect)
        move()
        screen.blit(tempSurface, ghoulPos)
        if (pygame.Rect.colliderect(ghoulHitbox,border)):
            ghoulPos[0] = 200
        elif (pygame.Rect.colliderect(ghoulHitbox,border2)):
            ghoulPos[0] = 555
        elif (pygame.Rect.colliderect(ghoulHitbox,enter)):
            gameState = 'room_2'
            ghoulPos = [360, 100]
        elif (pygame.Rect.colliderect(ghoulHitbox,cant)):
            ghoulPos[1] = 11

    if gameState == 'room_2':
        ghoulHitbox = pygame.Rect(ghoulPos[0], ghoulPos[1], 44, 72)
        screen.fill(light_red)
        ##pygame.draw.rect(screen, (0,255,0), ghoulHitbox, 2)
        tempSurface = pygame.Surface((ghoulRect[2], ghoulRect[3]))
        tempSurface.fill((1, 1, 1))
        tempSurface.set_colorkey((1, 1, 1))
        tempSurface.blit(spriteSheet, (0, 0), ghoulRect)
        move()
        screen.blit(tempSurface, ghoulPos)
        cant2 = pygame.draw.rect(screen, dark_red, pygame.Rect(300, 0, 200, 10))
        border3 = pygame.draw.rect(screen, black, pygame.Rect(0, 0, 300, 300))
        border4 = pygame.draw.rect(screen, black, pygame.Rect(500, 0, 300, 300))
        border5 = pygame.draw.rect(screen, black, pygame.Rect(0, 500, 800, 300))
        enter2 = pygame.draw.rect(screen, dark_red, pygame.Rect(790, 300, 10, 200))
        lose = pygame.draw.rect(screen, dark_red, pygame.Rect(0, 300, 10, 200))

        if (pygame.Rect.colliderect(ghoulHitbox,border3)):
            gameState = 'room_1'
            ghoulPos = [360, 60]

        elif (pygame.Rect.colliderect(ghoulHitbox,border4)):
            gameState = 'room_1'
            ghoulPos = [360, 60]

        elif (pygame.Rect.colliderect(ghoulHitbox,cant2)):
            ghoulPos[1] = 11

        elif (pygame.Rect.colliderect(ghoulHitbox,border5)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,enter2)):
            gameState = 'room_3'
            ghoulPos = [350, 100]
        elif (pygame.Rect.colliderect(ghoulHitbox,lose)):
            gameState = 'lost'

    if gameState == 'room_3':

        ghoulHitbox = pygame.Rect(ghoulPos[0], ghoulPos[1], 44, 72)
        screen.fill(light_red)
        #pygame.draw.rect(screen, (0,255,0), ghoulHitbox, 2)
        tempSurface = pygame.Surface((ghoulRect[2], ghoulRect[3]))
        tempSurface.fill((1, 1, 1))
        tempSurface.set_colorkey((1, 1, 1))
        tempSurface.blit(spriteSheet, (0, 0), ghoulRect)
        move()
        screen.blit(tempSurface, ghoulPos)
        cant3 = pygame.draw.rect(screen, dark_red, pygame.Rect(300, 0, 200, 10))
        border6 = pygame.draw.rect(screen, black, pygame.Rect(500, 0, 300, 350))
        border7 = pygame.draw.rect(screen, black, pygame.Rect(500, 450, 300, 450))
        border8 = pygame.draw.rect(screen, black, pygame.Rect(0, 0, 300, 800))
        enter3 = pygame.draw.rect(screen, dark_red, pygame.Rect(300, 790, 200, 10))
        lose2 = pygame.draw.rect(screen, dark_red, pygame.Rect(790, 350, 10, 100))

        if (pygame.Rect.colliderect(ghoulHitbox,border6)):
            gameState = 'room_1'
            ghoulPos = [360, 60]

        elif (pygame.Rect.colliderect(ghoulHitbox,border7)):
            gameState = 'room_1'
            ghoulPos = [360, 60]

        elif (pygame.Rect.colliderect(ghoulHitbox,cant3)):
            ghoulPos[1] = 11

        elif (pygame.Rect.colliderect(ghoulHitbox,border8)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,enter3)):
            ghoulPos = [470, 25]
            gameState = 'room_4'
        elif (pygame.Rect.colliderect(ghoulHitbox,lose2)):
            gameState = 'lost'

    if gameState == 'room_4':
        ghoulHitbox = pygame.Rect(ghoulPos[0], ghoulPos[1], 44, 72)
        screen.fill(light_red)
        #pygame.draw.rect(screen, (0,255,0), ghoulHitbox, 2)
        tempSurface = pygame.Surface((ghoulRect[2], ghoulRect[3]))
        tempSurface.fill((1, 1, 1))
        tempSurface.set_colorkey((1, 1, 1))
        tempSurface.blit(spriteSheet, (0, 0), ghoulRect)
        move()
        screen.blit(tempSurface, ghoulPos)
        cant4 = pygame.draw.rect(screen, dark_red, pygame.Rect(400, 0, 200, 10))
        cant5 = pygame.draw.rect(screen, dark_red, pygame.Rect(10, 0, 240, 10))
        border10 = pygame.draw.rect(screen, black, pygame.Rect(600, 0, 300, 800))
        border11 = pygame.draw.rect(screen, black, pygame.Rect(0, 600, 800, 200))
        borderGem = pygame.draw.rect(screen, black, pygame.Rect(0, 110, 150, 390))
        border12 = pygame.draw.rect(screen, black, pygame.Rect(250, 0, 150, 500))
        enterGem = pygame.draw.rect(screen, dark_red, pygame.Rect(0, 0, 10, 110))
        enter4 = pygame.draw.rect(screen, dark_red, pygame.Rect(0, 500, 10, 100))
        if (pygame.Rect.colliderect(ghoulHitbox,border10)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,border11)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,cant4)):
            ghoulPos[1] = 11
        elif (pygame.Rect.colliderect(ghoulHitbox,cant5)):
            ghoulPos[1] = 11
        elif (pygame.Rect.colliderect(ghoulHitbox,border12)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,borderGem)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,enterGem)):
            gameState = 'Key' #enter room to collect key
            ghoulPos = [725, 330]
        elif (pygame.Rect.colliderect(ghoulHitbox,enter4)):
            ghoulPos = [350, 100]
            gameState = 'room_5'

    if gameState == 'room_5':
        ghoulHitbox = pygame.Rect(ghoulPos[0], ghoulPos[1], 44, 72)
        screen.fill(light_red)
        #pygame.draw.rect(screen, (0,255,0), ghoulHitbox, 2)
        tempSurface = pygame.Surface((ghoulRect[2], ghoulRect[3]))
        tempSurface.fill((1, 1, 1))
        tempSurface.set_colorkey((1, 1, 1))
        tempSurface.blit(spriteSheet, (0, 0), ghoulRect)
        move()
        screen.blit(tempSurface, ghoulPos)
        cant6 = pygame.draw.rect(screen, dark_red, pygame.Rect(300, 0, 200, 10))
        border13 = pygame.draw.rect(screen, black, pygame.Rect(0, 0, 300, 800))
        border14 = pygame.draw.rect(screen, black, pygame.Rect(0, 600, 800, 200))
        border15 = pygame.draw.rect(screen, black, pygame.Rect(500, 0, 300, 500))
        enter5 = pygame.draw.rect(screen, dark_red, pygame.Rect(790, 500, 10, 100))
        if (pygame.Rect.colliderect(ghoulHitbox,border13)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,border14)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,cant6)):
            ghoulPos[1] = 11
        elif (pygame.Rect.colliderect(ghoulHitbox,border15)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,enter5)):
            ghoulPos = [10, 250]
            gameState = 'room_6'

    if gameState == 'room_6':

        ghoulHitbox = pygame.Rect(ghoulPos[0], ghoulPos[1], 44, 72)
        screen.fill(light_red)
        #pygame.draw.rect(screen, (0,255,0), ghoulHitbox, 2)
        tempSurface = pygame.Surface((ghoulRect[2], ghoulRect[3]))
        tempSurface.fill((1, 1, 1))
        tempSurface.set_colorkey((1, 1, 1))
        tempSurface.blit(spriteSheet, (0, 0), ghoulRect)
        move()
        screen.blit(tempSurface, ghoulPos)
        cant7 = pygame.draw.rect(screen, dark_red, pygame.Rect(0, 200, 10, 300))
        border16 = pygame.draw.rect(screen, black, pygame.Rect(450, 450, 350, 800))
        border17 = pygame.draw.rect(screen, black, pygame.Rect(0, 0, 800, 200))
        border18 = pygame.draw.rect(screen, black, pygame.Rect(0, 450, 300, 350))
        enter6 = pygame.draw.rect(screen, dark_red, pygame.Rect(790, 200, 10, 250))
        lose3 = pygame.draw.rect(screen, dark_red, pygame.Rect(300, 790, 150, 10))
        if (pygame.Rect.colliderect(ghoulHitbox,border16)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,border17)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,cant7)):
            ghoulPos[0] = 11
        elif (pygame.Rect.colliderect(ghoulHitbox,border18)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,lose3)):
            gameState = 'lost'
        elif (pygame.Rect.colliderect(ghoulHitbox,enter6)):
            ghoulPos = [40, 350]
            gameState = 'room_7'

    if gameState == 'room_7':

        ghoulHitbox = pygame.Rect(ghoulPos[0], ghoulPos[1], 44, 72)
        screen.fill(light_red)
        #pygame.draw.rect(screen, (0,255,0), ghoulHitbox, 2)
        tempSurface = pygame.Surface((ghoulRect[2], ghoulRect[3]))
        tempSurface.fill((1, 1, 1))
        tempSurface.set_colorkey((1, 1, 1))
        tempSurface.blit(spriteSheet, (0, 0), ghoulRect)
        move()
        screen.blit(tempSurface, ghoulPos)
        cant8 = pygame.draw.rect(screen, dark_red, pygame.Rect(0, 250, 10, 250))
        border19 = pygame.draw.rect(screen, black, pygame.Rect(0, 0, 400, 250))
        border20 = pygame.draw.rect(screen, black, pygame.Rect(0, 500, 400, 300))
        border21 = pygame.draw.rect(screen, black, pygame.Rect(650, 0, 150, 800))
        enter7 = pygame.draw.rect(screen, dark_red, pygame.Rect(400, 790, 250, 10))
        enterB = pygame.draw.rect(screen, brown, pygame.Rect(400, 0, 250, 10))
        if (pygame.Rect.colliderect(ghoulHitbox,border19)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,border20)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,cant8)):
            ghoulPos[0] = 11
        elif (pygame.Rect.colliderect(ghoulHitbox,border21)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,enter7)):
            ghoulPos = [40, 350]
            gameState = 'win'
        elif (pygame.Rect.colliderect(ghoulHitbox,enterB)) and keyBonus > 0:
            gameState = 'bonus' #enter easter egg room only if you have the key
            ghoulPos = [375, 705]
        elif (pygame.Rect.colliderect(ghoulHitbox,enterB)) and keyBonus == 0:
            ghoulPos[1] = 11
#--------GameStates not for gameplay---------------------#
    '''Contains win and lost screen'''
    if gameState == 'win':
        circSize += 1
        if circSize > 400:
            circSize = 400
        print(circSize)
        screen.fill(black)
        pygame.draw.circle(screen, (dark_red), (400, 400), circSize)
        if circSize == 400:
            winR = pygame.draw.rect(screen, yellow, pygame.Rect(265, 275, 290, 75))
            cursor_group.draw(screen)
            restart_group.draw(screen)
            cursor_group.update()
            screen.blit(text_2,(290,270))
            screen.blit(winText,(270,100))

            if event.type == pygame.MOUSEBUTTONDOWN:
                #time.sleep(0.2)
                if pygame.sprite.spritecollide(cursor,restart_group,False):
                    gameState = 'room_1'
                    ghoulPos = [360, 60]
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] in list(range(260, 555)) and mouse_pos[1] in list(range(275, 355)):
                    yellow = 255,165,0
                else:
                    yellow = 255,140,0

    if gameState == 'lost':
        #global sizeW
        #global sizeH
        screen.fill(black)
        sizeW+=0.5
        sizeH+=0.5
        if sizeH > 600:
            sizeH = 600
        if sizeW > 600:
            sizeW = 600

        loseR = pygame.draw.rect(screen, light_red, pygame.Rect(100,100, sizeW,sizeH))
        if sizeH == 600:
            play = pygame.draw.rect(screen, yellow, pygame.Rect(265, 275, 290, 75))
            cursor_group.draw(screen)
            restart_group.draw(screen)
            cursor_group.update()
            screen.blit(text_2,(290,270))
            screen.blit(loseText,(270,100))

            if event.type == pygame.MOUSEBUTTONDOWN:
                #time.sleep(0.2)
                if pygame.sprite.spritecollide(cursor,restart_group,False):
                    gameState = 'room_1'
                    ghoulPos = [360, 60]
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] in list(range(260, 555)) and mouse_pos[1] in list(range(275, 355)):
                    yellow = 255,165,0
                else:
                    yellow = 255,140,0
#----------------GameStates for easter egg-----------#
    '''Rooms to find key and bonus room for the sake of exploring'''
    if gameState == 'Key':

        ghoulHitbox = pygame.Rect(ghoulPos[0], ghoulPos[1], 44, 72)
        screen.fill(light_red)
        #pygame.draw.rect(screen, (0,255,0), ghoulHitbox, 2)
        tempSurface = pygame.Surface((ghoulRect[2], ghoulRect[3]))
        tempSurface.fill((1, 1, 1))
        tempSurface.set_colorkey((1, 1, 1))
        tempSurface.blit(spriteSheet, (0, 0), ghoulRect)
        move()
        goldKey = pygame.draw.rect(screen, gold, pygame.Rect(300, 400, 30, 10))
        screen.blit(tempSurface, ghoulPos)
        borderKey1 = pygame.draw.rect(screen, black, pygame.Rect(0,0, 100,800))
        borderKey2 = pygame.draw.rect(screen, black, pygame.Rect(0,0, 800,100))
        borderKey3 = pygame.draw.rect(screen, black, pygame.Rect(0,700, 800,100))
        borderKey4 = pygame.draw.rect(screen, black, pygame.Rect(700, 0, 100,300))
        borderKey5 = pygame.draw.rect(screen, black, pygame.Rect(700, 500, 100, 300))
        rEnter = pygame.draw.rect(screen, dark_red, pygame.Rect(790, 300, 10, 200))

        if (pygame.Rect.colliderect(ghoulHitbox,borderKey1)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,borderKey2)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,borderKey3)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,borderKey4)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,borderKey5)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,goldKey)):
            gold = 230, 0, 0
            keyBonus += 1
        elif (pygame.Rect.colliderect(ghoulHitbox,rEnter)):
            gameState = 'room_4'
            ghoulPos = [25, 20]

    if gameState == 'bonus':
        ghoulHitbox = pygame.Rect(ghoulPos[0], ghoulPos[1], 44, 72)
        screen.fill(light_red)
        #pygame.draw.rect(screen, (0,255,0), ghoulHitbox, 2)
        tempSurface = pygame.Surface((ghoulRect[2], ghoulRect[3]))
        tempSurface.fill((1, 1, 1))
        tempSurface.set_colorkey((1, 1, 1))
        tempSurface.blit(spriteSheet, (0, 0), ghoulRect)
        move()
        screen.blit(tempSurface, ghoulPos)
        borderGem1 = pygame.draw.rect(screen, black, pygame.Rect(0,0, 100,800))
        borderGem2 = pygame.draw.rect(screen, black, pygame.Rect(0,0, 800,100))
        borderGem3 = pygame.draw.rect(screen, black, pygame.Rect(0,700, 300,100))
        borderGem4 = pygame.draw.rect(screen, black, pygame.Rect(500, 700, 300,100))
        borderGem5 = pygame.draw.rect(screen, black, pygame.Rect(700, 0, 100, 800))
        rEnter1 = pygame.draw.rect(screen, dark_red, pygame.Rect(300, 790, 200, 10))
        hidden_group.draw(screen)
        if (pygame.Rect.colliderect(ghoulHitbox,borderGem1)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,borderGem2)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,borderGem3)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,borderGem4)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,borderGem5)):
            gameState = 'room_1'
            ghoulPos = [360, 60]
        elif (pygame.Rect.colliderect(ghoulHitbox,rEnter1)):
            gameState = 'room_7'
            ghoulPos = [485, 25]


#Movement of the sprite from left to right and up to down
def move():
    '''
    Movement

    Makes it so the character moves left,
    right, down and up using arrow keys

    Parameters
    ----------
    None

    returns
    -------
    None
    '''
    Move = "notMoving"
    Direction = "defualt"
    global tempSurface
    global ghoulPatchNumber
    global spriteSheet
    #Detects when key is pressed
    keys = pygame.key.get_pressed()
    #Detects when key is pressed right
    if keys[pygame.K_RIGHT]:
        Move = "moving"
        Direction = "right"
        ghoulPos[0] += 0.30

    #Detects when key is pressed left
    elif keys[pygame.K_LEFT]:
        Move = "moving"
        Direction = "left"
        ghoulPos[0] -= 0.30
    #Detects when key is pressed up
    elif keys[pygame.K_UP]:
        Move = "moving"
        Direction = "right"
        ghoulPos[1] -= 0.30
    #Detects when key is pressed down
    elif keys[pygame.K_DOWN]:
        Move = "moving"
        Direction ='left'
        ghoulPos[1] += 0.30
    else:
        Move = "notMoving"
        ghoulRect[0] = 78

    if Move == "moving":
        if Direction == "right":
            animate()

        if Direction == "left":
            tempSurface = pygame.transform.flip(tempSurface, True, False)
            animate()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    print(pygame.mouse.get_pos())
    rooms()
    pygame.display.flip()
    frameCount += 1
    clock.tick(1)
pygame.quit()
quit()




