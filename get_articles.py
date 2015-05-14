import newspaper
from pathlib import Path


news_folder = Path("E:\\", "code", 'news')

sites = {'exame': 'http://exame.abril.com.br/',
         'g1': 'http://g1.globo.com/',
         'uol': 'http://www.uol.com.br',
         'terra': 'http://www.terra.com'}


categories = {'exame': ['/tecnologia/',
                        '/negocios/',
                        '/economia/'],
              'uol': ['economia.uol',
                      'tecnologia.uol',
                      'mulher.uol',
                      'celebridades.uol'],
              'g1': ['/brasil/',
                     '/politica/',
                     '/ciencia-e-saude/'],
              'terra': ['tecnologia.terra',
                        'mulher.terra',
                        'economia.terra',
                        '/brasil/']}


news = newspaper.build(
    sites['exame'], language='pt', memoize_articles=False, fetch_images=False)


for art in news.articles:
    if any(category in str(art.url) for category in categories['exame']):
        print(art.url.encode('utf-8'))
