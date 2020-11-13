import gensim

model = gensim.models.Word2Vec.load('w2v.model')

print(model.most_similar(positive=['княжна']))