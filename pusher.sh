#!/bin/bash
black "."
isort .
pdoc -o docs policeVsProtesters
mv docs/policeVsProtesters/index.html docs/index.md
mv docs/policeVsProtesters/* docs/
git add . && git commit -m $1 && git push
