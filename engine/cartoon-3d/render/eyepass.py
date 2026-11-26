#!/usr/bin/env python3
"""Owner's-eye pass (rule 378): contact sheets of a finished video at 2 frames per second.
Usage: python3 eyepass.py VIDEO OUT_DIR [fps=2] [cols=6]
Writes OUT_DIR/sheet_NNN.jpg (cols frames per sheet, 720 px wide each, time stamped)
and OUT_DIR/QUESTIONS.md, the list every shot is answered against."""
import subprocess, sys, os
Q = """# Owner's-eye pass (rule 378). Answer for every shot; each NO gets a timestamp.
1. Does anything pass through anything (rule 372)?
2. Do all planted feet rest on a surface (372)?
3. Does every character that travels take steps (373)?
4. Can each held object be named at a glance (375)?
5. Is each tool or weapon held and used the way it works (374)?
6. Is every structure planted, square and uncut by its supports (376)?
7. Is the camera smooth, above all on boats and vehicles (377)?
8. Is there one steady shadow per character (367, 367c)?
9. Is every hung object attached to a line anchored at both ends (380)?
10. Does any garment flicker at a pose change (381)? Step these frame by frame.
11. Does every falling or thrown object have a source and a landing (382)? Step frame by frame.
12. Is every character at a desk or table wholly on its own side, only hands on top (383)?
13. Is every handled or optical tool gripped by the handle, working end the right way (374f)?
"""
def main():
    v, out = sys.argv[1], sys.argv[2]
    fps = sys.argv[3] if len(sys.argv) > 3 else "2"
    cols = sys.argv[4] if len(sys.argv) > 4 else "6"
    os.makedirs(out, exist_ok=True)
    vf = (f"fps={fps},scale=720:-2,"
          "drawtext=text='%{pts\\:hms}':x=12:y=12:fontsize=40:fontcolor=white:box=1:boxcolor=black@0.6,"
          f"tile={cols}x1")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", v, "-vf", vf, "-q:v", "3",
                    os.path.join(out, "sheet_%03d.jpg")], check=True)
    open(os.path.join(out, "QUESTIONS.md"), "w").write(Q)
    print(len([f for f in os.listdir(out) if f.startswith("sheet_")]), "sheets in", out)
if __name__ == "__main__":
    main()
