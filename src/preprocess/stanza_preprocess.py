from extractor.KL_divergence import epsilon_aspects_extraction
from item.stanza_item import StanzaItem

class StanzaPreProcess(object):
    def __init__(self, kl_threshold, top_k_number):
        self.__kl_threshold = kl_threshold
        self.__top_k_number = top_k_number

    def proprocess(self, items, persistence, general_corpus, nlp_pipeline):
        
        for item in items:
            new_movie = StanzaItem(item["id"], item["reviews"], general_corpus, nlp_pipeline)
            print("Item processed:", item["id"])

            new_movie.kl_values()
            new_movie.aspects_score = epsilon_aspects_extraction(new_movie.kl_nouns_values, self.__kl_threshold)
            new_movie.top_k_aspects_evaluation(self.__top_k_number)
            new_movie.sentence_filtering()

            persistence.persist_movie(new_movie)


    