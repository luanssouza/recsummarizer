class Item(object):
    def __init__(self, centroid, aspects_df, sentences_df):
        self.centroid = centroid
        self.aspects_df = aspects_df
        self.sentences_df = sentences_df
        self.aspects_embeddings = None
        self.aspects_tf_idf = None
        self.aspects = None
        self.clusters = None
