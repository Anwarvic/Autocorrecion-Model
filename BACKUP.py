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
            elif wrd.isupper() and len(wrd) != 1:
                output += ' ' + wrd
            else:
                wrd = wrd.lower()
                candidates = []
                for tupl in self.correct_word(wrd):
                    if start_word == '<s>':
                        editscore = 0
                    else:
                        editscore = self.__jaro_score((start_word, tupl[0]))
                    lmscore = self.__score((start_word, tupl[0]))
                    score = lmscore + editscore
                    candidates.append((tupl[0], lmscore)) ###--------------------->score instead of lmscore
                winner = max(candidates, key=lambda x: x[1])[0]
                output += ' ' + case_of(wrd)(winner)
                start_word = winner
        return output.strip()
