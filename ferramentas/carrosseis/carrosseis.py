# Carrosséis no estilo do site curtoesilva.com.br (fundo escuro com grade de planta, laranja #ff6a1f, Inter)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math, json, sys
D=os.path.dirname(os.path.abspath(__file__)); S=D+'/../stories/'; P=os.path.abspath(D+'/../..')+'/'
FD=S+'fontes/'
BG=(7,8,10); AC=(255,106,31); AC2=(255,179,107); TX=(244,244,246); MU=(178,180,188); W,H=1080,1350; X0=80; TW=W-2*X0
f=lambda n,s: ImageFont.truetype(FD+n,s)
HEAD='InterDisplay-ExtraBold.otf'; HB='InterDisplay-Bold.otf'; BODY='Inter-Medium.otf'; SEMI='Inter-SemiBold.otf'
logo=Image.open(S+'logo-curto-e-silva.png').convert('RGBA')
HOUSE=["M20 280 L200 370 L380 280 M20 280 L200 190 L380 280","M60 260 L200 330 L340 260 L340 150 L200 220 L60 150 Z","M200 330 L200 220",
"M60 150 L130 70 L270 0 L340 150 M130 70 L200 220 M270 0 L340 150","M240 245 L300 215 L300 175 L240 205 Z M270 230 L270 190","M110 245 L150 265 L150 300 L110 280 Z"]
def paths(p):
    import re
    out=[];cur=[];start=None;t=re.findall(r'[MLZ]|-?\d+\.?\d*',p);i=0
    while i<len(t):
        c=t[i]
        if c=='M':
            if len(cur)>1: out.append(cur)
            cur=[(float(t[i+1]),float(t[i+2]))];start=cur[0];i+=3
        elif c=='L': cur.append((float(t[i+1]),float(t[i+2])));i+=3
        elif c=='Z': cur.append(start);i+=1
        else: cur.append((float(t[i]),float(t[i+1])));i+=2
    if len(cur)>1: out.append(cur)
    return out
def house(im,x,y,sc,alpha=110,glow=True):
    lay=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    for p in HOUSE:
        for seg in paths(p): d.line([(x+a*sc,y+b*sc) for a,b in seg],fill=AC+(alpha,),width=max(2,int(2.2*sc)),joint='curve')
    if glow: comp(im,lay.filter(ImageFilter.GaussianBlur(10)))
    _c=(lay); im.paste(_c,(0,0),_c)
def comp(im,x):
    im.paste(x,(0,0),x)
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
def grad_text(im,xy,text,ft):
    d0=ImageDraw.Draw(im,'RGBA'); w=int(d0.textlength(text,font=ft))+4; h=int(ft.size*1.3)
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).text((0,0),text,font=ft,fill=255)
    g=Image.new('RGBA',(w,h))
    for i in range(w):
        t=i/max(1,w-1); c=tuple(int(AC[k]+(AC2[k]-AC[k])*t) for k in range(3))
        ImageDraw.Draw(g).line([(i,0),(i,h)],fill=c+(255,))
    g.putalpha(m); im.paste(g,(int(xy[0]),int(xy[1])),g)
def bgframe(n,tot,last=False):
    im=Image.new('RGB',(W,H),BG)
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    for x in range(0,W,54): d.line([(x,0),(x,H)],fill=(255,255,255,13))
    for y in range(0,H,54): d.line([(0,y),(W,y)],fill=(255,255,255,13))
    _c=(lay); im.paste(_c,(0,0),_c)
    gl=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(gl).ellipse((620,-260,1340,420),fill=AC+(70,))
    comp(im,gl.filter(ImageFilter.GaussianBlur(140)))
    d=ImageDraw.Draw(im,'RGBA')
    lg=logo.resize((96,96),Image.LANCZOS); im.paste(lg,(X0,56),lg)
    d.text((X0+112,72),'CURTO E SILVA',font=f(SEMI,30),fill=TX); d.text((X0+112,108),'Reformas e manutenção',font=f(BODY,24),fill=MU)
    t=f'{n:02d} / {tot:02d}'; ft=f(SEMI,28); w=d.textlength(t,font=ft)
    d.rounded_rectangle((W-X0-w-40,74,W-X0,124),radius=25,fill=(255,255,255,10),outline=(255,255,255,40),width=2); d.text((W-X0-w-20,83),t,font=ft,fill=TX)
    d.line([(X0,1236),(W-X0,1236)],fill=(255,255,255,30),width=2)
    d.text((X0,1262),'@curtoesilva',font=f(SEMI,32),fill=TX)
    ft=f(SEMI,30)
    if last:
        t='BH · CONTAGEM · NOVA LIMA'; d.text((W-X0-d.textlength(t,font=ft),1264),t,font=ft,fill=AC)
    else:
        t='ARRASTE'; d.text((W-X0-52-d.textlength(t,font=ft),1264),t,font=ft,fill=AC)
        ax=W-X0-40; ay=1283; d.line((ax,ay,ax+32,ay),fill=AC,width=4); d.polygon([(ax+38,ay),(ax+22,ay-11),(ax+22,ay+11)],fill=AC)
    return im,d
def chip(d,x,y,t):
    ft=f(SEMI,30); w=d.textlength(t,font=ft)
    d.rounded_rectangle((x,y,x+w+76,y+58),radius=29,fill=AC+(28,),outline=AC+(150,),width=2)
    d.ellipse((x+24,y+22,x+38,y+36),fill=AC); d.text((x+52,y+12),t,font=ft,fill=AC2); return y+58
def fit(d,t,maxh,sizes,font=HEAD,lh=1.08):
    for s in sizes:
        ft=f(font,s); ls=wrap(d,t,ft,TW)
        if len(ls)*s*lh<=maxh: return ft,ls,s
    return ft,ls,s
def heading(d,y,t,maxh,sizes):
    ft,ls,s=fit(d,t,maxh,sizes)
    for l in ls: d.text((X0,y),l,font=ft,fill=TX); y+=int(s*1.08)
    return y
def card(d,x0,y0,x1,y1):
    d.rounded_rectangle((x0,y0,x1,y1),radius=26,fill=(255,255,255,12),outline=(255,255,255,34),width=2)
def cover(c,n,tot):
    im,d=bgframe(n,tot); house(im,600,770,1.05,alpha=120)
    d=ImageDraw.Draw(im,'RGBA'); y=chip(d,X0,250,c['tag'])+56
    y=heading(d,y,c['head'],520,[124,112,100,90])+24
    fs=f(SEMI,52)
    for l in wrap(d,c['sub'],fs,TW-120): grad_text(im,(X0,y),l,fs); y+=66
    return im
def content(c,n,tot):
    im,d=bgframe(n,tot); y=chip(d,X0,250,c['kicker'])+52
    y=heading(d,y,c['head'],330,[96,88,80,72])+40
    fb=f(BODY,46)
    if c.get('body'):
        ls=wrap(d,c['body'],fb,TW-80); h=len(ls)*62+70
        card(d,X0,y,W-X0,y+h); d.rectangle((X0,y+26,X0+6,y+h-26),fill=AC); yy=y+35
        for l in ls: d.text((X0+44,yy),l,font=fb,fill=TX); yy+=62
        y+=h+30
    for i,b in enumerate(c.get('bullets',[]),1):
        ls=wrap(d,b,fb,TW-150); h=len(ls)*58+52
        card(d,X0,y,W-X0,y+h)
        cy=y+h//2; d.ellipse((X0+28,cy-26,X0+80,cy+26),fill=AC+(40,),outline=AC,width=2)
        nf=f(SEMI,28); nt=str(i); d.text((X0+54-d.textlength(nt,font=nf)/2,cy-17),nt,font=nf,fill=AC2)
        yy=y+26
        for l in ls: d.text((X0+110,yy),l,font=fb,fill=TX); yy+=58
        y+=h+18
    return im
def star(d,cx,cy,r,fill):
    pts=[(cx+(r if i%2==0 else r*.45)*math.cos(-math.pi/2+i*math.pi/5),cy+(r if i%2==0 else r*.45)*math.sin(-math.pi/2+i*math.pi/5)) for i in range(10)]
    d.polygon(pts,fill=fill)
def quote(c,n,tot):
    im,d=bgframe(n,tot); y=260
    fq=f(HB,72); ls=wrap(d,'“'+c['quote']+'”',fq,TW-110); h=110+len(ls)*88+200
    card(d,X0,y,W-X0,y+h); d.rectangle((X0,y+30,X0+6,y+h-30),fill=AC)
    for i in range(5): star(d,X0+70+i*62,y+70,26,AC)
    yy=y+130
    for l in ls: d.text((X0+50,yy),l,font=fq,fill=TX); yy+=88
    yy+=40; d.text((X0+50,yy),c['name'],font=f(SEMI,50),fill=AC2); d.text((X0+50,yy+66),c['ctx'],font=f(BODY,34),fill=MU)
    return im
def cta(c,n,tot):
    im,d=bgframe(n,tot,True); house(im,560,820,0.95,alpha=45,glow=False); d=ImageDraw.Draw(im,'RGBA')
    y=heading(d,270,c['head'],380,[112,100,92,84])+20
    fs=f(SEMI,52)
    for l in wrap(d,c['sub'],fs,TW): grad_text(im,(X0,y),l,fs); y+=66
    y=max(y+60,790)
    gl=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(gl).rounded_rectangle((X0,y,W-X0,y+128),radius=64,fill=AC+(150,))
    comp(im,gl.filter(ImageFilter.GaussianBlur(30))); d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle((X0,y,W-X0,y+128),radius=64,fill=AC)
    fb=f(HEAD,52); t='Orçamento sem custo'; d.text(((W-d.textlength(t,font=fb))/2,y+32),t,font=fb,fill=(12,10,9))
    fw=f(SEMI,48); t='WhatsApp (31) 99984-6776'; d.text(((W-d.textlength(t,font=fw))/2,y+170),t,font=fw,fill=TX)
    t='A nova geração que honra o velho compromisso.'; fm=f(BODY,32); d.text(((W-d.textlength(t,font=fm))/2,y+250),t,font=fm,fill=MU)
    return im
K={'cover':cover,'content':content,'quote':quote,'cta':cta}
def build(pid,slides):
    out=P+'posts-novos/'+pid+'/'; os.makedirs(out,exist_ok=True)
    for i,c in enumerate(slides,1): K[c['kind']](c,i,len(slides)).convert('RGB').save(out+f'{i}.jpg',quality=92)
if __name__=='__main__':
    data=json.load(open(D+'/novembro.json',encoding='utf-8'))
    for pid,sl in data.items():
        if len(sys.argv)<2 or pid in sys.argv[1:]: build(pid,sl)
