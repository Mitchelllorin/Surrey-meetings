from PIL import Image, ImageDraw, ImageFilter
import math
S=2048
BG=(10,32,72); LINK=(64,150,255); HI=(170,215,255); SHADOW=(4,14,36)

def link_layer(w,h,th,col,open_side=None,gap=0):
    """A chain link (stadium outline). open_side 'right'/'left' cuts it open."""
    pad=th; im=Image.new("RGBA",(w+2*pad,h+2*pad),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([pad,pad,pad+w,pad+h],radius=h//2,outline=col,width=th)
    if open_side:
        x0=pad+w-h//2 if open_side=="right" else pad-th
        x1=pad+w+th if open_side=="right" else pad+h//2
        d.rectangle([x0,pad+h//2-gap//2,x1,pad+h//2+gap//2],fill=(0,0,0,0)) if False else None
        cx=pad+w+th//2 if open_side=="right" else pad-th//2
        d.rectangle([cx-th,pad+h//2-gap//2,cx+th,pad+h//2+gap//2],fill=(0,0,0,0))
    return im

def place(base,layer,cx,cy,ang):
    r=layer.rotate(ang,resample=Image.BICUBIC,expand=True)
    base.alpha_composite(r,(int(cx-r.width/2),int(cy-r.height/2)))

def draw_link(base,cx,cy,ang,open_side=None):
    w,h,th=560,300,80
    sh=link_layer(w,h,th,SHADOW+(170,),open_side,gap=130).filter(ImageFilter.GaussianBlur(22))
    place(base,sh,cx+26,cy+34,ang)
    place(base,link_layer(w,h,th,LINK+(255,),open_side,gap=130),cx,cy,ang)
    hl=link_layer(w-th+18,h-th+18,22,HI+(150,),open_side,gap=165)
    place(base,hl,cx-10,cy-12,ang)

im=Image.new("RGBA",(S,S),BG+(255,))
# soft glow behind
g=Image.new("RGBA",(S,S),(0,0,0,0)); ImageDraw.Draw(g).ellipse([S*.2,S*.2,S*.8,S*.8],fill=(40,110,220,90))
im.alpha_composite(g.filter(ImageFilter.GaussianBlur(220)))
ang=35; dx,dy=math.cos(math.radians(ang)),-math.sin(math.radians(ang))
c=S/2; step=300; split=95
# left link, then the break, then right link: each half is an open link pulled apart
draw_link(im,c-dx*(step+split),c-dy*(step+split),ang,open_side="right")
draw_link(im,c+dx*(step+split),c+dy*(step+split),ang,open_side="left")
# burst in the gap
d=ImageDraw.Draw(im)
for i,a in enumerate(range(0,360,40)):
    r0,r1=48,(140 if i%2==0 else 100); t=math.radians(a+20)
    d.line([c+r0*math.cos(t),c+r0*math.sin(t),c+r1*math.cos(t),c+r1*math.sin(t)],fill=HI+(255,),width=22)
im=im.convert("RGB")
for s in (512,192): im.resize((s,s),Image.LANCZOS).save(f"site/icon-{s}.png")
im.resize((512,512),Image.LANCZOS).save("icon-preview.png")
