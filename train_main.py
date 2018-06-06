#!/usr/bin/python
#-*-encoding:utf-8-*-
import re
import sys
import pickle
import numpy as np
import pycrfsuite
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from collections import Counter

def extract(instance):
  words=[]
  for word in instance:
    word=re.sub(r'(.)\1{4,}',r'\1\1\1',word.decode('utf8')).lower()
    word_num=re.sub(r'\d','9',word)
    if word_num!=word:
    #  print word,word_num
      words.append(word_num.encode('utf8'))
    words.append(word.encode('utf8'))
  features=[]
  counts=Counter(words)
  for feat in counts.most_common(10):
    features.append('most_common10='+str(feat[0]))
  for feat in counts.most_common(20):
    features.append('most_common20='+str(feat[0]))
  #for feat,freq in counts.most_common():
  #  features.append('feat='+str(feat))#+':'+str(float(freq)/len(words)))
  for feat in words[:3]:
    features.append('first3='+str(feat))
  #if len(words)>0:
  #  features.append('first='+str(words[0]))
  features.append('num_words:'+str(len(words)))
  features.append('average_length:'+str(np.mean([len(e) for e in words])))
  return features

def enforce_constraints(instance):
  #order={'FRONT':1,'BODY':2,'BACK':3}
  fire=False
  last='FRONT'
  for idx,label in enumerate(instance):
    if not fire:
      fire=label=='BODY'
    if label=='FRONT' and fire:
      instance[idx]=last
    else:
      last=label
  fire=False
  last='BACK'
  for idx,label in list(enumerate((instance)))[::-1]:
    if not fire:
      fire=label=='BODY'
    if label=='BACK' and fire:
      instance[idx]=last
    else:
      last=label
    #if order[last]>order[label]:
    #  instance[idx]=last
    #else:
    #  last=label

if __name__=='__main__':
  X=[]
  Y=[]
  for file in open(sys.argv[1]):
    x=[]
    y=[]
    for line in open('docs/'+file.strip()+'.pages'):
      text,label1,label2=line.rstrip().split('\t')
      x.append(extract(text.split(' ')))
      y.append(label1)
    X.append(x)
    Y.append(y)

  X_train,X_test,Y_train,Y_test=train_test_split(X, Y, train_size=0.8, random_state=42)
  trainer=pycrfsuite.Trainer(algorithm='pa',verbose=True)
  trainer.set_params({'max_iterations':10})
  for feats,labels in zip(X_train,Y_train):
    trainer.append(feats,[str(e) for e in labels])
  trainer.train(sys.argv[1]+'.main.crfsuite')
  tagger=pycrfsuite.Tagger()
  tagger.open(sys.argv[1]+'.main.crfsuite')
  Y_test_pred=[]
  for instance in X_test:
    pred=tagger.tag(instance)
    enforce_constraints(pred)  
    Y_test_pred.extend(pred)
  Y_test_true=[]
  for instance in Y_test:
    Y_test_true.extend(instance)
  print classification_report(Y_test_true,Y_test_pred)
  print confusion_matrix(Y_test_true,Y_test_pred)

  for feats,labels in zip(X,Y):
    trainer.append(feats,[str(e) for e in labels])
  trainer.train(sys.argv[1]+'.main.crfsuite')
  print 'Model saved in '+sys.argv[1]+'.main.crfsuite'
