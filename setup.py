from distutils.core import setup
from setuptools import find_packages

setup(name='RecSummarizer',
      version='1.0',
      description='Summarization framework for Recommender Systems',
      author='Luan Souza',
      url='https://github.com/luanssouza/recsummarizer',
      packages=find_packages(),
      install_requires=[
            'scipy>=1.7.0',
            'numpy>=1.20.3',
            'pandas>=1.2.4',
            'corenlp_protobuf>=3.8.0',
            'nltk>=3.6.2',
            'gensim>=4.0.1',
            'sentence_transformers>=1.2.0',
            'scikit-learn>=0.24.2'
      ]
     )