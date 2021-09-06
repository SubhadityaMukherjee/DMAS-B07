#!/bin/bash
black "."
isort .
git add . && git commit -m $1 && git push
