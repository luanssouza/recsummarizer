from embedding.base_embedding import Embedding

from sentence_transformers import SentenceTransformer

class BertEmbedding(Embedding):

    def __init__(self, model_name_or_path: str):
        self.__model = SentenceTransformer(model_name_or_path)

    def sentence_embedding(self, sentence: str):
        return self.__model.encode(sentence)

    def sentences_embeddings(self, sentences: list):
        return self.__model.encode(sentences)