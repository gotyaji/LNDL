# -*- coding: utf-8 -*-
"""YZA_9.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ohhKvoJvfuwXZBViboEeckqvWxW5oJLS
"""

Doc1 = ["With the Union cabinet approving the amendments to the Motor Vehicles Act, 2016, those caught for drunken driving will have to have really deep pockets, as the fine payable in court has been enhanced to Rs 10,000 for first-time offenders." ]

Doc2 = ["Natural language processing (NLP) is an area of computer science and artificial intelligence concerned with the interactions between computers and human (natural) languages, in particular how to program computers to process and analyze large amounts of natural language data."]

Doc3 = ["He points out that public transport is very good in Mumbai and New Delhi, where there is a good network of suburban and metro rail systems."]

Doc4 = ["But the man behind the wickets at the other end was watching just as keenly. With an affirmative nod from Dhoni, India captain Rohit Sharma promptly asked for a review. Sure enough, the ball would have clipped the top of middle and leg."]

Doc5 = ['The education system plays a pivotal role in shaping the future of society by providing individuals with the knowledge and skills necessary to succeed in life. It encompasses various levels, from early childhood education to higher education, and aims to foster intellectual development, critical thinking, and personal growth. A strong education system not only imparts academic knowledge but also promotes social integration, character development, and the pursuit of lifelong learning.']

Doc6 =[" The development of vaccines, pharmaceuticals, and medical devices has significantly extended life expectancy and enhanced our ability to combat various diseases. In the face of global health challenges, such as the COVID-19 pandemic, medical science has played a crucial role in global response efforts, highlighting the vital importance of a robust and adaptable healthcare system. Medical research continues to unlock new frontiers, offering hope for better and more personalized healthcare solutions in the future."]

Doc7 =["Aviation is a dynamic and essential industry that encompasses the design, manufacturing, operation, and maintenance of aircraft. From commercial airlines connecting people across the globe to military aviation safeguarding nations, the field of aviation is a critical pillar of modern society. It continues to advance with cutting-edge technology, making air travel safer, more efficient, and environmentally friendly. The aviation sector is not only about airplanes but also includes helicopters, drones, and spacecraft, contributing to economic growth, global connectivity, and scientific exploration. This industry holds the promise of an exciting future, with ongoing innovations that improve both travel and our understanding of the world beyond our atmosphere."]

import nltk
nltk.download ('stopwords')

import nltk
nltk.download ('punkt')

#Step 7.1.1: Import the libraries

import gensim
from gensim.models import Word2Vec
import numpy as np
import nltk
import itertools
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import scipy
from scipy import spatial
from nltk.tokenize.toktok import ToktokTokenizer
import re
tokenizer =ToktokTokenizer()
stopword_list=nltk.corpus.stopwords.words('english')

# Step 7.1.2 - Create/import documents
#Doct Doc2, Doc3 and Doc4 as defined above in the code.
#Put all the documents in one 11st
fin=Doc1+Doc2+Doc3+Doc4+Doc5+Doc6+Doc7
print(fin)

# import gensim package
 #import gensim
#load the saved model
#model- gensin.models.KeyedVectors.load_word2vec_format(/http://diufe6q8s juo99.cloudfront.net/public/GoogleNews-vectors-negative380.bin. ## http://diufe8q8sjuo99.cloudfront.net/public/GoogleNews-vectors-negative38e.bin.gz
import gensim.downloader as api
wv=api.load('word2vec-google-news-300')

#print (model)
#print (gensin.models. Word2Vec0)

# Step 7.1.4: Create IR system
#Now we build the information retrieval system:
# Preprocessing
def remove_stopwords(text, is_lower_case=False):
  pattern= r'[^a-zA-Z0-9\s]'
  text= re.sub(pattern,"", text)
  tokens= tokenizer.tokenize(text)
  tokens =[token.strip() for token in tokens]
  if is_lower_case:
    filtered_tokens =[token for token in tokens if token not in stopword_list]
  else:
    filtered_tokens =[token for token in tokens if token.lower() not in stopword_list]
    filtered_text=''.join(filtered_tokens)
  return filtered_text

#Function to get the embedding vector for n dimension, we have used "300"
def get_embedding(word):
  if word in wv.key_to_index:
     return wv[word]
  else:
     return np.zeros(300)

#just to see the word vector for some word.
print(wv['cricket'])
print("-------------------------------------------")
print(len(wv['cricket']))
print(np.mean(np.array(wv['cricket']), axis=0))

#just to see no. of words in Doc1
print(len(tokenizer.tokenize (Doc1)))
#so, we would get 47 word vectors, each of size 300.
#One vector for one word.
#so, we could get the mean of each vector #so that we reduce of the values we have to handle

#Getting average vector for each document
out_dict={}
for sen in fin: #this loop will pick one sentence at a time from fin (final document)
    average_vector=(np.mean(np.array([get_embedding(x) for x in nltk.word_tokenize(remove_stopwords (sen))]), axis=0))
    dict ={sen : (average_vector)}
    out_dict.update(dict)
#Function to calculate the similarity between the query vector and document vector
def get_sim(query_embedding, average_vector_doc):
  sim=[(1- scipy.spatial.distance.cosine (query_embedding, average_vector_doc))]
  return sim

print(out_dict)

# Rank all the documents based on the similarity to get relevant docs
def Ranked_documents (query):
    query_words= (np.mean(np.array([get_embedding(x) for x in nltk.word_tokenize(query.lower())],dtype=float), axis=0))
    rank =[]
    for k,v in out_dict.items():
      rank.append((k, get_sim(query_words, v)))
    rank = sorted(rank,key=lambda t: t[1], reverse=True)
    print('Ranked Documents :')
    return rank

# Call the IR function with a query
Ranked_documents("cricket")

# Let's take one more example as may be driving.
Ranked_documents("driving is cool on National Highways")

# Let's take one more example as may be driving.
Ranked_documents("Maintaince of aircrafts")

# Let's take one more example as may be driving.
Ranked_documents("COVID-19 pandamic")

Ranked_documents("The education system plays a pivotal role")
