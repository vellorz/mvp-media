import sys,glob
from PIL import Image,ImageDraw
fs=sorted(glob.glob(sys.argv[1]+'/*.png')); out=sys.argv[2]; per=int(sys.argv[3]) if len(sys.argv)>3 else 8
W,H=Image.open(fs[0]).size; cols=min(per,len(fs))
for p in range(0,len(fs),per*2):
    ch=fs[p:p+per*2]; im=Image.new('RGB',(W*cols,H*((len(ch)+cols-1)//cols)),(0,0,0)); d=ImageDraw.Draw(im)
    for i,f in enumerate(ch): im.paste(Image.open(f).convert('RGB'),((i%cols)*W,(i//cols)*H)); d.text(((i%cols)*W+5,(i//cols)*H+5),f.split('/')[-1],fill=(255,255,0))
    im.save(f'{out}_{p//(per*2)}.jpg',quality=85); print(f'{out}_{p//(per*2)}.jpg')
