from Tkinter import *
import time,string,math
root = Tk()

def key(event):
    global x,y,z,rotation
    #print "pressed", repr(event.char)
    if str(event.char) == "w":
        rotation[0] +=1
    if str(event.char) == "s":
        rotation[0] -=1
    if str(event.char) == "a":
        rotation[1] +=1
    if str(event.char) == "d":
        rotation[1] -=1
    if str(event.char) == "t":
        rotation[2] +=1
    if str(event.char) == "g":
        rotation[2] -=1
    if str(event.char) == "f":
        rotation[3] +=1
    if str(event.char) == "h":
        rotation[3] -=1
    if str(event.char) == "i":
        rotation[4] +=1
    if str(event.char) == "k":
        rotation[4] -=1
    if str(event.char) == "j":
        rotation[5] +=1
    if str(event.char) == "l":
        rotation[5] -=1

    
def callback(event):
    c.focus_set()
    print "clicked at", event.x, event.y
       #x,y,z,w
obj =   [[1,1,0,0],[-1,1,0,0],[-1,-1,0,0],[1,-1,0,0]]

rel = [(1,3),(),(1,3),()]

pos = [0,0,6,6]

sheetpos = [100,100,200,10]
rotation = [0, 0, 0, 0, 0, 0]
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
c = Canvas(root, width=300, height=300)
c.bind("<Key>", key)
c.bind("<Button-1>", callback)
c.pack()
x,y,z = 1,1,1

while True:
    time.sleep(.025)
    nobj =[]+ obj
    c.delete("tes")
    for idx in range(len(nobj)):
        nobj[idx] = rotate(nobj[idx][0],nobj[idx][1],nobj[idx][2],nobj[idx][3])
        #print nobj[idx]
        nobj[idx] = move(nobj[idx])
        #print nobj[idx] 
        nobj[idx] = shadow(nobj[idx])
        #print nobj[idx] , "\n _____________________"
    for idx in range(len(nobj)):
        for x in rel[idx]:
            if rel[idx] != ():
                line = c.create_line(nobj[idx][0],nobj[idx][1],nobj[x][0],
                nobj[x][1],tag = "tes")
    c.update()



root.geometry('%sx%s+%s+%s' %(640, 480, 100, 100))
root.resizable(0, 0)
root.mainloop()




