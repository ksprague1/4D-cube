from Tkinter import *
import time,string,math
root = Tk()
controls = {"w":[0,1],"s":[0,-1],"a":[1,1],"d":[1,-1],"t":[2,1],"g":[2,-1],
"f":[3,1],"h":[3,-1],"i":[4,1],"k":[4,-1],"j":[5,1],"l":[5,-1]}
presets = {"1":[0]*6,"2":[9, 17, 0, 0, 0, 0],"3":[45,45,45,45,45,45],
"4":[45,35,0,0,0,0]}
def key(event):
    global x,y,z,rotation
    if str(event.char) in controls:
        index =  controls[str(event.char)]
        rotation[index[0]] += index[1]
        print rotation
    if str(event.char) in presets:
        rotation = []+ presets[str(event.char)]
def callback(event):
    c.focus_set()
    print "clicked at", event.x, event.y
       #x,y,z,w
obj = [[1,1,1,1],[-1,1,1,1],[-1,-1,1,1],[1,-1,1,1],[1,1,-1,1],[-1,1,-1,1],
[-1,-1,-1,1],[1,-1,-1,1],[1,1,1,-1],[-1,1,1,-1],[-1,-1,1,-1],[1,-1,1,-1],
[1,1,-1,-1],[-1,1,-1,-1],[-1,-1,-1,-1],[1,-1,-1,-1,]]

rel = [(1,3,4,8),(0,2,5,9),(1,3,6,10),(0,2,7,11),(0,5,7,12),(1,4,6,13),
(2,5,7,14),(3,4,6,15),(0,9,11,12),(1,8,10,13),(2,9,11,14),(3,8,10,15),
(4,8,13,15),(5,9,12,14),(6,10,13,15),(7,11,12,14)]

pos = [0,0,6,6]

sheetpos = [100,100,200,10]
rotation = [0, 0, 0, 0, 0, 0]
#           xz yz xw yw xy zw
#           ws ad tg fh ik jl
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
c = Canvas(root, width=300, height=300)
c.bind("<Key>", key)
c.bind("<Button-1>", callback)
c.pack()
x,y,z = 1,1,1

while True:
    #time.sleep(.015)
    nobj =[]+ obj
    c.delete("tes")
    for idx in range(len(nobj)):
        nobj[idx] = rotate(nobj[idx][0],nobj[idx][1],nobj[idx][2],nobj[idx][3])
        nobj[idx] = move(nobj[idx])
        nobj[idx] = shadow(nobj[idx])
    for idx in range(len(nobj)):
        for x in rel[idx]:
            line = c.create_line(nobj[idx][0],nobj[idx][1],nobj[x][0],
            nobj[x][1],tag = "tes")
    c.update()

root.geometry('%sx%s+%s+%s' %(640, 480, 100, 100))
root.resizable(0, 0)
root.mainloop()




