---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.8'
    jupytext_version: 1.5.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

+++ {"toc": true}

<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"></ul></div>

```{code-cell}
import numpy as np
theta=10*np.pi/180.
mu0 = np.cos(theta)
omega=2*np.pi*(1 - mu0)
print(f'solid angle omega is {omega} sr')
```

```{code-cell}
sin_theta=np.sin(theta)
print(f'A/r^2 = {np.pi*sin_theta**2}')
```

```{code-cell}

```
