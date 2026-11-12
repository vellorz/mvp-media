#!/bin/bash
# 2K final, clean setup: two browsers at concurrency 1 each (one GPU process per browser), every frame single-layer
# ("base"), dissolve over-layers rendered after as PNGs. Resumable; re-run until both workers print DONE.
cd /home/user/cart2
D=out/c2/final20; end=$((SECONDS+6900))
pkill -9 -f chrome-headless 2>/dev/null; sleep 2
( while true; do free -m | awk 'NR==2{print strftime("%H:%M:%S"), $3, $7}' >> $D/mem.txt; sleep 60; done ) & MP=$!
for k in 0 1; do (
  while [ $SECONDS -lt $end ]; do
    echo "=== run$k $(date)" >> $D/log$k.txt
    ONLY=base SCALE=1.3333333333333333 REMOTION_TMP=/home/user/rtmp timeout $((end-SECONDS)) node scripts/ranges.mjs /home/user/cart2 ChicagoV2 $D/r$k.json $D 1 >> $D/log$k.txt 2>&1
    tail -1 $D/log$k.txt | grep -q RENDERED || continue
    SCALE=1.3333333333333333 REMOTION_TMP=/home/user/rtmp timeout $((end-SECONDS)) node scripts/overframes.mjs /home/user/cart2 ChicagoV2 $D/d$k.json $D/over$k 1 >> $D/log$k.txt 2>&1
    tail -1 $D/log$k.txt | grep -q RENDERED && { echo DONE$k >> $D/log$k.txt; break; }
  done ) & W[$k]=$!
  sleep 90
done
wait ${W[0]} ${W[1]}
kill $MP
