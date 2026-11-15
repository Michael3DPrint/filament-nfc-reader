import os, numpy as np, math, trimesh
from manifold3d import Manifold, CrossSection

# ===== ES3C40P module (LCDWiki drawing + STEP) =====
PCB_W, PCB_L = 61.04, 112.21
STACK, BACK_H, PCB_T = 11.45, 5.0, 1.6
FRONT_TO_PCB = STACK - BACK_H - PCB_T
HOLE_U, HOLE_V = 52.1, 26.52
VA_W, VA_H = 83.82, 55.98
VA_U = -2.8                                  # USB end on the RIGHT
# ===== case parameters (v4: open front, rear NFC overhang) =====
TH = 65.0
LIP = 0.0                                    # no front lip: module pocket is open at the front
LENS_W = -0.2                                # lens front sits 0.2 mm below the rim (was 0.8)
DS = 12.6; DIV_T = 3.0; SIDE = 3.0           # pocket depth, divider thickness, side walls
BOT = 5.0
FP_T = 1.6; PLUG_D = 2.0
PW, PL = PCB_L + 1.6, PCB_W + 0.6
TOPX = 12.7                                    # chamber above the screen: cable turns 90 deg at 10 mm (+1.5 half thickness +1 slack)
W = PW + 2*SIDE; HS = BOT + PL + TOPX; FPH = HS + FP_T; V0 = BOT + PL/2; HW = PW/2   # slab has no top bar: pocket open at the top, faceplate caps it
BASE_T = 4.0; BASE_W = W + 6.0
YS, ZF = 38.0, 8.0
WASH_T = 0.0                                   # TPU washers dropped
PCB_BACK_W = LENS_W - FRONT_TO_PCB - PCB_T   # -7.25
SO_LEN = DS + PCB_BACK_W - WASH_T            # standoff height (4.95)
NFC_W, NFC_L, NFC_T, COMP_H = 43.0, 40.4, 1.2, 3.5
PLATE_T = 2.0
ARM_HW, ARM_WALL = 32.5, 3.0
c, s = math.cos(math.radians(TH)), math.sin(math.radians(TH))
VH = np.array([0,c,s]); NH = np.array([0,-s,c]); XH = np.array([1.0,0,0])
F0 = np.array([0,YS,ZF])
def L2W():
    m=np.zeros((3,4)); m[:,0]=XH; m[:,1]=VH; m[:,2]=NH; m[:,3]=F0; return m
def loc_box(u0,u1,v0,v1,w0,w1): return Manifold.cube([u1-u0,v1-v0,w1-w0]).translate([u0,v0,w0]).transform(L2W())
def loc_cyl(u,v,w0,w1,d,seg=48): return Manifold.cylinder(w1-w0,d/2,d/2,seg).translate([u,v,w0]).transform(L2W())
def extrude_yz(pts,x0,x1):
    m=CrossSection([np.array(pts,dtype=float)]).extrude(x1-x0)
    return m.transform(np.array([[0,0,1,x0],[1,0,0,0],[0,1,0,0]],dtype=float))
def box(x0,x1,y0,y1,z0,z1): return Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def cyl(x,y,z0,z1,d,seg=48): return Manifold.cylinder(z1-z0,d/2,d/2,seg).translate([x,y,z0])
def P(v,w):
    p=F0+v*VH+w*NH; return (float(p[1]),float(p[2]))
def plane_y_at_z(z, w=-DS-DIV_T):
    v=(z-ZF-w*c)/s; return P(v,w)[0]

TOP0 = HS
Y_TOP, ZT = P(FPH,0.0)                       # top front corner (faceplate flange)
RAISE = 0.0                                    # back raised half an inch
Z_ARM1 = P(FPH,-(DS+DIV_T))[1]+RAISE; Z_ARM0 = Z_ARM1-18.0; Z_FLOOR = Z_ARM1-13.0
GAPA = 0.8                                     # arm front clearance to the slab back plane
def yfc(z): return plane_y_at_z(z)+GAPA+3.3     # inner face of the arm's front wall
def AFY(z): return plane_y_at_z(z)+GAPA         # arm front face (0.3 clear of the slab back plane)
YC = yfc(Z_ARM1-PLATE_T) + 2.8 + NFC_L/2 + 0.4  # PN532 / pad centre (y)
YA_B = YC + NFC_L/2 + 0.4 + 2.0 + ARM_WALL
BASE_D = YA_B + 4.0; BASE_Y0 = 32.0

def rrect(x0,x1,y0,y1,z0,z1,r=8.0):
    pts=[]
    for (cx_,cy_) in [(x0+r,y0+r),(x1-r,y0+r),(x1-r,y1-r),(x0+r,y1-r)]:
        pts.append(Manifold.cylinder(z1-z0,r,r,40).translate([cx_,cy_,z0]))
    return Manifold.batch_hull(pts)
base = rrect(-BASE_W/2,BASE_W/2,BASE_Y0,BASE_D,0,BASE_T)

# ---------------- slab (screen frame, open at the top) ----------------
slab = loc_box(-W/2,W/2,-30,HS,-DS-DIV_T,0.0) ^ box(-W,W,-10,300,BASE_T-0.01,400)
body = base + slab
# ---------------- hollow rear spine (service cavity, snap-on rear cover) ----------------
SX0, SX1 = -21.5, 21.5                         # pillar centred on the body
CX0, CX1 = -14.5, 14.5                         # hollow inside, 7 mm side walls carry the arm rails and the screw
Z_B, Z_T = BASE_T+3.0, Z_ARM0+0.5
Yr0 = plane_y_at_z(BASE_T)+46.0; Yr1 = plane_y_at_z(Z_ARM0)+22.0
KK = (Yr1-Yr0)/(Z_ARM0-BASE_T)
def yr(z): return Yr0 + (z-BASE_T)*KK
spine = extrude_yz([(plane_y_at_z(BASE_T)-0.5,BASE_T-0.01),(Yr0,BASE_T-0.01),(yr(Z_ARM0),Z_ARM0),(plane_y_at_z(Z_ARM0)-1.0,Z_ARM0)],SX0,SX1)
body = body + spine
# module pocket: open at the front AND the top
body = body - loc_box(-HW,HW,BOT,HS+5.0,-DS,0.5)
# service cavity open to the rear (cover closes it) and open at the top (arm floor opening sits over it)
cav2 = extrude_yz([(plane_y_at_z(Z_B)-0.02,Z_B),(yr(Z_B)+1.5,Z_B),(yr(Z_T)+0.3,Z_T),(plane_y_at_z(Z_T)-0.02,Z_T)],CX0,CX1)
body = body - cav2
# shallow open-top cable notch in the divider: the cable turns at 10 mm above the PCB top, so the divider must end 8 mm above it here (the faceplate cap closes it)
body = body - loc_box(-19.5,-9.0,BOT+PL+8.0,TOP0+5.0,-DS-DIV_T-1.7,-DS+0.1)   # P4 at u -14.5 (the left 4-pin socket when viewed from the back of the board)
# snap dimples in the cavity side walls
SNAP_Z = (18.0, 44.0)
def mid_y(z): return yr(z)-1.6
for z in SNAP_Z:
    for xw in (CX0-0.15, CX1+0.15):
        body = body - Manifold.sphere(1.1,24).translate([xw,mid_y(z),z])
# arm mounting: dovetail rails on the pillar side walls (arm slides on from the back), one short screw stops it sliding back off
WX = 18.0
RB, RT, RH = 3.4, 5.8, 1.5                      # rail base width, top width, height
RE = yr(Z_ARM0) - 8.0                           # rails end here; the screw sits behind them
def extrude_xz(pts,y0,y1):
    m=CrossSection([np.array(pts,dtype=float)]).extrude(y1-y0)
    return m.transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0]],dtype=float))
RAIL_Y0 = plane_y_at_z(Z_ARM0) - 0.3
for sx_ in (-1,1):
    body = body + extrude_xz([(sx_*WX-RB/2,Z_ARM0-0.1),(sx_*WX+RB/2,Z_ARM0-0.1),(sx_*WX+RB/2,Z_ARM0),(sx_*WX+RT/2,Z_ARM0+RH),(sx_*WX-RT/2,Z_ARM0+RH),(sx_*WX-RB/2,Z_ARM0)],RAIL_Y0,RE)
SCR_P = (WX, yr(Z_ARM0)-3.5)
body = body - cyl(SCR_P[0],SCR_P[1],Z_ARM0-9.0,Z_ARM0+0.1,2.5,32)
# standoffs with M3 pilot holes (screws go through the PCB corner holes from the front)
for su in (-1,1):
    for sv in (-1,1):
        u,v=su*HOLE_U,V0+sv*HOLE_V
        body = body + loc_cyl(u,v,-DS-0.05,-DS+SO_LEN,6.4,40)
        body = body - loc_cyl(u,v,-DS+SO_LEN-7.0,-DS+SO_LEN+0.1,2.5,32)
# USB-C opening in right wall
USB_WC = PCB_BACK_W - 0.915                     # receptacle centre (w), follows the module
body = body - loc_box(HW-0.5,W/2+1,V0-7.0,V0+7.0,USB_WC-4.1,USB_WC+4.1)   # 8.2 mm tall: fits 7 mm overmolds
body = body - Manifold.batch_hull([loc_box(W/2-0.5,W/2-0.49,V0-7.0,V0+7.0,USB_WC-4.1,USB_WC+4.1),loc_box(W/2,W/2+0.3,V0-7.5,V0+7.5,USB_WC-4.6,USB_WC+4.6)])   # 0.5 chamfer on the outer edge
# faceplate snap grooves in the pocket side walls, above the PCB
FS_V = (68.5, 77.5); FS_W = (-12.0, -2.0)
for sg in (-1,1):
    body = body - loc_box(min(sg*HW,sg*(HW+0.8)),max(sg*HW,sg*(HW+0.8)),FS_V[0]-0.5,FS_V[1]+0.5,-12.3,-10.4)
# feet dimples
for x in (-45,45):
    for y in (BASE_Y0+10,BASE_D-12): body = body - cyl(x,y,-0.1,1.2,9.0,32)

# ---------------- NFC arm (separate part, prints flat; sits on the spine shelf) ----------------
AH = ARM_HW-ARM_WALL
arm = extrude_yz([(AFY(Z_ARM0),Z_ARM0),(YA_B,Z_ARM0),(YA_B,Z_ARM1),(AFY(Z_ARM1),Z_ARM1)],-ARM_HW,ARM_HW)
arm = arm - extrude_yz([(AFY(Z_FLOOR)-2.0,Z_FLOOR),(YA_B-ARM_WALL,Z_FLOOR),(YA_B-ARM_WALL,Z_ARM1+1),(AFY(Z_ARM1+1)-2.0,Z_ARM1+1)],-AH,AH)   # no front wall: floor + 3 walls, the faceplate box closes the front
Y0R = AFY(Z_ARM1)                              # lid starts flush with the open front
arm = arm - box(-ARM_HW+1.0,ARM_HW-1.0,AFY(Z_ARM1)-2.0,YA_B-1.0,Z_ARM1-PLATE_T,Z_ARM1+1)
SH = 3.0*math.sqrt(1+KK*KK)
# wide wire opening through the arm floor: full cavity width, open to the front edge of the arm
arm = arm - box(-13.0,13.0,AFY(Z_FLOOR)-3.0,yr(Z_ARM0)-SH-0.8,Z_ARM0-0.1,Z_FLOOR+0.01)
# dovetail grooves on the underside (open at the front, closed behind the rails)
GC = 0.3
for sx_ in (-1,1):
    GT = RB/2+GC + (RT-RB)/2*(RH+GC)/RH          # groove half-width at its ceiling: same flank slope as the rail
    arm = arm - extrude_xz([(sx_*WX-RB/2-GC,Z_ARM0-0.1),(sx_*WX+RB/2+GC,Z_ARM0-0.1),(sx_*WX+RB/2+GC,Z_ARM0),(sx_*WX+GT,Z_ARM0+RH+GC),(sx_*WX-GT,Z_ARM0+RH+GC),(sx_*WX-RB/2-GC,Z_ARM0)],AFY(Z_ARM0)-3.0,RE+0.5)
# single short screw through the floor into the pillar wall
arm = arm - cyl(SCR_P[0],SCR_P[1],Z_ARM0-0.1,Z_FLOOR+0.1,3.8,32) - cyl(SCR_P[0],SCR_P[1],Z_FLOOR-3.0,Z_FLOOR+0.1,6.4,32)
# snap grooves for the lid hooks in the inner side walls
ZL = Z_ARM1-PLATE_T                               # lid underside
HOOK_Y = (YC-12.0, YC+12.0); HOOK_W = 8.0
ZU = ZL-7.8                                       # barb 2 mm lower: longer hooks, ~0.9% strain
for sx_ in (-1,1):
    for yh in HOOK_Y:
        arm = arm - box(min(sx_*AH,sx_*(AH+1.0)),max(sx_*AH,sx_*(AH+1.0)),yh-HOOK_W/2-1.0,yh+HOOK_W/2+1.0,ZU-2.4,ZU+0.25)
for sx_ in (-1,1):
    arm = arm + cyl(sx_*17.0,YC-NFC_L/2-0.4-1.25,Z_FLOOR-0.01,Z_ARM1-PLATE_T-COMP_H-NFC_T+1.2+0.7,2.5,24)   # board front edge stops 0.4 short of these
BX0, BX1 = -ARM_HW, ARM_HW                   # faceplate box spans the arm width
arm_print = arm.translate([0,0,-Z_ARM0])
_b=arm_print.bounding_box(); arm_print=arm_print.translate([-(_b[0]+_b[3])/2,-(_b[1]+_b[4])/2,0])

# ---------------- NFC lid + PN532 cradle ----------------
LW = 2*(ARM_HW-1.0)-0.3; LD = (YA_B-1.0)-Y0R-0.3
lid = box(-LW/2,LW/2,Y0R+0.15,Y0R+0.15+LD,Z_ARM1-PLATE_T,Z_ARM1)
RC = 1.2                                       # inner recess: component side of the board sinks into the lid, board sits 1.2 mm closer to the scan surface (0.8 mm skin left on top)
zb = Z_ARM1-PLATE_T-COMP_H-NFC_T+RC
bx,by = NFC_W/2+0.7, NFC_L/2+0.8
lid = lid - box(-bx,bx,Y0R,YC+by,Z_ARM1-PLATE_T-0.01,Z_ARM1-PLATE_T+RC)
def bx_(xa,xb,ya,yb,za,zb_): return box(min(xa,xb),max(xa,xb),min(ya,yb),max(ya,yb),za,zb_)
# cradle open at the front: full-length side walls with lips under the board edges, closed only at the rear corners
for sx in (-1,1):
    ya,yb = YC-by, YC+by+1.6
    lid = lid + box(min(sx*bx,sx*(bx+1.6)),max(sx*bx,sx*(bx+1.6)),ya,yb,zb-1.5,Z_ARM1-PLATE_T)      # side wall
    lid = lid + box(min(sx*(bx-2.5),sx*bx),max(sx*(bx-2.5),sx*bx),ya,yb,zb-1.5,zb-0.2)   # 0.2 below the board absorbs droop of the 2.5 mm shelf                 # lip under the board edge
    y0=YC+by
    lid = lid + bx_(sx*bx-sx*6,sx*bx,y0,y0+1.6,zb-1.5,Z_ARM1-PLATE_T)                               # rear end wall (corner)
    lid = lid + bx_(sx*bx-sx*6,sx*bx,y0-2.5,y0,zb-1.5,zb-0.2)                                          # rear lip under the board
    lid = lid + bx_(sx*bx,sx*bx-sx*2.5,y0,y0-2.5,zb+NFC_T+0.2,Z_ARM1-PLATE_T+RC)                      # rear stop pad above the board
# press-click hooks (two per side) that snap into grooves in the arm walls
for sx in (-1,1):
    for yh in HOOK_Y:
        xi,xo = sx*(AH-0.3-1.4), sx*(AH-0.3)
        lid = lid + box(min(xi,xo),max(xi,xo),yh-HOOK_W/2,yh+HOOK_W/2,ZL-10.0,ZL+0.01)
        bp=[(xo,ZU),(xo+sx*0.6,ZU-0.6),(xo,ZU-1.6)]
        if sx>0: bp=bp[::-1]
        lid = lid + extrude_xz(bp,yh-HOOK_W/2,yh+HOOK_W/2)
lid_print = lid.transform(np.array([[1,0,0,0],[0,-1,0,0],[0,0,-1,0]],dtype=float))
bb=lid_print.bounding_box(); lid_print=lid_print.translate([0,0,-bb[2]])

# ---------------- snap-on rear cover ----------------
CT = Z_ARM0                                    # cover top flush with the shelf
cover = extrude_yz([(yr(Z_B)-SH,Z_B),(yr(Z_B),Z_B),(yr(CT),CT),(yr(CT)-SH,CT)],CX0+0.3,CX1-0.3)
for z in SNAP_Z:
    for sx_ in (-1,1):
        xe = sx_*(CX1-0.3)                           # cover side edge
        cover = cover + Manifold.sphere(0.9,24).translate([xe-sx_*0.2,mid_y(z),z])   # reaches 0.4 into the wall dimple
        # L-shaped slot frees a 2 mm wide, 16 mm long cantilever along the edge (flexes in the print plane)
        def slot(xa,xb,za,zb_):
            return extrude_yz([(yr(za)-SH-1,za),(yr(za)+1,za),(yr(zb_)+1,zb_),(yr(zb_)-SH-1,zb_)],min(xa,xb),max(xa,xb))
        cover = cover - slot(xe-sx_*2.0,xe-sx_*2.8,z-3.0,min(z+16.0,CT-2.0)) - slot(xe+sx_*0.5,xe-sx_*2.8,z-3.8,z-3.0)
# finger notch for prying (rear face, near the top)
zn = CT-9.0
cover = cover - Manifold.cube([10,2.0,3.0]).translate([(CX0+CX1)/2-5,yr(zn)-1.2,zn])
# lay it flat for printing: rear face down
phi = math.atan2(Z_ARM0-BASE_T, Yr1-Yr0)       # direction of the cover plane (from +y toward +z)
cph, sph = math.cos(phi), math.sin(phi)
cover_print = cover.transform(np.array([[1,0,0,0],[0,cph,sph,0],[0,-sph,cph,0]],dtype=float))
cb = cover_print.bounding_box(); cover_print = cover_print.translate([0,0,-cb[2]])

# ---------------- full faceplate (front panel + top cap; hides the screws and the open top) ----------------
fp = Manifold.cube([W,FPH+6.0,FP_T]).translate([-W/2,-6.0,0])      # panel runs down to the base
fp = fp.trim_by_plane([0.0,s,c],BASE_T-ZF)                            # clip it flat on the base top (z = BASE_T)
fp = fp + Manifold.cube([W,FP_T,DS+DIV_T-0.02]).translate([-W/2,HS,-(DS+DIV_T)+0.02])      # top cap flange resting on the slab top
fp = fp - Manifold.cube([VA_W+0.8,VA_H+0.8,FP_T+2]).translate([VA_U-(VA_W+0.8)/2,V0-(VA_H+0.8)/2,-1])
PU0, PU1 = 48.4, PW/2-0.12
PV0, PV1 = BOT+0.12, HS+0.01
for sg in (-1,1):
    u0,u1 = (PU0,PU1) if sg>0 else (-PU1,-PU0)
    fp = fp + Manifold.cube([u1-u0,PV1-PV0,PLUG_D+0.01]).translate([u0,PV0,-PLUG_D])
    for uu in (u0+2.0,(u0+u1)/2,u1-2.0):            # crush ribs on the lower face
        fp = fp + Manifold.cube([0.8,0.25,PLUG_D-0.3]).translate([uu-0.4,PV0-0.25,-PLUG_D+0.1])
    for vv in (PV0+8.0,(PV0+PV1)/2+4.0,PV1-8.0):    # crush ribs on the outer end face
        xo = u1 if sg>0 else u0-0.25
        fp = fp + Manifold.cube([0.25,0.8,PLUG_D-0.3]).translate([xo,vv-0.4,-PLUG_D+0.1])
fp = fp - Manifold.cylinder(FP_T+PLUG_D+2,0.7,0.7,24).translate([-50.0,V0+16.3,-PLUG_D-1])   # mic port
# press-click: one snap finger per end, hanging off the plug into the chamber above the PCB; 45 deg retention face so it pulls off
for sg in (-1,1):
    xo = sg*(HW-0.15); xi = sg*(HW-0.15-1.2)
    fp = fp + Manifold.cube([1.2,FS_V[1]-FS_V[0],FS_W[1]-FS_W[0]+0.01]).translate([min(xo,xi),FS_V[0],FS_W[0]])
    bp = [(xo,-12.0),(xo+sg*0.5,-11.2),(xo,-10.7)]
    if sg<0: bp = bp[::-1]
    fin = CrossSection([np.array(bp,dtype=float)]).extrude(FS_V[1]-FS_V[0]).transform(np.array([[1,0,0,0],[0,0,1,FS_V[0]],[0,1,0,0]],dtype=float))
    fp = fp + fin
# pry notch at the bottom edge (fingernail or coin) to pop the faceplate off
fp = fp - Manifold.cube([14.0,4.0,FP_T+2]).translate([-7.0,-7.4,-1])
fp_world = fp.transform(L2W())
fp_print = fp.transform(np.array([[1,0,0,0],[0,-1,0,0],[0,0,-1,0]],dtype=float))
bb_=fp_print.bounding_box(); fp_print=fp_print.translate([0,0,-bb_[2]])

# ---------------- TPU washers (4 behind the PCB, 4 under the screw heads) ----------------
wash=None
for i in range(8):
    w_=(Manifold.cylinder(WASH_T,3.2,3.2,40)-Manifold.cylinder(WASH_T+2,1.6,1.6,32).translate([0,0,-1])).translate([(i%4-1.5)*9.0,(i//4-0.5)*9.0,0])
    wash = w_ if wash is None else wash+w_

if __name__=='__main__':
    OUT_DIR=os.environ.get('CASE_OUT_DIR','.')   # STL files go here (default: current folder)
    def save(m,name):
        mm=m.to_mesh(); tm=trimesh.Trimesh(np.array(mm.vert_properties,dtype=np.float64)[:,:3],np.array(mm.tri_verts),process=False)
        tm.export(os.path.join(OUT_DIR,f'{name}.stl')); return tm
    tb=save(body,'body'); ta=save(arm_print,'arm'); tl=save(lid_print,'nfc_lid'); tc=save(cover_print,'spine_cover'); tf=save(fp_print,'faceplate')
    save(body+arm+lid+cover+fp_world,'assembly_preview')
    for n,t in [('body',tb),('arm',ta),('nfc_lid',tl),('cover',tc),('faceplate',tf)]:
        print(n,'watertight',t.is_watertight,'bbox',np.round(t.bounds[1]-t.bounds[0],1),'vol cm3',round(t.volume/1000,1))
    print('ZT',round(ZT,1),'YA_B',round(YA_B,1),'YC',round(YC,1),'BASE_D',round(BASE_D,1),body.status())
