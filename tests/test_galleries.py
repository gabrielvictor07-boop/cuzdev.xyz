"""Contextual gallery contracts for the generated game pages."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
LANGS=['','pt-br/','es/','de/','fr/','it/']

class GalleryContract(unittest.TestCase):
 def test_each_system_has_its_own_screenshot_album(self):
  for prefix in LANGS:
   for kind,slug in [('zzz','zzzombie-assault'),('floki','floki-heaven')]:
    text=(ROOT/prefix/slug/'index.html').read_text(encoding='utf-8')
    for section,markup in re.findall(r'<section class="chapter[^\"]*" id="([^\"]+)"[^>]*>(.*?)</section>',text,re.S):
     with self.subTest(lang=prefix,game=kind,section=section):
      albums=set(re.findall(r'data-album="([^\"]+)"',markup))
      self.assertEqual(albums,{kind+'-'+section})

if __name__=='__main__':unittest.main()
