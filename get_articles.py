# -*- coding: utf-8 -*-
import newspaper
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from collections import Counter

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


engine = create_engine('sqlite:///E:\\code\\news\\articles.db', echo=True)
base = declarative_base()
Session = sessionmaker(bind=engine)


class Article(base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    n_chars = Column(Integer)
    company = Column(String)
    url = Column(String)
    body = Column(String)

    def __repr__(self):
        # return self.url
        return u'id: {} \ntitle: {} \nurl: {} \nNumber of chars: {} \nbody: {}...'.format(self.id, self.title, self.url, self.n_chars, self.body[:100]).encode('utf-8')

base.metadata.create_all(engine)


add = True
# outlet_option = 'g1'
session = Session()
# def add_articles(articles, outlet_option, sites, categories):

if add:
    for outlet_option in sites:
        news = newspaper.build(sites[outlet_option], language='pt', memoize_articles=False,
                               fetch_images=False)
        for art in news.articles:
            # only accepts links from relevant categories
            if any(category in str(art.url) for category in categories[outlet_option]):
                try:
                    art.download()
                    art.parse()
                    chars_count = Counter(art.text.encode('utf-8'))
                    # don't let the same link be added twich
                    for unique_url in session.query(Article).filter(Article.url == art.url):
                        if unique_url is not 0:
                            break
                    else:
                        session.add(Article(title=art.title, n_chars=sum(
                            chars_count.values()), company=outlet_option, url=art.url, body=art.text))
                except Exception as e:
                    pass
        session.commit()


# total = 0
# for n in session.query(Article).filter(Article.url == 'http://exame.abril.com.br/negocios/noticias/grupo-com-sede-nos-eua-eleva-participacao-em-acoes-da-vale'):
#     print n.id
#     break
