#!/bin/bash
# build final21 from kept v20 segs + re-rendered halves, then assemble
set -e
O=/home/user/cart2/out/c2/final20; D=/home/user/cart2/out/c2/final21; N=$D/new
mkdir -p $D/over0 $D/over1
P=$N/p2
for h in 350 400; do a=$(printf %04d $h); b=$(printf %04d $((h+25)))
  printf "file '$P/seg_$a.mp4'\nfile '$P/seg_$b.mp4'\n" > $P/c$a.txt
  ffmpeg -v error -y -f concat -safe 0 -i $P/c$a.txt -c copy $N/seg_$a.mp4
done
for s in 200 300 400 500 600 700 800 900 1000 1300 1400 1500; do
  a=$(printf %04d $s); b=$(printf %04d $((s+50)))
  printf "file '$N/seg_$a.mp4'\nfile '$N/seg_$b.mp4'\n" > $N/c$a.txt
  ffmpeg -v error -y -f concat -safe 0 -i $N/c$a.txt -c copy $D/seg_$a.mp4
  [ "$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $D/seg_$a.mp4)" = 100 ] || { echo BAD $a; exit 1; }
done
for f in $O/seg_*.mp4; do b=$(basename $f); [ -e $D/$b ] || ln -s $f $D/$b; done
for f in $O/over1/*.png $O/over0/*.png; do ln -sf $f $D/over1/; done
cp -f $N/over0/*.png $N/over1/*.png $D/over0/
ls $D/seg_*.mp4 | wc -l
python3 /home/user/work/fin/assemble.py $D 2>&1 | tee $D/assemble.log
