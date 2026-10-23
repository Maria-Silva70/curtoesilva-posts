from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json, os
import os
D=os.path.dirname(os.path.abspath(__file__))
R=D+'/'
F=R+'fontes/BarlowCondensed-'; FB=R+'fontes/Barlow-'
P=os.path.abspath(D+'/../..')+'/'
BG=(30,26,24); OR=(232,96,28); WH=(255,255,255); GR=(200,200,200)
def f(n,s): return ImageFont.truetype(n,s)
logo=Image.open(R+'logo-curto-e-silva.png').convert('RGBA')
def wrap(d,text,font,w):
    out=[];
    for para in text.split('\n'):
        line=''
        for word in para.split():
            t=(line+' '+word).strip()
            if d.textlength(t,font=font)<=w: line=t
            else: out.append(line); line=word
        out.append(line)
    return out
def cover(im,w,h,top=0.0,crop=None):
    im=im.convert('RGB')
    if crop: im=im.crop((0,0,im.width,int(im.height*crop)))
    r=max(w/im.width,h/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    x=(im.width-w)//2; y=int((im.height-h)*top)
    return im.crop((x,y,x+w,y+h))
def base():
    im=Image.new('RGB',(1080,1920),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,1080,14),fill=OR)
    lg=logo.resize((150,150),Image.LANCZOS); im.paste(lg,(870,240),lg)
    return im,d
def footer(d,cta):
    d.text((70,1625),'@curtoesilva',font=f(FB+'SemiBold.ttf',36),fill=WH)
    t='BH · CONTAGEM · NOVA LIMA'; ft=f(F+'Bold.ttf',36)
    d.text((1010-d.textlength(t,font=ft),1625),t,font=ft,fill=OR)
def textblock(d,y,tag,head,sub,hs=104):
    if tag:
        ft=f(F+'Bold.ttf',40); w=d.textlength(tag,font=ft)
        d.rectangle((70,y,70+w+36,y+62),fill=OR); d.text((88,y+8),tag,font=ft,fill=(20,16,14)); y+=92
    fh=f(F+'ExtraBold.ttf',hs)
    for ln in wrap(d,head,fh,940):
        d.text((70,y),ln,font=fh,fill=WH); y+=int(hs*1.0)
    y+=14; fs=f(F+'SemiBold.ttf',48)
    for ln in wrap(d,sub,fs,940):
        d.text((70,y),ln,font=fs,fill=OR); y+=56
    return y
def lab(d,x,y,t,fill):
    ft=f(F+'Bold.ttf',40); w=d.textlength(t,font=ft)
    d.rectangle((x,y,x+w+36,y+60),fill=fill); d.text((x+18,y+7),t,font=ft,fill=WH if fill!=OR else (20,16,14))
def photo_story(src,tag,head,sub,crop=None,top=0.3,y0=0.0,src2=None):
    im=Image.new('RGB',(1080,1920),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,1080,14),fill=OR)
    H=930; Y=250
    def ld(p):
        x=Image.open(P+p).convert('RGB')
        if crop or y0: x=x.crop((0,int(x.height*y0),x.width,int(x.height*(crop or 1))))
        return x
    if src2:
        a=cover(ld(src),537,H,top); b=cover(ld(src2),537,H,top)
        im.paste(a,(0,Y)); im.paste(b,(543,Y)); d.rectangle((537,Y,543,Y+H),fill=OR)
        lab(d,24,Y+24,'ANTES',(20,16,14)); lab(d,567,Y+24,'DEPOIS',OR)
    else:
        im.paste(cover(ld(src),1080,H,top),(0,Y))
    lg=logo.resize((130,130),Image.LANCZOS); im.paste(lg,(926,Y+H-154),lg)
    y=textblock(d,Y+H+40,tag,head,sub,hs=88)
    assert y<1610,(head,y)
    footer(d,''); return im
def text_story(tag,head,sub,hl=None):
    im,d=base()
    y=560
    ft=f(F+'Bold.ttf',44); w=d.textlength(tag,font=ft)
    d.rectangle((70,y,70+w+40,y+70),fill=OR); d.text((90,y+9),tag,font=ft,fill=(20,16,14)); y+=120
    fh=f(F+'ExtraBold.ttf',130)
    for ln in wrap(d,head,fh,940):
        d.text((70,y),ln,font=fh,fill=OR if (hl and hl in ln) else WH); y+=128
    y+=30; fs=f(FB+'Medium.ttf',50)
    for ln in wrap(d,sub,fs,900):
        d.text((70,y),ln,font=fs,fill=(235,235,235)); y+=66
    d.text((70,1520),'(31) 99984-6776',font=f(F+'ExtraBold.ttf',64),fill=WH)
    footer(d,''); return im
def ep_story(ep,folder,tag,head,sub):
    im,d=base()
    c=Image.open(P+f'posts-novos/{folder}/1.jpg').convert('RGB').resize((760,950),Image.LANCZOS)
    d.rectangle((66,256,74+760,264+950),fill=OR)
    im.paste(c,(70,260))
    textblock(d,1250,tag,head,sub,hs=84)
    footer(d,''); return im
S=json.load(open(os.path.join(os.path.dirname(__file__),'stories.json')))
for s in S:
    k=s['kind']
    if k=='photo': im=photo_story(s['src'],s['tag'],s['head'],s['sub'],s.get('crop'),s.get('top',0.3),s.get('y0',0.0),s.get('src2'))
    elif k=='text': im=text_story(s['tag'],s['head'],s['sub'],s.get('hl'))
    else: im=ep_story(s['ep'],s['folder'],s['tag'],s['head'],s['sub'])
    im.save(P+'stories/serie/'+s['id']+'.jpg',quality=92)
print(len(S))
