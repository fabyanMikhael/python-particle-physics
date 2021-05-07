from threading import Thread
from random import randint
import pygame
pygame.init()

class Color():
    BLACK  = ( 0, 0, 0)
    WHITE  = ( 255, 255, 255)

    RED    = ( 255, 0, 0)
    GREEN  = ( 0, 255, 0)
    BLUE   = ( 0, 0, 255)

    YELLOW = ( 204, 255, 51 )
    PURPLE = ( 153, 0, 204  )
    BROWN  = ( 153, 102, 51 )
    PINK   = ( 255, 0, 102  )
    LIME   = ( 108, 218, 0  )

WINDOW_SIZE = (1000, 1000)
FPS = 144
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Template")

carryOn = True
clock = pygame.time.Clock()






GRID_SIZE = (100,100)
BOX_SIZE= (int(WINDOW_SIZE[0]/GRID_SIZE[0]), int(WINDOW_SIZE[1]/GRID_SIZE[1]))
objects = [[None for _ in range(GRID_SIZE[1]) ] for _ in range(GRID_SIZE[0])]

class Object:
    TYPE_SAND = 0
    TYPE_FIRE = 1
    TYPE_WATER = 2
    def __init__(self, type, color) -> None:
        self.color = color # (randint(1,255), randint(1,255), randint(1,255))
        self.type = type
        self.collides_with = [self.type]
        self.dont_bother = False

    def Draw(self,grid_x,grid_y):
        pygame.draw.rect(screen, self.color, pygame.Rect(grid_x * BOX_SIZE[0], grid_y * BOX_SIZE[1], *BOX_SIZE), width=0)

    def IsAvailable(self, x, y, types=[]):
        if (x >= 0 and x < GRID_SIZE[0] and y >= 0 and y < GRID_SIZE[1]):
            if (objects[x][y] == None or objects[x][y].type not in types): return True
        return False

    def NotifyOthers(self,x,y, tmp=None):
        tmp = [self.type] if tmp is None else tmp

        if y + 1 < GRID_SIZE[1]:
            if not self.IsAvailable(x,y+1, tmp):
                objects[x][y+1].dont_bother = False
            if x > 0:
                if not self.IsAvailable(x-1,y+1, tmp):
                    objects[x-1][y+1].dont_bother = False
            if x + 1 < GRID_SIZE[0]:
                if not self.IsAvailable(x+1,y+1, tmp):
                    objects[x+1][y+1].dont_bother = False

        if x > 0:
            if not self.IsAvailable(x-1,y, tmp):
                objects[x-1][y].dont_bother = False
        if x +1 < GRID_SIZE[0]:
            if not self.IsAvailable(x+1,y, tmp):
                objects[x+1][y].dont_bother = False

        if y > 1:
            if not self.IsAvailable(x,y-1, tmp):
                objects[x][y-1].dont_bother = False
            if x > 0:
                if not self.IsAvailable(x-1,y-1, tmp):
                    objects[x-1][y-1].dont_bother = False
            if x + 1< GRID_SIZE[0]:
                if not self.IsAvailable(x+1,y-1, tmp):
                    objects[x+1][y-1].dont_bother = False

class Sand(Object):
    def __init__(self) -> None:
        super().__init__(Object.TYPE_SAND, (76,70,50))

    def Update(self,x,y):
        if y == GRID_SIZE[1] - 1: return
        if self.IsAvailable(x,y+1, self.collides_with):
            objects[x][y] = None
            objects[x][y+1] = self
            self.NotifyOthers(x,y, [Object.TYPE_WATER])
        elif self.IsAvailable(x-1,y+1, self.collides_with):
            objects[x][y] = None
            objects[x-1][y+1] = self
            self.NotifyOthers(x,y, [Object.TYPE_WATER])
        elif self.IsAvailable(x+1,y+1, self.collides_with):
            objects[x][y] = None
            objects[x+1][y+1] = self
            self.NotifyOthers(x,y, [Object.TYPE_WATER])
        else : self.dont_bother = True

    

class Fire(Object):
    def __init__(self) -> None:
        super().__init__(type=Object.TYPE_FIRE,color=Color.RED)
        self.collides_with = [self.type]
        self.lifespan = 288
        self.lifetime = 0

    def Update(self,x,y):
        self.lifetime += 1
        if self.lifetime > self.lifespan:
            objects[x][y] = None
        else :
            move_y = int(randint(0,100) > 70)*2 - 1 + y
            move_x = randint(-1,1) + x
            if self.IsAvailable(move_x,move_y, self.collides_with):
                objects[x][y] = None
                objects[move_x][move_y] = self

class Water(Object):
    def __init__(self) -> None:
        super().__init__(Object.TYPE_WATER, Color.BLUE)
        self.collides_with.append(Object.TYPE_SAND)

    def Update(self, x, y):
        if y == GRID_SIZE[1] - 1: return
        if self.IsAvailable(x,y+1, self.collides_with):
            objects[x][y] = None
            objects[x][y+1] = self
        elif self.IsAvailable(x-1,y+1, self.collides_with):
            objects[x][y] = None
            objects[x-1][y+1] = self
            self.NotifyOthers(x,y)
        elif self.IsAvailable(x+1,y+1, self.collides_with):
            objects[x][y] = None
            objects[x+1][y+1] = self
            self.NotifyOthers(x,y)
        elif self.IsAvailable(x+1,y, self.collides_with):
            objects[x][y] = None
            objects[x+1][y] = self
            self.NotifyOthers(x,y)
        elif self.IsAvailable(x-1,y, self.collides_with):
            objects[x][y] = None
            objects[x-1][y] = self
            self.NotifyOthers(x,y)
        else : self.dont_bother = True


      

def Draw():
    if 0:
        for _x in range(1,GRID_SIZE[0]):
            pygame.draw.line(screen, Color.WHITE, (_x * BOX_SIZE[1],0), (_x * BOX_SIZE[1],WINDOW_SIZE[1]), width=1)
        for _y in range(1,GRID_SIZE[1]):
            pygame.draw.line(screen, Color.WHITE, (0, _y * BOX_SIZE[0]), (WINDOW_SIZE[0], _y * BOX_SIZE[0]), width=1)
    for x in range(len(objects)):
        for y in range(len(objects[0])):
            if objects[x][y] != None:
                objects[x][y].Draw(x,y)

def Update():
    updated = []
    objs = objects.copy()
    for x in range(len(objs)):
        for y in range(len(objs[0])):
            if objs[x][y] != None:
                if objects[x][y].dont_bother or objs[x][y] in updated:
                    continue
                updated.append(objs[x][y])
                objs[x][y].Update(x,y)

def MouseCoordinatesToGrid() -> tuple:
    mouse_pos = pygame.mouse.get_pos()
    grid_x = int(mouse_pos[0]/BOX_SIZE[0])
    grid_y = int(mouse_pos[1]/BOX_SIZE[1])
    return grid_x,grid_y

def loop():
    X = True
    while X:
        screen.fill(Color.BLACK)
        Draw()
        pygame.display.flip()



thread = Thread(target=loop,daemon=True)
thread.start()



def SpawnParticles():
    objects[50][60] = Fire()

while carryOn:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        if event.type == pygame.KEYUP:
            #Update()
            pass

    if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_q]:
        grid_x , grid_y = MouseCoordinatesToGrid()
        objects[grid_x][grid_y] = Sand()
    elif pygame.mouse.get_pressed()[2]:
        grid_x , grid_y = MouseCoordinatesToGrid()
        objects[grid_x][grid_y] = Fire()
    elif pygame.mouse.get_pressed()[0]:
        grid_x , grid_y = MouseCoordinatesToGrid()
        objects[grid_x][grid_y] = Water()

    #SpawnParticles()
    Update()

pygame.quit()