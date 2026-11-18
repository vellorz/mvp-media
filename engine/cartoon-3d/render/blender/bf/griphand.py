# Front-view hands gripping a newspaper edge (S15): mitten palm just outside the paper edge, thumb over the paper front, navy sleeve from below.
from PIL import Image, ImageDraw
T='/root/bf/tex/'; K=(30,22,20,255); SK=(252,246,236,255); NAVY=(38,52,96,255); O=12
def grip():
    im=Image.new('RGBA',(320,420),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.polygon([(190,420),(310,420),(300,250),(200,240)],fill=NAVY,outline=K); d.line([(190,420),(200,240)],fill=K,width=O); d.line([(310,420),(300,250)],fill=K,width=O)  # sleeve rising from below-outside
    d.rounded_rectangle([188,210,312,268],20,fill=(250,250,245,255),outline=K,width=10)   # cuff
    d.ellipse([150,70,310,240],fill=SK,outline=K,width=O)                                 # palm/fingers behind the paper edge
    d.rounded_rectangle([40,110,200,175],32,fill=SK,outline=K,width=O)                    # thumb across the paper front
    return im
g=grip(); g.save(T+'grip_R.png'); g.transpose(Image.FLIP_LEFT_RIGHT).save(T+'grip_L.png'); print('GRIP_OK')
