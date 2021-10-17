from __future__ import print_function
import networkx as nx
from scipy.spatial.distance import pdist
from scipy.spatial.distance import cosine as cosine_similarity
from scipy.special import comb
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
import string
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd

from sklearn.metrics.pairwise import pairwise_kernels

from nltk.stem.wordnet import WordNetLemmatizer
lemtz = WordNetLemmatizer()

def normalize_and_tokenize(text, stemmer = lemtz.lemmatize):
    tokens = word_tokenize(text)
    try:
        outv = [stemmer(t).translate(None, string.punctuation) for t in tokens] 
        return outv
    except:
        translator = str.maketrans(dict.fromkeys(string.punctuation))
        return [stemmer(t).translate(translator) for t in tokens]

def vectorize(sentences, tfidf=True, ngram_range=None):
    if ngram_range is None:
        ngram_range = (1,1)
    vect = TfidfVectorizer(sublinear_tf=True, max_df=0.5, analyzer='word', 
                   stop_words='english', lowercase=True, ngram_range=ngram_range)
    return vect.fit_transform(sentences)
       
def similarity_graph_from_term_document_matrix(sp_mat):
    dx = pairwise_kernels(sp_mat, metric='cosine')
    g = nx.from_numpy_matrix(dx)
    return g
    
def summarize(text=None, term_doc_matrix=None,  n=5, tfidf=False, ngram_range=None, verbose=False):
    if term_doc_matrix is None:
        if verbose: print("Reading document...")
        sentences = sent_tokenize(text)
        if verbose: print("Fitting vectorizer...")
        term_doc_matrix = vectorize(sentences, tfidf=tfidf, ngram_range=ngram_range)
    if verbose: print("Building similarity graph...")
    g = similarity_graph_from_term_document_matrix(term_doc_matrix)
    if verbose: print("Calculating sentence pagerank (lexrank)...")
    scores = pd.Series(nx.pagerank(g, weight='weight'))
    scores.sort_values(ascending=False, inplace=True)
    ix = pd.Series(scores.index[:n])
    ix.sort_values(inplace=True)
    summary = [sentences[i] for i in ix]
    abc={'summary':summary}
    return abc
