"""Build the meeting finder.

  python3 build.py

Makes two single-file pages in dist/:
  edic-meetings.html     your own copy, with your phone list
  surrey-meetings.html   the one to give away: same meetings, no phone list

To add a new list (another flyer, another fellowship), drop a file in sources/
that calls addSource({...}) the same way the others do, then build again.
"""
import glob, json, datetime, pathlib

ROOT = pathlib.Path(__file__).parent
style = (ROOT / "style.part.html").read_text()
app = (ROOT / "app.part.html").read_text()
sources = sorted(glob.glob(str(ROOT / "sources" / "*.js")))
built = datetime.date.today().strftime("%-d %b %Y")

def page(title, sub, personal):
    mods = [pathlib.Path(p).read_text() for p in sources]
    if personal:
        mods.append((ROOT / "people.private.js").read_text())
    cfg = {"title": title, "sub": sub, "personal": personal, "built": built}
    head = (f"<title>{title}</title>\n"
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Atkinson+Hyperlegible:wght@400;700&display=swap">\n')
    scripts = f"<script>window.BUILD={json.dumps(cfg)};</script>\n" + \
              "\n".join(f"<script>\n{m}\n</script>" for m in mods)
    return head + style + "\n" + app.replace("<!--@MODULES-->", scripts)

def standalone(body):
    # Full HTML document so the file opens on any phone or computer by itself.
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
            '[hidden]{display:none!important}body{margin:0}</style>\n'
            + body.replace("</style>\n", "</style>\n</head><body>\n", 1) + "\n</body></html>\n")

(ROOT / "dist").mkdir(exist_ok=True)
mine = page("EDIC Meetings", "Easy Does It Club · 7277 King George Blvd, Surrey · plus meetings across Surrey", True)
share = page("Surrey Meetings", "AA, NA, CA, CMA and SA meetings around Surrey, BC", False)
(ROOT / "dist" / "edic-meetings.html").write_text(mine)                      # published as the private artifact
(ROOT / "dist" / "surrey-meetings.html").write_text(standalone(share))      # the file to give away
(ROOT / "dist" / "surrey-meetings.artifact.html").write_text(share)         # same, as a shareable artifact
# The web app for GitHub Pages: the give-away page plus home-screen icon and offline support.
site_head = ('<link rel="manifest" href="manifest.webmanifest">\n'
             '<meta name="theme-color" content="#0f6e6a">\n'
             '<link rel="icon" href="icon-192.png">\n'
             '<link rel="apple-touch-icon" href="icon-192.png">\n'
             '<meta name="description" content="AA, NA, CA, CMA and SA meetings around Surrey, BC">\n')
site_sw = ('<script>if("serviceWorker" in navigator){addEventListener("load",()=>'
           'navigator.serviceWorker.register("sw.js").catch(()=>{}))}</script>\n')
site = standalone(share).replace("<title>", site_head + "<title>", 1).replace("</body>", site_sw + "</body>", 1)
(ROOT / "site" / "index.html").write_text(site)

print("built", len(sources), "sources ->", [p.name for p in (ROOT / "dist").iterdir()])
