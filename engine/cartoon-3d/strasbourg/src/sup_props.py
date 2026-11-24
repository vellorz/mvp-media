import sys; sys.path.insert(0,'/root/sb/src')
from PIL import Image
import cast as K
for n,p in [('kidC','gift')]:
    im=K.arm(n,p); im.save(f'{K.T}{n}_arm_{p}.png'); im.transpose(Image.FLIP_LEFT_RIGHT).save(f'{K.T}{n}_arm_{p}_L.png')
print('PROPS_OK')
