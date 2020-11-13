import gensim
from bs4 import BeautifulSoup
from gensim.utils import simple_preprocess
from requests import request
from gensim import models, corpora
from gensim.models import Word2Vec
import numpy as np
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
words = []
file_with_links = open('today_links_file.txt', 'r')
links = list(file_with_links.read().split())
ch = 0
words_of = []
for link in links:

    contents = request('GET', link).text

    soup = BeautifulSoup(contents, 'html.parser')
    s = soup.text.split()
    for i in range(len(s)):
        if s[i].count('.') == 0:
            p = morph.parse(s[i])[0]
            s[i] = p.normal_form
        else:
            s[i] += '.'
    s  = " ".join(str(x) for x in s)
    words_of += s.split('.')
    ch += 1

mydict = corpora.Dictionary([simple_preprocess(line) for line in words_of])
corpus = [mydict.doc2bow(simple_preprocess(line)) for line in words_of]
tfidf = models.TfidfModel(corpus, smartirs='ntc')

l = []
for doc in tfidf[corpus]:
    for id, freq in doc:
        l.append((mydict[id], np.around(freq, decimals=2)))

model = gensim.models.Word2Vec.load('w2v.model')

l.sort(key = lambda x : x[1], reverse=True)
for i in range(len(l) // 2):
    if 0.45 < l[i][1] < 0.85:
        words.append(l[i][0])
        try:
            same_words = []
            for j in model.most_similar(positive=l[i][0]):
                same_words.append(j[0])
            words += same_words
        except:
            continue

file_with_words = open('file_with_words.txt', 'w')
for i in words:
    file_with_words.write(str(i) + '\n')