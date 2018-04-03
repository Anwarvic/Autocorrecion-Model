import math, pickle
from collections import Counter, defaultdict
from nltk import word_tokenize


class Autocorrector:
    def __init__(self):
        """Initialize your data structures in the constructor."""
        self.UnigramCounts = pickle.load(file('data/grammarly_wikitionary.pickle', 'r')) #dict
        self.BigramCounts = pickle.load(file("data/count_2w.pickle",'r')) #dict
        self.vocabulary = self.UnigramCounts.keys()
        self.total = len(self.vocabulary)
        # ----- Applying Knser-Ney Method -----
        self.BeforeCounts = defaultdict(set)
        self.AfterCounts = defaultdict(set)
        for key in self.BigramCounts.keys():
            first_word, second_word = key.split(' ')
            self.AfterCounts[first_word].add(second_word)
            self.BeforeCounts[second_word].add(first_word)


    def __known(self, words):
        #Return a set of the words subset that are actually in the vocabulary.
        return {w for w in words if w.lower() in self.vocabulary}

    def correct_word(self, word):
        """
        Find the best spelling correction for this word.
        Prefer edit 1, then 2; otherwise default to word itself.
        """
        # ---------------- HELPFUL FUNCTIONS ----------------
        def levenstein1(word_1):
            #Return all strings that are one edit away from this word.
            # ---------------- HELPFUL FUNCTION ----------------
            def split_word(wrd):
                #Return a list of all possible (first, rest) character pairs that comprise word.
                return [(wrd[:i], wrd[i:]) 
                        for i in range(len(wrd)+1)]
            # --------------------------------------------------
            alphabet = "abcdefghijklmnopqrstuvwxyz'"
            pairs      = split_word(word_1)
            deletes    = [a+b[1:]           for (a, b) in pairs if b]
            transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
            replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
            inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
            return set(deletes + transposes + replaces + inserts)
        def levenstein2(word_2):
            #Return all strings that are two edits away from this word.
            return {e2 for e1 in levenstein1(word_2) for e2 in edits1(e1)}
        # ------------------------------------------------
        if self.__known([word]):  #the word in the vocabulary
            return [(word, self.UnigramCounts[word])]
        else: #the word not in the vocabulary
            candidates = self.__known(levenstein1(word))
            c = Counter({w: self.UnigramCounts[w] for w in candidates})
            if c:
                if c.most_common(1)[0][1] < 100000: #------------------------------> hyper-parameter
                    candidates = candidates.union(self.__known(levenstein2(word))) 
                    c = Counter({w: self.UnigramCounts[w] for w in candidates})
                return c.most_common(100)    #lists of tuple
            else: # didn't found candidates
                return [(word, 0)]


    def __score(self, tupl):
        """
        Takes a tuple and returns a score using Knser-Ney method
        This score depends on the count of bigram and unigram
        This score is used to correct a sentence
        """
        kn_score = 0.0
        d = 0.75
        first_word, second_word = tupl
        count1 = self.BigramCounts[' '.join(tupl).lower()]
        if first_word == '<s>':
            count2 = 10000000 #ten million
        else:
            count2 = self.UnigramCounts[first_word]
        _lambda = d/(count2+1.)*len(self.AfterCounts[first_word])
        if count1 == 0:
            d = 0.9
        p_continuation = float(len(self.BeforeCounts[second_word]))/self.total
        first_term = ( (count1-d)/(count2+1.) )
        if first_term == 0:
            kn_score += (_lambda*p_continuation)
        else:
            kn_score += first_term + (_lambda*p_continuation)
        return kn_score


    def __custom_tokenize(self, sentence):
        lst = word_tokenize(sentence)
        if len(lst) == 1:
            return [sentence]
        output = []
        for i in xrange(len(lst)-1):
            if "'" == lst[i][0]:
                continue
            elif "'" == lst[i+1][0]:
                output.append(lst[i]+lst[i+1])
            else:
                output.append(lst[i])
        if "'" not in lst[i+1]:
            output.append(lst[i+1])
        return output


    def correct_sentence(self, sentence):
        def case_of(text):
            #Return the case-function appropriate for text: upper, lower, title, or just str.
            return (str.upper if text.isupper() else
                    str.lower if text.islower() else
                    str.title if text.istitle() else
                    str)
        output = ''
        start_word = "<s>"
        for wrd in self.__custom_tokenize(sentence):
            if wrd in ",.;?!":
                output += wrd
            elif wrd.isupper():
                output += ' ' + wrd
            else:
                candidates = [(tupl[0], self.__score((start_word, tupl[0]))) for tupl in self.correct_word(wrd.lower())]
                winner = max(candidates, key=lambda x: x[1])[0]
                output += ' ' + case_of(wrd)(winner)
                start_word = winner
        return output.strip()







if __name__ == "__main__":
    model = Autocorrector()
    print model.correct_sentence('i lov arabick and MMA')
    print model.correct_sentence('no this answer doesnt saticfact me')
    print model.correct_sentence('In arabick')