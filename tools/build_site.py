"""Build the three CUZDEV pages in six languages. Standard library only."""
from pathlib import Path
import argparse, json, hashlib, datetime
from html import escape as esc

ROOT = Path(__file__).resolve().parents[1]
LANGS = {
 'en': ('', 'EN', 'English', 'en_US'),
 'pt-BR': ('pt-br/', 'PT', 'Português (BR)', 'pt_BR'),
 'es': ('es/', 'ES', 'Español', 'es_ES'),
 'de': ('de/', 'DE', 'Deutsch', 'de_DE'),
 'fr': ('fr/', 'FR', 'Français', 'fr_FR'),
 'it': ('it/', 'IT', 'Italiano', 'it_IT'),
}
SLUGS = {'home': '', 'zzz': 'zzzombie-assault/', 'floki': 'floki-heaven/'}
SHOTS = {
 'zzz': {
  'world': ['z-snow', 'z-neon', 'z-desert', 'z-forest', 'z-town'],
  'heroes': ['z-choice'], 'combat': ['z-fire', 'z-void'], 'skills': ['z-skills'],
  'gear': ['z-inventory', 'z-polar'], 'workshop': ['z-workshop'],
  'quests': ['z-contracts', 'z-story'], 'shelters': ['z-shelter'],
  'threat': ['z-bloodmoon'], 'weather': ['z-snow', 'z-neon'],
  'travel': ['z-coast'], 'survival': ['z-survival', 'z-rest'], 'coop': ['z-coop', 'z-split'],
 },
 'floki': {
  'combat': ['f-action'], 'world': ['f-cache', 'f-frost', 'f-ash'],
  'weapons': ['f-appearance'], 'active': ['f-active', 'f-turret'],
  'exploration': ['f-camp', 'f-forge', 'f-challenge', 'f-traveler'],
  'bosses': ['f-guardian', 'f-watcher'], 'journey': ['f-journey'],
 }
}
COMPANIONS = [('soldado','Rex'),('cole','Cole'),('samurai','Kenji'),('claire','Claire'),('brutus','Brutus'),('nina','Nina'),('rui','Wade & Sparky'),('tony','Tony'),('iara','Ivy')]
WEAPONS = ['shotgun','revolver','smg','staff','bazooka','sword','carbine','fan','needle','prism','ember','comet']
MEDIA = json.loads((ROOT/'content/media.json').read_text(encoding='utf-8'))

def href(lang, page='home'):
 return '/' + LANGS[lang][0] + SLUGS[page]

def paragraphs(lines):
 return ''.join('<p>'+esc(x)+'</p>' for x in lines)

def schema(value):
 if isinstance(value,dict): return {k:schema(v) for k,v in value.items()}
 if isinstance(value,list): return [schema(v) for v in value]
 return type(value).__name__

def image(ident, caption, common, album='zzz', eager=False, css=''):
 m=MEDIA[ident]
 assert (ROOT/m['src'].lstrip('/')).is_file(), m['src']
 loading='fetchpriority="high"' if eager else 'loading="lazy"'
 return f'''<figure class="game-photo {css}"><button class="shot-button" type="button" data-shot="{esc(m['src'])}" data-album="{album}" data-caption="{esc(caption)}" data-width="{m['width']}" data-height="{m['height']}" aria-label="{esc(common['enlarge']+': '+caption)}"><img src="{esc(m['src'])}" width="{m['width']}" height="{m['height']}" alt="{esc(caption)}" {loading}><span class="shot-expand" aria-hidden="true">↗</span></button><figcaption><span>{esc(caption)}</span><span class="photo-hint">{esc(common['enlarge'])} ↗</span></figcaption></figure>'''

def sprite(name, words, common, css=''):
 meta=json.loads((ROOT/'assets/sprites'/f'{name}.json').read_text(encoding='utf-8'))
 assert len(words)==4
 return f'''<figure class="sprite-study {css}"><div class="sprite-stage"><img class="sprite-poster" src="/assets/sprites/{name}.png" width="{meta['width']}" height="{meta['height']}" alt="{esc(words[3])}" loading="lazy"><canvas hidden data-animation="{name}" role="img" aria-label="{esc(words[3])}"></canvas></div><figcaption><p class="eyebrow">{esc(words[1])}</p><h3>{esc(words[0])}</h3><p>{esc(words[2])}</p></figcaption></figure>'''

def motion_control(c):
 return f'''<div class="motion-controls"><p>{esc(c['motion_note'])}</p><button type="button" data-motion-toggle data-pause="{esc(c['pause'])}" data-play="{esc(c['resume'])}" aria-pressed="false">{esc(c['pause'])}</button></div>'''

def header(d,lang,page):
 c=d['common'];links=''
 for code,(_,short,label,_) in LANGS.items():
  current=' aria-current="page"' if code==lang else ''
  links+=f'<li><a href="{href(code,page)}" lang="{code}" hreflang="{code}" data-language="{code}"{current}>{esc(label)}<span aria-hidden="true">{short}</span></a></li>'
 return f'''<a class="skip-link" href="#main">{esc(c['skip'])}</a><header class="site-header"><div class="header-inner wrap"><a class="wordmark" href="{href(lang)}" aria-label="CUZDEV · {esc(c['home'])}"><span class="brand-symbol" aria-hidden="true"><span></span></span>CUZDEV<span class="brand-dot">.</span></a><div class="header-actions"><nav id="navigation" aria-label="{esc(c['navigation'])}"><a href="{href(lang)}">{esc(c['home'])}</a><a href="{href(lang,'zzz')}"{' aria-current="page"' if page=='zzz' else ''}>ZZZombie Assault</a><a href="{href(lang,'floki')}"{' aria-current="page"' if page=='floki' else ''}>Floki Heaven</a><a class="nav-contact" href="{href(lang)}#contact">{esc(c['contact'])} ↗</a></nav><details class="language-menu"><summary aria-label="{esc(c['language'])}: {esc(LANGS[lang][2])}">{LANGS[lang][1]}<span aria-hidden="true">⌄</span></summary><ul aria-label="{esc(c['language'])}">{links}</ul></details><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="navigation">{esc(c['menu'])} <span aria-hidden="true">+</span></button></div></div></header>'''

def footer(d,lang):
 c=d['common'];year=datetime.date.today().year
 return f'''<footer class="site-footer"><div class="wrap footer-inner"><a class="wordmark" href="{href(lang)}">CUZDEV<span class="brand-dot">.</span></a><p>{esc(c['footer'])}</p><span>© <span id="year">{year}</span> CUZDEV</span><a class="back-top" href="#top">{esc(c['back_top'])} ↑</a></div></footer>'''

def dialog(c):
 return f'''<dialog class="lightbox" id="gallery-dialog" aria-labelledby="gallery-title" aria-describedby="gallery-description"><div class="lightbox-top"><div><p id="gallery-title"></p><p id="gallery-description">{esc(c['screenshot'])}</p></div><button type="button" class="lightbox-close" aria-label="{esc(c['close'])}">{esc(c['close'])} ×</button></div><div class="lightbox-stage"><img id="gallery-image" src="/assets/zzzombie-snow-dawn.webp" alt="" width="1600" height="900"><button type="button" class="lightbox-prev" aria-label="{esc(c['previous'])}">←</button><button type="button" class="lightbox-next" aria-label="{esc(c['next'])}">→</button></div><div class="lightbox-bottom"><p id="gallery-caption" aria-live="polite"></p><span id="gallery-count"></span></div></dialog><noscript><p class="noscript-message">{esc(c['no_js'])}</p></noscript>'''

def contact(c):
 return f'''<section class="contact wrap" id="contact"><div><p class="eyebrow">CUZDEV / {esc(c['contact'])}</p><h2>{esc(c['contact_title'])}</h2><p>{esc(c['contact_text'])}</p></div><a class="contact-cta" href="mailto:gabriel.victor@cuzdev.xyz"><span class="contact-arrow" aria-hidden="true">↗</span><span>{esc(c['hello'])}</span><span class="contact-address">gabriel.victor@cuzdev.xyz</span></a></section>'''

def home(d,lang):
 c,h=d['common'],d['home'];z=d['zzz']['chapters']['world'];f=d['floki']['chapters'];headline=h['headline']
 snow=image('z-snow',z[3],c,eager=True,css='home-lead-z')
 rabbit=image('f-action',f['combat'][3],c,album='floki',css='home-lead-f')
 def game_card(kind):
  is_z=kind=='zzz';prefix='z' if is_z else 'f';title='ZZZOMBIE<br>ASSAULT' if is_z else 'FLOKI<br>HEAVEN'
  primary=image('z-snow' if is_z else 'f-action',z[3] if is_z else f['combat'][3],c,album=kind)
  extras=[('z-neon',z[4]),('z-forest',z[6]),('z-desert',z[5])] if is_z else [('f-frost',f['world'][4]),('f-guardian',f['bosses'][3]),('f-ash',f['world'][5])]
  thumbs=''.join(image(k,cap,c,album=kind,css='thumbnail-photo') for k,cap in extras)
  visual='<div class="game-visual">'+primary+'<div class="game-thumbnails">'+thumbs+'</div></div>'
  tags=''.join('<li>'+esc(x)+'</li>' for x in h[prefix+'_tags'])
  copy=f'''<div class="game-copy"><div class="game-meta"><span>PROJECT_0{1 if is_z else 2}</span><span class="status">{esc(c['status'])}</span></div><h3>{title}<span class="accent">.</span></h3><p class="game-hook">{esc(h[prefix+'_hook'])}</p><p class="game-description">{esc(h[prefix+'_body'])}</p><ul class="game-tags">{tags}</ul><a class="button button-lime dossier-link" href="{href(lang,kind)}">{esc(c['view_game'])} ↗</a></div>'''
  return '<article class="game-feature game-'+prefix+'" id="'+('zzzombie-assault' if is_z else 'flokiheaven')+'">'+(visual+copy if is_z else copy+visual)+'</article>'
 ticker='<span class="ticker-plus" aria-hidden="true">+</span>'.join('<span>'+esc(x)+'</span>' for x in h['ticker'])
 process='<span aria-hidden="true">→</span>'.join('<span>'+esc(x)+'</span>' for x in h['process'])
 return f'''<main id="main"><section class="hero wrap" id="top"><div class="hero-copy"><p class="eyebrow"><span class="signal" aria-hidden="true"></span>{esc(h['kicker'])}</p><h1>{esc(headline[0])} <span class="accent">{esc(headline[1])}</span><br>{esc(headline[2])} <span class="outline">{esc(headline[3])}</span></h1><p class="hero-description">{esc(h['description'])}</p><div class="hero-actions"><a class="button button-lime" href="#games">{esc(h['cta'])} ↘</a><a class="text-link" href="#about">{esc(h['workshop_link'])} ↗</a></div><p class="hero-note">+ {esc(h['note'])}</p></div><div class="hero-art home-art"><div class="art-coordinate" aria-hidden="true">CUZ / FIELD NOTES_002</div><div class="home-shot-z">{snow}</div><div class="home-shot-f">{rabbit}</div><p class="art-caption">{esc(c['screenshot'])} / {esc(c['status'])}</p></div></section><div class="ticker" aria-hidden="true"><div class="wrap ticker-inner">{ticker}</div></div><section id="games" class="games wrap"><div class="section-heading"><div><p class="eyebrow">01 / {esc(c['games'])}</p><h2>{esc(h['games_title'][0])}<br>{esc(h['games_title'][1])}</h2></div><p>{esc(h['games_intro'])}</p></div>{game_card('zzz')}{game_card('floki')}<p class="development-note">{esc(c['dev_note'])}</p></section><section class="workshop" id="about"><div class="wrap workshop-inner"><div class="workshop-intro"><p class="eyebrow">02 / {esc(h['workshop_link'])}</p><h2>{esc(h['about_title'][0])}<br><span>{esc(h['about_title'][1])}</span></h2></div><div class="workshop-body"><p class="workshop-lead">{esc(h['about_lead'])}</p>{paragraphs(h['about_body'])}<div class="build-loop">{process}</div><p class="workshop-note">{esc(h['about_note'])}</p></div></div></section>{contact(c)}</main>'''

def game(d,lang,kind):
 c,g=d['common'],d[kind];chapters=g['chapters'];title='ZZZombie Assault' if kind=='zzz' else 'Floki Heaven'
 lead='z-snow' if kind=='zzz' else 'f-action';cap=chapters['world'][3] if kind=='zzz' else chapters['combat'][3]
 facts=''.join('<li>'+esc(x)+'</li>' for x in g['facts'])
 toc=''.join(f'<a href="#{key}">{esc(value[0])}</a>' for key,value in chapters.items())
 short_toc=''.join(f'<li><a href="#{key}"><span>{i:02}</span>{esc(value[0])}</a></li>' for i,(key,value) in enumerate(chapters.items(),1))
 sections=''
 for i,(key,values) in enumerate(chapters.items(),1):
  ids=SHOTS[kind][key]
  assert len(values)==3+len(ids),(lang,kind,key,'Missing localized captions')
  photos=''.join(image(ident,caption,c,album=kind+'-'+key) for ident,caption in zip(ids,values[3:]))
  extra=''
  if key=='heroes' and kind=='zzz':
   studies=sprite('akashi-wind',g['akashi'],c)+sprite('satoshi-combo',g['satoshi'],c)
   roster=''.join(f'<figure><div class="companion-portrait"><img src="/assets/sprites/{ident}.png" alt="{esc(name+": "+role)}" loading="lazy"></div><figcaption><strong>{esc(name)}</strong><span>{esc(role)}</span></figcaption></figure>' for (ident,name),role in zip(COMPANIONS,g['party_roles']))
   extra=f'<div class="protagonist-studies">{studies}</div>{motion_control(c)}<div class="party-heading"><h3>{esc(g["party_title"])}</h3><p>{esc(g["party_intro"])}</p></div><div class="party-roster">{roster}</div>'
  if key=='weapons' and kind=='floki':
   guns=''.join(f'<figure><img src="/assets/sprites/weapon-{ident}.png" alt="{esc(name)}" loading="lazy"><figcaption>{esc(name)}</figcaption></figure>' for ident,name in zip(WEAPONS,g['weapon_names']))
   extra='<div class="weapon-rack">'+guns+'</div>'
  if key=='travel' and kind=='zzz':
   extra=f'<figure class="world-map-art"><img src="/assets/sprites/world-map.webp" alt="{esc(c["source_art"]+": "+chapters["world"][0])}" width="900" height="1195" loading="lazy"><figcaption>{esc(c["source_art"])}</figcaption></figure>'
  if key=='combat' and kind=='floki':
   extra='<div class="rabbit-study">'+sprite('floki-hop',g['sprite'],c)+motion_control(c)+'</div>'
  wide=key in ['world','heroes','gear','exploration','coop']
  modifier='chapter--wide' if wide else ('chapter--reverse' if i%2==0 else '')
  sections+=f'''<section class="chapter {modifier}" id="{key}" aria-labelledby="title-{key}"><div class="chapter-heading"><p class="eyebrow"><span>{i:02}</span> / {esc(c['current_features'])}</p><h2 id="title-{key}">{esc(values[0])}</h2></div><div class="chapter-layout"><div class="chapter-copy">{paragraphs(values[1:3])}</div><div class="chapter-media media-{len(ids)}">{photos}</div></div>{extra}</section>'''
 rows=''.join('<tr><th scope="row">'+esc(action)+'</th><td>'+esc(keys)+'</td></tr>' for action,keys in g['control_rows'])
 other='floki' if kind=='zzz' else 'zzz';other_name='Floki Heaven' if other=='floki' else 'ZZZombie Assault'
 return f'''<main id="main" class="game-page game-page-{kind}"><section class="game-hero wrap" id="top"><div class="game-hero-media"><p class="eyebrow">CUZ / PROJECT_0{1 if kind=='zzz' else 2}</p>{image(lead,cap,c,album=kind,eager=True)}</div><div class="game-hero-copy"><div class="game-meta"><span>{esc(g['kicker'])}</span><span class="status">{esc(c['status'])}</span></div><h1>{'ZZZOMBIE<br>ASSAULT' if kind=='zzz' else 'FLOKI<br>HEAVEN'}<span class="accent">.</span></h1><p class="game-hook">{esc(g['hook'][0])}<br>{esc(g['hook'][1])}</p><p class="game-intro">{esc(g['intro'])}</p><ul class="game-facts">{facts}</ul><a class="button button-lime" href="#contents">{esc(c['read_sections'])} ↘</a></div></section><section class="contents-block wrap" id="contents"><div><p class="eyebrow">{esc(c['contents'])}</p><h2>{esc(c['current_features'])}</h2></div><ol>{short_toc}</ol></section><div class="chapter-index" aria-label="{esc(c['contents'])}"><div class="wrap">{toc}</div></div><article class="game-dossier wrap" aria-label="{esc(title+' · '+c['current_features'])}">{sections}<section class="controls-section" id="controls"><p class="eyebrow">{esc(c['build_label'])}</p><h2>{esc(c['controls'])}</h2><div class="control-table"><table><tbody>{rows}</tbody></table></div></section><section class="development-end"><p class="eyebrow">{esc(c['status'])}</p><h2>{esc(g['end_title'])}</h2><p>{esc(g['end_body'])}</p><p class="development-note">{esc(c['dev_note'])}</p><a class="button button-lime" href="{href(lang,other)}">{esc(c['more_games'])}: {other_name} ↗</a></section></article></main>'''

def render(d,lang,page):
 c=d['common'];title=d['home']['title'] if page=='home' else ('ZZZombie Assault' if page=='zzz' else 'Floki Heaven')+' · CUZDEV'
 description=d['home']['meta'] if page=='home' else d[page]['meta']
 url='https://cuzdev.xyz'+href(lang,page)
 alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="https://cuzdev.xyz{href(code,page)}">' for code in LANGS)
 alternates+=f'<link rel="alternate" hreflang="x-default" href="https://cuzdev.xyz{href("en",page)}">'
 hero='/assets/zzzombie-snow-dawn.webp' if page!='floki' else MEDIA['f-action']['src']
 social='/assets/social-card.jpg' if page=='home' else '/assets/social-'+page+'.jpg'
 content=home(d,lang) if page=='home' else game(d,lang,page)
 return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="dark"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#11140f"><link rel="canonical" href="{url}">{alternates}<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{LANGS[lang][3]}"><meta property="og:image" content="https://cuzdev.xyz{social}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/png" href="/assets/favicon.png"><link rel="apple-touch-icon" href="/assets/favicon.png"><link rel="stylesheet" href="/assets/fonts/fonts.css"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/pages.css"><link rel="preload" as="image" href="{hero}"><script src="/site.js" defer></script></head><body class="page-{page}">{header(d,lang,page)}{content}{footer(d,lang)}{dialog(c)}</body></html>
'''

def build(selected=None):
 baseline=json.loads((ROOT/'content/en.json').read_text(encoding='utf-8'));contract=schema(baseline);manifest=[]
 for lang in selected or LANGS:
  d=json.loads((ROOT/'content'/f'{lang}.json').read_text(encoding='utf-8'))
  assert schema(d)==contract,'Incomplete translation: '+lang
  for page in SLUGS:
   text=render(d,lang,page);dest=ROOT/LANGS[lang][0]/SLUGS[page]/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text,encoding='utf-8',newline='\n')
   manifest.append({'lang':lang,'page':page,'url':href(lang,page),'sha256':hashlib.sha256(text.encode()).hexdigest()})
 if selected is None:
  entries=''.join('<url><loc>https://cuzdev.xyz'+x['url']+'</loc></url>' for x in manifest)
  (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+entries+'</urlset>\n',encoding='utf-8')
 print(json.dumps({'pages':len(manifest),'routes':manifest},indent=2))
 return manifest

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--lang',action='append',choices=LANGS);args=parser.parse_args();build(args.lang)
