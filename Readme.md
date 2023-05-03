# RecSummarizer

A framework to generate summaries as explanations for recommendation engines.

## Instalation

Install our library: 

    pip install git+https://github.com/luanssouza/recsummarizer

Install [Stanza](https://github.com/stanfordnlp/stanza):

    pip install stanza

## Example Usage

Obtain our reference corpus:

    wget https://raw.githubusercontent.com/luanssouza/recsummarizer/main/resources/BNC_nouns.csv

Import the modules:

    # External modules
    import stanza
    import pandas as pd
    # Our modules
    from recsummarizer.corpus import CsvGeneralCorpus
    from recsummarizer.normalize.tf_idf_normalizer import TfIdfNormalizer
    from recsummarizer.centroid.centroid import Centroid
    from recsummarizer.persistence.stanza_persistence import StanzaPersistence
    from recsummarizer.preprocess.stanza_preprocess import StanzaPreProcess
    from recsummarizer.summarize.summarizer_baseline import SummarizerBaseline
    from recsummarizer.embedding.bert_embedding import BertEmbedding


Initialize the models:
    
    # Downloading english model
    stanza.download('en', verbose=False)

    # Creating our pipeline
    nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,sentiment', verbose=False)

    embedding = BertEmbedding('all-MiniLM-L6-v2')

    general_corpus = CsvGeneralCorpus(pd.read_csv('./BNC_nouns.csv', index_col='noun'))

Preprocess the reviews:

    raw_reviews = [
        "The director is really good. The movie is awesome! You will definetly enjoy it! The scenes are the best!", 
        "The racer is really good."
    ]

    items = [
        {"id": 0, "reviews": raw_reviews }
    ]

    # Creating normalizer instance
    normalizer = TfIdfNormalizer()

    # Creating centroid instance
    centroid = Centroid(normalizer, 0.35)

    # Creating persistence instance
    persistence = StanzaPersistence('./data/', embedding, centroid)

    # Creating a instance of PreProcess
    preprocess = StanzaPreProcess(-20, 20)

    # Preprocessing movies
    preprocess.proprocess(items, persistence, general_corpus, nlp)

Obtain the summary:

    SummarizerBaseline('./data/', 0.90, 5).summarize(0)
    
## Cite Us

    @inproceedings{10.1145/3539637.3557002,
        author = {Souza, Luan Soares de and Manzato, Marcelo Garcia},
        title = {Aspect-Based Summarization: An Approach With Different Levels of Details to Explain Recommendations},
        year = {2022},
        isbn = {9781450394093},
        publisher = {Association for Computing Machinery},
        address = {New York, NY, USA},
        url = {https://doi.org/10.1145/3539637.3557002},
        doi = {10.1145/3539637.3557002},
        booktitle = {Proceedings of the Brazilian Symposium on Multimedia and the Web},
        pages = {202–210},
        numpages = {9},
        keywords = {hierarchical clustering, multi-level summarization},
        location = {Curitiba, Brazil},
        series = {WebMedia '22}
    }
