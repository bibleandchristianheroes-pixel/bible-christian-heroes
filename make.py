"""python3 make.py episodes/ep008_x.py [--preview 3 7 12]  -> out/<name>.mp4 + prev/<name>_sheet.png"""
import importlib.util, os, subprocess, sys
from engine import Episode
here = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1]
spec = importlib.util.spec_from_file_location("ep", path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
cls = [v for v in vars(mod).values() if isinstance(v, type) and issubclass(v, Episode) and v is not Episode][0]
name = getattr(mod, "OUTPUT_NAME", os.path.splitext(os.path.basename(path))[0])
ep = cls()
os.makedirs(f"{here}/out", exist_ok=True); os.makedirs(f"{here}/prev", exist_ok=True)
if "--preview" in sys.argv:
    ts = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1:]]
    ep.render(f"{here}/prev/{name}.mp4", preview_times=ts)
    print("\n".join(f"{here}/prev/{name}.mp4.t{t:05.1f}.png" for t in ts))
else:
    out = f"{here}/out/{name}.mp4"; ep.render(out)
    sheet = f"{here}/prev/{name}_sheet.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf", "fps=0.5,scale=270:-1,tile=9x1", "-frames:v", "1", sheet], check=True)
    print(out); print(sheet)
