import hashlib
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "contracts" / "minima.py"
data = path.read_bytes()
print(hashlib.sha256(data).hexdigest())
