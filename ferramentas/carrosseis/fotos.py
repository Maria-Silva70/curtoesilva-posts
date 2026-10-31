# Carrossel de obra real (antes e depois) no padrão aprovado do "rufo-bonfim":
# foto grande em cima, painel escuro embaixo, etiqueta laranja, título Barlow Condensed com trecho em laranja (*assim*).
# Uso: python3 fotos.py [id ...]   (lê obras.json; fotos em fotos-obras/<obra>/)
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os, json, sys, re
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(D+'/../..')+'/'; FD=R+'ferramentas/stories/fontes/'
W,H=1080,1350; PH=930; X0=56
AC=(255,106,31); BG=(20,20,22); TX=(250,250,250); MU=(205,205,210); DIM=(150,150,155)
f=lambda n,s: ImageFont.truetype(FD+n,s)
TIT='BarlowCondensed-ExtraBold.ttf'; TAG='BarlowCondensed-Bold.ttf'; SUB='Barlow-Medium.ttf'; SEMI='Barlow-SemiBold.ttf'
logo=Image.open(R+'ferramentas/stories/logo-curto-e-silva.png').convert('RGBA')

def photo(src,w,h,fx=.5,fy=.5,blur=(),crop=None):
    im=ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    for b in blur:  # caixas [x0,y0,x1,y1] em fração da foto, para esconder pessoas
        bx=tuple(int(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(b))
        im.paste(im.crop(bx).filter(ImageFilter.GaussianBlur(14)),bx[:2])
    if crop: im=im.crop(tuple(int(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(crop)))
    return ImageOps.fit(im,(w,h),Image.LANCZOS,centering=(fx,fy))

def tag(d,x,y,t,fill=AC):
    ft=f(TAG,40); w=d.textlength(t,font=ft)
    d.rectangle((x,y,x+w+36,y+58),fill=fill); d.text((x+18,y+6),t,font=ft,fill=TX)

def badge(im,cx,cy,r=58):
    d=ImageDraw.Draw(im); d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=AC)
    lg=logo.resize((int(r*1.7),int(r*1.7)),Image.LANCZOS); im.paste(lg,(cx-lg.width//2,cy-lg.height//2),lg)

def rich(d,y,text,ft,lh,maxw):
    # quebra em linhas mantendo o trecho entre *...* em laranja
    words=[]
    for i,part in enumerate(re.split(r'\*',text)):
        for wd in part.split(): words.append((wd,i%2==1))
    lines=[];cur=[]
    for wd in words:
        t=' '.join(w for w,_ in cur+[wd])
        if cur and d.textlength(t,font=ft)>maxw: lines.append(cur);cur=[wd]
        else: cur.append(wd)
    lines.append(cur)
    for ln in lines:
        x=X0
        for k,(wd,hi) in enumerate(ln):
            nxt=ln[k+1][0] if k<len(ln)-1 else ''
            s=wd+(' ' if nxt and nxt[0] not in ',.?!:;' else '')
            d.text((x,y),s,font=ft,fill=AC if hi else TX); x+=d.textlength(s,font=ft)
        y+=lh
    return y

def wrap(d,t,ft,maxw):
    out=[];l=''
    for wd in t.split():
        c=(l+' '+wd).strip()
        if d.textlength(c,font=ft)<=maxw: l=c
        else: out.append(l);l=wd
    return out+[l]

def slide(s,obra,num,last):
    im=Image.new('RGB',(W,H),BG)
    fp=lambda k: R+'fotos-obras/'+obra+'/'+s[k]['src']
    if 'top' in s:  # comparação: antes em cima, depois embaixo
        hh=PH//2
        im.paste(photo(fp('top'),W,hh-3,*s['top'].get('focus',[.5,.5]),blur=s['top'].get('blur',()),crop=s['top'].get('crop')),(0,0))
        im.paste(photo(fp('bottom'),W,hh-3,*s['bottom'].get('focus',[.5,.5]),blur=s['bottom'].get('blur',()),crop=s['bottom'].get('crop')),(0,hh+3))
        d=ImageDraw.Draw(im); d.rectangle((0,hh-3,W,hh+3),fill=AC)
        tag(d,32,hh-82,'ANTES',fill=(30,30,32)); tag(d,32,hh+26,'DEPOIS')
        if s.get('tag'): tag(d,32,28,s['tag'])
    else:
        im.paste(photo(fp('photo'),W,PH,*s['photo'].get('focus',[.5,.5]),blur=s['photo'].get('blur',()),crop=s['photo'].get('crop')),(0,0))
        d=ImageDraw.Draw(im); tag(d,32,28,s['tag'])
    # degradê da foto para o painel
    g=Image.new('L',(1,140)); [g.putpixel((0,i),int(255*(i/139)**1.6)) for i in range(140)]
    im.paste(Image.new('RGB',(W,140),BG),(0,PH-140),g.resize((W,140)))
    d=ImageDraw.Draw(im)
    if num:
        ft=f(TAG,34); w=d.textlength(num,font=ft)
        d.rounded_rectangle((W-32-w-28,30,W-32,82),radius=8,fill=(25,25,27)); d.text((W-32-w-14,36),num,font=ft,fill=TX)
    badge(im,W-100,PH-120)
    d=ImageDraw.Draw(im)
    y=rich(d,PH+10,s['head'],f(TIT,74),78,W-2*X0)+12
    fs=f(SUB,34)
    for l in wrap(d,s['sub'],fs,W-2*X0): d.text((X0,y),l,font=fs,fill=MU); y+=44
    d.text((X0,H-62),'@curtoesilva',font=f(SEMI,28),fill=DIM)
    ft=f(TAG,32)
    if last:
        t='BH · CONTAGEM · NOVA LIMA'; d.text((W-X0-d.textlength(t,font=ft),H-64),t,font=ft,fill=AC)
    else:
        t='ARRASTE'; ax=W-X0-34; d.text((ax-14-d.textlength(t,font=ft),H-64),t,font=ft,fill=AC)
        ay=H-45; d.line((ax,ay,ax+24,ay),fill=AC,width=4); d.polygon([(ax+34,ay),(ax+20,ay-10),(ax+20,ay+10)],fill=AC)
    return im

def build(pid,post):
    out=R+'posts-novos/'+pid+'/'; os.makedirs(out,exist_ok=True); sl=post['slides']
    mid=len(sl)-2
    for i,s in enumerate(sl):
        num=f'{i}/{mid}' if 0<i<len(sl)-1 else ''
        slide(s,post['obra'],num,i==len(sl)-1).save(out+f'{i+1}.jpg',quality=92)
    open(out+'legenda.txt','w',encoding='utf-8').write(post['legenda'].strip()+'\n')

if __name__=='__main__':
    data=json.load(open(D+'/obras.json',encoding='utf-8'))
    for pid,p in data.items():
        if len(sys.argv)<2 or pid in sys.argv[1:]: build(pid,p)
