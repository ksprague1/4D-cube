import math
from operator import itemgetter
TOL = 0.000001
def sorting(x,y,z,w,N):
    idxng = "0"*(4-len(str(int((w+N)*100))))+str(int((w+N)*100))
    idxng += "0"*(4-len(str(int((z+N)*100))))+str(int((z+N)*100))
    idxng += "0"*(4-len(str(int((y+N)*100))))+str(int((y+N)*100))
    idxng += "0"*(4-len(str(int((x+N)*100))))+str(int((x+N)*100))
    idxng = -int(idxng)
    return [[x,y,z,w,idxng]]
def linesphere(D,sph,index):
    global obj,rel,TOL
    obj = []
    for s4 in range(int(sph**0.5*2/index + 2)):
        num4 = sph**0.5*math.sin(math.radians(360.0/int(sph**0.5*2/index + 1)*s4/4))
        if s4 == int(sph**0.5*2/index + 2)-1:
            num4 = (sph)**0.5
            if D < 4:
                num4 = 0
        elif D < 4:
            continue
        down4 = num4 ** 2
        for s3 in range(int(sph**0.5*2/index + 2)):
            num3 = (sph- down4)**0.5*math.sin(math.radians(360.0/int((sph)
            **0.5*2/index + 1)*s3/4))
            if s3 == int(sph**0.5*2/index + 2)-1:
                num3 = (sph-down4)**0.5
                if D < 3:
                    num3 = 0
            elif (s4 == int(sph**0.5*2/index + 2)-1 and D>3) or D < 3:
                #print "GOT EM1"
                continue
            down3 = num4 ** 2+num3 ** 2
            for s2 in range(int(sph**0.5*2/index + 2)):
                num2 = (sph- down3)**0.5*math.sin(math.radians(360.0/int((sph)
                **0.5*2/index + 1)*s2/4))
                if s2 == int(sph**0.5*2/index + 2)-1:
                    num2 = (sph-down3)**0.5
                elif s3 == int(sph**0.5*2/index + 2)-1 and D>2:
                    #print "GOT EM2"
                    continue
                down2 = num4 ** 2+num3 ** 2+ num2 **2
                s1 = (sph- down2)**0.5
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
    rel += [[w+axs*(num/2-2)+2+1 for w in range (axs-1)]]
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
D = int(raw_input("What Dimention"))
sph = float(raw_input("Radius"))   
#index = 3.5
num = int(raw_input("What Ring size?"))
index = sph**0.5*2/((num)/4.0 - 0.99)
linesphere(D,sph,index)
output(obj)
#print len(obj)
output(rel)
#print len(obj),len(rel)
#-----------------------------NEEDS_WORK_LINE-------------------------------
#---------------------------------------------------------------------------
