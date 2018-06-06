# kas-structure

This repository contains a tool for document structure prediction for diploma, master and doctoral theses, developed inside the KAS project (http://nl.ijs.si/kas/english). The scientific publications the models were trained on are in Slovene, therefore the final models work primarily for Slovene.

We frame the structure prediction task as a sequence prediction task, with instances of sequences being single pages.

While the ```train_*.py``` scripts evaluate the defined setup by splitting the training data in a 80:20 fashion, finally outputing a model trained on the whole dataset, the script ```kas-structure.py``` applies the trained models on documents encoded in a one-page-per-line format. Example files are available in the ```examples/``` directory.

## Dependencies

For running the code in this repository you need the following:
- python-crfsuite 0.12.2 (for building the model)
- sklearn 0.18.1 (for splitting the data and evaluation)
- python 2.7

## Running the tool with pre-trained models

The documents to be annotated are supposed to be prepared in the following manner: content of each page encoded in one line, with tokens separated with spaces. The output of the tool are labels on the coarse-grained level (FRONT, BODY, BACK) and fine-grained level (among the FRONT and BACK pages). The labels are written in a file with the ```.anno``` extension.

An example run of the ```kas-structure.py``` script is the following:

```
python kas-structure.py mag examples/kas-22502.pages
```

While the first argument defines the type of document to be annotated (```dipl```, ```mag``` or ```dr```), the second argument is the path to the properly prepared file. The output of the tool is written to the path ```python kas-structure.py mag examples/kas-22502.pages.anno```.

## Training discriminators between front, body and back

For running the experiment and training the final model for discriminating between the three main parts of each scientific work you can run the ```train_main.py``` script, giving it as the argument one of the four possible lists of training instances:

- train.dipl - a list of diploma theses
- train.mag - a list of master theses
- train.dr - a list of PhD theses
- train.all - a list of all theses

The specifics of this process, in comparison to the later two, is that structural integrity is enforced, each document starting with FRONT and having two transitions, first to BODY, then to BACK.

Below we present the results of each of the above setups (training and evaluating on each type of academic work, or on all together).

### Diploma theses

```
$ python train_main.py train.dipl
...
             precision    recall  f1-score   support

       BACK       0.98      0.75      0.85       110
       BODY       0.97      1.00      0.98      1125
      FRONT       1.00      0.97      0.98       166

avg / total       0.98      0.98      0.97      1401

[[  82   28    0]
 [   2 1123    0]
 [   0    5  161]]
...
```

### Master theses

```
$ python train_main.py train.mag
...
             precision    recall  f1-score   support

       BACK       0.99      0.80      0.89       347
       BODY       0.95      1.00      0.98      1744
      FRONT       1.00      0.93      0.96       204

avg / total       0.96      0.96      0.96      2295

[[ 278   69    0]
 [   2 1742    0]
 [   0   15  189]]
...
```

### PhD theses

```
$ python train_main.py train.dr
...
             precision    recall  f1-score   support

       BACK       0.96      0.87      0.92       645
       BODY       0.97      0.99      0.98      3404
      FRONT       1.00      0.90      0.95       294

avg / total       0.97      0.97      0.97      4343

[[ 562   83    0]
 [  21 3383    0]
 [   0   28  266]]
...
```

### All theses

```
$ python train_main.py train.all
...
             precision    recall  f1-score   support

       BACK       0.97      0.87      0.92      1501
       BODY       0.96      0.99      0.98      6031
      FRONT       1.00      0.96      0.98       704

avg / total       0.97      0.97      0.97      8236

[[1304  197    0]
 [  39 5992    0]
 [   0   31  673]]
...
```

Given the presented results, it seems that using a single model for all types of theses makes most sense.

## Training discriminators between fine categories in the FRONT

We again run similar experiments as with the main experiment, using various types of theses for training and testing. The features used in this process are identical to the previous, main process, with the difference that no structure is enforced.

### Diploma theses

```
$ python train_front.py train.dipl
...
             precision    recall  f1-score   support

     Abs-en       0.86      0.80      0.83        15
     Abs-sl       0.60      0.75      0.67         8
       Dict       0.00      0.00      0.00         1
          O       0.92      0.96      0.94        94
        Tnx       0.80      0.80      0.80        10
        ToC       0.97      0.87      0.92        38

avg / total       0.90      0.90      0.90       166

[[12  1  0  1  0  1]
 [ 2  6  0  0  0  0]
 [ 0  0  0  1  0  0]
 [ 0  2  0 90  2  0]
 [ 0  1  0  1  8  0]
 [ 0  0  0  5  0 33]]
...
```

### Master theses

```
$ python train_front.py train.mag
...
             precision    recall  f1-score   support

     Abs-en       0.92      0.96      0.94        23
     Abs-sl       0.85      0.77      0.81        22
          O       0.89      0.92      0.91       101
        Tnx       0.88      0.93      0.90        15
        ToC       0.93      0.86      0.89        43

avg / total       0.90      0.90      0.90       204

[[22  0  1  0  0]
 [ 0 17  4  1  0]
 [ 2  3 93  0  3]
 [ 0  0  1 14  0]
 [ 0  0  5  1 37]]
...
```

### PhD theses

```
$ python train_front.py train.dr
...
             precision    recall  f1-score   support

     Abs-en       0.81      0.86      0.83        35
     Abs-sl       0.76      0.83      0.79        35
       Dict       0.00      0.00      0.00         2
          O       0.93      0.92      0.93       155
        Tnx       0.83      0.77      0.80        13
        ToC       0.84      0.85      0.84        54

avg / total       0.87      0.87      0.87       294

[[ 30   0   0   2   1   2]
 [  2  29   0   3   0   1]
 [  0   0   0   2   0   0]
 [  3   3   0 142   1   6]
 [  0   3   0   0  10   0]
 [  2   3   0   3   0  46]]
...
```

### All theses

```
$ python train_front.py train.all
...
             precision    recall  f1-score   support

     Abs-en       0.89      0.94      0.91        67
     Abs-sl       0.90      0.91      0.90        66
   Abs-slen       1.00      0.70      0.82        10
       Dict       0.00      0.00      0.00         7
          O       0.93      0.95      0.94       379
        Tnx       0.87      0.89      0.88        38
        ToC       0.94      0.93      0.93       137

avg / total       0.91      0.92      0.92       704

[[ 63   0   0   0   3   0   1]
 [  3  60   0   0   3   0   0]
 [  1   1   7   0   1   0   0]
 [  0   0   0   0   7   0   0]
 [  4   5   0   0 359   4   7]
 [  0   1   0   0   3  34   0]
 [  0   0   0   0   9   1 127]]
...
```

On this level of processing it seems most reasonable to use a single model as it (1) covers all possible classes and (2) performs best.

## Training discriminators between fine categories in the BACK

### Diploma theses

```
$ python train_back.py train.dipl
...
             precision    recall  f1-score   support

     Abs-en       0.75      0.60      0.67         5
     Abs-sl       0.00      0.00      0.00         5
       Bibl       0.97      1.00      0.98        60
          O       0.81      0.97      0.89        36
        Tnx       1.00      0.25      0.40         4

avg / total       0.86      0.90      0.87       110

[[ 3  0  1  1  0]
 [ 1  0  0  4  0]
 [ 0  0 60  0  0]
 [ 0  0  1 35  0]
 [ 0  0  0  3  1]]
...
```

### Master theses

```
$ python train_back.py train.mag
...
             precision    recall  f1-score   support

     Abs-en       1.00      1.00      1.00         6
     Abs-sl       0.50      1.00      0.67         1
       Bibl       0.96      0.99      0.97       136
         CV       1.00      0.50      0.67         4
          O       0.98      0.96      0.97       199
        Tnx       0.50      1.00      0.67         1

avg / total       0.97      0.97      0.97       347

[[  6   0   0   0   0   0]
 [  0   1   0   0   0   0]
 [  0   0 134   0   2   0]
 [  0   0   0   2   2   0]
 [  0   1   5   0 192   1]
 [  0   0   0   0   0   1]]
...
```

### PhD theses

```
$ python train_back.py train.dr
...
             precision    recall  f1-score   support

     Abs-en       0.98      1.00      0.99        43
     Abs-sl       0.91      1.00      0.95        20
       Bibl       0.97      0.96      0.97       323
         CV       0.89      0.80      0.84        10
       Dict       0.00      0.00      0.00         2
          O       0.94      0.95      0.95       240
        Tnx       1.00      1.00      1.00         7

avg / total       0.96      0.96      0.96       645

[[ 43   0   0   0   0   0   0]
 [  0  20   0   0   0   0   0]
 [  0   0 311   0   0  12   0]
 [  0   0   1   8   0   1   0]
 [  0   0   0   0   0   2   0]
 [  1   2   7   1   0 229   0]
 [  0   0   0   0   0   0   7]]
...
```

### All theses

```
$ python train_back.py train.all
...
             precision    recall  f1-score   support

     Abs-en       0.85      0.91      0.88        32
     Abs-sl       0.92      0.72      0.81        32
   Abs-slen       0.00      0.00      0.00         1
       Bibl       0.95      0.99      0.97       548
         CV       0.24      0.25      0.25        28
       Dict       0.00      0.00      0.00         3
          O       0.97      0.95      0.96       841
        Tnx       1.00      0.94      0.97        16

avg / total       0.94      0.94      0.94      1501

[[ 29   0   0   2   0   0   1   0]
 [  3  23   0   0   0   0   6   0]
 [  1   0   0   0   0   0   0   0]
 [  0   0   0 543   0   0   5   0]
 [  0   0   0   9   7   0  12   0]
 [  0   0   0   0   0   0   3   0]
 [  1   2   0  15  22   0 801   0]
 [  0   0   0   0   0   0   1  15]]
...
```

Similar as with the annotator of the front, on the level of processing the back, although the dedicated models for master and doctoral theses have better results as they deal with a smaller number of classes, it seems most reasonable to use a single model as it (1) covers all possible classes and (2) has good performance.
