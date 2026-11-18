import pickle,sys,json,numpy as np
from shapely.geometry import Polygon,box,LineString
from shapely import affinity
from shapely.ops import unary_union
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
P=dict(clear=0.3, skirt=1.8, arm_keep=5.0, band_w=1.5, band_proud=0.4)
U=pickle.load(open('wall_top.pkl','rb'))
# clean: convex hull of each straight piece (tower, middle halves, arms), split at x=0 and the joint lines
def side(p,q):  # half-plane left of line p->q, big
    p,q=np.array(p),np.array(q); d=(q-p)/np.linalg.norm(q-p); n=np.array([-d[1],d[0]])
    return Polygon([p-d*100,q+d*100,q+d*100+n*100,p-d*100+n*100])
TW=box(-6.585,0.426,6.585,13.6)
rest=U.difference(TW.buffer(0.01))
pieces=[TW]
for s_ in (1,-1):
    a=(12.8*s_,-1.2); b=(10.6*s_,-7.1)
    jl=side(a,b) if s_==1 else side(b,a)          # outer side of the joint (arm)
    arm=rest.intersection(jl); mid=rest.difference(jl).intersection(box(0,-50,50,50) if s_==1 else box(-50,-50,0,50))
    for g in (arm,mid):
        g=max(g.geoms,key=lambda x:x.area) if hasattr(g,'geoms') else g
        pieces.append(g.convex_hull)
U=unary_union(pieces).buffer(0.05,join_style='mitre').buffer(-0.05,join_style='mitre')
C=U.buffer(P['clear'],join_style='mitre')                                # cavity (top course + tower + clips)
O=C.buffer(P['skirt'],join_style='mitre')                                # outer
# arm cut: half-planes perpendicular to each arm, arm_keep past the joint line
J=np.array([11.7,-4.15]); d=np.array([0.741,-0.671])                     # right joint centre, arm direction
def cut(g):
    for s in (1,-1):
        j=J*[s,1]; dd=d*[s,1]; c=j+dd*P['arm_keep']; n=np.array([-dd[1],dd[0]])
        far=c+dd*100
        hp=Polygon([c+n*100,c-n*100,far-n*100,far+n*100])
        g=g.difference(hp)
    return g
O=cut(O); C=cut(C)
# bands: strips along the joint line through the original clip centres
bands=[]
for s in (1,-1):
    a=np.array([12.8*s,-1.2]); b=np.array([10.6*s,-7.1])
    ln=LineString([a+(a-b)*2,b+(b-a)*2])
    bands.append(ln.buffer(P['band_w']/2,cap_style='flat'))
B=unary_union(bands)
Bo=B.intersection(O.buffer(P['band_proud'],join_style='mitre'))
print('outer bounds',[round(v,2) for v in O.bounds],'size',round(O.bounds[2]-O.bounds[0],2),round(O.bounds[3]-O.bounds[1],2))
print('outer verts',len(O.exterior.coords),'cavity verts',len(C.exterior.coords), C.geom_type)
pickle.dump(dict(O=O,C=C,B=Bo,Bstrip=B),open('frog_polys.pkl','wb'))
fig,ax=plt.subplots(figsize=(10,7))
for g,c in ((O,'g'),(C,'k'),(Bo,'b')):
    for gg in (g.geoms if hasattr(g,'geoms') else [g]):
        x,y=gg.exterior.xy; ax.plot(x,y,c+'-',lw=.8)
x,y=U.exterior.xy; ax.plot(x,y,'r:',lw=.6)
ax.set_aspect('equal'); ax.grid(True,lw=.3); plt.savefig('frog_plan.png',dpi=100,bbox_inches='tight')
