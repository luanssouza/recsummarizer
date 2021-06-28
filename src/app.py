from preprocess.preprocess import PreProcess
from corpus.bnc_general_corpus import BncGeneralCorpus
from embedding.bert_embedding import BertEmbedding
from persistence.simple_persistence import SimplePersistence

import time

if __name__ == '__main__':

    KL_threshold = -20
    top_k_number = 20

    review_file_type = 'dat'

    model_name = ''

    base_path = ''
    dist_path = ''

    bnc_db_path = ''

    start = time.perf_counter()

    # Creating embedding instance
    embedding = BertEmbedding(model_name)

    # Creating persistence instance
    persistence = SimplePersistence(dist_path, embedding)

    # Creating a instance of GeneralCorpus
    general_corpus = BncGeneralCorpus(bnc_db_path)

    # Creating a instance of PreProcess
    preprocess = PreProcess(KL_threshold, top_k_number)

    # Preprocessing movies
    preprocess.proprocess(base_path, persistence, general_corpus, review_file_type)


    end = time.perf_counter()
    # elapsed time is in seconds:
    elapsed_time = end - start
    elapsed_minutes = elapsed_time / 60

    print("elapsed minutes: ", elapsed_minutes)
