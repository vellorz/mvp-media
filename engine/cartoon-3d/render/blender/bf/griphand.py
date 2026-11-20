# S15 newspaper grips. r8b (Rick clone): the arm card already ends in a dark mitten at the grip point; this card redraws that mitten
# in front of the paper (plain round, 12 % of head width = 0.0516 m = 97 px on the 0.17 m / 320 px card), centred on the card.
from PIL import Image, ImageDraw
T='/root/bf/tex/'; K=(44,22,40,255)
def grip():
    im=Image.new('RGBA',(640,840),(0,0,0,0)); d=ImageDraw.Draw(im); d.ellipse([320-97,420-97,320+97,420+97],fill=K)
    return im.resize((320,420),Image.LANCZOS)
g=grip(); g.save(T+'grip_R.png'); g.transpose(Image.FLIP_LEFT_RIGHT).save(T+'grip_L.png'); print('GRIP_OK')
