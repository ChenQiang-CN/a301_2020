
```{code-cell}
from pathlib import Path
import sys
import pprint
```

```{code-cell}
a301_dir = Path("/Volumes/card/UBC/a301_code")
print(f"Status of a301_dir is {a301_dir.is_dir()}")
sys.path.insert(0, str(a301_dir))
stars = "*" * 20
print(f"{stars}\nfront of path is {pprint.pformat(sys.path[:4])}\n{stars}")
```
