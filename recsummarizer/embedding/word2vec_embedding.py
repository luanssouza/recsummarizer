from .base_embedding import Embedding

import gensim.downloader
from gensim.utils import tokenize

class Word2VecEmbedding(Embedding):
    def __init__(self, model_name: str):
        self.__model = gensim.downloader.load(model_name)

    def sentence_embedding(self, sentence: str):
        tokens = tokenize(sentence, True)
        embedding = []

        for t in tokens:
            if self.__model.has_index_for(t):
                if len(embedding) == 0:
                    embedding = self.__model[t]
                else:
                    embedding = embedding + self.__model[t]

        return embedding

    def sentences_embeddings(self, sentences: list):
        embeddings = [self.sentence_embedding(s) for s in sentences]
        return embeddings