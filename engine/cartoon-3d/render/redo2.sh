#!/bin/bash
cd /home/user/cart2; N=out/c2/final21/new; E="SCALE=1.3333333333333333 REMOTION_TMP=/home/user/rtmp"
( for i in 1 2 3; do
    ONLY=base SCALE=1.3333333333333333 REMOTION_TMP=/home/user/rtmp node scripts/ranges.mjs /home/user/cart2 ChicagoV2 $N/p2/r0.json $N/p2 1 >> $N/redo0.txt 2>&1
    tail -1 $N/redo0.txt | grep -q RENDERED && break; done
  for i in 1 2 3; do
    SCALE=1.3333333333333333 REMOTION_TMP=/home/user/rtmp node scripts/overframes.mjs /home/user/cart2 ChicagoV2 $N/d0.json $N/over0 1 >> $N/redo0.txt 2>&1
    tail -1 $N/redo0.txt | grep -q RENDERED && { echo DONE >> $N/redo0.txt; break; }; done ) &
sleep 60
( for i in 1 2 3; do
    SCALE=1.3333333333333333 REMOTION_TMP=/home/user/rtmp node scripts/overframes.mjs /home/user/cart2 ChicagoV2 $N/d1.json $N/over1 1 >> $N/redo1.txt 2>&1
    tail -1 $N/redo1.txt | grep -q RENDERED && { echo DONE >> $N/redo1.txt; break; }; done ) &
wait
grep -q DONE $N/redo0.txt && grep -q DONE $N/redo1.txt && /home/user/work/fin/splice21.sh > out/c2/final21/splice.log 2>&1
tail -3 out/c2/final21/splice.log
