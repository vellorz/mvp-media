# Top-down writing hand for the S13 ledger insert. r8b (Rick clone, guide v1.3 x.3): one dark noodle arm (5.5 % of head width = 79 px here),
# plain dark round mitten 12 % of head width (172 px), no thumb or fingers, gripping a slanted pen. 400x2500 card = 0.12 x 0.75 m plane, nib at the bottom edge.
from PIL import Image, ImageDraw
T='/root/bf/tex/'; K=(44,22,40,255)
def hand(pen):
    SS=2; full=Image.new('RGBA',(400*SS,2500*SS),(0,0,0,0)); d=ImageDraw.Draw(full); s=lambda v:int(v*SS)
    mx,my=262,2160
    P=[(330+(mx-330)*t+40*t*(1-t)*4*0.5,0+(my-0)*t) for t in [i/40 for i in range(41)]]   # gentle curve, no elbow
    d.line([(s(x),s(y)) for x,y in P],fill=K,width=s(79),joint='curve')
    d.line([s(200),s(2492),s(318),s(2050)],fill=K,width=s(40)); d.line([s(200),s(2492),s(318),s(2050)],fill=pen,width=s(26))   # pen barrel
    d.polygon([(s(188),s(2470)),(s(214),s(2476)),(s(200),s(2499))],fill=K)
    d.ellipse([s(mx-86),s(my-86),s(mx+86),s(my+86)],fill=K)   # mitten over the pen
    return full.resize((400,2500),Image.LANCZOS)
hand((196,30,30,255)).save(T+'exec81_writehand_red.png'); hand((24,24,28,255)).save(T+'exec81_writehand_black.png')
print('HAND_OK')
