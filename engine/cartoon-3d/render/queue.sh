#!/bin/bash
# wait for the Monday r3 render, then Tuesday (Eiffel), then Wednesday (Pisa)
while pgrep -f render_all.sh >/dev/null; do sleep 30; done
bash /home/user/cart/out/q/render_comp.sh EiffelShort /home/user/cart/out/e/r1 1962 /home/user/eiffel/audio/mix.wav /home/user/cart/out/e/r1/eiffel_r1.mp4 || exit 1
bash /home/user/cart/out/q/render_comp.sh PisaShort /home/user/cart/out/p/r1 2080 /home/user/pisa/audio/mix.wav /home/user/cart/out/p/r1/pisa_r1.mp4 || exit 1
echo QUEUEDONE
