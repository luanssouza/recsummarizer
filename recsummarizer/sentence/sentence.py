from collections import Counter


class Sentence:
    def __init__(self, id_sentence, sentiment_value, sentiment, xml_name):
        self._number_of_tokens = 0
        self._sentiment_value = sentiment_value
        self._tokens=[] 
        self._aspects=[]
        self._xml = xml_name
        self._id_sentence = id_sentence
        self._sentiment = sentiment
        self.personal_opinion = False
        self._nouns_occurrences = Counter()
        self._joined_string = ''.join(self._tokens)
        self._raw_sentence = ''

    @property
    def number_of_tokens(self):
        return self._number_of_tokens

    @property
    def sentiment_value(self):
        return self._sentiment_value

    @property
    def sentiment(self):
        return self._sentiment

    @property
    def tokens(self):
        return self._tokens
    
    @property
    def aspects(self):
        return self._aspects

    @property
    def xml(self):
        return self._xml

    @property
    def id_sentence(self):
        return self._id_sentence

    @property
    def sentiment(self):
        return self._sentiment

    @property
    def raw_sentence(self):
        return self._raw_sentence


    @number_of_tokens.setter
    def number_of_tokens(self, number_of_tokens):
        self._number_of_tokens = number_of_tokens

    @raw_sentence.setter
    def raw_sentence(self, raw_sentence):
        self._raw_sentence = raw_sentence

    def add_token(self, new_token):
        self._tokens.append(new_token)

    def add_noun(self, new_noun):
        self._nouns_occurrences[new_noun] += 1

    def retrieve_nouns(self):
        return self._nouns_occurrences

    def add_aspect(self, aspect):
        self._aspects.append(aspect)

    def __str__(self):
        if self._raw_sentence:
            return self._raw_sentence
        return ' '.join(self._tokens)

