# Auto-Correction Model

<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Explanation](#explanation)
- [Objective](#objective)
- [Setup](#setup)
- [Data](#data)
- [Methodologies](#methodologies)
- [Results](#results)
- [Conclusion](#conclusion)

<!-- /TOC -->
## Explanation
I believe it's self-exploratory. This model is a probabilistic model used to auto-correct misspelled words. It doesn't auto-correct any uppercase words. It auto-corrects names also (you can call it a feature). DON'T try to change that as (months, days, nationalities, ...) are treated as names in the data.

_Future Upgrade:_

I have used a bigram language model for this project, I think it will make a better performance if we used a trigram model instead. But, we need some top-notch data like. As the unigram and bigram frequencies are from "grammarly" (cleaned google book 1gram) and "google book 2gram".

## Objective
Creating a model that auto-corrects the users queries which reduces the user-wasted time.

## Setup
- You need to install `pyjarowinkler` module which is used to find the jaro-winkler distance, it's pretty small (3.2 MB) by running:
<pre>
$ pip install pyjarowinkler
</pre>
- You also need to install NLTK popular package. Run:
<pre>
$ python
\>>> import nltk
\>>> nltk.download('popular')
</pre>

## Data
There are three types of data used in this project:

- 'grammraly_wiktionary': this is a bag of words collected by grammraly web application provided as opensource.
- 'count_2w': this is a bigram frequency corpus which contains a sequence of two words and their frequency in google book ngram project.

## Methodologies
The model uses the data and derive probabilities. These probabilties are smoothed using "Knser-Ney smoothing metho". The final probability is used auto-correct misspelled words.
## Results
The model was able to auto-correct words that have one or two misspelled letters i.e, the sentence 'boooks abot fotware develpomeent' which has words with one-wrong letter like (boo<span style="color:red">o</span>ks) and (abo<span style="color:red">u</span>t) and words with two-wrong letters like (<span style="color:red">s(of)</span>tware) and (devel<span style="color:red">(op)</span>me<span style="color:red">e</span>nt)

## Conclusion
This model is a good-start.
