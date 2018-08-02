import math

def maths(a,b):
    theta = 60
    newa = a*math.cos(math.radians(theta)) - b*math.sin(math.radians(theta))
    newb = a*math.sin(math.radians(theta)) + b*math.cos(math.radians(theta))
    return newa,newb
def rotate(x,y,z,w):
    #y,w = maths(y,w)
    #x,w = maths(x,w)
    #y,z = maths(y,z)
    #x,z = maths(x,z)
    #z,w = maths(z,w)
    #x,y = maths(x,y)
    return [x,y,z,w]

print rotate (0,1,0,0)
