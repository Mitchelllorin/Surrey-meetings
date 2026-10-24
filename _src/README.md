# Build source

Build files for the site. Nothing private is in here.

- `sources/` one file per meeting list. Add a new flyer or fellowship by adding a file that calls `addSource({...})`.
- `app.part.html`, `style.part.html` the app itself.
- `build.py` builds the give-away page into the site root as `index.html`.
- `publish.sh` builds and pushes live (main + gh-pages).

Mitchell's personal copy with his phone list is NOT here on purpose. It lives in his private Claude artifact "EDIC Meetings". To rebuild it, read that artifact for the PEOPLE list into `people.private.js` (never commit that file).
