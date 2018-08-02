         #x,y,z,w
unused = '''
obj = {1:[1,1,1,1,(2,4,5,9)],2:[-1,1,1,1,(1,3,6,10)],3:[-1,-1,1,1,(2,4,7,11)],
4:[1,-1,1,1,(1,3,8,12)],5:[1,1,-1,1,(1,6,8,13)],6:[-1,1,-1,1,(2,5,7,14)],
7:[-1,-1,-1,1,(3,6,8,15)],8:[1,-1,-1,1,(4,5,7,16)],9:[1,1,1,-1,(1,10,12,13)],
10:[-1,1,1,-1,(2,9,11,14)],11:[-1,-1,1,-1,(3,10,12,15)],
12:[1,-1,1,-1,(4,9,11,16)],13:[1,1,-1,-1,(5,9,14,16)],
14:[-1,1,-1,-1,(6,9,13,15)],15:[-1,-1,-1,-1,(7,11,14,16)],
16:[1,-1,-1,-1,(8,12,13,15)]}

obj = [[1,1,1,1,(1,3,4,8)],[-1,1,1,1,(0,2,5,9)],[-1,-1,1,1,(1,3,6,10)],
[1,-1,1,1,(0,2,7,11)],[1,1,-1,1,(0,5,7,12)],[-1,1,-1,1,(1,4,6,13)],
[-1,-1,-1,1,(2,5,7,14)],[1,-1,-1,1,(3,4,6,15)],[1,1,1,-1,(0,9,11,12)],
[-1,1,1,-1,(1,8,10,13)],[-1,-1,1,-1,(2,9,11,14)],[1,-1,1,-1,(3,8,10,15)],
[1,1,-1,-1,(4,8,13,15)],[-1,1,-1,-1,(5,8,12,14)],[-1,-1,-1,-1,(6,10,13,15)],
[1,-1,-1,-1,(7,11,12,14)]]'''
from Tkinter import *
import math
root = Tk()
c = Canvas(root, width=300, height=300)
c.pack()
       #x,y,z,w
obj = [[1,1,1,1],[-1,1,1,1],[-1,-1,1,1],[1,-1,1,1],[1,1,-1,1],[-1,1,-1,1],
[-1,-1,-1,1],[1,-1,-1,1],[1,1,1,-1],[-1,1,1,-1],[-1,-1,1,-1],[1,-1,1,-1],
[1,1,-1,-1],[-1,1,-1,-1],[-1,-1,-1,-1],[1,-1,-1,-1,]]

rel = [(1,3,4,8),(0,2,5,9),(1,3,6,10),(0,2,7,11),(0,5,7,12),(1,4,6,13),
(2,5,7,14),(3,4,6,15),(0,9,11,12),(1,8,10,13),(2,9,11,14),(3,8,10,15),
(4,8,13,15),(5,8,12,14),(6,10,13,15),(7,11,12,14)]

pos = [0,0,6,6]

sheetpos = [100,100,200,10]
rotation = [0, 45, 0, 0, 0, 0]
#           xz yz xw yw xy zw

def maths(a,b, theta):
    newa = a*math.cos(math.radians(theta)) - b*math.sin(math.radians(theta))
    newb = a*math.sin(math.radians(theta)) + b*math.cos(math.radians(theta))
    return newa,newb
def rotate(x,y,z,w):
    y,w = maths(y,w,rotation[0])
    x,w = maths(x,w,rotation[1])
    y,z = maths(y,z,rotation[2])
    x,z = maths(x,z,rotation[3])
    z,w = maths(z,w,rotation[4])
    x,y = maths(x,y,rotation[5])
    return [x,y,z,w]
def move(item):
    return [item[0]+pos[0],item[1]+pos[1],item[2]+pos[2],item[3]+pos[3]]
def shadow(item):
    #x = item[0]*(sheetpos[2]/((sheetpos[3]/item[3])*item[2]))
    #y = item[1]*(sheetpos[2]/((sheetpos[3]/item[3])*item[2]))
    x = item[0]*(sheetpos[2]/item[2]) + sheetpos[0]
    y = item[1]*(sheetpos[2]/item[2]) + sheetpos[1]
    return [x,y]
nobj = obj
for idx in range(len(nobj)):
    nobj[idx] = rotate(nobj[idx][0],nobj[idx][1],nobj[idx][2],nobj[idx][3])
    print nobj[idx]
    nobj[idx] = move(nobj[idx])
    print nobj[idx] 
    nobj[idx] = shadow(nobj[idx])
    print nobj[idx] , "\n _____________________"
thing = c.create_line(1,1,10,10,tag = "ner")
for idx in range(len(nobj)):
    for x in rel[idx]:
        line = c.create_line(nobj[idx][0],nobj[idx][0],nobj[x][0],nobj[x][1],tag="hi")
c.delete("ner")

root.mainloop()
