# Parallel wall faces + wall-top grooves (user 2026-11-20), applied to frog_marker.sc after build_batch.py:
# O/G/C are OuterSketch, GrooveSketch and CavitySketch as build_batch.py made them; the middle inner face takes the outer face's slope,
# both arm faces the original arm direction (0.766, -0.643), and two 0.66 mm grooves split each wall segment in thirds.
# Writes par.json: new OuterSketch / GrooveSketch points (move them with sketch.move_points) and the SeamSketch polygons (cut 0.66 down from the wall top).
import numpy as np, json
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union
O=[(-11.9158,2.08),(-8.685,2.3543),(-8.685,13.596),(8.685,13.596),(8.685,2.3543),(11.9158,2.08),(12.1798,1.9845),(11.8693,1.1314),(14.964,0.005),(15.2746,0.8582),(15.6896,0.7068),(19.5209,-2.9597),(11.9529,-11.3173),(11.0625,-10.7126),(11.4654,-9.6061),(8.3708,-8.4794),(8.0311,-9.4125),(1.646,-8.2441),(1.646,-7.181),(-1.646,-7.181),(-1.646,-8.2441),(-8.0313,-9.4126),(-8.3708,-8.4799),(-11.4655,-9.6064),(-11.0627,-10.7127),(-11.9529,-11.3173),(-19.5209,-2.9597),(-15.6896,0.7068),(-15.2746,0.8582),(-14.9641,0.0051),(-11.8693,1.1315),(-12.1798,1.9845)]
G=[(-11.7732,1.4298),(-8.025,1.748),(-8.025,12.936),(8.025,12.936),(8.025,1.748),(11.7732,1.4298),(11.9541,1.3643),(11.8693,1.1314),(14.964,0.005),(15.0489,0.238),(15.3333,0.1343),(18.6007,-2.9926),(11.8489,-10.4488),(11.2954,-10.0729),(11.4654,-9.6061),(8.3708,-8.4794),(8.2601,-8.7835),(1.646,-7.5731),(1.646,-7.181),(-1.646,-7.181),(-1.646,-7.5731),(-8.2603,-8.7835),(-8.3708,-8.4799),(-11.4655,-9.6064),(-11.2956,-10.0731),(-11.8489,-10.4488),(-18.6007,-2.9926),(-15.3333,0.1343),(-15.0489,0.238),(-14.9641,0.0051),(-11.8693,1.1315),(-11.9541,1.3643)]
C=Polygon([(-14.7179,-0.8547),(-14.2668,-0.6902),(-14.0606,-0.6151),(-13.6786,-0.4761),(-13.1404,-0.2803),(-11.8104,0.204),(-11.5268,0.3066),(-6.885,0.7007),(-6.885,13.9),(6.885,13.9),(6.885,0.7007),(11.5268,0.3066),(11.8104,0.204),(13.1404,-0.2803),(13.6786,-0.4761),(14.0606,-0.6151),(14.2666,-0.6901),(14.7179,-0.8547),(18.3123,-4.2944),(13.1729,-9.97),(10.2577,-7.9901),(0,-6.113),(-10.2577,-7.9901),(-13.1729,-9.97),(-18.3123,-4.2944)])
O=[np.array(p) for p in O]; G=[np.array(p) for p in G]
def X(p,d,q,e):  # intersect lines p+t d, q+s e
    A=np.array([d,-np.array(e)]).T; t=np.linalg.solve(A,np.array(q)-np.array(p))[0]; return np.array(p)+t*np.array(d)
k=(-9.4125+8.2441)/(8.0311-1.646)          # middle slope (outer face, = original)
dm=np.array([1,k])/np.hypot(1,k)
a=np.array([0.766,-0.643]); a/=np.linalg.norm(a)   # original arm direction
nm=np.array([-dm[1],dm[0]]); na=np.array([-a[1],a[0]])  # left normals (point to inner/tower side)
gi=0.66
# indices (right side): O: 4 tower corner, 5 mid inner end, 10 arm inner start, 11 arm inner end, 12 arm outer end, 13 arm outer start
Pi_m=O[5]                                   # middle inner face through (11.9158, 2.08)
Pi_a=O[10]; Po_a=O[12]
newO=[p.copy() for p in O]; newG=[p.copy() for p in G]
newO[4]=X(Pi_m,dm,(8.685,0),(0,1))
newO[11]=X(Pi_a,a,O[11],O[12]-O[11])
newO[13]=X(Po_a,a,O[13],O[14]-O[13])
# groove course: same faces moved 0.66 into the wall
newG[4]=X(Pi_m-nm*gi,dm,(8.025,0),(0,1))
newG[5]=X(Pi_m-nm*gi,dm,G[5],G[6]-G[5])
newG[10]=X(Pi_a-na*gi,a,G[9],G[10]-G[9])
newG[11]=X(Pi_a-na*gi,a,G[11],G[12]-G[11])
newG[12]=X(Po_a+na*gi,a,G[11],G[12]-G[11])
newG[13]=X(Po_a+na*gi,a,G[13],G[14]-G[13])
# mirror the right side's edits onto the left; partner index (5 - i) mod 32: O[4] (8.685,2.35) <-> O[1] (-8.685,2.35); O[5]<->O[0]; O[10]<->O[27]; O[11]<->O[26]; O[12]<->O[25]; O[13]<->O[24]
for L,idx in ((newO,(4,11,13)),(newG,(4,5,10,11,12,13))):
    for i in idx:
        j=(5-i)%32
        L[j]=np.array([-L[i][0],L[i][1]])
PO=Polygon(newO)
Po_m=O[17]
Wm=np.dot(Pi_m-Po_m,nm); Wa=np.dot(Pi_a-Po_a,na); print('wall widths middle %.3f arm %.3f'%(Wm,Wa))
lines=[]
for f in (1/3,2/3):
    pm=Po_m+nm*Wm*f; pa=Po_a+na*Wa*f
    B=X(pm,dm,pa,a); apex=X(pm,dm,(0,0),(0,1)); E=B+a*12
    lines.append([(-E[0],E[1]),(-B[0],B[1]),tuple(apex),tuple(B),tuple(E)])
    print('groove',f,'bend',np.round(B,3),'apex',np.round(apex,3))
T=PO.intersection(box(-8.685,0.426,8.685,50))
seam=unary_union([LineString(l).buffer(gi/2,cap_style='flat',join_style='mitre') for l in lines]).difference(T).intersection(PO.buffer(1))
r=lambda g:[[round(x,4),round(y,4)] for x,y in list(g.exterior.coords)[:-1]]
out={'O':[[round(x,4),round(y,4)] for x,y in newO],'G':[[round(x,4),round(y,4)] for x,y in newG],'seams':[r(g) for g in getattr(seam,'geoms',[seam])]}
json.dump(out,open('par.json','w'))
# grooves down the arm end faces (user 2026-11-20: they should reach the end of that side): each top groove's arm line,
# 0.66 wide, from the end face 0.66 into the arm, cut over the full height (sketch at z 0)
from shapely import affinity
e0,e1=newO[11],newO[12]                     # right arm end face
inside=Polygon([e0,e1,e1-a*gi,e0-a*gi])      # the strip 0.66 deep behind the end face (a points out through it)
inside=inside.union(Polygon([e0,e1,e1+a*2,e0+a*2]))   # and past it, so the cut opens the face
ends=[]
for l in lines:
    strip=LineString([l[3],(np.array(l[4])+a*5)]).buffer(gi/2,cap_style='flat',join_style='mitre')
    g=strip.intersection(inside); ends+=[g,affinity.scale(g,-1,1,origin=(0,0))]
out['ends']=[r(g) for g in ends]
json.dump(out,open('par.json','w'))
print('end slots',[round(g.area,3) for g in ends])
