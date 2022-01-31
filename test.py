from gensim.models import word2vec
import logging

model = word2vec.Word2Vec.load("result.model")
print(model.wv.most_similar(positive=["walk"]))
