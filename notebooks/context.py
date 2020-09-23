```
put the current directory at the head of sys.path
so python can import modules from subfolders
```
import sys
from pathlib import Path

this_dir = Path(__file__).resolve().parent
root_dir = this_dir.parent
sys.path.insert(0, str(root_dir))
sep = "*" * 30
print(f"{sep}\ncontext imported. Front of path:\n{sys.path[0]}\n{sys.path[1]}\n{sep}\n")
