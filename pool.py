import phys
import pygame

WINDOW_SIZE=(800, 600)
FPS = 30

class Pool:
    '''The pool of interacting particles'''
    def __init__(self, size=(100, 100), ref=(50,50), par=[]):
        self.size = size
        self.ref = ref
        self.par = par

        self.ratio = (WINDOW_SIZE[0] / self.getField('size')[0], \
                      WINDOW_SIZE[1] / self.getField('size')[1] )

    def getField(self, mark):
        options = {'size': self.size, 'ref': self.ref, 'par': self.par}
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
                parts[i].interact(parts[k])

    def calcWallBounce(self):
        (up, left) = self.getField('ref')
        (width, height) = self.getField('size')        
        down, right = height - up, width - left
        for bod in self.getField('par'):
            coordinate = bod.getField('coord')
            x, y = coordinate.getCoord('x'), coordinate.getCoord('y')
            veloc = bod.getField('vel')
            vx, vy = veloc.getCoord('x'), veloc.getCoord('y')

            if x < up:
                bod.setField('coord', phys.Point(up, y)
                bod.setField('vel', phys.Vector(vx, -vy))
            elif x > down:
                bod.setField('coord', phys.Point(down, y))
                bod.setField('vel', phys.Vector(vx, -vy))
            elif y < left:
                bod.setField('coord', phys.Point(x, left))
                bod.setField('vel', phys.Vector(-vx, vy))
            elif y > right:
                bod.setField('coord', phys.Point(x, right))
                bod.setField('vel', phys.Vector(-vx, vy))

            else:
                pass
    def updatePartCoord(self):
        for bod in self.getField('par'):
            bod.updateCoord()

    
            
        
            
