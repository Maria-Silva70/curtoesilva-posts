# Layouts A (número gigante) e B (planta técnica) aprovados pela Maria em 18/11/2026.
# Uso: python3 layouts.py posts.json [id ...]  -> gera posts-novos/<id>/N.jpg
import os, re, sys, json, subprocess, tempfile
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(D+'/../..')+'/'
F=R+'ferramentas/stories/fontes/'; LOGO=R+'ferramentas/stories/logo-curto-e-silva.png'
def hi(t): return re.sub(r'\*(.+?)\*',r'<span class=or>\1</span>',t)
CSS=f"""<html><head><meta charset=utf-8><style>
@font-face{{font-family:BC;src:url({F}BarlowCondensed-ExtraBold.ttf);font-weight:800}}
@font-face{{font-family:BC;src:url({F}BarlowCondensed-Bold.ttf);font-weight:700}}
@font-face{{font-family:BC;src:url({F}BarlowCondensed-SemiBold.ttf);font-weight:600}}
@font-face{{font-family:IN;src:url({F}InterDisplay-ExtraBold.otf);font-weight:800}}
@font-face{{font-family:IN;src:url({F}InterDisplay-Bold.otf);font-weight:700}}
@font-face{{font-family:IN;src:url({F}Inter-SemiBold.otf);font-weight:600}}
@font-face{{font-family:IN;src:url({F}Inter-Medium.otf);font-weight:500}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;position:relative;font-family:IN;color:#F4F4F6;background:BG}}
.a{{position:absolute}} .or{{color:#FF6A1F}}
.logo{{width:84px;height:84px;border-radius:50%}}
.brand{{font:700 30px IN}} .brand small{{display:block;font:500 22px IN;color:#B2B4BC}}
.foot{{left:70px;right:70px;bottom:52px;display:flex;justify-content:space-between;font:600 26px IN}}
.kick{{font:700 30px BC;letter-spacing:.3em;color:#FF6A1F}}
.h{{font:800 110px/0.93 BC;text-transform:uppercase}}
</style></head><body>"""
GRID="background-image:linear-gradient(#ffffff0a 1px,transparent 1px),linear-gradient(90deg,#ffffff0a 1px,transparent 1px);background-size:54px 54px;"
GRIDC="background-image:linear-gradient(#5CE1FF14 1px,transparent 1px),linear-gradient(90deg,#5CE1FF14 1px,transparent 1px);background-size:45px 45px;"
HUD="radial-gradient(120% 80% at 70% 20%,#0F1E2E,#05070A 70%)"
def top(n,t): return f"""<div class=a style="left:70px;top:58px;display:flex;align-items:center;gap:18px"><img class=logo src="{LOGO}"><div class=brand>CURTO E SILVA<small>Reformas e manutenção</small></div></div>
<div class=a style="right:70px;top:76px;font:700 26px IN;border:2px solid #ffffff44;border-radius:40px;padding:8px 20px">{n:02d} / {t:02d}</div>"""
def foot(last): return f"""<div class="a foot"><span>@curtoesilva</span><span class=or>{'BH · CONTAGEM · NOVA LIMA' if last else 'ARRASTE →'}</span></div>"""
def ctablock(c,y):
    return f"""<div class=a style="left:70px;top:{y}px;width:940px" class=h><div class=h style="font-size:120px">{hi(c['head'])}</div><div style="font:600 40px/1.3 IN;color:#FF6A1F;margin-top:24px">{hi(c.get('sub',''))}</div></div>
<div class=a style="left:70px;right:70px;top:880px;height:120px;border-radius:60px;background:#FF6A1F;color:#07080A;font:800 50px/120px IN;text-align:center;box-shadow:0 0 50px #FF6A1F66">Orçamento sem custo</div>
<div class=a style="left:0;right:0;top:1040px;text-align:center;font:700 46px IN">WhatsApp (31) 99984-6776</div>
<div class=a style="left:0;right:0;top:1110px;text-align:center;font:500 30px IN;color:#B2B4BC">A nova geração que honra o velho compromisso.</div>"""
def bullets_A(items,y):
    return f'<div class=a style="left:70px;top:{y}px;right:70px">'+''.join(f'<div style="display:flex;align-items:center;gap:30px;padding:24px 0;border-bottom:2px solid #ffffff1a"><span style="font:800 92px/0.8 BC;color:transparent;-webkit-text-stroke:3px #FF6A1F;min-width:110px">{i+1:02d}</span><span style="font:700 42px/1.2 IN">{hi(t)}</span></div>' for i,t in enumerate(items))+'</div>'

def chip(t,col='#FF6A1F',fg='#07080A'): return f'<span style="display:inline-block;background:{col};color:{fg};padding:8px 20px;font:800 34px BC;letter-spacing:.12em">{t}</span>'
def photoA(c,n,t):
    img=R+c['img']; pos=c.get('pos','center')
    last=n==t
    h=CSS.replace('BG','#07080A')+f"""<div class=a style="inset:0;background:url({img}) {pos}/cover"></div>
<div class=a style="inset:0;background:linear-gradient(180deg,#07080Ad9 0%,#07080A40 14%,transparent 24%,transparent 56%,#07080Acc 74%,#07080A 90%)"></div>{top(n,t)}"""
    if c.get('chip'): h+=f'<div class=a style="left:70px;top:190px">{chip(c["chip"], "#FF6A1F" if c["chip"]!="ANTES" else "#F4F4F6")}</div>'
    if c.get('big'): h+=f'<div class=a style="right:50px;top:150px;font:800 260px/0.8 BC;color:transparent;-webkit-text-stroke:4px #FF6A1F">{c["big"]}</div>'
    h+=f"""<div class=a style="left:70px;right:70px;bottom:{c.get('bottom',130)}px"><div class=kick>{c.get('kicker','')}</div><div class=h style="font-size:{c.get('size',96)}px;margin-top:14px">{hi(c['head'])}</div>{'<div style="font:500 36px/1.38 IN;color:#D6D8DE;margin-top:22px">'+hi(c['body'])+'</div>' if c.get('body') else ''}</div>{foot(last)}</body></html>"""
    return h
def splitA(c,n,t):
    a,b=R+c['imgs'][0],R+c['imgs'][1]
    return CSS.replace('BG','#07080A')+f'<div class=a style="inset:0;{GRID}"></div>'+top(n,t)+f"""
<div class=a style="left:70px;top:190px"><div class=kick>{c.get('kicker','')}</div><div class=h style="font-size:84px;margin-top:10px">{hi(c['head'])}</div></div>
<div class=a style="left:70px;right:70px;top:420px;height:390px;background:url({a}) center/cover;border-radius:20px"></div><div class=a style="left:90px;top:440px">{chip('ANTES','#F4F4F6')}</div>
<div class=a style="left:70px;right:70px;top:830px;height:390px;background:url({b}) center/cover;border-radius:20px;outline:4px solid #FF6A1F"></div><div class=a style="left:90px;top:850px">{chip('DEPOIS')}</div>
{foot(n==t)}</body></html>"""
def A(c,n,t):
    if c['kind']=='photo': return photoA(c,n,t)
    if c['kind']=='split': return splitA(c,n,t)
    bg=CSS.replace('BG','#07080A')+f'<div class=a style="inset:0;{GRID}"></div>'
    last=n==t
    if c['kind']=='cover':
        big=c.get('big','')
        fs=1150 if len(big)<=1 else (700 if len(big)==2 else 400)
        return bg+f"""<div class=a style="right:{-60 if len(big)<=2 else 40}px;top:{170 if len(big)<=2 else 640}px;font:800 {fs}px/0.8 BC;color:transparent;-webkit-text-stroke:6px #FF6A1F;opacity:.9;white-space:nowrap">{big}</div>
{'<div class=a style="inset:0;background:linear-gradient(90deg,#07080A 40%,#07080Acc 65%,transparent)"></div>' if len(big)<=2 else ''}{top(n,t)}
<div class=a style="left:70px;top:300px;width:800px"><div class=kick>{c['tag']}</div><div class=h style="font-size:{c.get('size',124)}px;margin-top:18px">{hi(c['head'])}</div></div>
<div class=a style="left:70px;top:{c.get('subtop',1010)}px;width:700px;font:600 40px/1.25 IN;color:#C9CCD3;border-left:8px solid #FF6A1F;padding-left:26px">{hi(c.get('sub',''))}</div>{foot(last)}</body></html>"""
    if c['kind']=='cta':
        big=c.get('big','')
        return bg+(f'<div class=a style="right:-40px;top:120px;font:800 560px/0.8 BC;color:transparent;-webkit-text-stroke:4px #FF6A1F55">{big}</div>' if big else '')+top(n,t)+ctablock(c,330)+foot(True)+'</body></html>'
    num=c.get('num',f'{n-1:02d}')
    if 'bullets' in c:
        return bg+top(n,t)+f"""<div class=a style="left:70px;top:210px;width:940px"><div class=kick>{c['kicker']}</div><div class=h style="font-size:104px;margin-top:14px">{hi(c['head'])}</div></div>{bullets_A(c['bullets'],c.get('ly',560))}{foot(last)}</body></html>"""
    return bg+f"""<div class=a style="left:-40px;top:170px;font:800 520px/0.8 BC;color:transparent;-webkit-text-stroke:5px #FF6A1F">{num}</div>{top(n,t)}
<div class=a style="left:70px;top:640px;width:940px"><div class=kick>{c['kicker']}</div><div class=h style="font-size:{c.get('size',100)}px;margin-top:16px">{hi(c['head'])}</div>
<div style="font:500 38px/1.38 IN;color:#C9CCD3;margin-top:36px">{hi(c.get('body',''))}</div></div>{foot(last)}</body></html>"""
CORN="".join(f'<div class=a style="{p};width:60px;height:60px;border-{a}:4px solid #5CE1FF;border-{b}:4px solid #5CE1FF"></div>' for p,a,b in [("left:40px;top:40px","left","top"),("right:40px;top:40px","right","top"),("left:40px;bottom:40px","left","bottom"),("right:40px;bottom:40px","right","bottom")])
HOUSE="""<svg class=a style="left:190px;top:560px;filter:drop-shadow(0 0 10px #5CE1FF)" width=700 height=560 viewBox="0 0 700 560"><g fill="none" stroke="#5CE1FF" stroke-width="4"><polyline points="40,260 350,40 660,260"/><polyline points="90,225 90,520 610,520 610,225"/><polyline points="150,300 280,300 280,410 150,410 150,300"/><polyline points="420,300 550,300 550,410 420,410 420,300"/><polyline points="300,380 400,380 400,520 300,520"/></g><polyline points="30,268 670,268" fill="none" stroke="#FF6A1F" stroke-width="4"/></svg>"""
def callout(x,y,lx,ly,label):
    col='#FF6A1F'
    return f"""<div class=a style="left:{x-22}px;top:{y-22}px;width:44px;height:44px;border-radius:50%;border:4px solid {col};box-shadow:0 0 30px {col}"></div><div class=a style="left:{x-7}px;top:{y-7}px;width:14px;height:14px;border-radius:50%;background:{col}"></div>
<svg class=a style="left:0;top:0" width=1080 height=1350><line x1={x} y1={y} x2={lx} y2={ly} stroke="{col}" stroke-width=3 stroke-dasharray="8 6"/></svg>
<div class=a style="left:{lx}px;top:{ly-28}px;background:#05070Add;border-left:6px solid {col};padding:10px 18px;font:700 30px BC;letter-spacing:.18em">{label}</div>"""
SPOTS=[(560,830,760,700),(420,1015,680,1150),(230,828,380,1230),(700,960,780,1060),(330,960,90,1110)]
def B(c,n,t):
    bg=CSS.replace('BG',HUD)+f'<div class=a style="inset:0;{GRIDC}"></div>'+CORN+top(n,t)
    if c['kind']=='cover':
        cs=''.join(callout(*SPOTS[i],l) for i,l in enumerate(c.get('callouts',[])))
        return bg+f"""<div class=a style="left:70px;top:210px;width:940px"><div style="font:600 28px BC;letter-spacing:.35em;color:#5CE1FF">{c['tag']}</div><div class=h style="font-size:{c.get('size',100)}px;margin-top:14px">{hi(c['head'])}</div></div>
<div class=a style="right:80px;top:470px;font:600 26px BC;letter-spacing:.3em;color:#5CE1FF">ANALISANDO · {c.get('pct',72)}%</div>
<div class=a style="right:80px;top:510px;width:300px;height:8px;background:#5CE1FF33"><div style="width:{c.get('pct',72)}%;height:100%;background:#5CE1FF;box-shadow:0 0 14px #5CE1FF"></div></div>{HOUSE}{cs}</body></html>"""
    if c['kind']=='cta':
        return bg+ctablock(c,330).replace('#FF6A1F;color:#07080A','#FF6A1F;color:#07080A')+f'<div class=a style="left:0;right:0;top:1200px;text-align:center;font:600 26px BC;letter-spacing:.35em;color:#5CE1FF">BH · CONTAGEM · NOVA LIMA</div></body></html>'
    head=f"""<div class=a style="left:70px;top:230px;width:940px"><div style="font:600 28px BC;letter-spacing:.35em;color:#5CE1FF">{c['kicker']}</div><div class=h style="font-size:{c.get('size',100)}px;margin-top:14px">{hi(c['head'])}</div></div>"""
    if 'rows' in c:
        rows=''.join(f'<div style="display:flex;justify-content:space-between;gap:20px;font:600 36px IN;padding:16px 0;border-bottom:1px solid #ffffff22"><span>{a}</span><span style="color:{ {"r":"#FF3B30","g":"#34E07A","o":"#FF6A1F","c":"#5CE1FF"}[k]};white-space:nowrap">{s}</span></div>' for a,s,k in c['rows'])
        body=f"""<div class=a style="left:70px;top:{c.get('cy',620)}px;width:940px;border:2px solid #5CE1FF66;background:#05070Acc;padding:40px"><div style="font:600 28px BC;letter-spacing:.3em;color:#5CE1FF;margin-bottom:12px">{c.get('card','DIAGNÓSTICO')}</div>{rows}</div>"""
        note=f'<div class=a style="left:70px;top:1130px;width:940px;font:500 34px/1.4 IN;color:#C9D6E3">{hi(c.get("body",""))}</div>'
        return bg+head+body+note+'</body></html>'
    if 'checks' in c:
        items=''.join(f'<div style="display:flex;align-items:center;gap:26px;margin-bottom:24px;border:2px solid #5CE1FF55;background:#05070Acc;padding:24px 30px"><span style="width:46px;height:46px;border:4px solid #FF6A1F;flex:none"></span><span style="font:700 40px IN;flex:1">{a}</span><span style="font:600 26px BC;letter-spacing:.25em;color:#5CE1FF">{s}</span></div>' for a,s in c['checks'])
        return bg+head+f'<div class=a style="left:70px;top:{c.get("cy",560)}px;right:70px">{items}</div></body></html>'
    return bg+head+f'<div class=a style="left:70px;top:{c.get("cy",620)}px;width:940px;border:2px solid #5CE1FF66;background:#05070Acc;padding:44px;font:500 40px/1.4 IN;color:#E4ECF4">{hi(c["body"])}</div></body></html>'
def build(pid,post):
    out=R+'posts-novos/'+pid+'/'; os.makedirs(out,exist_ok=True)
    for f in os.listdir(out):
        if f.endswith('.jpg'): os.remove(out+f)
    fn={'A':A,'B':B}[post['style']]; sl=post['slides']; tmp=tempfile.mkdtemp(); hs=[]
    for i,c in enumerate(sl,1):
        h=f'{tmp}/{i}.html'; open(h,'w').write(fn(c,i,len(sl))); hs.append(h)
    subprocess.run(['node',D+'/render.js']+hs,check=True,env={**os.environ,'NODE_PATH':subprocess.check_output(['npm','root','-g']).decode().strip()})
    for i,h in enumerate(hs,1): os.replace(h.replace('.html','.jpg'),out+f'{i}.jpg')
if __name__=='__main__':
    data=json.load(open(sys.argv[1],encoding='utf-8'))
    for pid,p in data.items():
        if len(sys.argv)<3 or pid in sys.argv[2:]: build(pid,p)
