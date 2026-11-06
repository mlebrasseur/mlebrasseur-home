#!/usr/bin/env python3
"""Procedural geometry for V1–V4. Run via generate.py.

VERSION is injected into an isolated namespace for each configuration.
Shared construction code and explicit branches preserve the approved layouts.
Sources: SRC-2026-094, 098, 100, 102, 104, 105.
"""
import base64, gzip, hashlib, json, math, random, struct, zlib
from pathlib import Path
VERSION = globals().get("VERSION", 4)
assert VERSION in (1, 2, 3, 4)

INCH = 0.0254

W, D, H = 89.0, 86.5, 85.0

if VERSION == 2:

    LINEN_Z = D - 15.75

    VANITY_END = LINEN_Z - .75

    DOOR_PIVOT = (47.8, .9)

    MIRROR_DOOR = False

elif VERSION == 3:

    LW, LD, LH = 400/25.4, 350/25.4, 1400/25.4

    REAR_GAP = 5.0

    LINEN_END = D - REAR_GAP

    LINEN_Z = LINEN_END - LW

    VW, VD, VH = 894/25.4, 495/25.4, 500/25.4

    TW, TD, TH = 900/25.4, 500/25.4, 50/25.4

    HAMPER_END = .625 + 19.5

    FURNITURE_GAP = (LINEN_Z - HAMPER_END - TW)/2

    VANITY_END = LINEN_Z - FURNITURE_GAP

    TY = 34.0

    VB = TY - TH - VH

    LB = VB

    VZ = VANITY_END - (TW+VW)/2

    VC_END = VZ + VW

    TZ = VANITY_END - TW

    TCZ = VANITY_END - TW/2

    OZ = TZ - 3.0

    LINEN_PIVOT = (LD-18/25.4, LINEN_END-.2)

    DOOR_PIVOT = (47.8, .9)

    MIRROR_DOOR = False

elif VERSION == 4:

    LINEN_WIDTH, LINEN_DEPTH, LINEN_HEIGHT = 15.75, 14.1875, 70.875

    REAR_GAP = 5.0

    LINEN_END = D - REAR_GAP

    LINEN_Z = LINEN_END - LINEN_WIDTH

    LINEN_PIVOT = (14.22, LINEN_Z+15.25)

    VW, VD, VH = 894/25.4, 456/25.4, 820/25.4

    TW, TD, TH = 915/25.4, 465/25.4, 20/25.4

    HAMPER_END = .625 + 19.5

    FURNITURE_GAP = (LINEN_Z-HAMPER_END-TW)/2

    VANITY_END = LINEN_Z-FURNITURE_GAP

    TZ = VANITY_END-TW

    TCZ = TZ+TW/2

    VZ = TCZ-VW/2

    VC_END = VZ+VW

    TY = VH+TH

    OZ = TZ-3.0

    DOOR_PIVOT = (47.8, .9)

    MIRROR_DOOR = False

OUT = Path(__file__).resolve().parent / 'dist'

MATERIALS = []

MESHES = []

NODES = []

ACCESSORS = []

VIEWS = []

IMAGES = []

TEXTURES = []

BIN = bytearray()

OFFSET = (0, 0, 0)

def blob(data, target=None):
    BIN.extend(b'\0' * ((-len(BIN)) % 4))
    v = {'buffer': 0, 'byteOffset': len(BIN), 'byteLength': len(data)}
    if target:
        v['target'] = target
    VIEWS.append(v)
    BIN.extend(data)
    return len(VIEWS) - 1

def array(values, size):
    view = blob(struct.pack('<' + 'f' * len(values), *values), 34962)
    a = {'bufferView': view, 'componentType': 5126, 'count': len(values)//size,
         'type': {2: 'VEC2', 3: 'VEC3'}[size]}
    if size == 3:
        a.update(min=[min(values[i::3]) for i in range(3)],
                 max=[max(values[i::3]) for i in range(3)])
    ACCESSORS.append(a)
    return len(ACCESSORS) - 1

def png(w, h, pixels):
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t+d) & 0xffffffff)
    raw = b''.join(b'\x00'+bytes(pixels[y*w*3:(y+1)*w*3]) for y in range(h))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')

def texture(kind):
    rng = random.Random(285)
    n = 256
    pixels = []
    for y in range(n):
        for x in range(n):
            if kind == 'epoxy':
                noise = rng.uniform(-2,2)
                c = 244 + noise
                if rng.random() < 0.016:
                    c = rng.choice([110,145,175,195])
                pixels.extend([int(c),int(c),int(c-1)])
            elif kind == 'painted wood':
                # Subtle lengthwise grain under satin white paint, not a product swatch.
                wave=x+1.8*math.sin(y*.032)+.6*math.sin(y*.11)
                grain=2.8*math.sin(wave*1.8)+1.8*math.sin(wave*.42)
                c=244+grain+rng.uniform(-.6,.6)
                pixels.extend([int(c),int(c),int(c-1)])
            elif kind == 'SMC':
                c=246+rng.uniform(-3.5,3.5)
                pixels.extend([int(c),int(c),int(c)])
            else:
                # Sparse irregular veins; illustrative stone, not a retailer swatch.
                f = x*1.2-y*.7+18*math.sin(y*.025)+9*math.sin(y*.08)+2*math.sin(y*.39)
                distance=min(abs(f-k) for k in [-90,65,205,345])
                vein=math.exp(-distance*distance/1.7)*35
                fine=math.exp(-min(abs(f+6*math.sin(y*.045)-k) for k in [-82,73,213,353])**2/1.1)*12
                c = 246-vein-fine+rng.uniform(-1.1,1.1)
                pixels.extend([int(c),int(c),min(255,int(c+1))])
    view=blob(png(n,n,pixels))
    IMAGES.append({'bufferView':view,'mimeType':'image/png','name':kind})
    TEXTURES.append({'source':len(IMAGES)-1,'sampler':0})
    return len(TEXTURES)-1

def material(name, color, rough=.45, metal=0, alpha=1, tex=None, glow=None):
    # Input colours are linear PBR factors, not CSS hex values.
    p={'baseColorFactor':[*color,alpha],'roughnessFactor':rough,'metallicFactor':metal}
    if tex is not None: p['baseColorTexture']={'index':tex}
    m={'name':name,'pbrMetallicRoughness':p,'doubleSided':True}
    if alpha<1: m['alphaMode']='BLEND'
    if glow: m['emissiveFactor']=glow
    MATERIALS.append(m)
    return len(MATERIALS)-1

floor_mat=material('White epoxy · fine grey flecks (concept)',[.93,.93,.92],.46,tex=texture('epoxy'))

marble=material('Sapphire · pale marble interpretation',[.96,.96,.96],.3,tex=texture('marble'))

wallmat=material('Off-white paint · provisional',[.79,.77,.72],.92)

white=material('Gloss white cabinetry',[.94,.95,.94],.23)

porcelain=material('White porcelain',[.96,.97,.97],.15)

black=material('Matte black hardware',[.016,.02,.022],.38,.25)

shadow=material('Recess shadow',[.19,.22,.23],.85)

if VERSION in (1, 2, 4):

    mirror=material('ALEX mirror · exported approximation',[.63,.72,.75],.07,.93)

elif VERSION == 3:

    mirror=material('BIBO mirror · exported approximation',[.63,.72,.75],.07,.93)

glass=material('Clear shower glass',[.68,.86,.88],.1,.05,.13)

windowglass=material('Window glass · pale daylight',[.67,.8,.84],.18,.1,.58)

if VERSION in (1, 2, 4):

    led=material('ALEX · two inset vertical LED strips',[1,.98,.9],.3,glow=[1,.93,.78])

elif VERSION == 3:

    led=material('BIBO · two inset LED strips',[1,.98,.9],.3,glow=[1,.93,.78])

chrome=material('Drain finish',[.34,.38,.39],.22,.85)

woodtrim=material('Satin white painted wood · illustrative grain',[.94,.94,.91],.55,tex=texture('painted wood'))

groove=material('Painted wood groove shadow',[.66,.67,.64],.75)

smc=material('Malawi white textured SMC',[.95,.95,.94],.68,tex=texture('SMC'))

base=material('Cutaway foundation',[.31,.34,.34],.9)

if VERSION == 1:

    def mesh(name, vertices, normals, uv, mat, group='fixtures', info=''):
        assert len(vertices)==len(normals) and len(vertices)%9==0
        assert len(uv)==len(vertices)*2//3
        assert all(math.isfinite(v) for v in vertices+normals+uv)
        vertices=[v+OFFSET[i%3] for i,v in enumerate(vertices)]
        # Authoring +Z points into the room; glTF +Z points toward the entrance.
        # Reflecting Z changes handedness, so reverse every triangle as well.
        vertices=[vertices[t+k+j]*(-1 if j==2 else 1)*INCH for t in range(0,len(vertices),9) for k in (0,6,3) for j in range(3)]
        normals=[normals[t+k+j]*(-1 if j==2 else 1) for t in range(0,len(normals),9) for k in (0,6,3) for j in range(3)]
        uv=[uv[t+k+j] for t in range(0,len(uv),6) for k in (0,4,2) for j in range(2)]
        pos=array(vertices,3)
        norm=array(normals,3)
        attributes={'POSITION':pos,'NORMAL':norm}
        if 'baseColorTexture' in MATERIALS[mat]['pbrMetallicRoughness']:
            attributes['TEXCOORD_0']=array(uv,2)
        MESHES.append({'name':name,'primitives':[{'attributes':attributes,'material':mat}]})
        NODES.append({'name':name,'mesh':len(MESHES)-1,'extras':{'group':group,'note':info}})

elif VERSION in (2, 3, 4):

    def mesh(name, vertices, normals, uv, mat, group='fixtures', info=''):
        assert len(vertices)==len(normals) and len(vertices)%9==0
        assert len(uv)==len(vertices)*2//3
        assert all(math.isfinite(v) for v in vertices+normals+uv)
        vertices=[v+OFFSET[i%3] for i,v in enumerate(vertices)]
        if MIRROR_DOOR:
            # Reflect the original left-hinged assembly across the doorway centre.
            vertices=[65.5-v if i%3==0 else v for i,v in enumerate(vertices)]
            normals=[-v if i%3==0 else v for i,v in enumerate(normals)]
            vertices=[vertices[t+k+j] for t in range(0,len(vertices),9) for k in (0,6,3) for j in range(3)]
            normals=[normals[t+k+j] for t in range(0,len(normals),9) for k in (0,6,3) for j in range(3)]
            uv=[uv[t+k+j] for t in range(0,len(uv),6) for k in (0,4,2) for j in range(2)]
            if name.startswith(('Shaker door', 'Weiser Breton', 'Door hinge door leaf')):
                # Export the right-hinged door closed; viewer animates about its hinge.
                group='entrance_door'
        # Authoring +Z points into the room; glTF +Z points toward the entrance.
        # Reflecting Z changes handedness, so reverse every triangle as well.
        vertices=[vertices[t+k+j]*(-1 if j==2 else 1)*INCH for t in range(0,len(vertices),9) for k in (0,6,3) for j in range(3)]
        normals=[normals[t+k+j]*(-1 if j==2 else 1) for t in range(0,len(normals),9) for k in (0,6,3) for j in range(3)]
        uv=[uv[t+k+j] for t in range(0,len(uv),6) for k in (0,4,2) for j in range(2)]
        pos=array(vertices,3)
        norm=array(normals,3)
        attributes={'POSITION':pos,'NORMAL':norm}
        if 'baseColorTexture' in MATERIALS[mat]['pbrMetallicRoughness']:
            attributes['TEXCOORD_0']=array(uv,2)
        MESHES.append({'name':name,'primitives':[{'attributes':attributes,'material':mat}]})
        NODES.append({'name':name,'mesh':len(MESHES)-1,'extras':{'group':group,'note':info}})

def box(name, center, size, mat=white, group='fixtures', radius=0, info=''):
    # Subdivided rounded boxes for porcelain; plain boxes retain exact nominal envelopes.
    verts=[]; norms=[]; uv=[]
    radius=min(radius,min(size)/2)
    steps=6 if radius else 1
    for axis, sign, uaxis, vaxis in [(0,1,2,1),(0,-1,1,2),(1,1,0,2),(1,-1,2,0),(2,1,1,0),(2,-1,0,1)]:
        grid=[]
        for j in range(steps+1):
            for i in range(steps+1):
                def coord(k,t):
                    h=size[k]/2
                    if not radius: return (t/steps-.5)*size[k]
                    return [-h,-h+radius*(1-.7071),-h+radius,0,h-radius,h-radius*(1-.7071),h][t]
                q=[0.,0.,0.];q[axis]=sign*size[axis]/2;q[uaxis]=coord(uaxis,i);q[vaxis]=coord(vaxis,j)
                if radius:
                    inside=[max(-size[k]/2+radius,min(size[k]/2-radius,q[k])) for k in range(3)]
                    delta=[q[k]-inside[k] for k in range(3)]; length=math.sqrt(sum(d*d for d in delta))
                    normal=[d/length for d in delta];q=[inside[k]+normal[k]*radius for k in range(3)]
                else:
                    normal=[0.,0.,0.];normal[axis]=sign
                scale=96 if mat==marble else 24
                grid.append(([q[k]+center[k] for k in range(3)],normal,[(q[uaxis]+center[uaxis])/scale,(q[vaxis]+center[vaxis])/scale]))
        for j in range(steps):
            for i in range(steps):
                a=j*(steps+1)+i;b=a+1;c=a+steps+1;d=c+1
                # Fix orientation by comparing the generated triangle against its outward normal.
                for ids in [(a,b,d),(a,d,c)]:
                    pts=[grid[k][0] for k in ids]
                    ab=[pts[1][k]-pts[0][k] for k in range(3)];ac=[pts[2][k]-pts[0][k] for k in range(3)]
                    cross=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]]
                    if sum(cross[k]*grid[ids[0]][1][k] for k in range(3))<0: ids=ids[::-1]
                    for k in ids:
                        p,n,t=grid[k];verts.extend(p);norms.extend(n);uv.extend(t)
    mesh(name,verts,norms,uv,mat,group,info)

def bounds(name,x0,x1,y0,y1,z0,z1,mat=white,group='fixtures',radius=0,info=''):
    box(name,[(x0+x1)/2,(y0+y1)/2,(z0+z1)/2],[x1-x0,y1-y0,z1-z0],mat,group,radius,info)

def prism_xy(name, points, z0, z1, mat, group='wall_front', horizontal_grain=False):
    vs=[];ns=[];uv=[]
    def triangle(a,b,c,n):
        ab=[b[k]-a[k] for k in range(3)];ac=[c[k]-a[k] for k in range(3)]
        cross=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]]
        if sum(cross[k]*n[k] for k in range(3))<0:b,c=c,b
        for q in (a,b,c):
            vs.extend(q);ns.extend(n)
            uv.extend([q[1]/5,q[0]/28] if horizontal_grain else [q[0]/5,q[1]/28])
    for z,n in [(z0,[0,0,-1]),(z1,[0,0,1])]:
        for j in range(1,len(points)-1):triangle([*points[0],z],[*points[j],z],[*points[j+1],z],n)
    for j,a in enumerate(points):
        b=points[(j+1)%len(points)];dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy);n=[dy/length,-dx/length,0]
        triangle([*a,z0],[*b,z0],[*b,z1],n);triangle([*a,z0],[*b,z1],[*a,z1],n)
    mesh(name,vs,ns,uv,mat,group)

def ellipsoid(name,center,size,mat=porcelain,group='fixtures'):
    v=[];n=[];uv=[];rows=20;cols=36
    def point(i,j):
        a=math.pi*i/rows;b=2*math.pi*j/cols
        unit=[math.sin(a)*math.cos(b),math.cos(a),math.sin(a)*math.sin(b)]
        p=[center[k]+unit[k]*size[k]/2 for k in range(3)]
        normal=[unit[k]/size[k] for k in range(3)];l=math.sqrt(sum(t*t for t in normal));normal=[t/l for t in normal]
        return p,normal,[j/cols,i/rows]
    for i in range(rows):
        for j in range(cols):
            for a,b in [(i,j),(i+1,j+1),(i+1,j),(i,j),(i,j+1),(i+1,j+1)]:
                p,normal,t=point(a,b);v.extend(p);n.extend(normal);uv.extend(t)
    mesh(name,v,n,uv,mat,group)

def rod(name,start,end,r=.16,mat=black,group='fixtures'):
    # Closed cylinders between arbitrary points.
    d=[end[i]-start[i] for i in range(3)];l=math.sqrt(sum(t*t for t in d));d=[t/l for t in d]
    helper=[0,1,0] if abs(d[1])<.9 else [1,0,0]
    a=[d[1]*helper[2]-d[2]*helper[1],d[2]*helper[0]-d[0]*helper[2],d[0]*helper[1]-d[1]*helper[0]]
    l=math.sqrt(sum(t*t for t in a));a=[t/l for t in a]
    b=[d[1]*a[2]-d[2]*a[1],d[2]*a[0]-d[0]*a[2],d[0]*a[1]-d[1]*a[0]]
    v=[];n=[];uv=[]
    for i in range(16):
        ns=[[math.cos(t)*a[k]+math.sin(t)*b[k] for k in range(3)] for t in [2*math.pi*i/16,2*math.pi*(i+1)/16]]
        points=[[endp[k]+r*normal[k] for k in range(3)] for endp,normal in [(start,ns[0]),(end,ns[0]),(end,ns[1]),(start,ns[1])]]
        for idx in [0,1,2,0,2,3]:v.extend(points[idx]);n.extend(ns[0 if idx<2 else 1]);uv.extend([0,0])
        for endp,ids,sgn in [(start,[3,0],-1),(end,[1,2],1)]:
            for p in [endp,points[ids[0]],points[ids[1]]]:v.extend(p);n.extend([t*sgn for t in d]);uv.extend([0,0])
    mesh(name,v,n,uv,mat,group)

def handle(name,x,y,z,length=5,vertical=False):
    if vertical:
        bounds(name,x,x+.35,y-length/2,y+length/2,z-.15,z+.15,black)
        for yy in [y-length/2+.4,y+length/2-.4]:bounds(name+' mount',x-.8,x,yy-.16,yy+.16,z-.2,z+.2,black)
    else:
        bounds(name,x,x+.35,y-.15,y+.15,z-length/2,z+length/2,black)
        for zz in [z-length/2+.4,z+length/2-.4]:bounds(name+' mount',x-.8,x,y-.2,y+.2,zz-.16,zz+.16,black)

bounds('Floor slab',-4.5,W+4.5,-4,-.12,-4.5,D+4.5,base,'floor')

bounds('White speckled epoxy floor',0,W,-.12,0,0,D,floor_mat,'floor')

bounds('Left wall',-4.5,0,0,H,0,D,wallmat,'wall_left')

for name,y0,y1,z0,z1 in [('below niche',0,40,0,48),('above niche',64,H,0,48),('front return',40,64,0,18),('back return',40,64,30,48),('toilet end',0,H,48,D)]:
    bounds('Right wall · '+name,W,W+4.5,y0,y1,z0,z1,wallmat,'wall_right')

if VERSION in (2, 3, 4):

    MIRROR_DOOR = True

frosted=material('Door · frosted laminated glass approximation',[.62,.72,.71],.94)

for name,x0,x1,y0,y1 in [('hinge stile',17.75,22.25,0,80),('latch stile',43.25,47.75,0,80),
                        ('top rail',22.25,43.25,75.5,80),('bottom rail',22.25,43.25,0,8)]:
    bounds('Shaker door '+name,x0,x1,y0,y1,-.6875,.6875,white,'wall_front',radius=.06)

bounds('Shaker door frosted pane',22.25,43.25,8,75.5,-.13,.13,frosted,'wall_front')

for y in [8,40,72]:
    rod('Door hinge barrel',(17.7,y-1.2,.9),(17.7,y+1.2,.9),.16,black,'wall_front')
    bounds('Door hinge jamb leaf',16.8,17.6,y-1.15,y+1.15,.76,.84,black,'wall_front')
    bounds('Door hinge door leaf',17.8,18.6,y-1.15,y+1.15,.69,.77,black,'wall_front')

for face in [-1,1]:
    z0,z1=sorted([face*.69,face*.92])
    bounds('Weiser Breton square rose',44.0625,46.6875,34.8375,37.4625,z0,z1,black,'wall_front',radius=.09)
    rod('Weiser Breton round hub',(45.375,36.15,face*.92),(45.375,36.15,face*1.2),.65,black,'wall_front')
    rod('Weiser Breton spindle',(45.375,36.15,face*1.2),(45.375,36.15,face*2.95),.36,black,'wall_front')
    z0,z1=sorted([face*2.92,face*3.2655])
    bounds('Weiser Breton flat lever',41.15,45.8,35.68,36.62,z0,z1,black,'wall_front',radius=.12)

bounds('Weiser Breton interior privacy turn',45.22,45.53,35.8,36.5,3.2655,3.4055,black,'wall_front',radius=.07)

rod('Weiser Breton exterior emergency release',(45.375,36.15,-3.266),(45.375,36.15,-3.28),.085,shadow,'wall_front')

if VERSION in (2, 3, 4):

    MIRROR_DOOR = False

bounds('Above-bin robe hook mount',88.6,89,63.4,64.6,54.9,56.1,black,'wall_right')

bounds('Above-bin robe hook arm',87,88.6,63.8,64.2,55.2,55.8,black,'wall_right')

bounds('Above-bin robe hook tip',86.7,87.1,64,65.1,55.2,55.8,black,'wall_right')

for name,x0,x1,y0,y1 in [('below window',0,W,0,64),('above window',0,W,76,H),('left return',0,19,64,76),('right return',49,W,64,76)]:
    bounds('Back wall · '+name,x0,x1,y0,y1,D,D+4.5,wallmat,'wall_back')

for name,x0,x1,y0,y1 in [('left return',0,17.125,0,H),('right return',48.375,W,0,H),('header',17.125,48.375,80.75,H)]:
    bounds('Entrance wall · '+name,x0,x1,y0,y1,-4.5,0,wallmat,'wall_front')

bounds('Ceiling · hidden initially',0,W,H,H+3,0,D,wallmat,'ceiling')

for name,x0,x1,y0,y1 in [('left',17.125,17.625,0,80.75),('right',47.875,48.375,0,80.75),
                        ('head',17.625,47.875,80.125,80.75)]:
    bounds('Entrance jamb '+name,x0,x1,y0,y1,-4.5,.75,white,'wall_front')

for name,x0,x1,y0,y1 in [('left',17.625,18,0,80.125),('right',47.5,47.875,0,80.125),
                        ('head',17.625,47.875,79.75,80.125)]:
    bounds('Entrance door stop '+name,x0,x1,y0,y1,-1.15,-.70,white,'wall_front',radius=.025)

for face,z0,z1 in [('inside',.75,1.375),('outside',-5.125,-4.5)]:
    outward=1 if face=='inside' else -1
    front=z1 if outward==1 else z0
    backing=front-outward*.10
    for name,poly in [('left',[(15.25,0),(17.75,0),(17.75,80),(15.25,82.5)]),
                      ('right',[(47.75,0),(50.25,0),(50.25,82.5),(47.75,80)]),
                      ('head',[(15.25,82.5),(17.75,80),(47.75,80),(50.25,82.5)])]:
        prism_xy('Entrance casing '+face+' '+name,poly,min(backing,z0 if outward==1 else z1),max(backing,z0 if outward==1 else z1),woodtrim,horizontal_grain=name=='head')
    # Build raised face bands around two 0.075-inch wide, 0.10-inch deep grooves.
    for i,(d0,d1) in enumerate([(0,.45),(.45,.525),(.525,.85),(.85,.925),(.925,2.5)]):
        recessed=i in (1,3);depth=backing+outward*.012 if recessed else front
        mat=groove if recessed else woodtrim
        for name,poly in [('left',[(15.25+d0,0),(15.25+d1,0),(15.25+d1,82.5-d1),(15.25+d0,82.5-d0)]),
                          ('right',[(50.25-d1,0),(50.25-d0,0),(50.25-d0,82.5-d0),(50.25-d1,82.5-d1)]),
                          ('head',[(15.25+d0,82.5-d0),(15.25+d1,82.5-d1),(50.25-d1,82.5-d1),(50.25-d0,82.5-d0)])]:
            prism_xy(('Casing recessed line ' if recessed else 'Casing wood face ')+face+' '+name+' '+str(i),poly,min(backing,depth),max(backing,depth),mat,horizontal_grain=name=='head')

for x in [18,50]:bounds('Window side trim',x-.7,x+.7,63,77,D-.7,D+.1,white,'wall_back')

for y in [63,77]:bounds('Window horizontal trim',17.3,50.7,y-.7,y+.7,D-.7,D+.1,white,'wall_back')

bounds('Window sill',17.3,50.7,62.7,63.4,D-2,D+.3,white,'wall_back')

for x in [19.4,34,48.6]:bounds('Window sliding frame',x-.35,x+.35,64,76,D+.2,D+.9,white,'wall_back')

for y in [64.4,75.6]:bounds('Window sliding frame',19,49,y-.35,y+.35,D+.2,D+.9,white,'wall_back')

bounds('Two-pane window glass',19.5,48.5,64.8,75.2,D+.5,D+.6,windowglass,'wall_back')

if VERSION == 1:

    bounds('Left skirting',0,.45,0,3,17.75,D-1215/25.4,white,'wall_left')

    bounds('Back skirting',18.5,W,0,3,D-.45,D,white,'wall_back')

elif VERSION == 2:

    bounds('Left skirting',0,.45,0,3,0,VANITY_END-1215/25.4,white,'wall_left')

    bounds('Back skirting',14.1875,W,0,3,D-.45,D,white,'wall_back')

elif VERSION == 3:

    bounds('Left skirting',0,.45,0,3,0,D,white,'wall_left')

    bounds('Back skirting',14.1875,W,0,3,D-.45,D,white,'wall_back')

elif VERSION == 4:

    bounds('Left skirting',0,.45,0,3,0,TZ,white,'wall_left')

    bounds('Back skirting',14.1875,W,0,3,D-.45,D,white,'wall_back')

bounds('Right skirting',W-.45,W,0,3,48,D,white,'wall_right')

if VERSION == 1:

    LINEN_GAP=2.0

    OFFSET=(0,0,LINEN_GAP)

    bounds('LF1614-62GWH linen cabinet',0,14.1875,0,70.875,0,15.75,white,radius=.1,
           info='Body 15.75 wide by 14.1875 deep. Reversible doors per manufacturer; right hinges requested. Two-inch front-wall gap is provisional; verify actual hinge travel/clearance.')

    bounds('Linen toe recess',.1,13.2,0,2.6,.2,15.55,shadow)

    for y0,y1 in [(3,35.7),(35.9,70.6)]:
        bounds('Linen cabinet door · right hinged',14.2,14.7,y0,y1,.2,15.55,white,radius=.1)
        # Facing -X, left is toward the rear (high Z); hinges are toward the front.
        handle('Linen left-side handle',15.4,(y0+y1)/2,14.15,6,True)
        for y in [y0+4,y1-4]:
            bounds('Linen right hinge · schematic',14.18,14.26,y-.7,y+.7,.35,.65,chrome)

elif VERSION == 2:

    OFFSET=(0,0,LINEN_Z)

    bounds('LF1614-62GWH linen cabinet',0,14.1875,0,70.875,0,15.75,white,radius=.1,
           info='Body 15.75 wide by 14.1875 deep. Reversible doors per manufacturer; hinges right/rear, handles left/front when facing cabinet. Rear-left wall contact; 0.75-inch gap to vanity top is provisional. Verify hinge travel beside vanity.')

    bounds('Linen toe recess',.1,13.2,0,2.6,.2,15.55,shadow)

    for y0,y1 in [(3,35.7),(35.9,70.6)]:
        bounds('Linen cabinet door · right hinged',14.2,14.7,y0,y1,.2,15.55,white,radius=.1)
        # Facing the left wall from the room: screen-right is rear (+Z), left is front (-Z).
        handle('Linen left-side handle',15.4,(y0+y1)/2,1.6,6,True)
        for y in [y0+4,y1-4]:
            bounds('Linen right hinge · schematic',14.18,14.26,y-.7,y+.7,15.1,15.4,chrome)

elif VERSION == 3:

    OFFSET=(0,LB,LINEN_Z)

    bounds('LW1614-84GWH linen back',0,16/25.4,0,LH,0,LW,white)

    for z0,z1 in [(0,16/25.4),(LW-16/25.4,LW)]:
        bounds('Linen side carcass',0,LD-18/25.4,0,LH,z0,z1,white,radius=.04)

    for y0 in [0,LH-16/25.4,LH/3,2*LH/3]:
        bounds('Linen shelf',0,LD-18/25.4,y0,y0+16/25.4,0,LW,white)

    for y0,y1 in [(.08,LH/2-.3),(LH/2+.3,LH-.08)]:
        bounds('Linen cabinet door · right hinged',LD-18/25.4,LD,y0,y1,.06,LW-.06,white,radius=.04)
        for y in [y0+3,y1-3]:
            bounds('Linen right hinge · schematic',LD-18/25.4-.08,LD-18/25.4+.08,y-.6,y+.6,LW-.45,LW-.12,chrome)

    bounds('Linen recessed horizontal grip',LD-.9,LD-.72,LH/2-.3,LH/2+.3,.06,LW-.06,white)

elif VERSION == 4:

    OFFSET=(0,0,LINEN_Z)

    bounds('LF1614-62GWH linen cabinet',0,14.1875,0,70.875,0,15.75,white,radius=.1,
           info='Body 15.75 wide by 14.1875 deep. Reversible doors per manufacturer; hinges right/rear, handles left/front when facing cabinet. 5-inch rear-wall gap and equal approximately 4.80-inch gaps around vanity top; placement is provisional. Verify actual hinges on site.')

    bounds('Linen toe recess',.1,13.2,0,2.6,.2,15.55,shadow)

    for y0,y1 in [(3,35.7),(35.9,70.6)]:
        bounds('Linen cabinet door · right hinged',14.2,14.7,y0,y1,.2,15.55,white,radius=.1)
        # Facing the left wall from the room: screen-right is rear (+Z), left is front (-Z).
        handle('Linen left-side handle',15.4,(y0+y1)/2,1.6,6,True)
        for y in [y0+4,y1-4]:
            bounds('Linen right hinge · schematic',14.18,14.26,y-.7,y+.7,15.1,15.4,chrome)

OFFSET=(0,0,0)

bounds('Rectangular ventilation grille frame',1.1,13.1,75,81,0,.3,white,'wall_front',radius=.1)

bounds('Ventilation grille dark opening',1.6,12.6,75.5,80.5,.3,.32,shadow,'wall_front')

for y in [75.7+i*.55 for i in range(9)]:
    bounds('Ventilation grille louvre',1.65,12.55,y,y+.16,.33,.53,white,'wall_front')

def quad(name,points,mat):
    vs=[];ns=[];uv=[]
    for ids in [(0,1,2),(0,2,3)]:
        a,b,c=[points[i] for i in ids];ab=[b[k]-a[k] for k in range(3)];ac=[c[k]-a[k] for k in range(3)]
        n=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]];l=math.sqrt(sum(t*t for t in n));n=[t/l for t in n]
        for i in ids:vs.extend(points[i]);ns.extend(n);uv.extend([0,0])
    mesh(name,vs,ns,uv,mat)

if VERSION == 1:

    VW,VD,VH=1194/25.4,456/25.4,820/25.4

    TW,TD,TH=1215/25.4,465/25.4,20/25.4

    VZ=D-VW

    TZ=D-TW

    TCZ=D-TW/2

    TY=VH+TH

    bounds('VF4818-62GWH vanity back',0,16/25.4,0,VH,VZ,D,white,radius=.06)

    for z0,z1 in [(VZ,VZ+16/25.4),(D-16/25.4,D)]:
        bounds('Vanity side carcass',0,VD-16/25.4,0,VH,z0,z1,white,radius=.06)

    bounds('Vanity bottom carcass',0,VD-16/25.4,4.0,4.63,VZ,D,white)

    bounds('Vanity toe kick',.3,VD-1.3,0,4,VZ+.1,D-.1,white)

    DW=296/25.4

    DZ=(VW-2*DW)/2

    for z0,z1 in [(VZ+.08,VZ+DW-.04),(D-DW+.04,D-.08)]:
        for i in range(3):
            y0=4.1+i*(VH-4.2)/3;y1=4.1+(i+1)*(VH-4.2)/3-.08
            bounds('Vanity drawer · six total',VD-16/25.4,VD,y0,y1,z0,z1,white,radius=.06)
            handle('Drawer pull',VD+.7,(y0+y1)/2,(z0+z1)/2,6.3)

    for z0,z1,pull in [(VZ+DW+.04,VZ+VW/2-.05,VZ+VW/2-1.0),(VZ+VW/2+.05,D-DW-.04,VZ+VW/2+1.0)]:
        bounds('Vanity centre door',VD-16/25.4,VD,4.1,VH-.1,z0,z1,white,radius=.06)
        handle('Centre door pull',VD+.7,VH-5.0,pull,6.3,vertical=True)

    BX0,BX1=113/25.4,393/25.4

    BZ0,BZ1=TCZ-255/25.4,TCZ+255/25.4

    for name,x0,x1,z0,z1 in [('rear deck',0,BX0,TZ,D),('front deck',BX1,TD,TZ,D),('left deck',BX0,BX1,TZ,BZ0),('right deck',BX0,BX1,BZ1,D)]:
        bounds('VT-SQ1207 porcelain '+name,x0,x1,VH,TY,z0,z1,porcelain,radius=.055)

    DCX=225/25.4

elif VERSION == 2:

    VW,VD,VH=1194/25.4,456/25.4,820/25.4

    TW,TD,TH=1215/25.4,465/25.4,20/25.4

    VZ=VANITY_END-VW

    TZ=VANITY_END-TW

    TCZ=VANITY_END-TW/2

    TY=VH+TH

    bounds('VF4818-62GWH vanity back',0,16/25.4,0,VH,VZ,VANITY_END,white,radius=.06)

    for z0,z1 in [(VZ,VZ+16/25.4),(VANITY_END-16/25.4,VANITY_END)]:
        bounds('Vanity side carcass',0,VD-16/25.4,0,VH,z0,z1,white,radius=.06)

    bounds('Vanity bottom carcass',0,VD-16/25.4,4.0,4.63,VZ,VANITY_END,white)

    bounds('Vanity toe kick',.3,VD-1.3,0,4,VZ+.1,VANITY_END-.1,white)

    DW=296/25.4

    DZ=(VW-2*DW)/2

    for z0,z1 in [(VZ+.08,VZ+DW-.04),(VANITY_END-DW+.04,VANITY_END-.08)]:
        for i in range(3):
            y0=4.1+i*(VH-4.2)/3;y1=4.1+(i+1)*(VH-4.2)/3-.08
            bounds('Vanity drawer · six total',VD-16/25.4,VD,y0,y1,z0,z1,white,radius=.06)
            handle('Drawer pull',VD+.7,(y0+y1)/2,(z0+z1)/2,6.3)

    for z0,z1,pull in [(VZ+DW+.04,VZ+VW/2-.05,VZ+VW/2-1.0),(VZ+VW/2+.05,VANITY_END-DW-.04,VZ+VW/2+1.0)]:
        bounds('Vanity centre door',VD-16/25.4,VD,4.1,VH-.1,z0,z1,white,radius=.06)
        handle('Centre door pull',VD+.7,VH-5.0,pull,6.3,vertical=True)

    BX0,BX1=113/25.4,393/25.4

    BZ0,BZ1=TCZ-255/25.4,TCZ+255/25.4

    for name,x0,x1,z0,z1 in [('rear deck',0,BX0,TZ,VANITY_END),('front deck',BX1,TD,TZ,VANITY_END),('left deck',BX0,BX1,TZ,BZ0),('right deck',BX0,BX1,BZ1,VANITY_END)]:
        bounds('VT-SQ1207 porcelain '+name,x0,x1,VH,TY,z0,z1,porcelain,radius=.055)

    DCX=225/25.4

elif VERSION == 3:

    bounds('VW3620-84GWH vanity back',0,16/25.4,VB,VB+VH,VZ,VC_END,white,radius=.04)

    for z0,z1 in [(VZ,VZ+16/25.4),(VC_END-16/25.4,VC_END)]:
        bounds('Vanity side carcass',0,VD-18/25.4,VB,VB+VH,z0,z1,white,radius=.04)

    bounds('Vanity bottom carcass',0,VD-18/25.4,VB,VB+16/25.4,VZ,VC_END,white)

    DW=646/25.4

    for y0,y1 in [(VB+.08,VB+VH/2-.3),(VB+VH/2+.3,VB+VH-.3)]:
        bounds('Vanity drawer · two total',VD-18/25.4,VD,y0,y1,VZ+.04,VZ+DW,white,radius=.04)

    bounds('Vanity right door',VD-18/25.4,VD,VB+.08,VB+VH-.3,VZ+DW+.08,VC_END-.04,white,radius=.04)

    for y0,y1,z0,z1 in [(VB+VH/2-.3,VB+VH/2+.3,VZ+.04,VZ+DW),(VB+VH-.3,VB+VH,VZ+.04,VC_END-.04)]:
        bounds('Vanity recessed grip',VD-.95,VD-.72,y0,y1,z0,z1,white)

    BX0,BX1=110/25.4,410/25.4

    BZ0,BZ1=TCZ-260/25.4,TCZ+260/25.4

    for name,x0,x1,z0,z1 in [('rear deck',0,BX0,TZ,VANITY_END),('front deck',BX1,TD,TZ,VANITY_END),('left deck',BX0,BX1,TZ,BZ0),('right deck',BX0,BX1,BZ1,VANITY_END)]:
        bounds('VT-SQ3620 polymarble '+name,x0,x1,TY-TH,TY,z0,z1,porcelain,radius=.04)

    DCX=260/25.4

elif VERSION == 4:

    bounds('VF3618-62GWH vanity back',0,16/25.4,0,VH,VZ,VC_END,white,radius=.06)

    for z0,z1 in [(VZ,VZ+16/25.4),(VC_END-16/25.4,VC_END)]:
        bounds('Vanity side carcass',0,VD-16/25.4,0,VH,z0,z1,white,radius=.06)

    bounds('Vanity bottom carcass',0,VD-16/25.4,100/25.4,116/25.4,VZ,VC_END,white)

    bounds('Vanity toe kick',.3,VD-1.3,0,100/25.4,VZ+.1,VC_END-.1,white)

    DW=296/25.4

    DRAWER_Z=VC_END-DW

    FRONT_BOTTOM=100/25.4

    FRONT_TOP=697/25.4

    bounds('Vanity fixed upper front rail',VD-16/25.4,VD,700/25.4,VH,VZ,VC_END,white,radius=.06)

    for i in range(3):
        y0=FRONT_BOTTOM+i*199/25.4
        y1=y0+197.5/25.4
        bounds('Vanity drawer · three total',VD-16/25.4,VD,y0,y1,DRAWER_Z+.04,VC_END-.04,white,radius=.06)
        handle('Drawer pull',VD+.7,y1-1.3,(DRAWER_Z+VC_END)/2,6.3)

    DOOR_MID=VZ+298/25.4

    for name,z0,z1,pull in [('left',VZ+.04,DOOR_MID-.04,DOOR_MID-1),('right',DOOR_MID+.04,DRAWER_Z-.04,DOOR_MID+1)]:
        bounds('Vanity '+name+' door',VD-16/25.4,VD,FRONT_BOTTOM,FRONT_TOP,z0,z1,white,radius=.06)
        handle('Vanity '+name+' door pull',VD+.7,FRONT_TOP-5,pull,6.3,vertical=True)

    BX0,BX1=115/25.4,395/25.4

    BZ0,BZ1=TCZ-250/25.4,TCZ+250/25.4

    for name,x0,x1,z0,z1 in [('rear deck',0,BX0,TZ,VANITY_END),('front deck',BX1,TD,TZ,VANITY_END),('left deck',BX0,BX1,TZ,BZ0),('right deck',BX0,BX1,BZ1,VANITY_END)]:
        bounds('VT-SQ907 porcelain '+name,x0,x1,VH,TY,z0,z1,porcelain,radius=.055)

    DCX=230/25.4

bottom=TY-125/25.4

if VERSION in (1, 2):

    rings=[]

    for t in [0,.12,.3,.52,.75,1]:
        k=1-.64*t;cx=(BX0+BX1)/2*(1-t)+DCX*t
        hx=(BX1-BX0)/2*k;hz=(BZ1-BZ0)/2*k
        rings.append([(cx-hx,TY-(TY-bottom)*math.sin(t*math.pi/2),TCZ-hz),(cx+hx,TY-(TY-bottom)*math.sin(t*math.pi/2),TCZ-hz),(cx+hx,TY-(TY-bottom)*math.sin(t*math.pi/2),TCZ+hz),(cx-hx,TY-(TY-bottom)*math.sin(t*math.pi/2),TCZ+hz)])

    for i in range(len(rings)-1):
        for j in range(4):quad('VT-SQ1207 curved basin', [rings[i][j],rings[i+1][j],rings[i+1][(j+1)%4],rings[i][(j+1)%4]],porcelain)

    quad('VT-SQ1207 basin floor',rings[-1][::-1],porcelain)

    rod('VT-SQ1207 underside drain boss',(DCX,TY-185/25.4,TCZ),(DCX,TY-145/25.4,TCZ),1.0,porcelain)

elif VERSION == 3:

    upper=[(BX0,TY,BZ0),(BX1,TY,BZ0),(BX1,TY,BZ1),(BX0,TY,BZ1)]

    lower=[(DCX-105/25.4,bottom,TCZ-200/25.4),(DCX+105/25.4,bottom,TCZ-200/25.4),(DCX+105/25.4,bottom,TCZ+200/25.4),(DCX-105/25.4,bottom,TCZ+200/25.4)]

    for j in range(4):quad('VT-SQ3620 sloping basin',[upper[j],lower[j],lower[(j+1)%4],upper[(j+1)%4]],porcelain)

    quad('VT-SQ3620 basin floor',lower[::-1],porcelain)

    rod('VT-SQ3620 underside drain boss',(DCX,bottom-.8,TCZ),(DCX,bottom,TCZ),.9,porcelain)

elif VERSION == 4:

    rings=[]

    for t in [0,.12,.3,.52,.75,1]:
        k=1-.64*t;cx=(BX0+BX1)/2*(1-t)+DCX*t
        hx=(BX1-BX0)/2*k;hz=(BZ1-BZ0)/2*k
        rings.append([(cx-hx,TY-(TY-bottom)*math.sin(t*math.pi/2),TCZ-hz),(cx+hx,TY-(TY-bottom)*math.sin(t*math.pi/2),TCZ-hz),(cx+hx,TY-(TY-bottom)*math.sin(t*math.pi/2),TCZ+hz),(cx-hx,TY-(TY-bottom)*math.sin(t*math.pi/2),TCZ+hz)])

    for i in range(len(rings)-1):
        for j in range(4):quad('VT-SQ907 curved basin', [rings[i][j],rings[i+1][j],rings[i+1][(j+1)%4],rings[i][(j+1)%4]],porcelain)

    quad('VT-SQ907 basin floor',rings[-1][::-1],porcelain)

    rod('VT-SQ907 underside drain boss',(DCX,TY-180/25.4,TCZ),(DCX,TY-145/25.4,TCZ),1.0,porcelain)

rod('Sink drain',(DCX,bottom+.01,TCZ),(DCX,bottom+.08,TCZ),45/50.8,black)

if VERSION in (1, 2):

    ellipsoid('VT-SQ1207 overflow rim',(BX0+.20,TY-.55,TCZ),(.08,.36,22/25.4),chrome)

    ellipsoid('VT-SQ1207 overflow opening',(BX0+.25,TY-.55,TCZ),(.04,.22,.65),shadow)

    FX=55/25.4

elif VERSION == 3:

    bounds('VT-SQ3620 rectangular overflow rim',BX0+.15,BX0+.3,TY-.9,TY-.55,TCZ-.5,TCZ+.5,chrome,radius=.03)

    bounds('VT-SQ3620 overflow opening',BX0+.3,BX0+.32,TY-.82,TY-.63,TCZ-.4,TCZ+.4,shadow)

    FX=55/25.4

elif VERSION == 4:

    ellipsoid('VT-SQ907 overflow rim',(BX0+.20,TY-.55,TCZ),(.08,.36,24/25.4),chrome)

    ellipsoid('VT-SQ907 overflow opening',(BX0+.25,TY-.55,TCZ),(.04,.22,.65),shadow)

    FX=60/25.4

bounds('F-4021-3BK faucet base',FX-.8,FX+.8,TY,TY+.4,TCZ-.8,TCZ+.8,black,radius=.14)

bounds('F-4021-3BK faucet column',FX-.6,FX+.6,TY+.4,TY+5.5,TCZ-.6,TCZ+.6,black,radius=.18)

bounds('Black faucet spout',FX-.6,FX+5,TY+4.7,TY+5.5,TCZ-.6,TCZ+.6,black,radius=.13)

bounds('Black faucet lever',FX-.8,FX+1.5,TY+5.9,TY+6.15,TCZ-.3,TCZ+.3,black,radius=.10)

if VERSION in (1, 2):

    MW, MH, MD = 900/25.4, 700/25.4, 45/25.4

    MCZ, MB = TCZ, 44

    bounds('ALEX 84-ALEX-90 back',0,MD-.2,MB,MB+MH,MCZ-MW/2,MCZ+MW/2,white,radius=.08)

    bounds('ALEX reflective surface',MD-.2,MD,MB,MB+MH,MCZ-MW/2,MCZ+MW/2,mirror)

    for z in [MCZ-MW/2+2.9,MCZ+MW/2-2.9]:
        bounds('ALEX inset vertical LED strip',MD+.02,MD+.04,MB+2.35,MB+MH-2.35,z-.875,z+.875,led)

elif VERSION == 3:

    MW, MH, MD = 600/25.4, 700/25.4, 30/25.4

    MCZ, MB = TCZ, LB+LH-MH

    MFRAME = 0.0

    bounds('BIBO 84-BIBO-24 back',0,MD-.1,MB,MB+MH,MCZ-MW/2,MCZ+MW/2,white,radius=.04)

    bounds('BIBO reflective surface',MD-.1,MD,MB,MB+MH,MCZ-MW/2,MCZ+MW/2,mirror)

    for z in [MCZ-MW/2+50/25.4,MCZ+MW/2-50/25.4]:
        bounds('BIBO inset vertical LED strip',MD+.02,MD+.04,MB+75/25.4,MB+MH-75/25.4,z-20/25.4,z+20/25.4,led)

    TOUCH_Y, TOUCH_Z = MB+1.4, MCZ

    rod('BIBO touch-control ring',(MD+.02,TOUCH_Y,TOUCH_Z),(MD+.04,TOUCH_Y,TOUCH_Z),.30,led)

    rod('BIBO touch-control centre',(MD+.04,TOUCH_Y,TOUCH_Z),(MD+.05,TOUCH_Y,TOUCH_Z),.20,mirror)

elif VERSION == 4:

    MW, MH, MD = 600/25.4, 700/25.4, 30/25.4

    MCZ, MB = TCZ, LINEN_HEIGHT-MH

    MFRAME = 0.0

    bounds('BIBO 84-BIBO-24 back',0,MD-.1,MB,MB+MH,MCZ-MW/2,MCZ+MW/2,white,radius=.04)

    bounds('BIBO reflective surface',MD-.1,MD,MB,MB+MH,MCZ-MW/2,MCZ+MW/2,mirror)

    for z in [MCZ-MW/2+50/25.4,MCZ+MW/2-50/25.4]:
        bounds('BIBO inset vertical LED strip',MD+.02,MD+.04,MB+75/25.4,MB+MH-75/25.4,z-20/25.4,z+20/25.4,led)

    TOUCH_Y, TOUCH_Z = MB+1.4, MCZ

    rod('BIBO touch-control ring',(MD+.02,TOUCH_Y,TOUCH_Z),(MD+.04,TOUCH_Y,TOUCH_Z),.30,led)

    rod('BIBO touch-control centre',(MD+.04,TOUCH_Y,TOUCH_Z),(MD+.05,TOUCH_Y,TOUCH_Z),.20,mirror)

plastic=material('Sterilite white plastic',[.91,.92,.90],.42)

if VERSION == 1:

    HCX, HCZ = 6.75, (LINEN_GAP+15.75+TZ)/2

elif VERSION in (2, 3, 4):

    HCX, HCZ = 6.75, 10.375

def hamper_panel(axis,side,columns):
    v=[];n=[];uv=[]
    half=9.2 if axis==0 else 5.6
    def point(u,y):
        taper=.83+.17*y/23.5
        if axis==0:return [HCX+side*5.6*taper,y,HCZ+u*taper]
        return [HCX+u*taper,y,HCZ+side*9.2*taper]
    normal=[side,0,0] if axis==0 else [0,0,side]
    # A rectangle cell surrounds each oval, with matching rays at the cell boundaries.
    for row in range(9):
        for col in range(columns):
            cw=2*half/columns;ch=21/9
            cu=-half+(col+.5)*cw;cy=1.5+(row+.5)*ch
            rings=[]
            for i in range(24):
                t=2*math.pi*i/24;c=math.cos(t);d=math.sin(t)
                r=min(cw/2/max(abs(c),1e-9),ch/2/max(abs(d),1e-9))
                rings.append((point(cu+c*r,cy+d*r),point(cu+c*cw*.28,cy+d*ch*.39)))
            for i in range(24):
                a,b=rings[i];c,d=rings[(i+1)%24]
                for q in [a,c,d,a,d,b]:v.extend(q);n.extend(normal);uv.extend([0,0])
    mesh('Sterilite oval ventilation panel',v,n,uv,plastic)

for axis in [0,2]:
    for side in [-1,1]:hamper_panel(axis,side,10 if axis==0 else 6)

bounds('Sterilite base',HCX-4.8,HCX+4.8,0,1.5,HCZ-7.8,HCZ+7.8,plastic,radius=.6)

for dx in [-1,1]:
    for dz in [-1,1]:rod('Sterilite rounded corner',(HCX+dx*4.65,1.2,HCZ+dz*7.64),(HCX+dx*5.6,23.3,HCZ+dz*9.2),.24,plastic)

bounds('Sterilite upper rim',HCX-6.125,HCX+6.125,22.5,23.65,HCZ-9.75,HCZ+9.75,plastic,radius=.5)

bounds('Sterilite lift-top lid',HCX-5.9,HCX+5.9,23.68,24.5,HCZ-9.5,HCZ+9.5,plastic,radius=.4)

for z in [HCZ-8.7,HCZ+8.7]:
    bounds('Sterilite integrated grip recess',HCX-2.1,HCX+2.1,23.35,23.67,z-.3,z+.3,shadow,radius=.14)

rod('Sterilite lid hinge',(HCX-2.5,23.7,HCZ+9.25),(HCX+2.5,23.7,HCZ+9.25),.22,plastic)

BASEL,BASEW=47.75,36

PAN_Y=.75

bounds('Alaska KD3329 low base',53,89,0,.55,0,BASEL,smc,radius=.10)

bounds('Shower pan inset',54,88,.55,PAN_Y,1,BASEL-1,smc,radius=.15)

for x0,x1,z0,z1 in [(53,54,0,BASEL),(88,89,0,BASEL),(54,88,0,1),(54,88,BASEL-1,BASEL)]:
    bounds('Shower base rim',x0,x1,.55,1,z0,z1,smc,radius=.08)

SDX,SDZ=89-18.375,8.375

bounds('Malawi end-drain perimeter',SDX-3.5,SDX+3.5,PAN_Y+.001,PAN_Y+.015,SDZ-2.15,SDZ+2.15,shadow,radius=.10)

bounds('Malawi white end-drain cover',SDX-3.36,SDX+3.36,PAN_Y+.015,PAN_Y+.035,SDZ-2.01,SDZ+2.01,smc,radius=.09)

bounds('Sapphire front shower panel',53,89,1,H,0,.3,marble,'wall_front')

for name,y0,y1,z0,z1 in [('below niche',1,40,.3,48),('above niche',64,H,.3,48),('front niche return',40,64,.3,18),('back niche return',40,64,30,48)]:
    bounds('Sapphire right panel · '+name,88.7,89,y0,y1,z0,z1,marble,'wall_right')

bounds('Homevacious vertical niche back',92.15,92.4,40,64,18,30,white,'wall_right')

for y in [40.15,63.85]:bounds('Niche horizontal return',88.5,92.4,y-.15,y+.15,18,30,white,'wall_right')

bounds('Niche horizontal shelf',88.5,92.4,51.85,52.15,18,30,white,'wall_right')

for z in [18.15,29.85]:bounds('Niche vertical side',88.5,92.4,40,64,z-.15,z+.15,white,'wall_right')

SG=8/25.4

SH=1+2000/25.4

SL=1160/25.4

SIDE=852/25.4

GX=89-SIDE

bounds('Shower glass · sliding door concept',GX-.55,GX-.55+SG,1,SH,22.5,SL,glass,'glass')

bounds('Shower glass · fixed long panel',GX,GX+SG,1,SH,.2,23.5,glass,'glass')

bounds('Shower glass · short return',GX,89,1,SH,SL,SL+SG,glass,'glass')

if VERSION == 1:

    for x,z in [(GX,.2),(89,SL)]:bounds('Black shower wall channel',x-.22,x+.22,1,SH,z-.22,z+.22,black,'glass')

    bounds('Black top rail · long',GX-.5,GX+.4,SH-4.0,SH-3.2,.2,SL,black,'glass')

    for z in [25,SL-2.5]:
        bounds('Alaska square roller cover',GX-.76,GX-.4,SH-3.4,SH-1.7,z-.65,z+.65,black,'glass',radius=.04)
        bounds('Alaska lower roller stop',GX-.7,GX-.4,SH-5.1,SH-4.2,z-.45,z+.45,black,'glass')

elif VERSION in (2, 3, 4):

    bounds('Alaska black wall channel · front',GX-.38,GX+.38,1,SH,.05,.85,black,'glass')

    bounds('Alaska black wall channel · side return',88.2,89,1,SH,SL-.3,SL+.3,black,'glass')

    bounds('Alaska black overlap upright',GX-.16,GX+.43,1,SH,22.95,23.65,black,'glass')

    bounds('Alaska black door closing edge',GX-.65,GX-.55+SG+.10,1,SH,SL-.20,SL+.12,black,'glass')

    bounds('Alaska black corner profile',GX-.08,GX+.40,1,SH,SL+.17,SL+.48,black,'glass')

    bounds('Alaska black lower door rail',GX-.65,GX-.55+SG+.10,1,1.38,22.5,SL,black,'glass')

    bounds('Alaska black lower door seal',GX-.65,GX-.55+SG+.10,1.50,1.63,22.5,SL,black,'glass')

    bounds('Black top rail · long',GX-.5,GX+.4,SH-4.2,SH-3.05,.2,SL,black,'glass')

    for z in [25,SL-2.5]:
        bounds('Alaska square roller cover',GX-.76,GX-.4,SH-3.3,SH-1.95,z-.675,z+.675,black,'glass',radius=.04)
        bounds('Alaska lower roller stop',GX-.7,GX-.4,SH-5.0,SH-4.25,z-.375,z+.375,black,'glass')

for z in [2.2,20.8]:bounds('Alaska fixed rail bracket',GX-.6,GX+.4,SH-4.1,SH-3.1,z-.35,z+.35,black,'glass')

bounds('Black lower door guide',GX-.6,GX+.4,1,1.5,22,23.5,black,'glass')

for y in [32,45]:bounds('Shower handle mount',GX-1.65,GX-.55,y-.2,y+.2,SL-3.3,SL-2.7,black,'glass')

bounds('Left-opening door handle',GX-1.85,GX-1.4,31.8,45.2,SL-3.3,SL-2.7,black,'glass')

bounds('Square shower control plate',68,74,40,46,.35,.6,black,'wall_front')

bounds('Square shower control lever',70.4,71.6,39.5,43.5,.6,2,black,'wall_front')

rod('Shower arm',(71,77,.4),(71,77,10),.4,black,'wall_front')

rod('Shower head drop',(71,77,10),(71,75.8,10),.4,black,'wall_front')

bounds('Square black rain head',66,76,75,75.8,5,15,black,'wall_front',radius=.2)

rod('Hand-shower rail',(81,43,1.3),(81,66,1.3),.28,black,'wall_front')

bounds('Black hand shower',80.25,81.75,58,66,1.9,2.7,black,'wall_front',radius=.3)

last=(81,58,2.4)

for i in range(1,25):
    t=i/24;p=(81-7*t,58-24*math.sin(math.pi*t/2),2.4+3*math.sin(math.pi*t))
    rod('Hand shower hose',last,p,.12,black,'wall_front');last=p

hdpe=material('Chormtok black HDPE',[.027,.03,.029],.7)

SX,SZ,SY = 71,8.8,PAN_Y

def stool_leg(cx,cz):
    vertices=[];normals=[];uv=[]
    points=[]
    for y,dx,dz in [(SY+.25,cx*7.1,cz*5.15),(SY+15.5,cx*6.35,cz*4.7)]:
        for x,z in [(-.7,-.55),(.7,-.55),(.7,.55),(-.7,.55)]:points.append([SX+dx+x,y,SZ+dz+z])
    for ids in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:
        for tri in [(ids[0],ids[1],ids[2]),(ids[0],ids[2],ids[3])]:
            a,b,c=[points[i] for i in tri];ab=[b[k]-a[k] for k in range(3)];ac=[c[k]-a[k] for k in range(3)]
            n=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]];l=math.sqrt(sum(v*v for v in n));n=[v/l for v in n]
            for i in tri:vertices.extend(points[i]);normals.extend(n);uv.extend([0,0])
    mesh('Chormtok stool splayed leg',vertices,normals,uv,hdpe)
    rod('Chormtok adjustable foot',(SX+cx*7.1,SY,SZ+cz*5.15),(SX+cx*7.1,SY+.3,SZ+cz*5.15),.45,black)

for cx in [-1,1]:
    for cz in [-1,1]:stool_leg(cx,cz)

x0,x1=SX-8.45,SX+8.45

z0,z1=SZ-6.3,SZ+6.3

holes=[(x0+.7,x0+1.6,z0+2,z1-2)]

holes += [(SX+dx-.13,SX+dx+.13,z0+1.5,z1-1.5) for dx in [-5,-2.5,0,2.5,5]]

holes += [(x1-1.6,x1-.7,z0+2,z1-2)]

last=x0

for lo,hi,near,far in holes:
    bounds('Chormtok slotted seat',last,lo,SY+15.8,SY+16.5,z0,z1,hdpe,radius=.08)
    for a,b in [(z0,near),(far,z1)]:bounds('Chormtok slot end',lo,hi,SY+15.8,SY+16.5,a,b,hdpe,radius=.06)
    last=hi

bounds('Chormtok slotted seat',last,x1,SY+15.8,SY+16.5,z0,z1,hdpe,radius=.08)

for z in [SZ-4.8,SZ+4.8]:bounds('Chormtok seat apron',SX-6.5,SX+6.5,SY+13.5,SY+15.8,z-.3,z+.3,hdpe)

for x in [SX-6.5,SX+6.5]:bounds('Chormtok side apron',x-.3,x+.3,SY+13.5,SY+15.8,SZ-4.8,SZ+4.8,hdpe)

for z in [SZ-4.7,SZ-1.5,SZ+1.7]:bounds('Chormtok lower shelf slat',SX-6.7,SX+6.7,SY+3.2,SY+3.8,z,z+3,hdpe,radius=.08)

for z in [SZ-4.9,SZ+4.9]:bounds('Chormtok shelf rail',SX-6.8,SX+6.8,SY+4.1,SY+4.65,z-.18,z+.18,hdpe,radius=.08)

for x in [SX-6.8,SX+6.8]:bounds('Chormtok shelf side rail',x-.18,x+.18,SY+4.1,SY+4.65,SZ-4.9,SZ+4.9,hdpe,radius=.08)

OFFSET = (0, 0, 3)

def d_ring(front,back,halfwidth,y,zc=68):
    # Rounded front (-X) joins straight sides and a square rear with small corners.
    radius=min(halfwidth,5.8);pts=[]
    for i in range(33):
        a=math.pi/2+math.pi*i/32
        pts.append([front+radius+radius*math.cos(a),y,zc+halfwidth*math.sin(a)])
    pts.extend([[back-.5,y,zc-halfwidth],[back,y,zc-halfwidth+.5],[back,y,zc+halfwidth-.5],[back-.5,y,zc+halfwidth]])
    return pts

def loft_toledo(name,profiles,mat=porcelain):
    rings=[d_ring(*p) for p in profiles];vs=[];ns=[];uv=[]
    def tri(a,b,c):
        ab=[b[k]-a[k] for k in range(3)];ac=[c[k]-a[k] for k in range(3)]
        n=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]];length=math.sqrt(sum(v*v for v in n));n=[v/length for v in n]
        for p in (a,b,c):vs.extend(p);ns.extend(n);uv.extend([0,0])
    for low,high in zip(rings,rings[1:]):
        for j in range(len(low)):
            k=(j+1)%len(low);tri(low[j],high[j],high[k]);tri(low[j],high[k],low[k])
    for ring,reverse in [(rings[0],False),(rings[-1],True)]:
        center=[sum(p[k] for p in ring)/len(ring) for k in range(3)]
        for j in range(len(ring)):
            a,b=ring[j],ring[(j+1)%len(ring)];tri(center,b,a) if reverse else tri(center,a,b)
    mesh(name,vs,ns,uv,mat)

loft_toledo('Toledo concept · skirted body',[(55.2,81,6.2,0),(55.0,81,6.3,.4),(54.5,81,6.8,10),(54.2,81,7.3,15.9),(54.2,81,7.3,16.5)])

loft_toledo('Toledo concept · seat',[(54.25,74.4,7.25,16.6),(54.2,74.4,7.3,17.1),(54.3,74.35,7.2,17.25)])

loft_toledo('Toledo concept · closed lid',[(54.3,74.35,7.2,17.35),(54.25,74.4,7.25,17.6),(54.4,74.25,7.1,17.95)])

bounds('Toledo concept · tank',74.1,81,15.8,28.9,60.7,75.3,porcelain,radius=.7)

bounds('Toledo concept · tank lid',74.1,81,29.0,29.46,60.7,75.3,porcelain,radius=.23)

bounds('Toledo dual flush plate',76.7,78.4,29.46,29.5,66.5,69.5,chrome)

bounds('Toledo split flush button',76.72,78.38,29.499,29.5,67.96,68.04,shadow)

bounds('Behind-toilet storage · provisional',82,89,0,35,58,78,white,radius=.14)

for z0,z1 in [(58.2,67.9),(68.1,77.8)]:bounds('Storage door · provisional',81.5,82,2.5,34.8,z0,z1,white,radius=.1)

for z in [66.4,69.6]:bounds('Storage handle · provisional',80.8,81.2,25,30,z-.13,z+.13,black)

OFFSET = (0, 0, 0)

BR, BH = 17/2.54/2, 26/2.54

rod('GANSJON black bin',(82,0.15,55.5),(82,BH-.55,55.5),BR,black)

rod('GANSJON lid',(82,BH-.5,55.5),(82,BH,55.5),BR,black)

bounds('GANSJON pedal',77.5,79.2,.4,.75,54.4,56.6,black,radius=.15)

bounds('GANSJON rear hinge',84.9,85.7,BH-1.3,BH-.1,54.9,56.1,black,radius=.15)

for z in [54.5,56.5]:rod('GANSJON handle arm',(85,7.5,z),(85.8,7.5,z),.13)

rod('GANSJON rear carry handle',(85.8,7.5,54.5),(85.8,7.5,56.5),.13)

for x in [24,48]:bounds('Towel bar square mount',x-.65,x+.65,49.35,50.65,85,86.5,black)

rod('24-inch towel bar',(24,50,83.5),(48,50,83.5),.2)

for x in [24,48]:rod('Towel bar arm',(x,50,83.5),(x,50,85.5),.2)

for y in [43,49]:rod('Hamper-wall square hand towel ring',(2,y,HCZ-3),(2,y,HCZ+3),.16)

for z in [HCZ-3,HCZ+3]:rod('Hamper-wall square hand towel ring',(2,43,z),(2,49,z),.16)

bounds('Hand towel ring left mount',0,2,48.5,49.5,HCZ-.5,HCZ+.5,black)

linen=material('Illustrative folded towels · warm grey',[.54,.53,.49],.98)

def towel(name,u0,u1,bottom,top,left_wall=False):
    v=[];n=[];uv=[];cols=28;rows=24
    def point(i,j):
        u=u0+(u1-u0)*i/cols;t=j/rows;y=bottom+(top-bottom)*t
        depth=.16*math.sin(i/cols*math.pi*8)*(.3+.7*(1-t))
        return [2.25+depth,y,u] if left_wall else [u,y,83.2-depth]
    for j in range(rows):
        for i in range(cols):
            for indices in [[(i,j),(i+1,j),(i+1,j+1)],[(i,j),(i+1,j+1),(i,j+1)]]:
                pts=[point(*q) for q in indices]
                ab=[pts[1][k]-pts[0][k] for k in range(3)];ac=[pts[2][k]-pts[0][k] for k in range(3)]
                normal=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]]
                length=math.sqrt(sum(q*q for q in normal));normal=[q/length for q in normal]
                for q in pts:v.extend(q);n.extend(normal);uv.extend([0,0])
    mesh(name,v,n,uv,linen)

towel('Bath towel · folded hanging envelope',25,35,24,50)

towel('Bath towel · folded hanging envelope',37,47,24,50)

towel('Hand towel · above hamper',HCZ-2.5,HCZ+2.5,29.5,43,True)

if VERSION == 1:

    OFFSET = (TD/2-33.875, 0, 0)

    bounds('Rear-wall tool outlet plate',32.5,35.25,44.75,49.25,86.15,86.5,white,radius=.1)

    for y in [45.9,48.1]:
        bounds('Outlet receptacle',33,34.75,y-.6,y+.6,86.05,86.15,porcelain,radius=.15)
        for x in [33.45,34.2]:bounds('Outlet slot',x,x+.09,y-.15,y+.22,86.02,86.05,black)
        bounds('Outlet ground',33.78,33.98,y-.46,y-.3,86.02,86.05,black)

    bounds('Outlet test button',33.65,34.05,46.73,46.98,86.02,86.05,shadow)

    bounds('Outlet reset button',33.65,34.05,47.07,47.32,86.02,86.05,shadow)

    OFFSET = (0, 0, 0)

elif VERSION == 2:

    OZ=25.3

    bounds('Vanity-side tool outlet plate',0,.35,44.75,49.25,OZ-1.375,OZ+1.375,white,radius=.1)

    for y in [45.9,48.1]:
        bounds('Outlet receptacle',.35,.45,y-.6,y+.6,OZ-.875,OZ+.875,porcelain,radius=.15)
        for z in [OZ-.425,OZ+.325]:bounds('Outlet slot',.45,.48,y-.15,y+.22,z,z+.09,black)
        bounds('Outlet ground',.45,.48,y-.46,y-.3,OZ-.1,OZ+.1,black)

    bounds('Outlet test button',.45,.48,46.73,46.98,OZ-.2,OZ+.2,shadow)

    bounds('Outlet reset button',.45,.48,47.07,47.32,OZ-.2,OZ+.2,shadow)

    bounds('Light dimmer and vent switch plate',5.25,10,44.75,49.25,0,.25,white,'wall_front',radius=.1,
           info='Side-by-side controls on front wall left of entrance. Facing plate from inside: light dimmer LEFT, ventilation switch RIGHT; schematic 4.75 x 4.5 plate, centre height 47 in. Products and compatibility unselected.')

    bounds('Light dimmer rocker',8.05,9,45.5,48.5,.25,.38,white,'wall_front',radius=.05)

    bounds('Light dimmer slider track',9.15,9.35,45.5,48.5,.25,.39,shadow,'wall_front')

    bounds('Light dimmer slider',9.07,9.43,47.3,47.65,.39,.52,white,'wall_front',radius=.03)

    bounds('Ventilation switch rocker',5.7,7.05,45.5,48.5,.25,.38,white,'wall_front',radius=.05)

    bounds('Ventilation switch indicator',6.2,6.55,45.8,45.9,.38,.4,shadow,'wall_front')

elif VERSION == 3:

    bounds('Vanity-side tool outlet plate',0,.35,44.75,49.25,OZ-1.375,OZ+1.375,white,radius=.1)

    for y in [45.9,48.1]:
        bounds('Outlet receptacle',.35,.45,y-.6,y+.6,OZ-.875,OZ+.875,porcelain,radius=.15)
        for z in [OZ-.425,OZ+.325]:bounds('Outlet slot',.45,.48,y-.15,y+.22,z,z+.09,black)
        bounds('Outlet ground',.45,.48,y-.46,y-.3,OZ-.1,OZ+.1,black)

    bounds('Outlet test button',.45,.48,46.73,46.98,OZ-.2,OZ+.2,shadow)

    bounds('Outlet reset button',.45,.48,47.07,47.32,OZ-.2,OZ+.2,shadow)

    bounds('Light dimmer and vent switch plate',5.25,10,44.75,49.25,0,.25,white,'wall_front',radius=.1,
           info='Side-by-side controls on front wall left of entrance. Facing plate from inside: light dimmer LEFT, ventilation switch RIGHT; schematic 4.75 x 4.5 plate, centre height 47 in. Products and compatibility unselected.')

    bounds('Light dimmer rocker',8.05,9,45.5,48.5,.25,.38,white,'wall_front',radius=.05)

    bounds('Light dimmer slider track',9.15,9.35,45.5,48.5,.25,.39,shadow,'wall_front')

    bounds('Light dimmer slider',9.07,9.43,47.3,47.65,.39,.52,white,'wall_front',radius=.03)

    bounds('Ventilation switch rocker',5.7,7.05,45.5,48.5,.25,.38,white,'wall_front',radius=.05)

    bounds('Ventilation switch indicator',6.2,6.55,45.8,45.9,.38,.4,shadow,'wall_front')

elif VERSION == 4:

    OZ=TZ-3.0

    bounds('Vanity-side tool outlet plate',0,.35,44.75,49.25,OZ-1.375,OZ+1.375,white,radius=.1)

    for y in [45.9,48.1]:
        bounds('Outlet receptacle',.35,.45,y-.6,y+.6,OZ-.875,OZ+.875,porcelain,radius=.15)
        for z in [OZ-.425,OZ+.325]:bounds('Outlet slot',.45,.48,y-.15,y+.22,z,z+.09,black)
        bounds('Outlet ground',.45,.48,y-.46,y-.3,OZ-.1,OZ+.1,black)

    bounds('Outlet test button',.45,.48,46.73,46.98,OZ-.2,OZ+.2,shadow)

    bounds('Outlet reset button',.45,.48,47.07,47.32,OZ-.2,OZ+.2,shadow)

    bounds('Light dimmer and vent switch plate',5.25,10,44.75,49.25,0,.25,white,'wall_front',radius=.1,
           info='Side-by-side controls on front wall left of entrance. Facing plate from inside: light dimmer LEFT, ventilation switch RIGHT; schematic 4.75 x 4.5 plate, centre height 47 in. Products and compatibility unselected.')

    bounds('Light dimmer rocker',8.05,9,45.5,48.5,.25,.38,white,'wall_front',radius=.05)

    bounds('Light dimmer slider track',9.15,9.35,45.5,48.5,.25,.39,shadow,'wall_front')

    bounds('Light dimmer slider',9.07,9.43,47.3,47.65,.39,.52,white,'wall_front',radius=.03)

    bounds('Ventilation switch rocker',5.7,7.05,45.5,48.5,.25,.38,white,'wall_front',radius=.05)

    bounds('Ventilation switch indicator',6.2,6.55,45.8,45.9,.38,.4,shadow,'wall_front')

rod('Rear-wall toilet paper holder',(59,27,83.5),(64.5,27,83.5),.16)

rod('Paper holder rear arm',(59,27,83.5),(59,27,86.5),.16)

bounds('Paper holder square mount',58.4,59.6,26.4,27.6,86,86.5,black)

if VERSION == 1:

    ASSUMPTIONS = [
        'Room: 89 × 86½ in; height 85 in. These are homeowner measurements, not a site survey.',
        'Ordered: Alaska 48 × 36 shower, Sapphire panels, 48 × 18 vanity/top, 16-in linen cabinet, black faucet/accessories, ALEX 36 × 28 mirror and Amazon niche.',
        'Window assumed 30 × 12 in with sill at 64 in; exact size and position are unknown.',
        'Vanity cabinet 1194 × 456 × 820 mm, top 1215 × 465 mm; assembly flush left/rear, top Z=38.67–86.5 in; linen against left wall with 2-in front-wall gap, Z=2–17.75. Reversible doors have handles left/hinges right; actual hinge travel and swing clearance need site checks. Close room door before opening cabinet fully.',
        'ALEX 84-ALEX-90 actual 900 × 700 × 45 mm with two inset vertical LED strips; bottom assumed 44 in. Strip dimensions approximate; live reflection is a viewer effect.',
        'Niche vertical 12 wide × 24 high with horizontal shelf; bottom assumed 40 in. Rough opening and waterproofing remain to verify.',
        'Toledo remains provisional; centre Z=71 in, shifted 3 in rearward as an assumption. Tank back X=81 in; plumbing rough-in unknown.',
        'Behind-toilet storage assumed 7 deep × 20 wide × 35 high; product and access are unconfirmed.',
        'Square shower fixture is a provisional Brigitta-inspired shape. Alaska glass 2000 mm tall above 1-in threshold, 8 mm thick; corner door span 1160 mm and side 852 mm. Detailed hardware is schematic. End drain is provisionally near front beneath removable stool; rough-in unverified. The back half represents the requested left opening when facing from the vanity; panels are shown closed.',
        'Sterilite white lidded hamper: 19.5 × 12.25 × 24.5 in, centred between linen and projecting vanity top at Z=28.208 in, with about 0.708 in clearance each side; hand-towel ring centred directly above; lid and cabinet access unverified.',
        'IKEA GANSJON black bin: 17 cm diameter × 26 cm high, between shower and toilet. Hamper and bin selected for visualization; purchase not reported.',
        'Front-wall ducted ventilation grille above linen assumed 12 × 6 in, bottom 75 in. Duct function and actual grille dimensions unknown.',
        'Rear-wall outlet centered at X=9.154 in above vanity end; hand towel on left wall over hamper; rear towel bar spans X=24–48, paper holder X=59–64.5. Hanging towel envelopes are illustrative.',
        'Canac 88001678 door shown closed: 30 × 80 × 1.375 in, one frosted pane. Rail/stile sizes and hinges approximate; matte-black Weiser Breton privacy lever 9GLC3310-069 represented schematically; opening/jamb fit and inward-left swing unverified. Automatic front cutaway hides the door.' ,
        'Doorway has 2.5-in satin white wood-grain casing with two recessed border lines, jambs, stops and schematic hinges. Door trimming is homeowner-planned; finished cut height is not recorded, so the 80-in stock height remains a placeholder.',
        'Chormtok black HDPE stool B0FR49WRFK: 16.9 × 12.6 × 16.5 in from product diagram; contradictory 32 × 32 × 41.9 cm listing table. Seat centered X=71, Z=8.8 near front wall; purchase unreported.',
        'Robe hook on right wall above trash bin, at Z=55.5 in and assumed 64 in mounting center; verify clearance with actual hanging robe/towel.',
        'VT-SQ1207 basin opening 510 × 280 mm, deck 20 mm, total top/basin depth 185 mm including underside boss; interior contour inferred. Base drawing dimensions conflict with header; 47.75 × 36 corner plan used.',
        'Vanity recessed base is glossy white to match the cabinet; natural shadows still apply.',
        'Cabinet fronts, marble veining, floor speckles, accessory positions and lighting are schematic, not exact manufacturer meshes or finish samples.',
        'Model is a layout concept, not a construction, plumbing, electrical or clearance certification.'
    ]

elif VERSION == 2:

    ASSUMPTIONS = [
        'Room: 89 × 86½ in; height 85 in. These are homeowner measurements, not a site survey.',
        'Ordered: Alaska 48 × 36 shower, Sapphire panels, 48 × 18 vanity/top, 16-in linen cabinet, black faucet/accessories, ALEX 36 × 28 mirror and Amazon niche.',
        'Window assumed 30 × 12 in with sill at 64 in; exact size and position are unknown.',
        'Concept v2: linen at rear-left, Z=70.75–86.5 in, facing toilet, handles left/front and hinges right/rear when facing cabinet. Vanity beside it along left wall; top Z=22.165–70 in, leaving a provisional 0.75-in furniture gap. Cabinet 1194 × 456 × 820 mm; top 1215 × 465 mm. Actual hinge travel and fit need site checks.',
        'ALEX 84-ALEX-90 actual 900 × 700 × 45 mm with two inset vertical LED strips; bottom assumed 44 in. Strip dimensions approximate; live reflection is a viewer effect.',
        'Niche vertical 12 wide × 24 high with horizontal shelf; bottom assumed 40 in. Rough opening and waterproofing remain to verify.',
        'Toledo remains provisional; centre Z=71 in, shifted 3 in rearward as an assumption. Tank back X=81 in; plumbing rough-in unknown.',
        'Behind-toilet storage assumed 7 deep × 20 wide × 35 high; product and access are unconfirmed.',
        'Square shower fixture is a provisional Brigitta-inspired shape. Alaska glass 2000 mm tall above 1-in threshold, 8 mm thick; corner door span 1160 mm and side 852 mm. Black wall channels, overlap upright, closing/corner profiles, lower sliding-door rails and square upper rollers follow the archived product photograph; profile dimensions remain schematic. End drain is provisionally near front beneath removable stool; rough-in unverified. The back half represents the requested left opening when facing from the vanity; panels are shown closed.',
        'Sterilite white hamper: 19.5 × 12.25 × 24.5 in, front-left corner, Z=0.625–20.125 in; about 2.04 in to vanity top. Hand-towel ring remains above hamper. Lid movement and reach unverified.',
        'IKEA GANSJON black bin: 17 cm diameter × 26 cm high, between shower and toilet. Hamper and bin selected for visualization; purchase not reported.',
        'Front-wall ducted ventilation grille above hamper assumed 12 × 6 in, bottom 75 in. Duct function and actual grille dimensions unknown.',
        'Outlet on left wall above front end of vanity, centre Z=25.3 / Y=47 in, beside mirror. Light dimmer and ventilation switch side by side on front wall LEFT of entrance, above hamper: light dimmer LEFT, vent RIGHT when facing the plate from inside. Plate 4.75 × 4.5 in, centre Y=47 in, schematic. Light/dimmer products, compatibility and electrical placement require verification; no dimmability of the ordered mirror is inferred. Hand towel above front-left hamper; rear towel bar X=24–48 and paper holder X=59–64.5 retained.',
        'Canac 88001678 door: 30 × 80 × 1.375 in, frosted pane, inward-right toward shower; hinges on right, lever on left when closed. GLB and initial viewer show the door closed (0 degrees). Animated Open/Close button and angle slider preview 0–90 degrees; GLB download retains the initial closed pose. Door remains visible with wall cutaways. Assumed hinge axis X=47.8 / Z=0.9 in; actual hinge, handle and shower clearances unverified.' ,
        'Doorway has 2.5-in satin white wood-grain casing with two recessed border lines, jambs, stops and schematic hinges. Door trimming is homeowner-planned; finished cut height is not recorded, so the 80-in stock height remains a placeholder.',
        'Chormtok black HDPE stool B0FR49WRFK: 16.9 × 12.6 × 16.5 in from product diagram; contradictory 32 × 32 × 41.9 cm listing table. Seat centered X=71, Z=8.8 near front wall; purchase unreported.',
        'Robe hook on right wall above trash bin, at Z=55.5 in and assumed 64 in mounting center; verify clearance with actual hanging robe/towel.',
        'VT-SQ1207 basin opening 510 × 280 mm, deck 20 mm, total top/basin depth 185 mm including underside boss; interior contour inferred. Base drawing dimensions conflict with header; 47.75 × 36 corner plan used.',
        'Vanity recessed base is glossy white to match the cabinet; natural shadows still apply.',
        'Cabinet fronts, marble veining, floor speckles, accessory positions and lighting are schematic, not exact manufacturer meshes or finish samples.',
        'Linen-door clearance: rear-side hinges and front-side handles match handles LEFT when facing cabinet; doors swing toward the rear wall. Simplified sweep conflicts with rear wall, assumed window sill/trim and towel area. Cabinet offset/rear fittings need review; this concept preserves requested rear-wall contact.',
        'Model is a layout concept, not a construction, plumbing, electrical or clearance certification.'
    ]

elif VERSION == 3:

    ASSUMPTIONS = [
        'Room: 89 × 86½ in; height 85 in. These are homeowner measurements, not a site survey.',
        'V3 furniture selections: Madison VW3620-84GWH vanity, VT-SQ3620 top and LW1614-84GWH linen. These are concept alternatives; purchase/order changes have not been reported. Existing shower, faucet/accessories and niche references retained. ALEX collection 84-BIBO-24 replaces HIHI in v3 only; no mirror order amendment is reported.',
        'Window assumed 30 × 12 in with sill at 64 in; exact size and position are unknown.',
        f'Concept v3: floating linen 400 W × 350 D × 1400 H mm, 5-in rear-wall gap, rear/right hinges. Vanity 894 W × 495 D × 500 H mm; top 900 W × 500 D × 50 H mm; {FURNITURE_GAP:.2f}-in equal gaps from sink top to linen and hamper. Top height {TY:g} in; both cabinet bottoms {VB:.2f} in; linen top {LB+LH:.2f} in. Heights and offsets are design assumptions. Wall support, anchoring and plumbing need site review.',
        f'ALEX collection / BIBO 84-BIBO-24: drawing 600 W × 700 H mm, retailer depth 30 mm. Top {MB+MH:.2f} in aligns with linen; bottom {MB:.2f} in, {MB-TY:.2f} in above countertop. Inset {(TW-MW)/2:.2f} in per side from vanity top. Two inset light strips and touch ring are schematic; live reflection is a viewer effect. Mirror bottom is about 0.24 in below the static modeled faucet lever top, with about 0.18 in depth separation between glass and lever. Actual faucet dimensions and lever motion must be checked; no operating clearance is certified. Touch control and anti-fog are documented; dimming/wall-dimmer compatibility are not established by the drawing.' ,
        'Niche vertical 12 wide × 24 high with horizontal shelf; bottom assumed 40 in. Rough opening and waterproofing remain to verify.',
        'Toledo remains provisional; centre Z=71 in, shifted 3 in rearward as an assumption. Tank back X=81 in; plumbing rough-in unknown.',
        'Behind-toilet storage assumed 7 deep × 20 wide × 35 high; product and access are unconfirmed.',
        'Square shower fixture is a provisional Brigitta-inspired shape. Alaska glass 2000 mm tall above 1-in threshold, 8 mm thick; corner door span 1160 mm and side 852 mm. Black wall channels, overlap upright, closing/corner profiles, lower sliding-door rails and square upper rollers follow the archived product photograph; profile dimensions remain schematic. End drain is provisionally near front beneath removable stool; rough-in unverified. The back half represents the requested left opening when facing from the vanity; panels are shown closed.',
        f'Sterilite white hamper: 19.5 × 12.25 × 24.5 in, front-left corner, Z=0.625–20.125 in; {TZ-20.125:.2f} in to vanity top. Hand-towel ring remains above hamper. Lid movement and reach unverified.',
        'IKEA GANSJON black bin: 17 cm diameter × 26 cm high, between shower and toilet. Hamper and bin selected for visualization; purchase not reported.',
        'Front-wall ducted ventilation grille above hamper assumed 12 × 6 in, bottom 75 in. Duct function and actual grille dimensions unknown.',
        f'Outlet on left wall above front end of vanity, centre Z={OZ:.2f} / Y=47 in, beside mirror. Light dimmer and ventilation switch side by side on front wall LEFT of entrance, above hamper: light dimmer LEFT, vent RIGHT when facing the plate from inside. Plate 4.75 × 4.5 in, centre Y=47 in, schematic. Light/dimmer products, compatibility and electrical placement require verification; no dimmability of the ordered mirror is inferred. Hand towel above front-left hamper; rear towel bar X=24–48 and paper holder X=59–64.5 retained.',
        'Canac 88001678 door: 30 × 80 × 1.375 in, frosted pane, inward-right toward shower; hinges on right, lever on left when closed. GLB and initial viewer show the door closed (0 degrees). Animated Open/Close button and angle slider preview 0–90 degrees; GLB download retains the initial closed pose. Door remains visible with wall cutaways. Assumed hinge axis X=47.8 / Z=0.9 in; actual hinge, handle and shower clearances unverified.' ,
        'Doorway has 2.5-in satin white wood-grain casing with two recessed border lines, jambs, stops and schematic hinges. Door trimming is homeowner-planned; finished cut height is not recorded, so the 80-in stock height remains a placeholder.',
        'Chormtok black HDPE stool B0FR49WRFK: 16.9 × 12.6 × 16.5 in from product diagram; contradictory 32 × 32 × 41.9 cm listing table. Seat centered X=71, Z=8.8 near front wall; purchase unreported.',
        'Robe hook on right wall above trash bin, at Z=55.5 in and assumed 64 in mounting center; verify clearance with actual hanging robe/towel.',
        'VT-SQ3620 top outer dimensions and single faucet hole are drawing-sourced. Basin opening 520 × 300 mm, 125-mm depth, slopes and faucet/drain positions are photo-based approximations. Shower base drawing dimensions conflict with header; retained 47.75 × 36 corner plan.',
        'Floating glossy-white furniture with recessed horizontal grips, without toe kicks. Cabinet bottoms aligned as a visualization choice; plumbing routes and wall fixings are not designed.',
        'Cabinet fronts, marble veining, floor speckles, accessory positions and lighting are schematic, not exact manufacturer meshes or finish samples.',
        'Linen-door clearance: rear/right hinges retained; horizontal grips follow Madison product photos. A 5-in rear offset is tested against the rear wall, window, towels and fixtures with a simplified 0–90-degree sweep. Actual hinges, measurements and installation clearances remain unverified.',
        'Model is a layout concept, not a construction, plumbing, electrical or clearance certification.'
    ]

elif VERSION == 4:

    ASSUMPTIONS = [
        'Room: 89 × 86½ in; height 85 in. These are homeowner measurements, not a site survey.',
        'V4 concept selections: 36 x 18 Alder VF3618-62GWH, Saxe porcelain VT-SQ907, existing floor linen LF1614-62GWH, and 24 x 28 BIBO 84-BIBO-24. The documented order still contains the 48-inch vanity/top and 36-inch ALEX mirror; no order amendment reported.',
        'Window assumed 30 × 12 in with sill at 64 in; exact size and position are unknown.',
        'V4 starts from V2: floor linen rear-left, handles left/front, hinges right/rear; 5-inch rear-wall gap. Vanity centred between linen and front-left hamper, with equal 4.80-inch gaps measured to top edges. Cabinet 894 x 456 x 820 mm; top 915 x 465 mm. Floor furniture retains its matching black pulls.',
        'BIBO 84-BIBO-24: 600 x 700 x 30 mm; centred above sink, top aligned with linen at 70.875 inches, bottom 43.316 inches. Two inset light strips and touch ring follow archived evidence; strip details approximate. Static faucet lever is about 4.10 inches below mirror; actual lever motion unverified.',
        'Niche vertical 12 wide × 24 high with horizontal shelf; bottom assumed 40 in. Rough opening and waterproofing remain to verify.',
        'Toledo remains provisional; centre Z=71 in, shifted 3 in rearward as an assumption. Tank back X=81 in; plumbing rough-in unknown.',
        'Behind-toilet storage assumed 7 deep × 20 wide × 35 high; product and access are unconfirmed.',
        'Square shower fixture is a provisional Brigitta-inspired shape. Alaska glass 2000 mm tall above 1-in threshold, 8 mm thick; corner door span 1160 mm and side 852 mm. Black wall channels, overlap upright, closing/corner profiles, lower sliding-door rails and square upper rollers follow the archived product photograph; profile dimensions remain schematic. End drain is provisionally near front beneath removable stool; rough-in unverified. The back half represents the requested left opening when facing from the vanity; panels are shown closed.',
        'Sterilite white hamper: 19.5 x 12.25 x 24.5 in, front-left at Z=0.625–20.125 in; approximately 4.80 inches to vanity top. Hand towel retained above hamper; lid travel and reach unverified.',
        'IKEA GANSJON black bin: 17 cm diameter × 26 cm high, between shower and toilet. Hamper and bin selected for visualization; purchase not reported.',
        'Front-wall ducted ventilation grille above hamper assumed 12 × 6 in, bottom 75 in. Duct function and actual grille dimensions unknown.',
        'Tool outlet beside mirror near front end of vanity, Z approximately 21.93 / Y=47 inches, following V3 spacing. Controls retain V2 front-left arrangement: dimmer LEFT and ventilation switch RIGHT when facing plate. Device compatibility, circuits and electrical placement unverified.',
        'Canac 88001678 door: 30 × 80 × 1.375 in, frosted pane, inward-right toward shower; hinges on right, lever on left when closed. GLB and initial viewer show the door closed (0 degrees). Animated Open/Close button and angle slider preview 0–90 degrees; GLB download retains the initial closed pose. Door remains visible with wall cutaways. Assumed hinge axis X=47.8 / Z=0.9 in; actual hinge, handle and shower clearances unverified.',
        'Doorway has 2.5-in satin white wood-grain casing with two recessed border lines, jambs, stops and schematic hinges. Door trimming is homeowner-planned; finished cut height is not recorded, so the 80-in stock height remains a placeholder.',
        'Chormtok black HDPE stool B0FR49WRFK: 16.9 × 12.6 × 16.5 in from product diagram; contradictory 32 × 32 × 41.9 cm listing table. Seat centered X=71, Z=8.8 near front wall; purchase unreported.',
        'Robe hook on right wall above trash bin, at Z=55.5 in and assumed 64 in mounting center; verify clearance with actual hanging robe/towel.',
        'Saxe VT-SQ907: porcelain, 500 x 280 mm basin opening, 20-mm deck, 180-mm total depth including underside boss; 60-mm rear faucet offset and 230-mm drain offset. Interior contour/125-mm drop inferred. Alaska base-sheet conflict retained: 47.75 x 36-inch corner plan used.',
        'Vanity recessed base is glossy white to match the cabinet; natural shadows still apply.',
        'Cabinet fronts, marble veining, floor speckles, accessory positions and lighting are schematic, not exact manufacturer meshes or finish samples.',
        'Linen has V3-style 5-inch rear clearance, with V2 floor-cabinet doors and projecting handles. Simplified sweeps are documented in source notes. Actual hinge travel, site/window dimensions, plumbing, drawer travel and hamper access remain unverified.',
        'Model is a layout concept, not a construction, plumbing, electrical or clearance certification.',
    ]

def build_glb():
    full=list(range(len(NODES)))
    cut=[i for i,n in enumerate(NODES) if n['extras']['group'] not in ['wall_front','ceiling']]
    doc={'asset':{'version':'2.0','generator':'Bathroom Concept v4 Python generator · SRC-2026-102',
                  'copyright':'Model: homeowner project; viewer libraries: Three.js MIT'},
         'scene':0,'scenes':[{'name':'Cutaway overview','nodes':cut},{'name':'Full room shell','nodes':full}],
         'nodes':NODES,'meshes':MESHES,'materials':MATERIALS,'accessors':ACCESSORS,'bufferViews':VIEWS,
         'buffers':[{'byteLength':len(BIN)}],'images':IMAGES,'textures':TEXTURES,
         'samplers':[{'magFilter':9729,'minFilter':9987,'wrapS':10497,'wrapT':10497}],
         'extras':{'source':'SRC-2026-102','units':'metres','authoringUnit':'inch','roomInches':[W,H,D],
                   'axes':'X left-to-right; Y up; negative Z entrance-to-back','assumptions':ASSUMPTIONS}}
    js=json.dumps(doc,separators=(',',':'),ensure_ascii=True).encode();js+=b' '*((-len(js))%4)
    binary=bytes(BIN);binary+=b'\0'*((-len(binary))%4)
    out=struct.pack('<4sII',b'glTF',2,12+8+len(js)+8+len(binary))
    out+=struct.pack('<I4s',len(js),b'JSON')+js+struct.pack('<I4s',len(binary),b'BIN\0')+binary
    return out
