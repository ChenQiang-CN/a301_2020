#!/bin/bash -v
jb build notebooks
cp -a notebooks/week6/images notebooks/_build/html/week6/.
cp -a notebooks/week6/figures notebooks/_build/html/week6/.
cp -a notebooks/week6/answers/figures notebooks/_build/html/week6/answers/.
cp -a notebooks/week9/figures notebooks/_build/html/week9/.
cp -a notebooks/week10/figures notebooks/_build/html/week10/.
mkdir -p notebooks/_build/html/week11/figures
cp -a notebooks/week11/figures/* notebooks/_build/html/week11/figures/.
mkdir -p notebooks/_build/html/week12/figures
cp -a notebooks/week12/figures/* notebooks/_build/html/week12/figures/.
