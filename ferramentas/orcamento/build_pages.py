import os
D=os.path.dirname(os.path.abspath(__file__))
b64=open(os.path.join(D,'logo.b64')).read()
s=open(os.path.join(D,'gerador.src.html')).read().replace("LOGO_SRC","data:image/png;base64,"+b64)
open(os.path.join(D,'gerador-artifact.html'),'w').write(s)
head='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex,nofollow"><link rel="icon" href="/favicon-32.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'
site=head+s.replace('<title>Gerador de Orçamento Curto e Silva</title>','<title>Orçamento · Curto e Silva (equipe)</title>',1)+'</body></html>'
open(os.path.join(D,'..','..','docs','orcamento-equipe','index.html'),'w').write(site)
print('built')
