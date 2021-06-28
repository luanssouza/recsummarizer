from sentence_transformers import SentenceTransformer

modelBERT = SentenceTransformer('bert-large-nli-stsb-mean-tokens')

def sentences_embeddings(sentences):
    return modelBERT.encode(sentences)