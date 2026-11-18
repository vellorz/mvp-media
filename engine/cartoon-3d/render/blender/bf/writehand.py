# Top-down writing hand for the S13 ledger insert: red sleeve, white cartoon mitten gripping a slanted pen, nib at the bottom centre.
# Drawn in the cast style (flat fill, dark monoline outline). 400x2500 card = 0.12 x 0.75 m plane, nib tip at the bottom edge.
from PIL import Image, ImageDraw
T='/root/bf/tex/'; K=(30,22,20,255); SK=(252,246,236,255); R=(190,40,50,255); O=14
def hand(pen):
    big=Image.new('RGBA',(400,900),(0,0,0,0))
    im=Image.new('RGBA',(400,900),(0,0,0,0)); d=ImageDraw.Draw(im)
    full=Image.new('RGBA',(400,2500),(0,0,0,0)); fd=ImageDraw.Draw(full)
    fd.rectangle([150,0,400,1700],fill=R); fd.line([150,0,150,1700],fill=K,width=O); fd.line([393,0,393,1700],fill=K,width=O)   # forearm sleeve rising to the elbow
    d.rounded_rectangle([150,-40,400,260],50,fill=R,outline=K,width=O)                 # sleeve entering from the top right
    d.rounded_rectangle([140,220,400,290],24,fill=(250,250,245,255),outline=K,width=O)  # shirt cuff
    # pen: slanted barrel from the nib (bottom centre) up to the right
    d.line([200,880,330,470],fill=K,width=40); d.line([200,880,330,470],fill=pen,width=26)
    d.polygon([(186,860),(214,868),(200,899)],fill=K)
    # mitten palm and fingers wrapped round the pen
    d.ellipse([150,270,390,560],fill=SK,outline=K,width=O)
    for i in range(3):
        y=560+i*48; d.rounded_rectangle([170-i*10,y-40,300-i*20,y+12],26,fill=SK,outline=K,width=11)   # three finger rolls
    d.ellipse([90,430,210,560],fill=SK,outline=K,width=12)                              # thumb on the left side of the pen
    full.alpha_composite(im,(0,1600)); return full
hand((196,30,30,255)).save(T+'exec81_writehand_red.png'); hand((24,24,28,255)).save(T+'exec81_writehand_black.png')
print('HAND_OK')
