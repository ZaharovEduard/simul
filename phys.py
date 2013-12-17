import operator
import math

INTERACT_DISTANCE = 10000
SIM_STEP = 0.01
class Point:
    """ 2-D point. coordinates x and y. Point(3, 5.5) """
    def __init__(self, x=0, y=0):
        if isinstance(x, (int,float)) and isinstance(y, (int,float)):        
            self.x = x
            self.y = y
        else:
            print("error. Coordinates are not int or float \n")

    def getCoord(self, mark):
        '''Get coordinate 'x' or 'y': getCoord('x')'''
        if mark == 'x':
            return self.x
        elif mark == 'y':
            return self.y
        else: 
            print("error. getCoord:  wrong mark \n")
    
    def setCoord(self, mark, value):
        '''Set coordinate 'x' or 'y' by the 'value': setCoord('x', 3) '''
        if mark == 'x':
            self.x = value
        elif mark == 'y':
            self.y = value
        else: 
            print("error. Point.setCoord: wrong mark \n")

    def dist(self, point):
        return math.sqrt( (self.getCoord('x') - point.getCoord('x'))**2 + \
                          (self.getCoord('y') - point.getCoord('y'))**2 )

class Vector:
    '''Representing vector using coordinates x and y. Vector(3,4)'''
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def getCoord(self, mark):
        '''Get coordinate 'x' or 'y': getCoord('x')'''
        if mark == 'x':
            return self.x
        elif mark == 'y':
            return self.y
        else: 
            print("error. Vector.getCoord:  wrong mark \n")
    
    def setCoord(self, mark, value):
        '''Set coordinate 'x' or 'y' by the 'value': setCoord('x', 3) '''
        if mark == 'x':
            self.x = value
        elif mark == 'y':
            self.y = value
        else: 
            print("error. Vector.setCoord: wrong mark \n")

    def __add__(self, vec):
        '''operator +'''
        if isinstance(vec , self.__class__):
            return Vector(self.getCoord('x') + vec.getCoord('x'), \
                          self.getCoord('y') + vec.getCoord('y'))
        else:  
            print('error. Operator "+". operand is not vector \n')

    def __abs__(self):
        '''operator || (abs)'''
        return math.sqrt( self.getCoord('x')**2 + self.getCoord('y')**2 )

    def __mul__(self, oper):
        '''operator *.  issue here!!! (Vec * num) is ok. (num * Vec) is not'''
        if isinstance(oper, self.__class__):
            return self.getCoord('x') * oper.getCoord('x') + \
                   self.getCoord('y') * oper.getCoord('y')
        elif isinstance(oper, (int, float)):
            return Vector(oper * self.getCoord('x'), \
                          oper * self.getCoord('y'))        
        else:    
            print("error. operand of multiplication is not vector or real number\n")
    
    def __neg__(self):
       '''operator -. -vec'''
       return Vector( - self.getCoord('x'), - self.getCoord('y'))

    def __sub__(self, vec):
        if isinstance(vec , self.__class__):
            return self + (-vec)
    def normalize(self):
        a = self.getCoord('x')
        b = self.getCoord('y')        
        return Vector(a / abs(self) , b / abs(self) )
    
class Body:
    def __init__(self, coord=Point(), vel=Vector(), r=1, m=1, \
                 inter='molec' ):
        self.coord = coord # coord is Point
        self.vel = vel # vel is Vector
        self.r = r
        self.m = m
        self.mom = vel * m
        self.ener = vel * vel * m / 2
        self.inter = inter
    def getField(self, mark):
        options = {'coord': self.coord, 'vel': self.vel, 'r': self.r, 'm': self.m,\
                    'mom': self.mom, 'ener': self.ener, 'inter': self.inter}
        return options[mark]

    def setField(self, mark, value):
        if isinstance(mark, str): 
            if mark == 'coord':
                self.coord = value
            elif mark == 'vel':
                self.vel = value
            elif mark == 'r':
                self.r = value
            elif mark == 'm':
                self.m = value
            elif mark == 'inter':
                self.force = value
            else:
                print("error setMatpointCharac is not valid string \n")
        else:
            print("error setMatpointCharac mark is not string \n")

    def updateCoord(self):
        dx = self.getField('vel').getCoord('x') * SIM_STEP
        dy = self.getField('vel').getCoord('y') * SIM_STEP
        pos = self.getField('coord')
        self.setField('coord', Point( dx + pos.getCoord('x'), dy + pos.getCoord('y')))

class Interaction:
    def __init__(self, interType='dummy'):
        self.interType = interType

    def interact(self, ob1, ob2):
        if self.isIntersec(ob1, ob2):
            self.collide(ob1, ob2)
        elif self.isInteract(ob1, ob2):
            self.influence(ob1, ob2)
        else:
            pass
    
    def isIntersec(self, ob1, ob2):
        if ob1.getField('coord').dist(ob2.getField('coord')) < \
           ob1.getField('r') + ob2.getField('r'):
            return True
        else: 
            return False
            
    def collide(self, ob1, ob2):
        '''dummy realisation'''    
        ob1.setField('vel', -ob1.getField('vel'))
        ob2.setField('vel', -ob2.getField('vel')) 
        

    def isInteract(self, ob1, ob2):
        if ob1.getField('coord').dist(ob2.getField('coord')) < INTERACT_DISTANCE : 
            return True
        else: 
            return False

    def force(self, ob1, ob2):
        r = ob1.getField('coord').dist(ob2.getField('coord'))
        REP_DIST = 100  
        DUMMY_FORCE = 100
        if self.interType == 'dummy':
            if r < REP_DIST:
                return -DUMMY_FORCE 
            else:
                return DUMMY_FORCE
                

    def influence(self, ob1, ob2):                    
        a = ob1.getField('coord')
        b = ob2.getField('coord')
        ax = a.getCoord('x')
        ay = a.getCoord('y')
        bx = b.getCoord('x')
        by = b.getCoord('y')
        f = self.force(ob1, ob2)
        direct_vec = Vector(bx - ax, by - ay).normalize()
        a_dv = direct_vec * ((SIM_STEP * f ) / ob1.getField('m'))
        b_dv = (- direct_vec ) * ((SIM_STEP * f) / ob2.getField('m'))
        ob1.setField('vel', ob1.getField('vel') + a_dv)
        ob2.setField('vel', ob2.getField('vel') + b_dv)
