import re,zipfile,glob,numpy as np,sys
from shapely.geometry import Polygon,MultiPolygon
from shapely.ops import unary_union, polygonize
from shapely import LineString
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def load(f):
    z=zipfile.ZipFile(f)
    for n in z.namelist():
        if not n.startswith('3D/Objects/'): continue
        s=z.read(n).decode()
        V=np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"',s),float)
        if len(V):
            T=np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"',s),int)
            return V-[0,0,V[:,2].min()],T
def slice_poly(V,T,z):
    segs=[]
    P=V[T]; d=P[:,:,2]-z
    for p,dd in zip(P,d):
        pts=[]
        for i in range(3):
            a,b=p[i],p[(i+1)%3]; da,db=dd[i],dd[(i+1)%3]
            if (da<0)!=(db<0): pts.append(tuple(np.round(a[:2]+(b[:2]-a[:2])*da/(da-db),3)))
        if len(pts)==2 and pts[0]!=pts[1]: segs.append(LineString(pts))
    polys=list(polygonize(unary_union(segs)))
    # even-odd: union of faces then remove holes by symmetric difference
    res=Polygon()
    for p in sorted(polys,key=lambda p:-p.area): res=res.symmetric_difference(p)
    return res
R=[load(f) for f in sorted(glob.glob('/home/viridjan/Projects/root_organizer/reference/*.3mf'))]
zs=[float(a) for a in sys.argv[1].split(',')]
U=unary_union([slice_poly(V,T,z) for V,T in R for z in zs])
print('area',round(U.area,2),'bounds',[round(b,2) for b in U.bounds], U.geom_type)
import pickle; pickle.dump(U,open(sys.argv[2],'wb'))
fig,ax=plt.subplots(figsize=(10,6))
for g in (U.geoms if hasattr(U,'geoms') else [U]):
    x,y=g.exterior.xy; ax.plot(x,y,'k-',lw=.7)
    for h in g.interiors: x,y=h.xy; ax.plot(x,y,'r-',lw=.7)
ax.set_aspect('equal'); ax.grid(True,lw=.3); ax.set_xticks(range(-24,25,2)); ax.tick_params(labelsize=6)
plt.savefig(sys.argv[3],dpi=110,bbox_inches='tight')
