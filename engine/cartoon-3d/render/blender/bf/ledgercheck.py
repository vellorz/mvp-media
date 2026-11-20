# r7 rule 273: no ledger glyph touches a ruled line. For each text item, glyph bbox (anchor 'ls') must lie strictly between two ruled lines.
import sys; sys.path.insert(0,'/root/bf/src')
from PIL import ImageFont
FS='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
LINES=list(range(80,1024,40)); bad=0; n=0
def chk(label,x,y,s,size):
    global bad,n
    f=ImageFont.truetype(FS,size); x0,y0,x1,y1=f.getbbox(s,anchor='ls'); top,bot=y+y0,y+y1; n+=1
    hit=[L for L in LINES if top-2<=L<=bot+2]
    if hit: bad+=1; print('CROSS',label,s,top,bot,hit)
for k in range(18):
    BL=120+40*k-11
    for s in ('(9,999.99)','9,999.99','sales','gifts','toys','coats','hats'): chk(f'row{k}',0,BL,s,26)
for s in ('TOTAL','+ 18,240.00','(9,410.00)'): chk('total',0,990,s,28)
print('LEDGER_LINES',n,'items',bad,'cross')
# vertical rules: x=120, 728, 768, 1276 (W=1536). Column items must not straddle one.
VR=[120,728,768,1276]; vb=0
for lab,x,s,size in [('red',568,'(9,999.99)',26),('lab',808,'coats',26),('blk',1296,'9,999.99',26),('tot',W:=0,'',0)][:3]+[('redtot',438,'(9,410.00)',28),('TOTAL',828,'TOTAL',28),('blktot',1284,'+18,240.00',28)]:
    f=ImageFont.truetype(FS,size); x0,_,x1,_=f.getbbox(s,anchor='ls')
    h=[v for v in VR if x+x0-2<=v<=x+x1+2]
    if h: vb+=1; print('VCROSS',lab,s,x+x0,x+x1,h)
print('LEDGER_VRULES',vb,'cross')
