from review.base_review import Review
from review.dat_review import DatReview
from review.xml_review import XmlReview

def review_factory(review_type:str = "XmlReview", file:str) -> Review:
    """
    Review Factory Method

    Parameters
    ----------
    review_tyoe : str
        DatReview or XmlReview.
        Default XmlReview.

    file : str
        Given a file that represents a review, this function instantiates review objects (and consequently, sentence objects) by parsing the tree.

    Returns:
    ----------
    A Review instance.
    """

    reviews = {
        "DatReview": DatReview,
        "XmlReview": XmlReview
    }

    return reviews[algorithm](file)