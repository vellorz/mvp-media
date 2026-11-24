# Rule 330 reference sheets: every new asset / set mock-up beside 2+ Rick frames with a PASS/FAIL checklist.
# python3 refsheet_bcn.py OUTDIR   rows come from ROWS (our image(s), Rick frames, checklist [(item, PASS/FAIL, note)])
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)
T='/root/cc/tex/'; RK='/root/bcn/rick/'
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26); FR=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
def tile(p,h=520,bg=(236,230,218)):
    im=Image.open(p).convert('RGBA'); s=h/im.height; im=im.resize((max(1,int(im.width*s)),h))
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def sheet(name,title,ours,ricks,checks,extra_rows=None):
    tiles=[(tile(p),cap) for p,cap in ours]+[(tile(RK+r+'.jpg'),'Rick '+r) for r in ricks]
    W=sum(t.width for t,_ in tiles)+20*(len(tiles)+1); W=max(W,1400); H=60+520+50+40*len(checks)+30
    im=Image.new('RGB',(W,H),(250,248,244)); d=ImageDraw.Draw(im); d.text((20,14),title,font=FB,fill=(30,30,30)); x=20
    for t,cap in tiles: im.paste(t,(x,60)); d.text((x,586),cap,font=FR,fill=(60,60,60)); x+=t.width+20
    y=630; allpass=True
    for it,res,note in checks:
        allpass&=(res=='PASS'); d.text((20,y),('[PASS] ' if res=='PASS' else '[FAIL] ')+it,font=FB if res!='PASS' else FR,fill=(20,120,40) if res=='PASS' else (190,30,30)); d.text((1000,y),note,font=FR,fill=(80,80,80)); y+=40
    im.save(f'{OUT}/{name}.jpg',quality=88); return allpass
if __name__=='__main__':
    PV='/root/bcn/prev/'; ST='/root/bcn/stills/'; ST2='/root/bcn/stills2/'; T_='/root/cc/tex/'
    res={}
    res['A01_boater3d']=sheet('A01_boater3d','New asset: boater3d straw hat (library item)',[(T_+'hero_h_happy@R2.png','hero, R2 turn'),(T_+'hero_h_grin@L2.png','hero, L2 turn'),(ST+'S01_0028.png','in shot S01')],['r23_f665','r23_f690'],
        [('Flat straw crown + wide brim + dark band, reads as a boater','PASS','same build as Rick #23 f665 boater'),('Sits tilted on the head at 3/4 turns (rule 333)','PASS','tilt follows the turn level'),('Ink weight matches the head outline','PASS','OUT 23 px'),('No logo or text on the band','PASS','')])
    res['A02_props']=sheet('A02_props','New props: 1899 football, newspaper, suitcase, dumbbell (rule 375: nameable at a glance)',[(T_+'hero_arm_ball.png','ball'),(T_+'hero_arm_paper.png','newspaper'),(T_+'heroH_arm_suitcase.png','suitcase'),(T_+'gymA_arm_dumbbell.png','dumbbell')],['r23_f440','r23_f520'],
        [('Each prop held in the mitten, not floating (Rick f440 paper, f520 note)','PASS','mitten drawn over the prop'),('Readable as the named object at phone size','PASS','ball laces, masthead bar, handle + straps, two weights'),('Prop never in an arm a combo swaps (vanishing prop)','PASS','builder rule F4; nobody walks holding a prop'),('Ball leather brown, no modern panel pattern','PASS','1899 laced ball')])
    res['A03_paper_insert']=sheet('A03_paper_insert','New asset: LOS DEPORTES page with the FOOT-BALL notice (S02) and the misprint circled (S06)',[(PV+'N_desk_paper.png','set preview'),(ST+'S02_0113.png','S02'),(ST+'S06_0508.png','S06')],['r23_f440','r21_f1030'],
        [('Newspaper reads as a period paper (masthead, columns), like Rick #23 f440','PASS',''),('Notice text legible on a phone in the insert','PASS','push ends ~0.5 m over the page'),('Name misprint "Kans Kamper" shown circled','PASS','red ring on S06'),('Date 22 OCTUBRE 1899 matches script fact 1','PASS','')])
    res['S01_night_street']=sheet('S01_night_street','Set R: Barcelona street at night, LOS DEPORTES + GIMNASIO in one building (S01, S09, S11)',[(PV+'R_street_night.png','preview'),('/root/bcn/stills5/S09_0760.png','S09 (r3b)'),('/root/bcn/stills5/S01_0060.png','S01 (r3b)')],['r10_f606','r10_f771'],
        [('Painted 3D buildings with ink edges, warm lamp pools (Rick #10 night porch)','PASS',''),('Both signs on the same block (fact 6)','PASS',''),('Street lamps planted on the pavement (rule 376)','PASS','base on the kerb-side walk'),('Night sky colour, no grey world band over the roofs','PASS','skydome cap')])
    res['S02_newsroom']=sheet('S02_newsroom','Set N: newsroom of Los Deportes (S02, S05-S08)',[(PV+'N_newsroom.png','preview'),('/root/bcn/stills4/S08_0600.png','S08 (r3b)'),(ST+'S05_0438.png','S05')],['r21_f1030','r23_f520'],
        [('Counter, clock at nine, type cases, hand press, pendant lamps','PASS',''),('Ceiling hides the sky over the walls (fixed in r2)','PASS','camera-only ceiling'),('Clerk stands behind the counter, feet on the floor (rule 372)','PASS','ground snap'),('Window swaps day/night with the shot','PASS','')])
    res['S03_gym']=sheet('S03_gym','Set G: Gimnasio Sole, rings, bars, founding table (S04, S10, S12)',[(PV+'G_gym.png','preview'),(ST+'S10_0841.png','S10'),(ST+'S12_0956.png','S12')],['r14_f695','r23_f520'],
        [('Long table with the twelve behind it (Rick #14 f695 banquet table)','PASS',''),('Gym kit: rings on ropes, parallel bars, dumbbell rack','PASS',''),('Lamps hang from ceiling cords, not floating (rule 376)','PASS',''),('All twelve faces visible, none hidden behind another','PASS','checked at 25 % res')])
    res['S04_velodrome']=sheet('S04_velodrome','Set V: old Bonanova bike track, banked oval, turf, goals, small stand (S13-S17)',[(PV+'V_velodrome.png','preview'),(ST2+'S13_1100.png','S13'),(ST2+'S15_1250.png','S15 board')],['r22_f1353','r24_f300'],
        [('Banked cycling track around a turf infield (fact 7: old bike track)','PASS',''),('Goals: two posts and a bar, no nets','PASS','1899 photos'),('Score board appears only after the goal (continuity)','PASS','fixed in r3'),('Hills + sky backdrop, no flat colour gaps','PASS','')])
    res['S05_stadium']=sheet('S05_stadium','Set B: big stadium bowl and crowd (S18)',[(PV+'B_stadium.png','preview'),('/root/bcn/stills5/S18_1440.png','S18 early (r3b)'),('/root/bcn/stills3/S18_1490.png','S18 late (r3)')],['r22_f1353','r22_f1293'],
        [('Packed crowd reads as people, like Rick #22 f1353','PASS','r3: crowd_xl big bright figures on upright stepped cards (r1 grey rows fixed)'),('No club crest, colours or real stadium likeness','PASS','generic bowl'),('Players stand on the pitch (rule 372)','PASS','')])
    res['S06_rambla_kiosk']=sheet('S06_rambla_kiosk','Set K: the Rambla today, plane trees, kiosk with the poster (S03, S19, S20)',[(PV+'K_rambla_kiosk.png','preview'),(ST2+'S19_1560.png','S19'),('/root/bcn/stills5/S20_1740.png','S20 payoff (r3b)')],['r21_f260','r24_f300'],
        [('Poster whole incl. border and bottom text in the payoff scene','PASS','on the kiosk side, framed'),('Plane trees and facades frame the promenade','PASS',''),('Falling leaves for environment life (rule 379)','PASS','leaf cards in S01/S03/S19/S20'),('Kiosk planted on the paving (rule 376)','PASS','')])
    res['A04_kit1899']=sheet('A04_kit1899','New cue: kit1899 plain football shirt (no crest, no stripes, no number)',[('/root/bcn/gate/castcheck.png/02_heroK.png','heroK'),('/root/bcn/gate/castcheck.png/14_engT1.png','engT1 (English, green)')],['r22_f1293','r10_f606'],
        [('Plain shirt, lace-up neck, no badge/stripes/number (no club kit)','PASS','brief: no official strip'),('Our side white, English side green: two teams read apart','PASS',''),('Body passes rule 336 sheet bands','PASS','castcheck 1.00/1.29/3.29 H')])
    json.dump(res,open(OUT+'/RESULTS.json','w'),indent=1); print(res)
