# Build-time visual check: 300px thumbnail + illustration crop for inspection.
from pathlib import Path

from PIL import Image

repo = Path(__file__).resolve().parent.parent
scratch = Path("C:/Users/Kaz/AppData/Local/hermes/cache/scratch")
scratch.mkdir(parents=True, exist_ok=True)

img = Image.open(repo / "entry.png")
img.resize((300, 300), Image.Resampling.LANCZOS).save(scratch / "news21_thumb300.png")
img.crop((32, 392, 992, 600)).save(scratch / "news21_illustration.png")
print("thumb and crop written to", scratch)
