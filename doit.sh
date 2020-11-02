#!/bin/bash -v
jb build notebooks
cp -a notebooks/week6/images notebooks/_build/html/week6/.
cp -a notebooks/week6/figures notebooks/_build/html/week6/.
cp -a notebooks/week6/answers/figures notebooks/_build/html/week6/answers/.
cp -a notebooks/week9/figures notebooks/_build/html/week9/.
