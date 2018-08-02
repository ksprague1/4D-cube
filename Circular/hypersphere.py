from Tkinter import *
from operator import itemgetter
import time,string,math
import ctypes
u = ctypes.windll.user32
root = Tk()

controls = {"w":[0,1],"s":[0,-1],"a":[1,1],"d":[1,-1],"t":[2,1],"g":[2,-1],
"f":[3,1],"h":[3,-1],"i":[4,1],"k":[4,-1],"j":[5,1],"l":[5,-1]}
presets = {"1":[0]*6,"2":[9, 17, 0, 0, 0, 0],"3":[45,45,45,45,45,45],
"4":[45,35,0,0,0,0],"5":[3,90,103,10,45,0]}
speedset = {"=":[1,1],"-":[-1,1],"+":[0.1,1],"_":[-0.1,1],"0":[0,0]}
Dctn = {"Left":[2,0.1,0,0],"Right":[2,-0.1,0,0],"Up":[0,0,2,25],
"Down":[0,0,2,-25],"comma":[0,0,3,-0.1],"period":[0,0,3,0.1]}
contr = [40.2, 1.6]
contrastop = {"'":[0.1,0],";": [-0.1,0],'"':[0,0.1],":":[0,-0.1]}
pressed = {}
speed = 1
obj = []
#x + y + z + w = sph
sph = 16.0
#index = 3.5
num = 8
index = sph**0.5*2/((num)/4.0 - 0.99)
TOL = 0.000001
def sorting(x,y,z,w,N):
    idxng = "0"*(3-len(str(int((w+N)*10))))+str(int((w+N)*10))
    idxng += "0"*(3-len(str(int((z+N)*10))))+str(int((z+N)*10))
    idxng += "0"*(3-len(str(int((y+N)*10))))+str(int((y+N)*10))
    idxng += "0"*(3-len(str(int((x+N)*10))))+str(int((x+N)*10))
    idxng = -int(idxng)
    return [[x,y,z,w,idxng]]
for s4 in range(int(sph**0.5*2/index + 2)):
    num4 = sph**0.5*math.sin(math.radians(360.0/int(sph**0.5*2/index + 1)*s4/4))
    if s4 == int(sph**0.5*2/index + 2)-1:
        num4 = (sph)**0.5
    down4 = num4 ** 2
    for s3 in range(int(sph**0.5*2/index + 2)):
        num3 = (sph- down4)**0.5*math.sin(math.radians(360.0/int((sph)
        **0.5*2/index + 1)*s3/4))
        if s3 == int(sph**0.5*2/index + 2)-1:
            num3 = (sph-down4)**0.5
        elif s4 == int(sph**0.5*2/index + 2)-1:
            print "GOT EM"
            continue
        down3 = num4 ** 2+num3 ** 2
        for s2 in range(int(sph**0.5*2/index + 2)):
            num2 = (sph- down3)**0.5*math.sin(math.radians(360.0/int((sph)
            **0.5*2/index + 1)*s2/4))
            if s2 == int(sph**0.5*2/index + 2)-1:
                num2 = (sph-down3)**0.5
            elif s3 == int(sph**0.5*2/index + 2)-1:
                print "GOT EM"
                continue
            down2 = num4 ** 2+num3 ** 2+ num2 **2
            s1 = (sph- down2)**0.5
            print s1,"|",num3,"|",num4,"|"
            N = sph ** 0.5
            obj += sorting(s1,num2,num3,num4,N)
            if s1 > TOL:
                obj += sorting(-s1,num2,num3,num4,N)
            if num2 > TOL:
                obj += sorting(s1,-num2,num3,num4,N)
            if num3 > TOL:
                obj += sorting(s1,num2,-num3,num4,N)
            if num4 > TOL:
                obj += sorting(s1,num2,num3,-num4,N)
            if s1 > TOL and num2 > TOL:
                obj += sorting(-s1,-num2,num3,num4,N)
            if s1 > TOL and num3 > TOL:
                obj += sorting(-s1,num2,-num3,num4,N)
            if num3 > TOL and num2 > TOL:
                obj += sorting(s1,-num2,-num3,num4,N)
            if s1 > TOL and num2 > TOL and num3 > TOL:
                obj += sorting(-s1,-num2,-num3,num4,N)
            if s1 > TOL and num4 > TOL:
                obj += sorting(-s1,num2,num3,-num4,N)
            if num2 > TOL and num4 > TOL:
                obj += sorting(s1,-num2,num3,-num4,N)
            if num3 > TOL and num4 > TOL:
                obj += sorting(s1,num2,-num3,-num4,N)
            if s1 > TOL and num2 > TOL and num4 > TOL:
                obj += sorting(-s1,-num2,num3,-num4,N)
            if s1 > TOL and num3 > TOL and num4 > TOL:
                obj += sorting(-s1,num2,-num3,-num4,N)
            if num3 > TOL and num2 > TOL and num4 > TOL:
                obj += sorting(s1,-num2,-num3,-num4,N)
            if s1 > TOL and num2 > TOL and num3 > TOL and num4 > TOL:
                obj += sorting(-s1,-num2,-num3,-num4,N)
print obj[0]
obj = sorted(obj, key=itemgetter(4))
print
for x in range(len(obj)):
    #print obj[x],"|",x
    del obj[x][4]

axs = num*(num/2-1)+2
rel = [[w+1 for w in range (axs)]]
for w in range(num/2-2):
    rel += [[x+2+(w)*axs for x in range (num)]+[x+1+(w+1)*axs]]
    for x in range(num / 2 - 2):
        rel += [[3+(x)*num+w*axs,4+(x)*num+w*axs,2+(x+1)*num+w*axs,
        1+x*num+(w+1)*axs]]
        for y in range(num-3):
            rel += [[y+5+(x)*num+w*axs,y+3+(x+1)*num+w*axs,y+2+x*num+(w+1)*axs]]
        rel += [[num+(x+1)*num+w*axs,num+x*num+(w+1)*axs]]
        rel +=[[(x+1)*num+w*axs,num+1+w*axs+(x+1)*num,num+1+x*num+(w+1)*axs]]
    x = num / 2 - 2
     
    rel += [[3+(x)*num+w*axs,4+(x)*num+w*axs,1+x*num+(w+1)*axs]]
    for y in range(num-3):
        rel += [[y+5+(x)*num+w*axs,y+2+x*num+(w+1)*axs]]
    rel += [[(x+1)*num+1+w*axs,1+x*num+(w+1)*axs]]
    rel +=[[num*(num/2-1)+2+w*axs,2+x*num+(w+1)*axs]]    
    rel += [[x+num*(num/2-2)+2+w*axs for x in range (num-1)]+
            [x+num*(num/2-2)+1+w*axs]]
#------------------------------------------------------------
w = num/2-2
rel += [[x+2+(w)*axs for x in range (num)]]
for x in range(num / 2 - 2):
    rel += [[3+(x)*num+w*axs,4+(x)*num+w*axs,2+(x+1)*num+w*axs]]
    for y in range(num-3):
        rel += [[y+5+(x)*num+w*axs,y+3+(x+1)*num+w*axs]]
    rel += [[num+(x+1)*num+w*axs]]
    rel +=[[(x+1)*num+w*axs,num+1+w*axs+(x+1)*num]]
x = num / 2 - 2
     
rel += [[3+(x)*num+w*axs,4+(x)*num+w*axs]]
for y in range(num-3):
    rel += [[y+5+(x)*num+w*axs]]
rel += [[(x+1)*num+1+w*axs]]
rel +=[[num*(num/2-1)+2+w*axs]]    
rel += [[x+num*(num/2-2)+2+w*axs for x in range (num-1)]]
rel += [[w+axs*(num/2-2)+2+1 for w in range (axs-1)]]

print len(rel)
print obj
print len(obj)
print rel
#print obj[0]'''
pos = [0,0,30,6]
sheetpos = [500,400,800,8]
rotation = [0, 0, 0, 0, 0, 0]
#           xz yz xw yw xy zw
#           ws ad tg fh ik jl

def keypress(event):
    global rotation,speed
    pressed[str(event.char)] = str(event.char)
    if event.keysym in Dctn:
        pos[Dctn[event.keysym][0]] += Dctn[event.keysym][1]
        sheetpos[Dctn[event.keysym][2]] += Dctn[event.keysym][3]
        c.configure(background='dodger blue')
        print sheetpos
        print pos
    if event.char in contrastop:
        contr[0] += contrastop[event.char][0]
        contr[1] += contrastop[event.char][1]
        print contr
    
def keyrelease(event):
    del pressed[str(event.char)]
    
def handleroat():
    global rotation,speed
    for Hash in pressed:
        if Hash in controls:
            index =  controls[Hash]
            rotation[index[0]] += index[1]*speed
        if Hash in presets:
            rotation = []+ presets[Hash]
        if Hash in speedset:
            speed += speedset[Hash][0]
            speed *= speedset[Hash][1]
    for rot in range(len(rotation)):
        rotation[rot] = rotation[rot] % 360
    c.delete("text")
    c.create_text(0, 15, text=str(rotation),tag = "text",anchor=SW)
    
def callback(event):
    c.focus_set()
    #print "clicked at", event.x, event.y
    
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
    #z = item[2]*(sheetpos[3]/item[3])
    if var2.get():
        #item[2] = z
        item[0] = item[0]*(sheetpos[3]/item[3])
        item[1] = item[1]*(sheetpos[3]/item[3])
    x = item[0]*(sheetpos[2]/item[2]) + sheetpos[0]
    y = item[1]*(sheetpos[2]/item[2]) + sheetpos[1]
    ce = var.get()
    idxng = [str(int(item[3]*100 + 0.5)),str(int(item[2]*100 + 0.5))]
    idxng = -int(idxng[ce]+"0"*(4-len(idxng[ce]))+
    idxng[(ce+1)%2]+"0"*(4-len(idxng[(ce+1)%2])))
    return [x,y,item[2],idxng]

c = Canvas(root, width=u.GetSystemMetrics(0), height=u.GetSystemMetrics(1)-80)
c.bind("<KeyPress>", keypress)
c.bind("<KeyRelease>", keyrelease)
c.bind("<Button-1>", callback)
c.create_text(0, 15, text=str(rotation),tag = "text",anchor=SW)
c.pack()
var,var2,v = IntVar(),BooleanVar(),IntVar()
#for txt in range(len(options)):
    #Radiobutton(root,text=options[txt],variable=v,value=txt,
    #command=change).pack(side='left')
Checkbutton(root, text="Preference 3D", variable=var).pack()
Checkbutton(root, text="Distort with 4D", variable=var2).pack()
while True:
    time.sleep(.010)
    handleroat()
    tobe = []
    nobj =[]+ obj
    c.delete("tes")
    for idx in range(len(nobj)):
        nobj[idx] = rotate(nobj[idx][0],nobj[idx][1],nobj[idx][2],nobj[idx][3])
        nobj[idx] = move(nobj[idx])
        nobj[idx] = shadow(nobj[idx])
    for idx in range(len(nobj)):

        num = (-nobj[idx][2]+contr[0])/contr[1]
        tobe +=[[num,nobj[idx][0],nobj[idx][1],
        (nobj[idx][3])]]
    #x,y,x2,y2 = tobe[0][1],tobe[0][2],tobe[2][1],tobe[2][2]
    #tobe = sorted(tobe, key=itemgetter(3))
    for tob in range(len(tobe)):
        #print tob
        if 100-int(tobe[tob][0]*10) >99 or 100-int(tobe[tob][0]*10)<1:
            pos = [0,0,30,6]
            sheetpos = [500,400,800,8]
            #print "ner"
            break
        #line = c.create_line(tob[1],tob[2],tob[1]-16,
            #tob[2]-16,tag="tes",width=16,
            #fill = "gray"+ str(int(tob[0]*10)))
        line = c.create_text(tobe[tob][1],tobe[tob][2],text = str(tob),
        tag="tes",fill = "gray"+ str(int(tobe[tob][0]*10)))
        if "m" in pressed:
            print tob[1],tob[2],tob[3],tob[4]
    #line = c.create_line(x2,y2,x2-16,y2-16,tag="tes",width=16,fill = "red")
    #line2 = c.create_line(x,y,x-16,y-16,tag="tes",width=16,fill = "blue")
    c.update()

root.geometry('%sx%s+%s+%s' %(1024, 768, 100, 100))
root.resizable(0, 0)
root.mainloop()




