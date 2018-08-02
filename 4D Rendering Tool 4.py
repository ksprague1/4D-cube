def get_options():
    global options,filename,prefabs
    filename = "Files\Objects.txt"
    fil = open(filename, 'r')
    options = fil.readline()[:-1].split("|")
    options += ["Shape Builder","Sphere Builder"]
    prefabs = fil.readline()[:-1].split("|")
    for x in range(len(prefabs)):
        prefabs[x]= map(float,prefabs[x].split(","))

def change():
    global obj,rel,SphereCurrently,faces,selectedDot,specialDot,rndReady
    tag = options[v.get()]
    SphereCurrently = False
    rndReady = False
    if tag == "Sphere Builder":
        faces = []
        SphereGUI("null")
        return
    if tag == "Shape Builder":
        rel = [[0]]
        obj = [[0,0,0,0]]
        faces = []
        selectedDot = [0]
        return
    selectedDot = [0]
    specialDot = None
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
            if rel == ['']:
                rel = []
            else:
                for x in range(len(rel)):
                    rel[x]= map(int,rel[x].split(","))
            line=3
        elif line == 3:
            faces = ln[:-1].split("|")
            print faces
            if faces == ['']:
                faces = []
            else:
                for x in range(len(faces)):
                    faces[x]= map(int,faces[x].split(","))
            break
    if v2.get() == 2:
        initface()
    fil.close()
    
def keypress(event):
    global rotation,speed,GUI,FGUI,curot,rotsp,prefabs
    pressed[str(event.keysym)] = str(event.char)
    if objectname != None or event.char == "v":
        beforesave(event)
        return
    if GUI:
        SphereGUI(event.keysym)
        return
    if FGUI:
        FaceGUI(event.keysym)
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
    if event.keysym == "space" and rotsp == [0]*6:
        curot = (curot + 1) % len(prefabs)
        for x in range(6):
            if speed != 0:
                rotsp[x]=(prefabs[curot][x]-rotation[x])/int(prefabs[curot][6]
                /speed)
            else:
                rotsp[x]=(prefabs[curot][x]-rotation[x])/int(prefabs[curot][6])
    
def keyrelease(event):
    if str(event.keysym) in pressed:
        del pressed[str(event.keysym)]
    
def handleroat():
    global rotation,speed
    for Hash in pressed:
        if Hash in controls:
            index =  controls[Hash]
            rotation[index[0]] += index[1]*speed
        if Hash in presets:
            rotation = []+ presets[Hash]
        if Hash in movement:
            index =  movement[Hash]
            for dit in selectedDot:
                obj[dit][index[0]] = int(obj[dit][index[0]]*1000+
            index[1]*speed*20)/1000.0
    for rot in range(len(rotation)):
        rotation[rot] = rotation[rot] % 360
    c.delete("text")
    #c.create_text(0, 15, text=str(rotation),tag = "text",anchor=SW)
    
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
    idxng = -(item[0]**2+item[1]**2+item[2]**2+(item[3]**2)
              *(1-p4/30.0)+36*p4/30.0)**0.5
    return [x,y,item[2],idxng]
def line_rend():
    global pos,sheetpos
    time.sleep(0.010)
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
            fill = "gray"+ str(int(tob[0]*10))) #str(100-int(tob[0]*10)))
    if var3.get():
        tobe = []
        for idx in range(len(nobj)):
            num = (-nobj[idx][2]+contr[0])/contr[1]
            tobe +=[[num,nobj[idx][0],nobj[idx][1],
            (nobj[idx][3])]]
        #tobe = sorted(tobe, key=itemgetter(3))
        for tob in range(len(tobe)):
            dot=c.create_text(tobe[tob][1],tobe[tob][2],text=str(tob),
            tag="tes",fill='magenta')#,fill = "red",font = ('Times', 20, 'bold'))
def dot_rend():
    global pos,sheetpos
    tobe = []
    for idx in range(len(nobj)):
        num = (-nobj[idx][2]*2+contr[0]/2)/contr[1]
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
    #if it is a Linesphere
    if Type:
        rel = []
        if D == 2:
            circle(0,0)
        elif D==3:
            sphere(0)
        elif D==4:
            hypersphere()
    else:
        rel = []
        for x in range(len(obj)):
            rel += [[x]]
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
    c.create_text(c.winfo_width()/2, c.winfo_height()/2,fill = 'red',
    text=Itms[CurItm][0] + str(Itms [CurItm][1]),tag = "tes",
    anchor=N,font = ('Times', 69, 'bold'))
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
def import_imgs():
    imageimp = []
    X = 0
    while True:
        imageimp += [cv2.imread('Files\img'+str(X)+'.jpg')]
        if imageimp[X] is None:
            X+=1
            break
        X+=1
    imageimp[-1] = cv2.imread('Files\Default.jpg')
    return imageimp,X
def image_face():
    global faces,X
    for y in range (len(faces)):
        faces[y] = faces[y][0:4] + [(X-1)*var3.get()]
    FaceGUI('')
def FaceGUI(Input):
    global FGUI,CurItm,faces,X,rel
    FGUI = True
    c.delete("tes")
    if Input == "Right":
        CurItm +=1
    if Input == "Left":
        CurItm -=1
    CurItm = CurItm % len(faces)
    if Input == "Up":
        faces[CurItm][4] = (faces[CurItm][4]+1) % X
    if Input == "Down":
        faces[CurItm][4] =(faces[CurItm][4]-1) % X
    if Input.isdigit():
        faces[CurItm][4] = str(faces[CurItm][4])+Input      
    if Input == "BackSpace":
        faces[CurItm][4] = str(faces[CurItm][4])[:-1]
    #print faces
    faces[CurItm][4] = int("0"+str(faces[CurItm][4])) % X
    c.create_text(c.winfo_width()/2, c.winfo_height()/2,fill = 'red',
    text="Face "+ str(CurItm)+": Image = " + str(faces[CurItm][4]),tag = "tes",
    anchor=N,font = ('Times', 69, 'bold'))
    c.update()
    if  Input == "Return":
        FGUI = False
def angle_between_points( p0, p1, p2 ):
    a = (p1[0]-p0[0])**2 + (p1[1]-p0[1])**2
    b = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
    c = (p2[0]-p0[0])**2 + (p2[1]-p0[1])**2
    if (4*a*b) == 0:
        return 0
    elif abs((a+b-c) / (4*a*b)**0.5) > 1.0:
        return 0
    if math.acos( (a+b-c) / (4*a*b)**0.5 ) * 180/math.pi >= 179.99:
        return 0
    return math.acos( (a+b-c) / (4*a*b)**0.5 ) * 180/math.pi
def check_vld(x):
    return ((angle_between_points(x[0],x[1],x[2])+
    angle_between_points(x[1],x[2],x[3])+
    angle_between_points(x[2],x[3],x[0])+
    angle_between_points(x[3],x[0],x[1])+0.001) >= 360.0)
def dewit():
    global went,DispImg,imageimp
    #pts1 = np.float32([[800,923],[0,923],[0,0],[800,0]])
    went = False
    dst = None
    #dst = np.zeros((infnum,infnum,3), np.uint8)
    
    #pts1 = np.float32([[width,height],[0,height],[0,0],[width,0]])
    for face in faces:
        #if not went:
            #dst = imgit(True,imageimp[face[4]],face) 
        dst = imgit(dst,imageimp[face[4]],face)
    if went:
        dst = cv2.resize(dst,(600,600))
        dst = cv2.cvtColor(dst, cv2.COLOR_RGB2BGR)
        #dst[np.where((dst == [0,0,0]).all(axis = 2))] = [240,240,240]
        #cv2.imshow("hop",dst)
        dst = Image.fromarray(dst,"RGB")
        dst = ImageTk.PhotoImage(dst)
        DispImg = dst
        c.create_image(300,300,image = dst,tag  = "tes")

def imgit(dst,defimg,face):
    global went,imageimp,nobj,contr,infnum
    height,width = defimg.shape[0:2]
    pts1 = np.float32([[width,height],[0,height],[0,0],[width,0]])
    newthang = [nobj[face[0]][:2],nobj[face[1]][:2],
                nobj[face[2]][:2],nobj[face[3]][:2]]
    depth = (nobj[face[0]][3]+nobj[face[1]][3]+
              nobj[face[2]][3]+nobj[face[3]][3])**3/contr[0]+contr[1]
    if "q"  in pressed:
        image_face()
    if (not check_vld(newthang)) or depth < 0:
        #if not var4.get():
        return dst    
        depth = 0.0
    pts2 = np.float32(newthang)
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dstI = cv2.warpPerspective(defimg,M,(infnum,infnum))
    if not went:
        dst = cv2.addWeighted(dstI,depth,dstI,0.0,0)
        went = True
    else:
        dst = cv2.addWeighted(dstI,depth,dst,1.0,0)
    return dst
        #pass
    #dstI = True
def initface():
    global contr,sheetpos,rndReady
    if v2.get() == 2:
        if not rndReady:
            image_face()
            rndReady = True
        contr = [13000, 3.2]
        sheetpos = [infnum/2,infnum/2,infnum,7]
    else:
        sheetpos = [300,300,600,7]
        contr = [40,1.4]
        #change()
def scaleit(event):
    global infnum,sheetpos
    infnum = int(event)
    if v2.get() == 2:
        sheetpos = [infnum/2,infnum/2,infnum,7]
#------------------------------OBJ-BUILDING-------------------------------------
def integrend():
    global pos,sheetpos
    time.sleep(0.010)
    tobe = []
    for idx in range(len(obj)):
        for x in rel[idx]:
            num = (-nobj[idx][2]- nobj[x][2]+contr[0]/2)/contr[1]
            tobe +=[[num,nobj[idx][0],nobj[idx][1],nobj[x][0],nobj[x][1],
            (nobj[idx][3]+nobj[x][3])/2,"blue"]]
    #for idx in range(len(nobj)):
    for idx in range(len(obj)):
        num = (-nobj[idx][2]*2+contr[0]/2)/contr[1]
        tobe +=[[num,nobj[idx][0],nobj[idx][1],0,0,(nobj[idx][3]),"Sph"]]
    for face in faces:
        for x in range(4):
            n2 = (x+1)%4
            num = (-nobj[face[x]][2]- nobj[face[n2]][2]+contr[0]/2)/contr[1]
            tobe +=[[num,nobj[face[x]][0],nobj[face[x]][1],nobj[face[n2]][0]
            ,nobj[face[n2]][1],(nobj[face[x]][3]+nobj[face[n2]][3])/2,"red"]]
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
        if tob[6] != "Sph":
            line = c.create_line(tob[1],tob[2],tob[3],
            tob[4],tag="tes",width=tob[0]+(len(tob[6])-3)*4,
            fill = tob[6])#"gray"+ str(100-int(tob[0]*10)))
        else:
            dot = c.create_oval(tob[1]+12,tob[2]+12,tob[1]-12,
            tob[2]-12,tag="tes",width=0,
            fill = "gray"+ str(int(tob[0]*10)))
    if isinstance(specialDot,int):
        dot = c.create_oval(nobj[specialDot][0]+12,nobj[specialDot][1]+12
            ,nobj[specialDot][0]-12,nobj[specialDot][1]-12,tag="tes",width=0,
            fill = "yellow")
    elif isinstance(specialDot,list):
        for sDot in specialDot:
            dot = c.create_oval(nobj[sDot][0]+12,nobj[sDot][1]+12
            ,nobj[sDot][0]-12,nobj[sDot][1]-12,tag="tes",width=0,
            fill = "green")
    for dit in range(len(selectedDot)):
        c.create_text(600, 15*(dit+1), text=str(obj[selectedDot[dit]]),
        tag = "text",anchor=SW,fill='magenta')
        dot = c.create_oval(nobj[selectedDot[dit]][0]+12,
            nobj[selectedDot[dit]][1]+12,nobj[selectedDot[dit]][0]-12,
            nobj[selectedDot[dit]][1]-12,tag="tes",width=0,fill = "blue")
def form_itm(item):
    #formats arrays into a file friendly string
    new_file = ""
    for x in item:
        for y in range(len(x)):
            new_file += str(x[y])
            if y < len(x)-1:
                new_file +=","
        new_file += "|"
    return new_file[:-1] + "\n"
def beforesave(event):
    #creates a small gui for naming your saved object based on sphereGUI
    c.delete("tes")
    global objectname
    if objectname == None:
        objectname = "New Object"
    if event == None:
        pass
    elif event.keysym == "BackSpace" and len(objectname) > 0:
        objectname = objectname[:-1]
    elif event.keysym == "Return":
        #the save function saves all the shape data currently in the ram
        save(objectname)
        objectname = None
        return
    else:
        objectname += event.char
    c.create_text(c.winfo_width()/2, c.winfo_height()/2,fill = 'red',
    text=objectname,tag = "tes",
    anchor=N,font = ('Times', 69, 'bold'))
    c.update()
def save(objectname):
    global filename,obj,rel,faces
    print filename
    savefile = open(filename, 'a')
    savefile.write(objectname+"\n")
    savefile.write(form_itm(obj))
    savefile.write(form_itm(rel))
    savefile.write(form_itm(faces))
    savefile.close()
def callback(event):
    global nobj,obj,selectedDot,specialDot,rel,faces
    #print pressed
    focused = root.focus_get() == c
    c.focus_set()
    print "clicked at", event.x, event.y
    for x in range(len(nobj)):
        if ((event.x-nobj[x][0])**2 + (event.y - nobj[x][1])**2 < 144):
            #selectedDot = x
            #specialDot is an int when creating edges and a list
            #when creating faces
            if "Shift_L" in pressed:
                if isinstance(specialDot,int):
                    print specialDot
                    #makes sure the edge is between two seperate points
                    if (specialDot != x and not specialDot in
                    rel[x]):
                        #creates the edge
                        rel[specialDot] +=[x]
                        #resets specialDot
                        specialDot = None
                        return
                    specialDot = None
                #if special dot is not an int it is set to selectedDot
                specialDot = x
                
            if "Alt_L" in pressed:
                if isinstance(specialDot,list):
                    #makes sure each point is unique
                    if (not x in specialDot):
                        specialDot +=[x]
                    if len(specialDot) ==4:
                        #when 4 points are selected a face is created
                        if not specialDot in faces:
                            faces += [specialDot]
                        specialDot = None
                        #specialDot is once again reset
                        return
                else:
                    specialDot = [x]
            if "Control_L" in pressed:
                if not x in selectedDot:
                    selectedDot +=[x]
            else:
                selectedDot = [x]
            return
    if "Shift_L" in pressed or "Alt_L" in pressed:
        specialDot = None
        return
    #if the screen is clicked where there is no dot without any modifiers,
    # A new dot is created
    if focused:
        obj += [[0,0,0,0]]
        rel += [[len(obj)-1]]
        selectedDot = [len(obj)-1]
        
def delete(event):
    global nobj,obj,rel,faces,selectedDot,deleting
    focused = root.focus_get() == c
    c.focus_set()
    for x in range(len(obj)):
        if ((event.x-nobj[x][0])**2 + (event.y - nobj[x][1])**2 < 144 and len(obj)>1):
            del obj[x]
            del rel[x]
            #clear some of the edges linked to the point
            selectedDot = [0]
            y = 0
            #clear any faces linked to the point
            while y <(len(faces)):
                if x in faces[y]:
                    del faces[y]
                    continue
                y+=1
            y = 0
            #clear the rest of the edges linked to the point
            for prt in range(len(rel)):    
                while y < len(rel[prt]):
                    if x == rel[prt][y]:
                        del rel[prt][y]
                        continue
                    y+=1
                y=0
            #change indexing in faces as to not include the point
            for dlt in range(len(faces)):
                for fc in range(len(faces[dlt])):
                    if faces[dlt][fc] >= x:
                        faces[dlt][fc]-=1
            #now changeing indexing in rel
            for dlt in range(len(rel)):
                for fc in range(len(rel[dlt])):
                    if rel[dlt][fc] >= x:
                        rel[dlt][fc]-=1
                if len(rel[dlt]) == 0:
                    rel[dlt] += [dlt]
    if "Shift_L" in pressed:
        for indx in range(len(rel)):
            for idx in range(len(rel[indx])):
                #delets an edge if the click is close enough
                if proximity(nobj[indx],nobj[rel[indx][idx]],event) < 4:
                    del rel[indx][idx]
                    if len(rel[indx]) == 0:
                        rel[indx] += [indx]
                    return
    if "Alt_L" in pressed:
        for dlt in range(len(faces)):
                for fc in range(len(faces[dlt])):
                    #delets an face if the click is close enough
                    if proximity(nobj[faces[dlt][fc]],nobj[faces[dlt][(fc+1)%4]],event) < 4:
                        del faces[dlt]
                        return
def proximity(a,b,c):
    #A and B are two coordinates of a line, C is a point
    if abs(a[1]-b[1])+abs(a[0]-b[0]) < 0.00001:
    #if the line is a point
        x = a[0]
        y = a[1]
    elif abs(a[1]-b[1])< 0.00001:
    #if the line is horizontal
        y = a[1]
        x = c.x
    elif abs(a[0]-b[0])< 0.00001:
    #if the line is vertical
        x = a[0]
        y = c.y
    else:
        m1 = (a[1]-b[1])/(a[0]-b[0])
        b1 = a[1] - m1*a[0]
        m2 = -1/m1
        b2 = c.y - m2*c.x
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
    #determines the edges of the line (domain and range)
    if a[0] > b[0]:
        maxX = a[0]+2
        minX = b[0]-2
    else:
        minX = a[0]-2
        maxX = b[0]+2
    if a[1] > b[1]:
        maxY = a[1]+2
        minY = b[1]-2
    else:
        minY = a[1]-2
        maxY = b[1]+2
    if not (minX<x<maxX and minY<y<maxY):
    #if the coordinates of the point do not fit within the domain and
    #range of the line, a large value is returned
        return 100
    #otherwise, the actual distance is returned
    return ((x-c.x)**2+(y-c.y)**2)**0.5
#-------------------------------------------------------------------------------
from Tkinter import *
from operator import itemgetter
import time,string,math
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#------------------------------------------------------------------------
import cv2
import numpy as np
#import matplotlib.pyplot as plt
from PIL import Image, ImageTk
#defimg = cv2.imread('GOT EEM.jpg')
imageimp,X = import_imgs()
p4 = 0
FGUI = False
#rows,cols,ch = img.shape
#--------------------------------------------------------------------------
movement = {"W":[1,-1],"S":[1,1],"A":[0,-1],"D":[0,1],"T":[2,1],"G":[2,-1],
"F":[3,1],"H":[3,-1]}
selectedDot = [0]
specialDot = None
objectname = None
rendoptns = ["Lines","Points","Images","Integrated"]
rendermodes = [line_rend,dot_rend,dewit,integrend]
rndReady = False
#--------------------------------------------------------------------------
controls = {"w":[0,1],"s":[0,-1],"a":[1,1],"d":[1,-1],"t":[2,1],"g":[2,-1],
"f":[3,1],"h":[3,-1],"i":[4,1],"k":[4,-1],"j":[5,1],"l":[5,-1]}
presets = {"1":[0]*6,"2":[9, 17, 0, 0, 0, 0],"3":[45,45,45,45,45,45],
"4":[45,35,0,0,0,0],"5":[3,90,103,10,45,0]}
speedset = {"=":[1,1],"-":[-1,1],"+":[0.1,1],"_":[-0.1,1],"0":[0,0]}
Dctn = {"Left":[2,0.1,0,0],"Right":[2,-0.1,0,0],"Up":[0,0,2,25],
"Down":[0,0,2,-25],"comma":[0,0,3,-0.1],"period":[0,0,3,0.1]}
contrastop = {"'":[0.1,0],";": [-0.1,0],'"':[0,0.1],":":[0,-0.1]}
contr = [40,1.4]#[13000, 3.2]
pressed = {}
TOL = 0.000001
speed = 1
pos = [0,0,6,6]
sheetpos = sheetpos = [300,300,600,7]#[infnum/2,infnum/2,infnum,7]
rotation = [0, 0, 0, 0, 0, 0]
#           xz yz xw yw xy zw
#           ws ad tg fh ik jl
pefabs = []
curot = -1
rotsp = [0,0,0,0,0,0]

c = Canvas(root, width=screen_width, height=screen_height-80)
c.configure(background='black')
c.bind("<KeyPress>", keypress)
c.bind("<KeyRelease>", keyrelease)
c.bind("<Button-1>", callback)
c.bind("<Button-3>", delete)
c.create_text(0, 15, text=str(rotation),tag = "text",anchor=SW)
c.pack()
var,var2,v,var3,var4 = IntVar(),BooleanVar(),IntVar(),BooleanVar(),BooleanVar()
v2 = IntVar()
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
#Checkbutton(root, text="Images", variable=var4,command=initface).pack(side='right')
for txt in range(len(rendoptns)):
    Radiobutton(root,text=rendoptns[txt],variable=v2,value=txt,
                command = initface).pack(side='right')
scl = Scale(root,from_=50,to=600,command=scaleit,orient = HORIZONTAL).pack()
#initface()
change()
while True:
    end = False
    if rotsp != [0,0,0,0,0,0]:
        end = True
        for x in range(6):
            rotation[x] += rotsp[x]
            if end and abs(rotation[x]-prefabs[curot][x]%360) > 0.001:
                end = False
    if end:
        rotsp = [0]*6
        for x in range(6):
            rotation[x] = int(rotation[x] + 0.5)
    if objectname != None:
        beforesave(None)
        continue
    if FGUI:
        FaceGUI('')
        continue
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
    rendermodes[v2.get()]()
    if p4 != 30*var.get():
        p4 += var.get()*2-1
    c.create_text(0, 15, text=str(rotation),tag = "text",anchor=SW,
    fill='magenta')
    c.update()
root.geometry('%sx%s+%s+%s' %(1024, 768, 100, 100))
root.resizable(0, 0)
root.mainloop()




