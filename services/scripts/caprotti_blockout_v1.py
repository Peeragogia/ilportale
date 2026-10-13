# ═══════════════════════════════════════════════════════════════════
#  CAPROTTI PAVILION — PROPORTIONAL BLOCKOUT v1 (Phase 2)
#  Dossier: docs/caprotti/ v0.3 — Pi review: CONDITIONAL GO, 83/100
#
#  SCALE CONVENTION: principal façade width = 100 proportional units.
#  NO METRES CLAIMED. Ratios INFERRED from VISUAL_ANALYSIS.md + typology;
#  all ratios documented below. Rescale via root CAPROTTI_MASTER later.
#
#  Evidence tags:
#    [OBS]  from evidence register (OBSERVED/OBSERVED-VISUAL)
#    [INF]  inferred ratio, hostile to invention: keep coarse
#    [EST]  geometry that will move after field photos/measurement
#    [UNK]  placeholder — must not be presented as fact
#
#  Ratio log (architectural hier -> key clues):
#   façade width              = 100 u   [OBS-VISUAL anchor]
#   plan depth                =  78 u   [INF: compact pavilion]
#   base (plinth)             =   6 u   [INF]
#   column axes               =  ±37.5  [INF: bay rhythm 48 u arch]
#   cornice top               = 112 u   [EST: strong vertical articulation]
#   entablature depth         =   8 u   [INF]
#   terrace deck              = 120 u   [INF]
#   balustrade height         =   8 u   [INF]
#   arch opening width        =  52 u   [OBS-VISUAL: tall full arch]
#   arch springline           =  78 u, key 104 u  [EST]
#   rect bay w/h              =  40 × 50 u  [OBS-VISUAL]
#   semicircular panel r      =  20 u   [OBS-VISUAL]
#   column r / capital        = 2.8 / 5.4 plate [EST]
#   stair total rise          = 116 u, run ~64 u  [EST: single flight + landing]
#   glazing node spacing      = ~10 u   [EST: dark frame + circular nodes]
# ═══════════════════════════════════════════════════════════════════
import bpy
import bmesh
import math
from mathutils import Vector

# ── purga scena (partiamo da un ambiente pulito) ────────────────────
for coll in list(bpy.data.collections):
    if coll.users == 0:
        bpy.data.collections.remove(coll)
for scene in list(bpy.data.scenes):
    if scene.users == 0:
        bpy.data.scenes.remove(scene)

# scena attiva: pulisci oggetti ma conserva scene
scene = bpy.context.scene
for o in list(scene.objects):
    bpy.data.objects.remove(o, do_unlink=True)
scene.name = "CAPROTTI"

# ── helpers ─────────────────────────────────────────────────────────
ME = None  # material cache

def M(name, rgba=(0.8, 0.8, 0.8, 1), rough=0.8, metal=0.0):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

def link(ob, coll):
    if ob.name not in coll.objects:
        coll.objects.link(ob)
    return ob

def new_mesh(name, verts, faces, mat=None, coll=None, parent=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    if mat:
        me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    ob.parent = parent
    if coll:
        link(ob, coll)
    return ob

def prim(kind, name, x, y, z, mat, parent=None, coll=None, **kw):
    bm = bmesh.new()
    if kind == "cube":
        s = kw.get("size", 1.0)
        bmesh.ops.create_cube(bm, size=s)
        obloc = (x, y, z + s / 2)
    elif kind == "box":
        sx, sy, sz = kw["sx"], kw["sy"], kw["sz"]
        bmesh.ops.create_cube(bm, size=1.0)
        obloc = (x, y, z + sz / 2)
        scale = (sx, sy, sz)
    elif kind == "cyl":
        r, h = kw["r"], kw["h"]
        bmesh.ops.create_cone(bm, cap_ends=True, segments=kw.get("seg", 24), radius1=r, radius2=r, depth=h)
        obloc = (x, y, z + h / 2)
        scale = None
    elif kind == "cone":
        rb, rt, h = kw["rb"], kw["rt"], kw["h"]
        bmesh.ops.create_cone(bm, cap_ends=True, segments=kw.get("seg", 20), radius1=rb, radius2=rt, depth=h)
        obloc = (x, y, z + h / 2)
        scale = None
    elif kind == "sphere":
        r = kw["r"]
        bmesh.ops.create_uvsphere(bm, u_segments=kw.get("seg_u", 16), v_segments=kw.get("seg_v", 12), radius=r)
        obloc = (x, y, z + r)
        if kw.get("flat"):
            scale = (1, 1, kw["flat"])
        else:
            scale = None
    elif kind == "disc":
        r = kw["r"]
        h = kw.get("h", 0.8)
        bmesh.ops.create_cone(bm, cap_ends=True, segments=kw.get("seg", 16), radius1=r, radius2=r, depth=h)
        obloc = (x, y, z + h / 2)
        scale = None
    else:
        raise ValueError(kind)
    me = bpy.data.meshes.new(name.replace(" ", "_"))
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    ob.location = obloc
    if scale:
        ob.scale = scale
    if parent:
        ob.parent = parent
    if coll:
        link(ob, coll)
    return ob

# ── materiali (blockout, flat colors) ──────────────────────────────
M_PLASTER   = M("CAP_plaster", (0.855, 0.82, 0.75, 1), rough=0.95)
M_STONE     = M("CAP_stone",   (0.72, 0.70, 0.66, 1), rough=1.0)
M_GLASS     = M("CAP_glass",   (0.25, 0.32, 0.38, 0.35), rough=0.1)
M_FRAME     = M("CAP_frame",   (0.13, 0.13, 0.14, 1), rough=0.6, metal=0.6)
M_ROOF      = M("CAP_roof",    (0.42, 0.40, 0.38, 1), rough=0.9)
M_TILE      = M("CAP_tile",    (0.55, 0.30, 0.22, 1), rough=0.9)
M_TERRACE   = M("CAP_terrace", (0.60, 0.58, 0.54, 1), rough=0.9)
M_GREEN     = M("CAP_green",   (0.30, 0.45, 0.22, 1), rough=1.0)
M_DARKGREEN = M("CAP_dgreen",  (0.20, 0.32, 0.16, 1), rough=1.0)
M_BROWN     = M("CAP_trunk",   (0.42, 0.30, 0.18, 1), rough=1.0)
M_WATER     = M("CAP_water",   (0.28, 0.42, 0.50, 0.85), rough=0.15)
M_SAND      = M("CAP_sand",    (0.78, 0.72, 0.60, 1), rough=1.0)
M_STATUE    = M("CAP_statue",  (0.82, 0.80, 0.76, 1), rough=0.9)
M_BASE      = M("CAP_base",    (0.55, 0.52, 0.48, 1), rough=1.0)

# ── collezioni ──────────────────────────────────────────────────────
def collection(name, parent_coll=None):
    c = bpy.data.collections.new(name)
    if parent_coll:
        parent_coll.children.link(c)
    return c

MASTER = bpy.data.collections.new("CAPROTTI_MASTER")
bpy.context.scene.collection.children.link(MASTER)

CAP = collection("CAPROTTI_ARCHITECTURE", MASTER)
CTX = collection("CONTEXT", MASTER)
REF = collection("REFERENCE", MASTER)
LIG = collection("LIGHTING", MASTER)
CAM = collection("CAMERAS", MASTER)
PORT = collection("IL_PORTALE", MASTER)   # separato e intatto — oggi vuoto + proxy

# root scalabile unica
root_arch = bpy.data.objects.new("CAPROTTI_ARCHITECTURE_ROOT", None)
link(root_arch, CAP)

root_ctx = bpy.data.objects.new("CONTEXT_ROOT", None)
link(root_ctx, CTX)

# ── CONTESTO: terreno, stagno, vialetto ─────────────────────────────
ground = prim("box", "CAP_Ground", 0, -60, -2, M_GREEN, parent=root_ctx, coll=CTX,
              sx=1400, sy=1100, sz=4)
ground.name = "CAP_Ground"

pond = prim("cyl", "CAP_Pond_PROXY", 0, 170, -4.6, M_WATER, parent=root_ctx, coll=CTX,
            r=150, h=2.2, seg=40)
pond.scale = (1.0, 0.62, 1.0)
pond.name = "CAP_Pond_PROXY"
pond_bed = prim("cyl", "CAP_PondBed_PROXY", 0, 170, -7.5, M_BASE, parent=root_ctx, coll=CTX,
                r=158, h=3, seg=40)
pond_bed.scale = (1.0, 0.62, 1.0)

path = prim("box", "CAP_Path", 0, 105, -1.9, M_SAND, parent=root_ctx, coll=CTX,
            sx=34, sy=150, sz=0.8)
path.name = "CAP_Path"

# roccaglia/grotta: sfere schiacciate di pietra
for i, (gx, gy, gz, gr, fl) in enumerate([
        (78, 40, -1.5, 30, 0.55), (104, 78, -2.5, 22, 0.5),
        (66, 92, -2, 26, 0.6), (120, 130, -3, 18, 0.5)]):
    r = prim("sphere", f"CAP_Grotto_PROXY_{i:02d}", gx, gy, gz, M_STONE,
             parent=root_ctx, coll=CTX, r=gr, seg_u=14, seg_v=10, flat=fl)
    r.rotation_euler = (0.2 * i, 0.3 * i, 0)

# vegetazione: alberi + cespugli
for i, (tx, ty, s) in enumerate([(-170, 130, 1.25), (185, 60, 1.0), (-210, 40, 1.4),
                                  (160, 210, 0.9), (-150, -80, 1.1)]):
    tr = prim("cyl", f"CAP_TreeTrunk_{i:02d}", tx, ty, 0, M_BROWN, parent=root_ctx, coll=CTX,
              r=3.2 * s, h=26 * s, seg=10)
    canopy = prim("sphere", f"CAP_TreeCanopy_{i:02d}", tx, ty + 0, 26 * s, M_DARKGREEN,
                  parent=root_ctx, coll=CTX, r=26 * s, seg_u=12, seg_v=10)
    canopy.scale = (1.15, 1.15, 0.85)
for i, (bx, by, br) in enumerate([(-40, 150, 8), (46, 128, 7), (-28, 205, 7),
                                   (58, 175, 6), (30, -90, 8), (-35, -100, 7)]):
    prim("sphere", f"CAP_Bush_{i:02d}", bx, by, 0, M_GREEN, parent=root_ctx, coll=CTX,
         r=br, seg_u=10, seg_v=8)

# ── PADIGLIONE (coordinate: Y+ = facciata principale verso lo stagno) ──
PX = 54   # mezza larghezza muro esterno
PY = 42   # mezza profondità
ZP = 6    # zoccolo

# basamento
prim("box", "CAP_Base", 0, 0, 0, M_BASE, parent=root_arch, coll=CAP, sx=116, sy=94, sz=ZP)
# gradini principali
for i in range(3):
    prim("box", f"CAP_BaseStep_{i:02d}", 0, PY + 6 + i * 5, 0 + i * (ZP / 3.2), M_STONE,
         parent=root_arch, coll=CAP, sx=92 - i * 14, sy=5, sz=ZP / 3.2 + 0.01)

def column(cx, cy, cz, h, mat, name):
    c = prim("cyl", name, cx, cy, cz, mat, parent=root_arch, coll=CAP, r=2.9, h=h, seg=18)
    pl = prim("box", name + "_plinth", cx, cy, cz - 1.6, M_STONE, parent=root_arch, coll=CAP,
              sx=5.6, sy=5.6, sz=1.6)
    cap = prim("box", name + "_cap_PROXY", cx, cy, cz + h - 0.6, M_PLASTER, parent=root_arch,
               coll=CAP, sx=5.2, sy=5.2, sz=2.2)
    return c

# colonne: 4 angoli + 4 ai lati delle campate maggiori  [INF]
COLS = [(-PX + 3.2, -PY + 3.2), (PX - 3.2, -PY + 3.2), (-PX + 3.2, PY - 3.2), (PX - 3.2, PY - 3.2),
        (-37.5, PY - 3.2), (37.5, PY - 3.2), (-37.5, -PY + 3.2), (37.5, -PY + 3.2)]
for i, (cx, cy) in enumerate(COLS):
    column(cx, cy, ZP, 106, M_PLASTER, f"CAP_Columns_{i:02d}")

# corpo: fascia cieca tra zoccolo e vetrata
prim("box", "CAP_MainMass_plinthBand", 0, 0, ZP, M_PLASTER, parent=root_arch, coll=CAP,
     sx=108, sy=88, sz=12)

# ── FACCIATA PRINCIPALE (Y+): campata centrale ad arco [OBS-VISUAL] ──
# muri laterali alla campata
for sx_ in (-1, 1):
    prim("box", f"CAP_MainMass_side_{'L' if sx_ < 0 else 'R'}", sx_ * 38, PY - 2, ZP + 12, M_PLASTER,
         parent=root_arch, coll=CAP, sx=24, sy=2.5, sz=88)
# architrave sopra l'arco
prim("box", "CAP_MainMass_lintel", 0, PY - 2, 104, M_PLASTER, parent=root_arch, coll=CAP,
     sx=108, sy=2.5, sz=22)
# vetrata ad arco (vetro scuro)
vrets, vfaces = [], []
ARC_R = 26.0
seg = 18
for i in range(seg + 1):
    a = math.pi * (1 - i / seg)  # da pi a 0
    vrets.append((math.cos(a) * ARC_R, 0.0, ZP + 12 + 66 + math.sin(a) * ARC_R))
base_y = 0.0
# pannello: arco + rettangolo sotto
pts = []
for i in range(seg + 1):
    a = math.pi * (1 - i / seg)
    pts.append((math.cos(a) * ARC_R, 0, ZP + 12 + 66 + math.sin(a) * ARC_R))
pts.append((ARC_R, 0, ZP + 12))
pts.append((-ARC_R, 0, ZP + 12))
me = bpy.data.meshes.new("CAP_ArchedBay_glass")
me.from_pydata(pts, [], [list(range(len(pts)))])
me.update()
me.materials.append(M_GLASS)
ob = bpy.data.objects.new("CAP_ArchedBay", me)
ob.location = (0, PY - 0.2, 0)
ob.parent = root_arch
link(ob, CAP)

# telaio dell'arco: montanti + archi + nodi circolari  [EST]
frame_c = [(-ARC_R * 0.66, PY - 0.4, ZP + 12 + 66), (0.0, PY - 0.4, ZP + 12 + 66),
           (ARC_R * 0.66, PY - 0.4, ZP + 12 + 66)]
for i, (fx, fy, fz) in enumerate(frame_c):
    prim("box", f"CAP_Glazing_mullion_{i}", fx, fy, fz - 45, M_FRAME, parent=root_arch,
         coll=CAP, sx=2.4, sy=0.8, sz=90)
for i, rz in enumerate([26, 46, 66]):
    r = ARC_R * math.sqrt(max(0.0, 1 - (rz / ARC_R) ** 2)) if rz <= ARC_R else 0
    if r > 1:
        prim("box", f"CAP_Glazing_arch_{i}", 0, PY - 0.4, ZP + 12 + 66 + rz, M_FRAME,
             parent=root_arch, coll=CAP, sx=2 * r, sy=0.8, sz=1.8)
# nodi circolari alle intersezioni
for fx in (-ARC_R * 0.66, 0.0, ARC_R * 0.66):
    for fz in (ZP + 12 + 66 - 45, ZP + 12 + 35, ZP + 12 + 79):
        if fx == 0.0 and fz >= ZP + 12 + 79:
            continue
        prim("disc", f"CAP_Glazing_node_{abs(fx):.0f}_{fz:.0f}", fx, PY - 0.5, fz,
              M_FRAME, parent=root_arch, coll=CAP, r=2.4, h=1.0, seg=14)

# ── FACCIATA LATO EST (X+): campata rettangolare + pannello semicirc. ──
prim("box", "CAP_RectangularBay_wall", PX - 2, 0, ZP + 12, M_PLASTER, parent=root_arch,
     coll=CAP, sx=2.5, sy=30, sz=80)
# apertura vetrata rettangolare 40 × 50
prim("box", "CAP_RectangularBay_glass", PX - 1.2, 0, ZP + 12 + 8, M_GLASS, parent=root_arch,
     coll=CAP, sx=0.4, sy=40, sz=50)
# pannello semicircolare a rilievo sopra [OBS-VISUAL]
prp = []
for i in range(seg + 1):
    a = math.pi * (1 - i / seg)
    prp.append((math.cos(a) * 20, 0.0, math.sin(a) * 20))
me2 = bpy.data.meshes.new("CAP_ReliefPanels_PROXY")
me2.from_pydata(prp, [], [list(range(len(prp)))])
me2.update()
me2.materials.append(M_STONE)
ob2 = bpy.data.objects.new("CAP_ReliefPanels_PROXY", me2)
ob2.location = (PX - 1.2, 0, ZP + 12 + 62)
ob2.parent = root_arch
link(ob2, CAP)
# colonne già ai lati (angoli est)

# ── RETRO (Y-): fascia piena + 2 vetrate rettangolari ──
prim("box", "CAP_RearWall", 0, -PY + 2, ZP + 12, M_PLASTER, parent=root_arch, coll=CAP,
     sx=108, sy=2.5, sz=88)
for dx in (-24, 24):
    prim("box", f"CAP_RearWindow_{dx}", dx, -PY + 1.4, ZP + 12 + 22, M_GLASS, parent=root_arch,
         coll=CAP, sx=28, sy=0.4, sz=40)

# ── ENTABLATURA (cornice + dentelli) ─────────────────────────────────
prim("box", "CAP_Entablature", 0, 0, 112, M_PLASTER, parent=root_arch, coll=CAP,
     sx=118, sy=96, sz=8)
dent_off = 4.0
for dx in range(-52, 53, 7):
    if abs(dx) <= 52:
        prim("box", f"CAP_Entablature_dentel_{dx:+04d}", dx, PY + dent_off, 114, M_STONE,
             parent=root_arch, coll=CAP, sx=3.4, sy=3.4, sz=4)
        prim("box", f"CAP_Entablature_dentel2_{dx:+04d}", dx, -PY - dent_off, 114, M_STONE,
             parent=root_arch, coll=CAP, sx=3.4, sy=3.4, sz=4)

# ── TERRAZZA + BALUSTRA ─────────────────────────────────────────────
prim("box", "CAP_RoofTerrace", 0, 0, 120, M_TERRACE, parent=root_arch, coll=CAP,
     sx=120, sy=98, sz=3)
# balaustra perimetrale [OBS-VISUAL]
bals = []
for px_ in range(-58, 59, 6):
    for py_ in (-48, 48):
        prim("box", f"CAP_Balustrade_pier_{px_:+04d}_{py_:+03d}", px_, py_, 123, M_STONE,
             parent=root_arch, coll=CAP, sx=2.8, sy=2.8, sz=10)
for py_ in range(-42, 43, 6):
    prim("box", f"CAP_Balustrade_pier2_0_{py_:+03d}", -58, py_, 123, M_STONE,
         parent=root_arch, coll=CAP, sx=2.8, sy=2.8, sz=10)
    prim("box", f"CAP_Balustrade_pier2_1_{py_:+03d}", 58, py_, 123, M_STONE,
         parent=root_arch, coll=CAP, sx=2.8, sy=2.8, sz=10)
prim("box", "CAP_Balustrade_rail", 0, 0, 130.5, M_STONE, parent=root_arch, coll=CAP,
     sx=121, sy=99, sz=2.4)

# ── SCALA ESTERNA (lato X+, da roccaglia al terrazzo) [OBS-VISUAL] ──
# rampa 1: da y=-30 a y=+30, quota 6 → 63 ; rampa 2: quota 63 → 120
for i in range(9):
    prim("box", f"CAP_ExternalStair_t1_{i:02d}", PX + 4, -44 + i * 10, ZP + i * 6.5, M_STONE,
         parent=root_arch, coll=CAP, sx=7, sy=10, sz=6)
for i in range(9):
    prim("box", f"CAP_ExternalStair_t2_{i:02d}", PX + 4, 46 + i * 10, ZP + 58 + i * 6.5, M_STONE,
         parent=root_arch, coll=CAP, sx=7, sy=10, sz=6)
# pianerottolo
prim("box", "CAP_ExternalStair_landing", PX + 4, 4, ZP + 57, M_STONE, parent=root_arch,
     coll=CAP, sx=12, sy=16, sz=6)
# parapetto scala
prim("box", "CAP_ExternalStair_rail", PX + 9, 10, ZP + 60, M_FRAME, parent=root_arch, coll=CAP,
     sx=1.6, sy=120, sz=2)

# ── STATUE PROXY ai lati della facciata principale [OBS-VISUAL] ─────
for i, sx_ in enumerate((-1, 1)):
    bx = sx_ * 56
    prim("box", f"CAP_Statues_PROXY_{i}_base", bx, PY + 2, ZP, M_STONE, parent=root_arch,
         coll=CAP, sx=10, sy=8, sz=14)
    prim("cyl", f"CAP_Statues_PROXY_{i}_body", bx, PY + 2, ZP + 14, M_STATUE,
         parent=root_arch, coll=CAP, r=2.2, h=24, seg=12)
    prim("sphere", f"CAP_Statues_PROXY_{i}_head", bx, PY + 2, ZP + 14 + 26, M_STATUE,
         parent=root_arch, coll=CAP, r=3.2, seg_u=12, seg_v=8)

# ── IL PORTALE (separato): proxy dal PDF — struttura a goccia [UNK] ──
port_root = bpy.data.objects.new("IL_PORTALE_ROOT", None)
link(port_root, PORT)
prim("sphere", "PORTALE_PROXY_drop", 0, 0, 30, M_STATUE, parent=port_root, coll=PORT,
     r=16, seg_u=18, seg_v=14)
prim("box", "PORTALE_PROXY_screen", 0, 14, 52, M_FRAME, parent=port_root, coll=PORT,
     sx=16, sy=2, sz=10)
prim("box", "PORTALE_PROXY_keys", 0, 4, 14, M_BASE, parent=port_root, coll=PORT,
     sx=12, sy=8, sz=6)
# portale posizionato provvisoriamente al centro (Y=0, Z=a livello piano)
port_root.location = (0, -6, ZP + 14)

# ── 5 CAMERE DI VERIFICA ────────────────────────────────────────────
def make_cam(name, loc, rot, coll):
    cam = bpy.data.cameras.new(name)
    ob = bpy.data.objects.new(name, cam)
    ob.location = loc
    ob.rotation_euler = (math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]))
    link(ob, coll)
    return ob

CAM_COLL = CAM  # already created

make_cam("EXT_FRONT_3Q", (140, -60, 50), (58, 0, 125), CAM_COLL)
make_cam("EXT_STAIR_3Q", (120, 70, 40), (68, 0, -70), CAM_COLL)
make_cam("EXT_POND", (-130, 180, 15), (8, 0, 10), CAM_COLL)
make_cam("INT_ENTRANCE", (0, 20, 40), (90, 0, 0), CAM_COLL)
make_cam("INT_PORTALE_POSITION", (10, -10, 35), (90, 0, 45), CAM_COLL)

# ── LUCE ────────────────────────────────────────────────────────────
# sun lamp
sun = bpy.data.lights.new("CAP_Sun", type="SUN")
sun.angle = 0.05
sun.energy = 4.2
sunob = bpy.data.objects.new("CAP_Sun", sun)
sunob.location = (-80, 100, 200)
sunob.rotation_euler = (math.radians(60), math.radians(10), math.radians(150))
link(sunob, LIG)

# environment light
world = scene.world
if not world:
    world = bpy.data.worlds.new("CAP_World")
    scene.world = world
world.use_nodes = True
# in Blender 5.2, .use_nodes might not populate defaults on existing world
nodes = world.node_tree.nodes
if "Background" not in nodes:
    ng = world.node_tree
    bg = ng.nodes.new("ShaderNodeBackground")
    if "World Output" in nodes:
        wo = nodes["World Output"]
        ng.links.new(bg.outputs[0], wo.inputs[0])
else:
    bg = nodes["Background"]
bg.inputs["Strength"].default_value = 0.6
bg.inputs["Color"].default_value = (0.6, 0.65, 0.75, 1)

# eevee
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = True

# ── REPORT FINALE ────────────────────────────────────────────────────
print("=" * 60)
print("CAPROTTI BLOCKOUT v1 — BUILD COMPLETE")
print("=" * 60)
print(f"Collections: {[c.name for c in bpy.data.collections]}")
print(f"Total objects: {len(bpy.data.objects)}")
print(f"Cameras: {[o.name for o in bpy.data.objects if o.type == 'CAMERA']}")
for c_n, c in zip(["EXT_FRONT_3Q", "EXT_STAIR_3Q", "EXT_POND", "INT_ENTRANCE", "INT_PORTALE_POSITION"],
                  [(140, -60, 50), (120, 70, 40), (-130, 180, 15), (0, 20, 40), (10, -10, 35)]):
    print(f"  {c_n}: {c}")
print(f"Arch root scale factor: {root_arch.scale[0]:.4f} (rescale all CAPROTTI_ARCHITECTURE via this)")
print("All ratios documented in header. [UNK] tags: internal dimensions, roof, rear full elevation")
print("Quality gate BLOCKOUT: run auto-review before proceeding to Phase 3 (3 collocation hps)")

# ── SALVATAGGIO ────────────────────────────────────────────────────
save_path = "/workspace/versions/0043.blend"  # fallback: scrive sopra
import sys
if "--" in sys.argv:
    argv2 = sys.argv[sys.argv.index("--") + 1:]
    if len(argv2) > 0:
        save_path = argv2[0]
bpy.ops.wm.save_as_mainfile(filepath=save_path)
print("SAVE_OK:" + save_path)