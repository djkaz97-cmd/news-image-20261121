# Build-time gate verification: entry.png integrity, dimensions and byte cap.
from pathlib import Path

from PIL import Image

repo = Path(__file__).resolve().parent.parent
p = repo / "entry.png"
data = p.read_bytes()

assert data[:8] == b"\x89PNG\r\n\x1a\n", "bad PNG magic"
assert len(data) <= 1_048_576, f"too big: {len(data)}"

img = Image.open(p)
img.verify()                      # integrity of every chunk
img = Image.open(p)
assert img.format == "PNG", img.format
assert img.size == (1024, 1024), img.size

print(f"OK: {p.name} {len(data)} bytes, {img.size[0]}x{img.size[1]}, {img.mode}")
