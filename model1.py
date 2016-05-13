import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import linear_kernel

def main(n):
    # GET THE DATA
    df = pd.read_pickle('data_consolidated.pkl')
    member_id = df['member_id']

    # DO TFIDF TRANSFORMATION
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(df['event_description']).toarray()

    # RANKING
    ranking(vectorizer, vectors, member_id, upcomings, n)

    
def get_top_values(lst, n, labels):
    '''
    Given a list of values, find the indices with the highest n values.
    Return the labels for each of these indices.
    '''
    return [labels[i] for i in np.argsort(lst)[-1:-n-1:-1]]

def ranking(vectorizer, vectors, member_id, upcomings, n):
    '''
    Print out the top n members for each of the upcoming events.
    '''
    tokenized_upcomings = vectorizer.transform(upcomings)
    cosine_similarities = linear_kernel(tokenized_upcomings, vectors)
    for i, upcoming in enumerate(upcomings):
        print upcoming
        print get_top_values(cosine_similarities[i], n, member_id)
        print


if __name__ == '__main__':
    
    upcomings = ['there is a python work shop tonight', 'Just land a new DS \
                job? Contact me to speak on this panel! Tell current job seekers \
                about your experiences and takeaways. \
                Tell employers and recruiters how they should improve the process.']
    main(5)