import math, pickle
from collections import Counter, defaultdict
from pyjarowinkler.distance import get_jaro_distance
from nltk import word_tokenize





class Autocorrector:
    def __init__(self):
        """Initializes our model."""
        self.UnigramCounts = pickle.load(open('data/grammarly_wikitionary.pickle', 'rb'))
        self.BigramCounts = pickle.load(open("data/count_2w.pickle",'rb')) #dict
        self.vocabulary = self.UnigramCounts.keys() #represents roughly all the english words 
        self.total = len(self.vocabulary)
        #dictionary of letters that have been misspelled and the correct letter
        self.edit_table = defaultdict(set)
        
        #initialize self.edit_table
        with open('data/count_1edit.txt') as fin:
            for line in fin:
                ch_tuple, count = line.split('\t')
                first, second = ch_tuple.split('|')
                if first != ' ':
                    self.edit_table[first.lower()].add(second)
        # ----- variables used for ppplying Knser-Ney smoothing Method -----
        self.BeforeCounts = defaultdict(set)
        self.AfterCounts = defaultdict(set)
        for key in self.BigramCounts.keys():
            first_word, second_word = key.split(' ')
            self.AfterCounts[first_word].add(second_word)
            self.BeforeCounts[second_word].add(first_word)
        print ("Done Reading...")


    def __known(self, words):
        """
        Takes a list of words
        Returns only the words that are actually in the vocabulary.
        """
        return {w for w in words if w.lower() in self.vocabulary}


    def correct_word(self, word):
        """
        Finds the best spelling correction for the given word.
        Prefers one edit levenstein distance, then 2
        Otherwise default to the word itself.
        """
        # ---------------- HELPFUL FUNCTIONS ----------------
        def levenstein1(word_1):
            """
            Returns all strings that are one edit away from the given word.
            """
            # ---------------- HELPFUL FUNCTION ----------------
            def split_word(wrd):
                """
                Returns a list of all possible (first, rest) character pairs that comprise word.
                """
                return [(wrd[:i], wrd[i:]) 
                        for i in range(len(wrd)+1)]
            # --------------------------------------------------
            alphabet = "abcdefghijklmnopqrstuvwxyz'" #note that "'" at the end
            pairs = split_word(word_1)
            #replaces uses the 'edit_table' member variable to try to replace characters
            replaces = [word_1.replace(ch, sub) for ch in word_1 for sub in self.edit_table[ch]]
            #tries to delete a certain character each iteration.
            deletes = [a+b[1:] for (a, b) in pairs if b]
            #transposes two consecutive letters each iteration.
            transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
            #inserts a new character each iteration
            inserts = [a+c+b for (a, b) in pairs for c in alphabet]
            return set(deletes + transposes + replaces + inserts)
        def levenstein2(word_2):
            """
            Returns all strings that are two edits away from the given word.
            """
            return {e2 for e1 in levenstein1(word_2) for e2 in levenstein1(e1)}
        # ------------------------------------------------
        if self.__known([word]):  #the word in the vocabulary
            return [(word, self.UnigramCounts[word])]
        else: #the word not in the vocabulary
            candidates = self.__known(levenstein1(word))
            c = Counter({w: self.UnigramCounts[w] for w in candidates})
            if c: #there are candidates
                if c.most_common(1)[0][1] < 1000000:
                    candidates = candidates.union(self.__known(levenstein2(word))) 
                    c = Counter({w: self.UnigramCounts[w] for w in candidates})
                    if c: #there are candidates
                        return c.most_common(100)
                    else:
                        return [(word, 0)]
                else:
                    return c.most_common(100)
            else: #c is empty
                candidates = self.__known(levenstein2(word))
                c = Counter({w: self.UnigramCounts[w] for w in candidates})
                if c:
                    return c.most_common(100)
                else:
                    return [(word, 0)]


    def __jaro_score(self, tupl):
        """
        calculates Jaro-Winkler distance between two given words.
        """
        w1, w2 = tupl
        return get_jaro_distance(w1, w2)


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
        """
        Tokenizes a given sentence
        The only difference between this method and word_tokenize() is
        that this method treats "benchmark's" as one word, while word_tokenize()
        treats it as two words ["benchmark", "'s"]
        """
        lst = word_tokenize(sentence)
        if len(lst) == 1:
            return [sentence]
        output = []
        for i in range(len(lst)-1):
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
        """
        The main method for our class, it corrects a given sentence.
        """
        def case_of(text):
            """
            Return the case-function appropriate for text: upper, lower, title, or just str.
            """
            return (str.upper if text.isupper() else
                    str.lower if text.islower() else
                    str.title if text.istitle() else
                    str)
        output = ''
        print ('Sentence: {}'.format(sentence))
        print('{')
        start_word = '<s>'
        for idx, wrd in enumerate(self.__custom_tokenize(sentence)):
            print ('   "{}" at index {}:'.format(wrd, idx+1))
            if wrd in ",.;?!":
                output += wrd
                print ('      candidate word: {}'.format(wrd))
            elif wrd.isupper() and len(wrd) != 1:
                output += ' ' + wrd
                print ('      candidate word: {}'.format(wrd))
            else:
                case = case_of(wrd)
                wrd = wrd.lower()
                candidates = []
                for tupl in self.correct_word(wrd):
                    if start_word == '<s>':
                        editscore = 0
                    else:
                        editscore = self.__jaro_score((start_word, tupl[0]))
                    lmscore = self.__score((start_word, tupl[0]))
                    score = lmscore + editscore
                    candidates.append((tupl[0], lmscore)) ###--------------------->lmscore instead of score
                winner = max(candidates, key=lambda x: x[1])[0]
                output += ' ' + case(winner)
                start_word = winner
                print ('      candidate word: {}'.format(case(winner)))
            print('}')
        return output.strip()







if __name__ == "__main__":
    model = Autocorrector()
    print (model.correct_sentence('i Lov engls and MMA'))
    print (model.correct_sentence('no tis answr doesnt saticfay me'))
    print (model.correct_sentence('In arabicke'))
    print (model.correct_sentence('boooks abot fotware develpomeent'))
