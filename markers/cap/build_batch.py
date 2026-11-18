import pickle,json,re,zipfile,glob,numpy as np
from shapely.geometry import box,Polygon,MultiPoint
from shapely.ops import unary_union
G=pickle.load(open('frog_polys.pkl','rb')); O,C,B,Bs=G['O'],G['C'],G['B'],G['Bstrip']
# back of the tower flush with the original's tower back (user: both end at the same point; no back wall needed)
back_y=pickle.load(open('wall_top.pkl','rb')).bounds[3]
O=O.intersection(box(-50,-50,50,back_y))
course,groove,band_skin,band_top=2.96,0.66,0.8,0.3
ceiling=10.536-6.914; wall_top=course*2+groove; tower_top=wall_top+groove
head_clear,head_h,icon_h=0.4,2.0,1.2
# heads: union of the three originals' heads (z top), convex hull, + clearance
H=[]
for f in sorted(glob.glob('/home/viridjan/Projects/root_organizer/reference/*.3mf')):
    z=zipfile.ZipFile(f)
    for n in z.namelist():
        if n.startswith('3D/Objects/'):
            V=np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"',z.read(n).decode()),float)
            if len(V): break
    V=V-[0,0,V[:,2].min()]; H+=V[V[:,2]>12.5][:,:2].tolist()
Hp=MultiPoint(H).convex_hull.buffer(head_clear,join_style='mitre').simplify(0.05)
tx=O.bounds[2]  # not used
T=O.intersection(box(-6.585-2.1,0.426,6.585+2.1,50))
Oin=O.buffer(-groove,join_style='mitre')
core=Bs.intersection(O.buffer(-band_skin,join_style='mitre'))
def pts(g):
    gs=g.geoms if hasattr(g,'geoms') else [g]
    out=[]
    for p in gs:
        c=list(p.exterior.coords)[:-1]; out.append([[round(x,4),round(y,4)] for x,y in c])
    return out
cmds=[]
def sk(name,g,off=0):
    cmds.append({"command":"sketch.create","params":{"plane":"XY","offset":off,"name":name}})
    for p in pts(g): cmds.append({"command":"sketch.line","params":{"closed":True,"points":p,"connect":False}})
    cmds.append({"command":"sketch.finish","params":{}})
def ex(name,sketch,z0,h,op,targets=None,body=None):
    p={"sketch":sketch,"distance":h,"operation":op,"name":name}
    if z0: p["start_offset"]=z0
    if targets: p["targets"]=targets
    if body: p["body_name"]=body
    cmds.append({"command":"solid.extrude","params":p})
# posts: the originals' 5 gray posts (3.39 x 1.42, on the bend faces and the middle inner face), moved out onto the cap's face
from shapely import affinity
from shapely.geometry import Point
Uorig=pickle.load(open('wall_top.pkl','rb')); A=pickle.load(open('above.pkl','rb'))
off=G.get('off',2.1)
posts=[]
for r in A.geoms:
    if r.area>10: continue
    c=np.array(r.minimum_rotated_rectangle.exterior.coords[:4]); e1,e2=c[1]-c[0],c[2]-c[1]
    sh=e1 if np.linalg.norm(e1)<np.linalg.norm(e2) else e2; n=sh/np.linalg.norm(sh)
    cen=np.array(r.centroid.coords[0])
    if Uorig.contains(Point(cen+n*1.0)): n=-n
    rr=r.minimum_rotated_rectangle; L=max(np.linalg.norm(e1),np.linalg.norm(e2))
    t=off
    while affinity.translate(rr,*(n*t)).difference(O).area/L<0.4: t+=0.01   # 0.4 mm proud of the cap face
    posts.append(affinity.translate(rr,*(n*t)))
P=unary_union(posts)
for p in posts: print('post proud %.2f, wall left behind it %.2f'%(p.difference(O).area/3.39, 1.8-(p.intersection(O).area/3.39)))
sk("OuterSketch",O.difference(P)); ex("Course1","OuterSketch",0,course,"new",body="Body")
sk("GrooveSketch",Oin.difference(P)); ex("Groove","GrooveSketch",course,groove,"join",["Body"])
ex("Course2","OuterSketch",course+groove,course,"join",["Body"])
sk("TowerSketch",T); ex("Tower","TowerSketch",wall_top,groove,"join",["Body"])
# tower ledges like the originals' (plinth, middle ledge, cornice, 0.98 mm proud); side faces only, the back stays flush at back_y
tx0,ty0=T.bounds[2],T.bounds[1]; lp=0.98
L2=unary_union([box(sx*tx0-(lp if sx<0 else 0),ty0-0.2,sx*tx0+(lp if sx>0 else 0),back_y) for sx in (1,-1)])
sk("LedgeSketch",L2)
for name,z0,h in (("Plinth",0,1.4),("MidLedge",course+groove/2-0.5,1.0),("Cornice",tower_top-1.34,1.34)):
    ex(name,"LedgeSketch",z0,h,"join",["Body"])
sk("CavitySketch",C); ex("Cavity","CavitySketch",0,ceiling,"cut",["Body"])
sk("HeadPocketSketch",Hp); ex("HeadPocket","HeadPocketSketch",ceiling,head_h+0.3,"cut",["Body"])
sk("PostSketch",P); ex("Posts","PostSketch",0,tower_top,"new",body="Details")
# close each band over the wall top: bend posts joined in pairs (outer + inner face), the middle post runs to the tower
Tb=O.intersection(box(-50,0.426,50,50))
caps=[]
for sx in (1,-1):
    pair=[p for p in posts if p.centroid.x*sx>1]
    caps.append(unary_union(pair).convex_hull)
mid=[p for p in posts if abs(p.centroid.x)<1][0]
caps.append(unary_union([mid,affinity.translate(mid,0,20)]).convex_hull.difference(Tb))
K=unary_union(caps).difference(P)
sk("BandTopSketch",K); ex("BandTops","BandTopSketch",wall_top,groove,"new",body="Tops")
cmds.append({"command":"solid.combine","params":{"target":"Details","tools":[f"Details ({i})" for i in range(2,6)]+["Tops","Tops (2)","Tops (3)"],"operation":"join","name":"DetailsJoin"}})
cy=7.0
cmds+= [{"command":"sketch.create","params":{"plane":"XY","offset":tower_top,"name":"FrogSketch"}},
 {"command":"sketch.ellipse","params":{"center":[0,cy-0.8],"major":[5.2,cy-0.8],"minor_radius":3.6,"axes":False}},
 {"command":"sketch.circle.center","params":{"center":[-3.1,cy+2.4],"radius":2.1}},
 {"command":"sketch.circle.center","params":{"center":[3.1,cy+2.4],"radius":2.1}},
 {"command":"sketch.finish","params":{}},
 {"command":"solid.extrude","params":{"sketch":"FrogSketch","distance":icon_h,"operation":"join","targets":["Details"],"name":"FrogHead"}},
 {"command":"sketch.create","params":{"plane":"XY","offset":tower_top,"name":"FrogEyesSketch"}},
 {"command":"sketch.circle.center","params":{"center":[-3.1,cy+2.6],"radius":0.8}},
 {"command":"sketch.circle.center","params":{"center":[3.1,cy+2.6],"radius":0.8}},
 {"command":"sketch.finish","params":{}},
 {"command":"solid.extrude","params":{"sketch":"FrogEyesSketch","distance":icon_h+1,"operation":"cut","targets":["Details"],"name":"FrogEyes"}},
 {"command":"sketch.create","params":{"plane":"XY","offset":tower_top,"name":"FrogMouthSketch"}},
 {"command":"sketch.arc.three_point","params":{"start":[-2.7,cy-1.1],"through":[0,cy-2.4],"end":[2.7,cy-1.1]}},
 {"command":"sketch.finish","params":{}},
 {"command":"solid.extrude","params":{"sketch":"FrogMouthSketch","thin":True,"thickness":0.8,"distance":icon_h+1,"operation":"cut","targets":["Details"],"name":"FrogMouth"}},
 {"command":"measure","params":{"summary":True}}]
json.dump({"commands":cmds},open('/tmp/solidcraft-mcp-31882-249d7689/frog/cap_batch.json','w'))
print(len(cmds),'steps; ceiling',round(ceiling,3),'wall_top',wall_top,'tower_top',tower_top,'head pocket bounds',[round(v,2) for v in Hp.bounds],'tower bounds',[round(v,2) for v in T.bounds])
