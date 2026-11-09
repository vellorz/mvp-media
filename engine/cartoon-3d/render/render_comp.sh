#!/bin/bash
# usage: render_comp.sh <Comp> <outdir> <totalFrames> <mix.wav> <final.mp4>
COMP=$1; OUT=$2; TOTAL=$3; MIX=$4; FIN=$5; STEP=300
cd /home/user/cart
export REMOTION_TMP=/home/user/rtmp TMPDIR=/home/user/rtmp TEMP=/home/user/rtmp TMP=/home/user/rtmp
mkdir -p $OUT/chunks
for ((a=0; a<TOTAL; a+=STEP)); do
  b=$((a+STEP-1)); [ $b -ge $TOTAL ] && b=$((TOTAL-1))
  f=$OUT/chunks/c_$(printf %04d $a).mp4
  [ -s $f ] && continue
  echo "$COMP chunk $a-$b start $(date +%T)"
  npx remotion render src/index.ts $COMP $f.tmp.mp4 --frames=$a-$b --codec h264 --crf 16 --gl=swangle --concurrency=4 --log=error && mv $f.tmp.mp4 $f || { echo "$COMP chunk $a FAILED"; exit 1; }
  echo "$COMP chunk $a-$b done $(date +%T)"
done
ls $OUT/chunks/c_*.mp4 | sed "s#^.*/#file '#;s/$/'/" > $OUT/chunks/list.txt
ffmpeg -y -v error -f concat -safe 0 -i $OUT/chunks/list.txt -c copy $OUT/video.mp4
ffmpeg -y -v error -i $OUT/video.mp4 -i $MIX -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest $FIN
echo "$COMP DONE $FIN"
