# supplemental textures after the parallel cast run: mother's gift arm, talk mouths for the two quoted speakers
import sys; sys.path.insert(0,'/root/sb/src')
from PIL import Image
import cast as K
T=K.T
for n,p in [('mother','gift')]:
    im=K.arm(n,p); im.save(f'{T}{n}_arm_{p}.png'); im.transpose(Image.FLIP_LEFT_RIGHT).save(f'{T}{n}_arm_{p}_L.png')
for n in ('kidA','councilA'):
    for fk in ('talkA','talkB','talkC','talkD'): K.head(n,fk).save(f'{T}{n}_h_{fk}.png')
print('SUP_OK')
