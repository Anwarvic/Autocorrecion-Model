from collections import Counter, defaultdict
import math, pickle
from nltk import word_tokenize
from nltk.util import ngrams


class CustomLanguageModel:
    def __init__(self):
        """Initialize your data structures in the constructor."""
        self.UnigramCounts = pickle.load(file('data/grammarly_wikitionary.pickle', 'r')) #dict
        self.BigramCounts = pickle.load(file("data/count_2w.pickle",'r')) #dict
        self.total = len(self.UnigramCounts.keys())
        self.BeforeCounts = defaultdict(set)
        self.AfterCounts = defaultdict(set)
        self.train()


    def train(self):
        """ Takes a corpus and trains your language model. 
            Compute any counts or other corpus statistics in this function.
        """  
        for key in self.BigramCounts.keys():
            first_word, second_word = key.split(' ')
            self.AfterCounts[first_word].add(second_word)
            self.BeforeCounts[second_word].add(first_word)


    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the 
            sentence using your language model. Use whatever data you computed in train() here.
        """
        kn_score = 0.0
        d = 0.75
        tokens = word_tokenize(sentence)
        bigrams = ngrams(tokens, 2)
        for first_word, second_word in bigrams:
            count1 = self.BigramCounts[first_word+' '+second_word]
            count2 = self.UnigramCounts[first_word]
            _lambda = d/(count2+1.)*len(self.AfterCounts[first_word])
            if count1 == 0:
                d = 0.9
            p_continuation =  float(len(self.BeforeCounts[second_word]))/self.total
            first_term = ( (count1-d)/(count2+1.) )
            if first_term == 0:
                kn_score += (_lambda*p_continuation)
            else:
                kn_score += first_term + (_lambda*p_continuation)
        return kn_score




print 'Custom Language Model:'
model = CustomLanguageModel()
print model.score('i want to love you')
