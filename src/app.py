from preprocess.preprocess import PreProcess
from corpus.bnc_general_corpus import BncGeneralCorpus

import time

if __name__ == '__main__':

    KL_threshold = -20
    top_k_number = 20

    base_path = ''
    dist_path = ''

    bnc_db_path = ''

    start = time.perf_counter()

    # all the paper pipeline is rpresented in this function:
    PreProcess(KL_threshold, top_k_number).proprocess(base_path, dist_path, BncGeneralCorpus(bnc_db_path))


    end = time.perf_counter()
    # elapsed time is in seconds:
    elapsed_time = end - start
    elapsed_minutes = elapsed_time / 60

    print("elapsed minutes: ", elapsed_minutes)
