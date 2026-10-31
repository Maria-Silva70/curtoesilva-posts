# Reel 9:16 de obra real: abertura com trecho do vídeo da visita + fotos ANTES / DURANTE / DEPOIS + cartão final.
# Uso: python3 reel_obra.py <pasta_quadros_video> <saida.mp4>
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os, sys, glob, subprocess
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(D+'/../..')+'/'; FD=R+'ferramentas/stories/fontes/'
W,H,FPS=1080,1920,30; AC=(255,106,31); BG=(20,20,22); TX=(250,250,250); MU=(205,205,210)
f=lambda n,s: ImageFont.truetype(FD+n,s)
TIT='BarlowCondensed-ExtraBold.ttf'; TAG='BarlowCondensed-Bold.ttf'; SUB='Barlow-Medium.ttf'
logo=Image.open(R+'ferramentas/stories/logo-curto-e-silva.png').convert('RGBA')
F=R+'fotos-obras/jaragua/'
SEQ=[('ANTES','dcc8c92b','Parede descascando'),('ANTES','61e83ac6','Taco soltando'),('ANTES','c2d6e593','Teto caindo no subsolo'),
     ('ANTES','2238d0f5','Fachada desbotada'),('DURANTE','8de6cae0','Preparo do chão'),('DURANTE','adaca161','Raspando o teto'),
     ('DURANTE','5c4fa90d','Massa na fachada'),('DEPOIS','0a18cfb5','Quarto pronto'),('DEPOIS','9730e48c','Subsolo renovado'),
     ('DEPOIS','f24c852f','Efeito mármore'),('DEPOIS','fca3911d','Fachada nova')]

def base(im):
    # monta o fundo 9:16 com 6% de folga para o zoom lento
    w,h=int(W*1.06),int(H*1.06)
    if im.width/im.height>0.8:  # foto deitada: fundo desfocado + foto inteira na largura
        bg=ImageOps.fit(im,(w,h)).filter(ImageFilter.GaussianBlur(40)); bg=Image.blend(bg,Image.new('RGB',bg.size,BG),.45)
        ph=ImageOps.fit(im,(w,int(h*0.56)),Image.LANCZOS); bg.paste(ph,(0,int(h*0.37)-ph.height//2)); return bg
    return ImageOps.fit(im,(w,h),Image.LANCZOS,centering=(.5,.4))

def chrome(fr,tag,cap):
    d=ImageDraw.Draw(fr,'RGBA')
    d.rectangle((0,H-560,W,H),fill=(0,0,0,0))
    g=Image.new('L',(1,520)); [g.putpixel((0,i),int(235*(i/519)**1.4)) for i in range(520)]
    fr.paste(Image.new('RGB',(W,520),BG),(0,H-520-120),g.resize((W,520))); fr.paste(Image.new('RGB',(W,120),BG),(0,H-120))
    d=ImageDraw.Draw(fr,'RGBA')
    if tag:
        ft=f(TAG,64); tw=d.textlength(tag,font=ft); d.rectangle((60,1290,60+tw+48,1290+86),fill=AC if tag!='ANTES' else (30,30,32)); d.text((84,1295),tag,font=ft,fill=TX)
    if cap: d.text((60,1395),cap,font=f(TIT,104),fill=TX)
    # barra da marca
    d.ellipse((60,1560,180,1680),fill=AC); lg=logo.resize((104,104),Image.LANCZOS); fr.paste(lg,(68,1568),lg)
    d.text((204,1566),'Curto e Silva',font=f(TIT,56),fill=TX); d.text((204,1630),'Reformas em BH · (31) 99984-6776',font=f(SUB,34),fill=MU)
    return fr

def kb(b,t):  # zoom lento
    s=1.06-0.06*t; w,h=int(W*s),int(H*s); x=(b.width-w)//2; y=(b.height-h)//2
    return b.crop((x,y,x+w,y+h)).resize((W,H),Image.BILINEAR)

def frames(vdir):
    vf=sorted(glob.glob(vdir+'/*.png'))
    for i,p in enumerate(vf):  # abertura: vídeo da visita técnica
        fr=ImageOps.fit(Image.open(p).convert('RGB'),(W,H),Image.LANCZOS); d=ImageDraw.Draw(fr,'RGBA')
        d.rectangle((0,250,W,760),fill=(10,10,12,190))
        ft=f(TAG,54); t='VISITA TÉCNICA · JARAGUÁ, BH'; d.rectangle((60,290,60+d.textlength(t,font=ft)+44,362),fill=AC); d.text((82,295),t,font=ft,fill=TX)
        y=400
        for l,c in (('Olha o que a gente',TX),('encontrou nessa casa',AC)): d.text((60,y),l,font=f(TIT,112),fill=c); y+=120
        yield chrome(fr,'','')
    for k,(tag,src,cap) in enumerate(SEQ):
        b=base(ImageOps.exif_transpose(Image.open(F+src+'.jpg')).convert('RGB')); n=int(FPS*(2.6 if k==len(SEQ)-1 else 1.8))
        for i in range(n): yield chrome(kb(b,i/n),tag,cap)
    end=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(end)
    d.ellipse((W//2-130,330,W//2+130,590),fill=AC); lg=logo.resize((220,220),Image.LANCZOS); end.paste(lg,(W//2-110,350),lg)
    y=700
    for l,c in (('Sua casa',TX),('precisa disso?',TX),('A visita é',AC),('sem custo.',AC)):
        ft=f(TIT,140); d.text(((W-d.textlength(l,font=ft))/2,y),l,font=ft,fill=c); y+=150
    for l,ft,c in (('WhatsApp (31) 99984-6776',f(TAG,72),TX),('BH · Contagem · Nova Lima',f(SUB,44),MU),('A nova geração que honra o velho compromisso.',f(SUB,36),MU)):
        d.text(((W-d.textlength(l,font=ft))/2,y+40),l,font=ft,fill=c); y+=90
    for i in range(FPS*3): yield end

if __name__=='__main__':
    out=sys.argv[2]
    p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-f','lavfi','-i','anullsrc=r=44100:cl=stereo','-shortest','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
        '-c:a','aac','-movflags','+faststart',out],stdin=subprocess.PIPE)
    for fr in frames(sys.argv[1]): p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
