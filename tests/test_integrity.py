"""Static publication integrity. All checks use the standard library."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin,unquote
from collections import Counter
import json,re,unittest,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PREFIXES=['','pt-br/','es/','de/','fr/','it/']
PAGES=['','zzzombie-assault/','floki-heaven/']
ROUTES=['/'+a+b for a in PREFIXES for b in PAGES]
class Document(HTMLParser):
 def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
def local_file(address,route='/'):
 parsed=urlsplit(urljoin('https://cuzdev.xyz'+route,address))
 if parsed.netloc!='cuzdev.xyz' or parsed.scheme not in ['http','https']:return None
 path=unquote(parsed.path)
 return ROOT/path.lstrip('/')/('index.html' if path.endswith('/') else '')

class PublicationIntegrity(unittest.TestCase):
 def test_all_page_resources_exist(self):
  for route in ROUTES:
   page=local_file(route);assert page is not None
   doc=Document(page.read_text(encoding='utf-8'))
   for tag,attrs in doc.tags:
    refs=[attrs[k] for k in ['src','href','data-shot'] if k in attrs]
    if tag=='meta' and attrs.get('property')=='og:image':refs.append(attrs['content'])
    for ref in refs:
     file=local_file(ref,route)
     if file is not None:self.assertTrue(file.is_file(),(route,ref))
  for css in [ROOT/'styles.css',ROOT/'pages.css',ROOT/'assets/fonts/fonts.css']:
   for address in re.findall(r'url\(([^)]+)\)',css.read_text(encoding='utf-8')):
    address=address.strip(' \"\'')
    if not address.startswith('data:'):
     target=ROOT/address.lstrip('/') if address.startswith('/') else css.parent/address
     self.assertTrue(target.is_file(),address)
 def test_ids_are_unique(self):
  for route in ROUTES:
   page=local_file(route);assert page is not None
   doc=Document(page.read_text(encoding='utf-8'))
   duplicates=[key for key,count in Counter(a['id'] for _,a in doc.tags if 'id' in a).items() if count>1]
   self.assertEqual(duplicates,[],route)
 def test_every_system_has_photos_with_localized_captions(self):
  for code in ['en','pt-BR','es','de','fr','it']:
   content=json.loads((ROOT/'content'/f'{code}.json').read_text(encoding='utf-8'))
   for game in ['zzz','floki']:
    for key,rows in content[game]['chapters'].items():
     self.assertGreaterEqual(len(rows),4,(code,game,key))
     self.assertTrue(all(isinstance(row,str) and row.strip() for row in rows))
 def test_sitemap_contains_exactly_the_localized_routes(self):
  urls=[node.text for node in ET.parse(ROOT/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
  self.assertEqual(set(urls),{'https://cuzdev.xyz'+r for r in ROUTES})
  self.assertEqual(len(urls),len(ROUTES))
 def test_selected_original_animations_have_complete_metadata(self):
  for name,count in [('akashi-wind',32),('satoshi-combo',58),('floki-hop',4)]:
   meta=json.loads((ROOT/'assets/sprites'/f'{name}.json').read_text(encoding='utf-8'))
   self.assertEqual(len(meta['frames']),count,name)
   sheet=local_file(meta['image']);assert sheet is not None
   self.assertTrue(sheet.is_file())
   self.assertTrue(all(f['ms']>0 for f in meta['frames']))
   self.assertGreaterEqual(meta['hold'],0)
 def test_public_text_contains_no_private_paths_or_credentials(self):
  forbidden=re.compile(r'C:[/\\]Users[/\\]|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----')
  files=[local_file(r) for r in ROUTES]+list((ROOT/'content').glob('*.json'))+list((ROOT/'assets/sprites').glob('*.json'))+[ROOT/'site.js',ROOT/'pages.css',ROOT/'tools/build_site.py',ROOT/'README.md']
  for file in files:
   assert file is not None
   self.assertIsNone(forbidden.search(file.read_text(encoding='utf-8')),file.name)

if __name__=='__main__':unittest.main()
