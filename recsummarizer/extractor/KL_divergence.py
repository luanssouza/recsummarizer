
import numpy as np


def KL_divergence(frequency_corpora_reviews, frequency_corpora_BNC):

    """Computes the discrete KL divergence for a noun present in the corpora review.
        KL value = (frequency_corpora_reviews) * log(frequency_corpora_reviews/frequency_corpora_BNC)

    Args:
        frequency_corpora_reviews (int): The number of occurrences of the noun in the reviews
        corpora of a given movie; it's the term "ca" in the formula described in the paper

        frequency_corpora_BNC (int): The number of occurrences of the noun in the BNC
        corpora; it's the term "cb" in the formula described in the paper

    Returns:
        KL (double): The KL value calculated for the noun
        
    """
    
    #by definition, if the number of occurrences of the noun in the BNC
    #corpora is zero, that means that the kl value for this noun is infinity:
    if frequency_corpora_BNC == 0:
        return np.inf

    division_term = (frequency_corpora_reviews/frequency_corpora_BNC)
    second_term= np.log(division_term)
    KL = frequency_corpora_reviews*second_term

    return (KL)


def epsilon_aspects_extraction(KL_values, threshold):

    """Given a certain threshold for KL divergence, this function extracts 
        aspects from the KL_values dict

    Args:
        KL_values (dict): dict containing each noun in the corpora review
        associated with it's KL value

        threshold (double): The Epsilon cited in the paper


    Returns:
        aspects(dict): A dict that relates each aspect to it's KL value
    """
    aspects={}

    for noun in KL_values:
        if KL_values[noun] > threshold:
            aspects[noun] = KL_values[noun]
    

    return aspects

