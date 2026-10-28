# Etsy listing video (shop-wide, Oct 28 2026)
etsy-listing-video.mp4: 1080x1080, 10 s, 30 fps, H.264, silent, ~3.9 MB. Same file goes on every listing.
Look: sunlit plaster wall, oak frame + mat, leaf shadows, 7 posters swap every 1.2 s with museum placard, torn-paper end card (logo, "Vintage travel posters", "600+ destinations · several sizes"), seamless loop back to Cefalù.
Rebuild: Remotion 4.0.537 project = src/ + public/{posters/*.png, logo.png, fonts/cg*.woff2} + .browser (headless shell path); node stills.mjs <frames>; node render.mjs . ; then ffmpeg re-encode -an -movflags +faststart.
Posters/logos source: repo vellorz/mvp-media branch claude/project-thread-1je1p3, etsy-listing-video/.
