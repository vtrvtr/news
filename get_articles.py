import newspaper
from pathlib import Path


news_folder = Path("E:\\", "code", 'news')

sites = {'exame': 'http://exame.abril.com.br/',
              'g1': 'http://g1.globo.com/',
              'uol': 'http://www.uol.com.br', 
              'terra': 'http://www.terra.com'}

news = newspaper.build(
    sites['g1'], language='pt', memoize_articles=False, fetch_images=False)



for art in news.articles:
    if '/mundo/' in str(art.url):
        print(art.title.encode('utf-8')) 



