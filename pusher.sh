#!/bin/bash
black "."
isort .
pdoc3 --force --html -o docs pvp
mv docs/pvp/index.html docs/index.md
mv docs/pvp/* docs/
git fetch
git add . && git commit -m $1 && git push
