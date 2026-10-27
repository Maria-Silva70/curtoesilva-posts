from PIL import Image, ImageDraw, ImageFont
import os, math, json, sys
D=os.path.dirname(os.path.abspath(__file__)); S=D+'/../stories/'; P=os.path.abspath(D+'/../..')+'/'
F=S+'fontes/BarlowCondensed-'; FB=S+'fontes/Barlow-'
BG=(30,26,24); OR=(232,96,28); WH=(255,255,255); GR=(205,200,196); W,H=1080,1350
f=lambda n,s: ImageFont.truetype(n,s)
logo=Image.open(S+'logo-curto-e-silva.png').convert('RGBA')
def wrap(d,t,ft,w):
    out=[]
    for para in t.split('\n'):
        l=''
        for wd in para.split():
            c=(l+' '+wd).strip()
            if d.textlength(c,font=ft)<=w: l=c
            else: out.append(l); l=wd
        out.append(l)
    return out
def star(d,cx,cy,r,fill):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*0.45
        pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    d.polygon(pts,fill=fill)
def frame(n,tot,last=False):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,14),fill=OR)
    lg=logo.resize((120,120),Image.LANCZOS); im.paste(lg,(70,50),lg)
    t=f'{n}/{tot}'; ft=f(F+'Bold.ttf',40); w=d.textlength(t,font=ft)
    d.rounded_rectangle((W-70-w-44,66,W-70,126),radius=30,outline=OR,width=3); d.text((W-70-w-22,73),t,font=ft,fill=OR)
    d.text((70,1265),'@curtoesilva',font=f(FB+'SemiBold.ttf',36),fill=WH)
    ft=f(F+'Bold.ttf',38)
    if last:
        t='BH · CONTAGEM · NOVA LIMA'; d.text((W-70-d.textlength(t,font=ft),1265),t,font=ft,fill=OR)
    else:
        t='ARRASTE'; x=W-70-44-d.textlength(t,font=ft); d.text((x,1265),t,font=ft,fill=OR)
        ax=W-70-36; ay=1286; d.line((ax,ay,ax+30,ay),fill=OR,width=5); d.polygon([(ax+34,ay),(ax+18,ay-12),(ax+18,ay+12)],fill=OR)
    return im,d
def tag(d,x,y,t):
    ft=f(F+'Bold.ttf',42); w=d.textlength(t,font=ft)
    d.rectangle((x,y,x+w+40,y+64),fill=OR); d.text((x+20,y+8),t,font=ft,fill=(20,16,14)); return y+64
def fit_head(d,t,maxh,w,sizes):
    for s in sizes:
        ft=f(F+'ExtraBold.ttf',s); ls=wrap(d,t,ft,w)
        if len(ls)*s*1.0<=maxh: return ft,ls,s
    return ft,ls,s
def cover(c,n,tot):
    im,d=frame(n,tot); y=tag(d,70,330,c['tag'])+70
    ft,ls,s=fit_head(d,c['head'],560,940,[140,128,116,104])
    for l in ls: d.text((70,y),l,font=ft,fill=WH); y+=int(s*1.0)
    y+=30; fs=f(F+'SemiBold.ttf',60)
    for l in wrap(d,c['sub'],fs,940): d.text((70,y),l,font=fs,fill=OR); y+=70
    return im
def content(c,n,tot):
    im,d=frame(n,tot); y=300
    if c.get('kicker'): y=tag(d,70,y,c['kicker'])+60
    ft,ls,s=fit_head(d,c['head'],360,940,[112,104,96,88,80])
    for l in ls: d.text((70,y),l,font=ft,fill=WH); y+=int(s*1.0)
    y+=40; fb=f(FB+'Medium.ttf',58)
    if c.get('body'):
        for l in wrap(d,c['body'],fb,940): d.text((70,y),l,font=fb,fill=GR); y+=78
    for b in c.get('bullets',[]):
        d.rectangle((70,y+24,98,y+52),fill=OR); ls2=wrap(d,b,fb,840)
        for l in ls2: d.text((124,y),l,font=fb,fill=WH); y+=74
        y+=30
    return im
def quote(c,n,tot):
    im,d=frame(n,tot); y=310
    for i in range(5): star(d,104+i*84,y+36,38,OR)
    y+=130; fq=f(F+'SemiBold.ttf',96)
    for l in wrap(d,'“'+c['quote']+'”',fq,940): d.text((70,y),l,font=fq,fill=WH); y+=100
    y+=50; ft=f(F+'ExtraBold.ttf',68); d.text((70,y),c['name'],font=ft,fill=OR); y+=84
    d.text((70,y),c['ctx'],font=f(FB+'Medium.ttf',44),fill=GR)
    return im
def cta(c,n,tot):
    im,d=frame(n,tot,True); y=300
    ft,ls,s=fit_head(d,c['head'],420,940,[120,108,96,84])
    for l in ls: d.text((70,y),l,font=ft,fill=WH); y+=int(s*1.0)
    y+=24; fs=f(F+'SemiBold.ttf',56)
    for l in wrap(d,c['sub'],fs,940): d.text((70,y),l,font=fs,fill=OR); y+=64
    y=max(y+50,830); d.rounded_rectangle((70,y,W-70,y+120),radius=24,fill=OR)
    fb=f(F+'ExtraBold.ttf',64); t='ORÇAMENTO SEM CUSTO'; d.text(((W-d.textlength(t,font=fb))/2,y+26),t,font=fb,fill=(20,16,14))
    fw=f(F+'Bold.ttf',60); t='WhatsApp (31) 99984-6776'; d.text(((W-d.textlength(t,font=fw))/2,y+170),t,font=fw,fill=WH)
    d.text((70,y+270),'A nova geração que honra o velho compromisso.',font=f(FB+'Medium.ttf',38),fill=GR)
    return im
K={'cover':cover,'content':content,'quote':quote,'cta':cta}
def build(pid,slides):
    out=P+'posts-novos/'+pid+'/'; os.makedirs(out,exist_ok=True)
    for i,c in enumerate(slides,1):
        K[c['kind']](c,i,len(slides)).save(out+f'{i}.jpg',quality=92)
if __name__=='__main__':
    data=json.load(open(D+'/novembro.json',encoding='utf-8'))
    for pid,sl in data.items():
        if len(sys.argv)<2 or pid in sys.argv[1:]: build(pid,sl)
