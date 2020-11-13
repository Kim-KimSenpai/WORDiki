# -*- coding: utf-8 -*-
# imports
import gensim
import string
from nltk.tokenize import sent_tokenize
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from gensim.models.word2vec import LineSentence
from nltk.tokenize import word_tokenize
# load text
text = open('voinaimir.txt', 'r', encoding='utf-8').read()
def tokenize_ru(file_text):
    #firstly let's apply nltk tokenization
    tokens = word_tokenize(file_text)

    tokens = [i for i in tokens if (i not in string.punctuation)]

    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...'])
    tokens = [i for i in tokens if (i not in stop_words)]

    tokens = [i.replace("«", "").replace("»", "") for i in tokens]

    return tokens


sentences = [tokenize_ru(sent) for sent in sent_tokenize(text, 'russian')]
print(len(sentences))

w2v_model = Word2Vec(
    min_count=4,
    window=2,
    size=300,
    negative=10,
    alpha=0.03,
    min_alpha=0.0007,
    sample=6e-5,
    sg=1)

w2v_model = gensim.models.Word2Vec(sentences, size=150, window=5, min_count=5, workers=4)
w2v_model.save('w2v.model')