
# coding: utf-8

# In[1]:


import feedparser
import pandas as pd
import tldextract
from postagem.Util import download_image, extract_domain, downlaod_and_move_image, get_noticia_uol, get_noticia_comercio
import os
from postagem.lexical_analyzer import lexical
from postagem.site_wordpress import post_news
from Model.News import News
from Database.new_database import save_news, select_news

# In[2]:


# hit_list = ["https://www.jornaldocomercio.com/_conteudo/politica/rss.xml",
#            "http://pox.globo.com/rss/g1/politica/mensalao/", "https://feeds.folha.uol.com.br/poder/rss091.xml"]

hit_list = ["https://www.jornaldocomercio.com/_conteudo/politica/rss.xml",
           "http://pox.globo.com/rss/g1/politica/", "https://feeds.folha.uol.com.br/poder/rss091.xml"]

# hit_list = ["http://pox.globo.com/rss/g1/politica/", "https://feeds.folha.uol.com.br/poder/rss091.xml"]


future_calls = [feedparser.parse(rss_url) for rss_url in hit_list]


# In[3]:


entries = []
for feed in future_calls:
    entries.extend( feed[ "items" ] )


# In[4]:


resultados = pd.DataFrame({'titulos': [], 'links': [], 'noticia': [], 'image': [], 'abstract': [], 'date': []})


# In[5]:


i = 0
for entrie in entries:
    i+=1
    row = {'titulos': [], 'links': [], 'noticia': [], 'image': [], 'abstract': [], 'date': []}
    domain = extract_domain(entrie['link'])
    if  domain == 'globo':
        row['titulos'].append(entrie['title'])
        row['links'].append(entrie['link'])
        row['date'].append(entrie['published'])
        row['noticia'].append(entrie['summary_detail']['value'])
        row['abstract'].append(entrie['summary_detail']['value'])
        if 'media_content' in entrie:
            path_image = entrie['media_content'][0]['url']
            row['image'].append(downlaod_and_move_image(path_image))
        else:
            row['image'].append(0)

    elif domain == 'jornaldocomercio':
        row['titulos'].append(entrie['title'])
        row['links'].append(entrie['link'])
        row['date'].append(entrie['published'])
        row['abstract'].append(entrie['summary'])
        noticia = get_noticia_comercio(entrie['link'])
        row['noticia'].append(noticia)
        if 'media_content' in entrie:
            path_image = entrie['media_url']
            if path_image != '':
                row['image'].append(downlaod_and_move_image(path_image))
            else:
                row['image'].append(0)
        else:
            row['image'].append(0)
    elif domain == 'folha':
        pass

    news = News(row['abstract'], row['noticia'], row['date'], row['links'], row['titulos'], row['image'])
    if select_news(news) is None:
        save_news(news)
        row = pd.DataFrame(row)
        resultados_cat = lexical(row)
        post_news(resultados_cat)


# In[6]:
 
 
resultados_cat = lexical(resultados)
 
 
# In[7]:
 
 
post_news(resultados_cat)

