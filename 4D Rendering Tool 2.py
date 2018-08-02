def get_options():
    global options,filename
    filename = "Objects.txt"
    options = open(filename, 'r').readline()[:-1].split("|")   

def change():
    global obj,rel,SphereCurrently
    tag = options[v.get()]
    SphereCurrently = False
    if tag == "Sphere Builder":
        SphereGUI("null")
        return
    fil = open(filename, 'r')
    line=0
    for ln in fil:
        if ln[:-1] == tag:
            line=1
        elif line == 1:
            obj = ln[:-1].split("|")
            for x in range(len(obj)):
                obj[x]= map(float,obj[x].split(","))
            line=2
        elif line ==2 :
            rel = ln[:-1].split("|")
            if rel != [""]:
                for x in range(len(rel)):
                    rel[x]= map(int,rel[x].split(","))
            break
    fil.close()
    
def keypress(event):
    global rotation,speed
    pressed[str(event.char)] = str(event.char)
    if GUI:
        SphereGUI(event.keysym)
        return
    if event.keysym in Dctn:
        pos[Dctn[event.keysym][0]] += Dctn[event.keysym][1]
        sheetpos[Dctn[event.keysym][2]] += Dctn[event.keysym][3]
        c.configure(background='dodger blue')
    if event.char in contrastop:
        contr[0] += contrastop[event.char][0]
        contr[1] += contrastop[event.char][1]
    if event.char in speedset:
        speed += speedset[event.char][0]
        speed *= speedset[event.char][1]
    
def keyrelease(event):
    if str(event.char) in pressed:
        del pressed[str(event.char)]
    
def handleroat():
    global rotation,speed
    for Hash in pressed:
        if Hash in controls:
            index =  controls[Hash]
            rotation[index[0]] += index[1]*speed
        if Hash in presets:
            rotation = []+ presets[Hash]
    for rot in range(len(rotation)):
        rotation[rot] = rotation[rot] % 360
    c.delete("text")
    c.create_text(0, 15, text=str(rotation),tag = "text",anchor=SW)
    
def callback(event):
    c.focus_set()
    print "clicked at", event.x, event.y
    
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
    #idxng = [str(int(item[3]*100 + 0.5)),str(int(item[2]*100 + 0.5))]
    #idxng = -int("0"*(4-len(idxng[ce]))+idxng[ce]+
    #"0"*(4-len(idxng[(ce+1)%2]))+idxng[(ce+1)%2])
    idxng = -(item[0]**2+item[1]**2+item[2]**2+(item[3]**2)*(ce+1%2))**0.5
    return [x,y,item[2],idxng]
def line_rend():
    global pos,sheetpos
    tobe = []
    for idx in range(len(nobj)):
        for x in rel[idx]:
            num = (-nobj[idx][2]- nobj[x][2]+contr[0]/2)/contr[1]
            tobe +=[[num,nobj[idx][0],nobj[idx][1],nobj[x][0],nobj[x][1],
            (nobj[idx][3]+nobj[x][3])/2]]      
    tobe = sorted(tobe, key=itemgetter(5))
    for tob in tobe:
        if 100-int(tob[0]*10) >99:
            tob[0] = 1
            c.create_text(0,25,text="NO MORE CONTRAST",tag="tes",
            fill = "red",anchor=SW)
        elif 100-int(tob[0]*10)<1:
            tob[0] = 9
            c.create_text(0,25,text="NO MORE CONTRAST",tag="tes",
            fill = "red",anchor=SW)
        line = c.create_line(tob[1],tob[2],tob[3],
            tob[4],tag="tes",width=tob[0],
            fill = "gray"+ str(100-int(tob[0]*10)))
    if var3.get():
        tobe = []
        for idx in range(len(nobj)):
            num = (-nobj[idx][2]+contr[0])/contr[1]
            tobe +=[[num,nobj[idx][0],nobj[idx][1],
            (nobj[idx][3])]]
        #tobe = sorted(tobe, key=itemgetter(3))
        for tob in range(len(tobe)):
            dot=c.create_text(tobe[tob][1],tobe[tob][2],text=str(tob),
            tag="tes")#,fill = "red",font = ('Times', 20, 'bold'))
def dot_rend():
    global pos,sheetpos
    tobe = []
    for idx in range(len(nobj)):
        num = (-nobj[idx][2]+contr[0])/contr[1]
        tobe +=[[num,nobj[idx][0],nobj[idx][1],
        (nobj[idx][3])]]
    if not var3.get():
        tobe = sorted(tobe, key=itemgetter(3))
    for tob in range(len(tobe)):
        if 100-int(tobe[tob][0]*10) >99:
            tobe[tob][0] = 9
            c.create_text(0,25,text="NO MORE CONTRAST",tag="tes",
            fill = "red",anchor=SW)
        elif 100-int(tobe[tob][0]*10)<1:
            tobe[tob][0] = 1
            c.create_text(0,25,text="NO MORE CONTRAST",tag="tes",
            fill = "red",anchor=SW)
        if var3.get():
            dot=c.create_text(tobe[tob][1],tobe[tob][2],text=str(tob),tag="tes",
            fill = "gray"+ str(int(tobe[tob][0]*10)))
        else:
            dot = c.create_oval(tobe[tob][1],tobe[tob][2],tobe[tob][1]-24,
            tobe[tob][2]-24,tag="tes",width=0,
            fill = "gray"+ str(int(tobe[tob][0]*10)))
#---------------------------------------------------------------------------
def sorting(x,y,z,w,N):
    idxng = "0"*(6-len(str(int((w+N)*10000))))+str(int((w+N)*10000))
    idxng += "0"*(6-len(str(int((z+N)*10000))))+str(int((z+N)*10000))
    idxng += "0"*(6-len(str(int((y+N)*10000))))+str(int((y+N)*10000))
    idxng += "0"*(6-len(str(int((x+N)*10000))))+str(int((x+N)*10000))
    idxng = -int(idxng)
    return [[x,y,z,w,idxng]]
def linesphere(D,sph,index,Type):
    global obj,rel,TOL
    obj = []
    rad4 = sph**0.5*2/index
    for s4 in range(int(rad4 + 2)):
        num4 = sph**0.5*math.sin(math.radians(360.0/int(rad4+1)*s4/4))
        if s4 == int(rad4+ 1):
            num4 = (sph)**0.5
            if D < 4:
                num4 = 0
        elif D < 4:
            continue
        down4 = num4 ** 2
        rad3 = rad4
        if not Type:
            print "KKKK"
            rad3 = (sph-down4)**0.5*2/index
        for s3 in range(int(rad3 + 2)):
            num3 = (sph- down4)**0.5*math.sin(math.radians(360.0/int
            (rad3+1)*s3/4))
            if s3 == int(rad3 + 1):
                num3 = (sph-down4)**0.5
                if D < 3:
                    num3 = 0
            elif (s4 == int(rad4 + 1) and D>3) or D < 3:
                #print "GOT EM1"
                continue
            down3 = num4 ** 2+num3 ** 2
            rad2 = rad4
            if not Type:
                rad2 = (sph-down3)**0.5*2/index
            for s2 in range(int(rad2+ 2)):
                num2 = (sph- down3)**0.5*math.sin(math.radians(360.0/int(
                rad2+ 1)*s2/4))
                if s2 == int(rad2+ 1):
                    num2 = (sph-down3)**0.5
                elif s3 == int(rad3 + 1) and D>2:
                    #print "GOT EM2"
                    continue
                down2 = num4 ** 2+num3 ** 2+ num2 **2
                s1 = abs(sph- down2)**0.5
                #print s1,"|",num3,"|",num4,"|"
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
    #print obj[0]
    obj = sorted(obj, key=itemgetter(4))
    #print
    for x in range(len(obj)):
        #print obj[x],"|",x
        del obj[x][4]
    if Type:
        rel = []
        if D == 2:
            circle(0,0)
        elif D==3:
            sphere(0)
        elif D==4:
            hypersphere()
# x*num is the index for the ring it's on and w*axs is the index for the sphere.
#(x+1) or (w+1) means I'm adressing the ring or sphere ahead.
#indexing from a sphere is displaced by 1 to account for the first point on the
# Hypersphere.
def hypersphere():
    global rel,num
    axs = num*(num/2-1)+2
    rel = [[w+1 for w in range (axs)]]
    #first point on hypersphere to each point on the first sphere
    for w in range(num/2-2):
        #for all spheres except the last
        rel += [[x+2+(w)*axs for x in range (num)]+[1+(w+1)*axs]]
        #First point on current sphere to the first ring of the sphere and
        #It's corresponding point on the next sphere
        for x in range(num / 2 - 2):
            #for each ring in the current sphere except the last
            rel += [[3+(x)*num+w*axs,4+(x)*num+w*axs,2+(x+1)*num+w*axs,
            2+x*num+(w+1)*axs]]
            #first point in the ring to the 2nd,3rd and
            #its corresponding point on the ring above and
            #It's corresponding point on the next sphere
            for y in range(num-3):
                rel += [[y+5+(x)*num+w*axs,y+3+(x+1)*num+w*axs,y+3+x*num+(w+1)*axs]]
                #2nd point to 3rd last point connected to 2 ahead and
                #its corresponding point on the ring above and
                #It's corresponding point on the next sphere
            rel += [[num+(x+1)*num+w*axs,num+x*num+(w+1)*axs]]
            #2nd last point in ring to its corresponding point on the ring above and
            #it's corresponding point on the next sphere
            rel +=[[(x+1)*num+w*axs,num+1+w*axs+(x+1)*num,num+1+x*num+(w+1)*axs]]
            #last point in ring to the second last point and
            #its corresponding point on the ring above
            #it's corresponding point on the next sphere
        x = num / 2 - 2
        #LAST RING 
        rel += [[3+(x)*num+w*axs,4+(x)*num+w*axs,2+x*num+(w+1)*axs]]
        #first point in the ring to the 2nd,3rd and
        #it's corresponding point on the next sphere
        for y in range(num-3):
            rel += [[y+5+(x)*num+w*axs,y+3+x*num+(w+1)*axs]]
            #2nd point to 3rd last point in ring connected to the point 2 ahead and
            #it's corresponding point on the next sphere
        rel += [[(x+1)*num+1+w*axs,num+x*num+(w+1)*axs]]
        #2nd last point in ring to last point in ring and
        #it's corresponding point on the next sphere
        rel +=[[num*(num/2-1)+2+w*axs,num+1+x*num+(w+1)*axs]]
        #last point in 2nd last ring to the one point in the ring above and
        #it's corresponding point on the next sphere
        rel += [[x+num*(num/2-2)+2+w*axs for x in range (num-1)]+
            [2+num*(num/2-1)+(w+1)*axs]]
        #last ring (now a single point) to all the points on the second last ring
        #and it's corresponding point on the next sphere
    #LAST SPHERE
    w = num/2-2
    sphere(w*axs + 1)
    rel += [[w+axs*(num/2-2)+1 for w in range (axs)]]
    #Last point to last sphere
def sphere(add):
    global rel,num
    rel += [[x+1+add for x in range (num)]]
    #point at the top to the first ring of points
    for x in range(num / 2 - 2):
    #for all rings except the last
        rel += [[2+(x)*num+add,3+(x)*num+add,1+(x+1)*num+add]]
        #first point in the ring to the 2nd,3rd and
        #its corresponding point on the ring above
        for y in range(num-3):
            rel += [[y+4+(x)*num+add,y+2+(x+1)*num+add]]
            #2nd point to 3rd last point connected to 2 ahead and
            #its corresponding point on the ring above
        rel += [[num-1+(x+1)*num+add]]
        #2nd last point in ring to its corresponding point on the ring above
        rel +=[[(x+1)*num+add-1,num+add+(x+1)*num]]
        #last point in ring to the second last point and
        #its corresponding point on the ring above
    #LAST RING
    x = num / 2 - 2
    circle(add+1, x)
    rel +=[[num*(num/2-1)+1+add]]
    #last point in 2nd last ring to the one point in the ring above
    rel += [[x+num*(num/2-2)+1+add for x in range (num-1)]]
    #last on last sphere point to all the points on the last ring
def circle(add,x):
    global rel,num
    rel += [[1+(x)*num+add,2+(x)*num+add]]
    #first point in the ring to the 2nd,3rd
    for y in range(num-3):
        rel += [[y+3+(x)*num+add]]
        #2nd point to 3rd last point connected to 2 ahead
    rel += [[(x+1)*num-1+add]]
    #2nd last point in ring to last point in ring
    if add == 0:
        rel+= [[num-2]]
def output(array):
    new_file = ""
    for x in array:
        for y in range(len(x)):
            new_file += str(x[y])
            if y < len(x)-1:
                new_file +=","
        new_file += "|"
    print new_file[:-1]

def SphereGUI(Input):
    global num,GUI,CurItm,rel,SphereCurrently
    GUI = True
    c.delete("tes")
    if Input == "Right":
        CurItm = (CurItm+1)%4
    if Input == "Left":
        CurItm = (CurItm-1)%4
    if CurItm <3:
        if Input == "Up":
            Itms[CurItm][1] += 1*Itms[CurItm][2]
        if Input == "Down":
            Itms[CurItm][1] -=1*Itms[CurItm][2]
    else:
        if Input.isdigit():
            Itms[3][1] += Input
        if Input == "period" and not "." in Itms[3][1]:
            Itms[3][1] += "."
        if Input == "BackSpace":
            Itms[3][1] = Itms[3][1][:-1]
    if Itms[0][1] >4 or Itms[0][1] <2:
       Itms[0][1] = 2
    if Itms[1][1] < 4:
        Itms[1][1] = 4
    Itms[2][1] = Itms[2][1] % 2
    c.create_text(c.winfo_width()/2, c.winfo_height()/2,
    text=Itms[CurItm][0] + str(Itms [CurItm][1]),tag = "tes",anchor=N)
    c.update()
    if  Input == "Return":
        GUI = False
        SphereCurrently = True
        index = float(Itms[3][1])**0.5*2/((Itms[1][1])/4.0 - 0.99)
        if not bool(Itms[2][1]):
            #index = Itms[1][1]
            rel = [""]
        num = Itms[1][1]
        linesphere(Itms[0][1],float(Itms[3][1]),index,bool(Itms[2][1]))
        #main()
#print len(obj),len(rel)
#-------------------------------------------------------------------------------
from Tkinter import *
from operator import itemgetter
import time,string,math
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

controls = {"w":[0,1],"s":[0,-1],"a":[1,1],"d":[1,-1],"t":[2,1],"g":[2,-1],
"f":[3,1],"h":[3,-1],"i":[4,1],"k":[4,-1],"j":[5,1],"l":[5,-1]}
presets = {"1":[0]*6,"2":[9, 17, 0, 0, 0, 0],"3":[45,45,45,45,45,45],
"4":[45,35,0,0,0,0],"5":[3,90,103,10,45,0]}
speedset = {"=":[1,1],"-":[-1,1],"+":[0.1,1],"_":[-0.1,1],"0":[0,0]}
Dctn = {"Left":[2,0.1,0,0],"Right":[2,-0.1,0,0],"Up":[0,0,2,25],
"Down":[0,0,2,-25],"comma":[0,0,3,-0.1],"period":[0,0,3,0.1]}
contr = [40,1.4]
contrastop = {"'":[0.1,0],";": [-0.1,0],'"':[0,0.1],":":[0,-0.1]}
pressed = {}
TOL = 0.000001
speed = 1
pos = [0,0,6,6]
sheetpos = [500,400,800,7]
rotation = [0, 0, 0, 0, 0, 0]
#           xz yz xw yw xy zw
#           ws ad tg fh ik jl
c = Canvas(root, width=screen_width, height=screen_height-80)
c.bind("<KeyPress>", keypress)
c.bind("<KeyRelease>", keyrelease)
c.bind("<Button-1>", callback)
c.create_text(0, 15, text=str(rotation),tag = "text",anchor=SW)
c.pack()
var,var2,v,var3 = IntVar(),BooleanVar(),IntVar(),BooleanVar()
CurItm = 0
Itms = [["Dimension ",2,1],["Ring Size ",8,4],["LineSphere ",1,1],
        ["Radius ","4"]]
GUI = False
get_options()
for txt in range(len(options)):
    Radiobutton(root,text=options[txt],variable=v,value=txt,
    command=change).pack(side='left')
Checkbutton(root, text="Preference 3D", variable=var).pack(side='right')
Checkbutton(root, text="Distort with 4D", variable=var2).pack(side='right')
Checkbutton(root, text="Label Points", variable=var3).pack(side='right')
change()
while True:
    if GUI:
        SphereGUI("nill")
        continue
    handleroat()
    nobj =[]+ obj
    c.delete("tes")
    for idx in range(len(nobj)):
        nobj[idx] = rotate(nobj[idx][0],
        nobj[idx][1],nobj[idx][2],nobj[idx][3])
        nobj[idx] = move(nobj[idx])
        nobj[idx] = shadow(nobj[idx])
    if rel == [""]:
        dot_rend()
    else:
        if not SphereCurrently:
            time.sleep(.015)
        line_rend()
    c.update()
root.geometry('%sx%s+%s+%s' %(1024, 768, 100, 100))
root.resizable(0, 0)
root.mainloop()




