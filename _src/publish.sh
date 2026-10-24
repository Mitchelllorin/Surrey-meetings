#!/bin/sh
# Rebuild everything and push the web app live. The site is served from the gh-pages branch.
set -e
cd "$(dirname "$0")"
python3 build.py
cd site
git add -A
git -c user.name="Mitchelllorin" -c user.email="mitchelllorinmcknight@gmail.com" commit -qm "${1:-Update meeting list}" || echo "nothing new"
git push -q origin main
git push -q origin main:gh-pages
echo "pushed: https://mitchelllorin.github.io/Surrey-meetings/"
