import phys, pool

def  body(coord, vel, rad, m):
    (x, y) = coord
    (velx, vely) = vel
    return phys.Body(phys.Point(x,y), phys.Vector(velx, vely), rad, m)

def interaction(interType):
    return phys.Interaction(interType)

def apool(size, ref, par, borders):
    return pool.Pool(size, ref, par, phys.Interaction('grav'), borders)

def gravtest():
    A = body((-200, 200), (35, 35 ), 10, 100)
    B = body((0,0), (3,-3), 20, 500)   
    C = body((-250, 250), (13, 13), 5, 10)
    D = body((130,0),(0,40), 8, 45)
    pool = apool((1000,750), (200, 150), [A,B,C,D], False)
    pool.mainLoop()

def collistest():
    A = body((0,0), (-125, -100), 20,100)
    #A = body((0,80), (25, -10), 20,100)
    B = body((-140,-140), (25, 25), 20,100)
    #B = body((0,0), (25, 10), 20,100)
    D = body((100,0),(30,-40), 8, 40)
    C = body((-130,180),(70,40), 10, 50)
    P = apool((800,600), (400,400), [A,B,C,D], True)
    P.mainLoop()

if __name__ == "__main__":
    gravtest() 
