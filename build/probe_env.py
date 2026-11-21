# Probe: Pillow availability + weekday of the target date (build-time only).
import datetime

import PIL

print("Pillow", PIL.__version__)
d = datetime.date(2026, 11, 21)
print(d.strftime("%A %d %B %Y"))
