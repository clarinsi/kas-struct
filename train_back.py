#!/usr/bin/python
#-*-encoding:utf-8-*-
import sys
import pickle
import numpy as np
import pycrfsuite
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from collections import Counter
from train_main import extract

X=[]
Y=[]
for file in open(sys.argv[1]):
  x=[]
  y=[]
  for line in open('docs/'+file.strip()+'.pages'):
    text,label1,label2=line.rstrip().split('\t')
    if label1=='BACK':
      x.append(extract(text.split(' ')))
      y.append(label2)
  X.append(x)
  Y.append(y)

X_train,X_test,Y_train,Y_test=train_test_split(X, Y, train_size=0.8, random_state=42)
trainer=pycrfsuite.Trainer(algorithm='pa',verbose=True)
trainer.set_params({'max_iterations':10})
for feats,labels in zip(X_train,Y_train):
  trainer.append(feats,[str(e) for e in labels])
trainer.train(sys.argv[1]+'.back.crfsuite')
tagger=pycrfsuite.Tagger()
tagger.open(sys.argv[1]+'.back.crfsuite')
Y_test_pred=[]

for instance in X_test:
  pred=tagger.tag(instance)
  Y_test_pred.extend(pred)
Y_test_true=[]
for instance in Y_test:
  Y_test_true.extend(instance)
print classification_report(Y_test_true,Y_test_pred)
print confusion_matrix(Y_test_true,Y_test_pred)

for feats,labels in zip(X,Y):
  trainer.append(feats,[str(e) for e in labels])
trainer.train(sys.argv[1]+'.back.crfsuite')
print 'Model saved in '+sys.argv[1]+'.back.crfsuite'
