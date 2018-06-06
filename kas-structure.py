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
from train_main import extract,enforce_constraints
import os
reldir=os.path.dirname(os.path.abspath(__file__))

models={'dipl':['train.all.main.crfsuite','train.all.front.crfsuite','train.all.back.crfsuite'],'mag':['train.all.main.crfsuite','train.all.front.crfsuite','train.all.back.crfsuite'],'dr':['train.all.main.crfsuite','train.all.front.crfsuite','train.all.back.crfsuite']}

tagger=pycrfsuite.Tagger()
tagger.open(os.path.join(reldir,models[sys.argv[1]][0]))

x=[]
for line in open(sys.argv[2]):
  page=line.strip().split(' ')
  x.append(extract(page))
#for i in range(10):
#  print i
#  print x[i]
#  print '###'
print 'Data read'
pred_main=tagger.tag(x)
enforce_constraints(pred_main)
print 'Main tagged'

front=[]
back=[]
for idx,pred in enumerate(pred_main):
  if pred=='FRONT':
    front.append(x[idx])
  elif pred=='BACK':
    back.append(x[idx])

tagger=pycrfsuite.Tagger()
tagger.open(os.path.join(reldir,models[sys.argv[1]][1]))
pred_front=tagger.tag(front)
print 'Front tagged'

tagger=pycrfsuite.Tagger()
tagger.open(os.path.join(reldir,models[sys.argv[1]][2]))
pred_back=tagger.tag(back)
print 'Back tagged'
f=open(sys.argv[2]+'.anno','w')
front_idx=0
back_idx=0
for tag in pred_main:
  tag2='O'
  if tag=='FRONT':
    tag2=pred_front[front_idx]
    front_idx+=1
  elif tag=='BACK':
    tag2=pred_back[back_idx]
    back_idx+=1
  f.write(tag+'\t'+tag2+'\n')
f.close()
