import phys
import pygame

WINDOW_SIZE=(800, 600)
FPS = 30

class Pool:
    '''The pool of interacting particles'''
    def __init__(self, size=(100, 100), ref=(50,50), par=[], interact=phys.Interaction() ):
        self.size = size
        self.ref = ref
        self.par = par
        self.interact = interact
        self.ratio = (WINDOW_SIZE[0] / self.size[0], \
                      WINDOW_SIZE[1] / self.size[1] )
        pygame.init()        
        self.screen = pygame.display.set_mode(WINDOW_SIZE)


    def getField(self, mark):
        options = {'size': self.size, 'ref': self.ref, 'par': self.par,\
                    'ratio': self.ratio, 'screen': self.screen}
        return options[mark]
    
    def setField(self, mark, value):
        if mark == 'size':
            self.size = value
        elif mark == 'ref':
            self.ref = value
        elif mark =='par':
            self.par = value
        else:
            print('error Pool.setField: wrong mark')

    def calcInteract(self):
        parts = self.getField('par')
        end = len(parts)
        for i in range(0, end):
            for k in range(i+1, end):
                self.interact.interact(parts[i], parts[k])

    def calcWallBounce(self):
        (refx, refy) = self.getField('ref')
        up, left = -refy, -refx
        (width, height) = self.getField('size')        
        down, right = height + up, width + left
        for bod in self.getField('par'):
            coordinate = bod.getField('coord')
            x, y = coordinate.getCoord('x'), coordinate.getCoord('y')
            veloc = bod.getField('vel')
            vx, vy = veloc.getCoord('x'), veloc.getCoord('y')
            r = bod.getField('r')
            if x + r > right:
                bod.setField('coord', phys.Point(right - r, y))
                bod.setField('vel', phys.Vector(-vx, vy))
            elif x - r < left:
                bod.setField('coord', phys.Point(left + r, y))
                bod.setField('vel', phys.Vector(-vx, vy))
            elif y + r > down:
                bod.setField('coord', phys.Point(x, down - r))
                bod.setField('vel', phys.Vector(vx, -vy))
            elif y - r < up :
                bod.setField('coord', phys.Point(x, up + r))
                bod.setField('vel', phys.Vector(vx, -vy))

            else:
                pass

    def updatePartCoord(self):
        for bod in self.getField('par'):
            bod.updateCoord()

    def drawAllPart(self):
        for bod in self.getField('par'):
            coord = bod.getField('coord')
            x, y = coord.getCoord('x'), coord.getCoord('y') 
            pygame.draw.circle(self.getField('screen'), (0,0,0,0) ,\
                ( int(self.ratio[0]*(x+self.ref[0])) , int(self.ratio[1]*(y+self.ref[1])) ), int(self.ratio[0]*bod.getField('r')) ) 

    def mainLoop(self):
        background = pygame.Surface(self.getField('screen').get_size())
        background = background.convert()
        
        work = True
        while work:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    work = False
            background.fill((250,250,250))
            self.getField('screen').blit(background, (0,0))
            self.drawAllPart()     
            pygame.display.flip()
            self.calcWallBounce()
            self.calcInteract()
            self.updatePartCoord()  
            pygame.time.wait(int(1000 * phys.SIM_STEP))
        pygame.quit()

#            A = phys.Body(phys.Point(100,0), phys.Vector(-24,10), 5, 10)
#    B = phys.Body(phys.Point(0,0), phys.Vector(2,-1), 5, 10)

#pool = pool.Pool((400,300),(200,150),[A,B])

