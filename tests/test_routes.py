"""Public route contract. Run with: python -m unittest discover -s tests."""
from pathlib import Path
from html.parser import HTMLParser
import unittest

ROOT=Path(__file__).resolve().parents[1]
LANGS={'en':'','pt-BR':'pt-br/','es':'es/','de':'de/','fr':'fr/','it':'it/'}
PAGES=['','zzzombie-assault/','floki-heaven/']

class Document(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))

class RouteContract(unittest.TestCase):
 def test_all_localized_routes_are_static_complete_pages(self):
  for lang,prefix in LANGS.items():
   for page in PAGES:
    with self.subTest(lang=lang,page=page):
     p=ROOT/prefix/page/'index.html'
     self.assertTrue(p.exists(),f'Missing dedicated localized page: {prefix}{page}')
     text=p.read_text(encoding='utf-8');doc=Document(text)
     self.assertIn(('html',{'lang':lang}),doc.tags)
     self.assertEqual(len([a for t,a in doc.tags if t=='h1']),1)
     alternatives=[a for t,a in doc.tags if t=='link' and a.get('rel')=='alternate']
     self.assertEqual({a.get('hreflang') for a in alternatives},set(LANGS)|{'x-default'})
     self.assertEqual(len([a for t,a in doc.tags if t=='a' and 'data-language' in a]),6)
     if page:
      images=[a for t,a in doc.tags if t=='button' and 'data-shot' in a]
      self.assertGreaterEqual(len(images),8,f'Not enough contextual screenshots: {prefix}{page}')
      self.assertIn('class="chapter',text)
     self.assertNotIn('TODO',text)

if __name__=='__main__':unittest.main()
