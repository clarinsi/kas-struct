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

The three example runs of the ```kas-structure.py``` script is the following:

```
$ python kas-structure.py dipl examples/kas-8395397.pages
$ python kas-structure.py mag examples/kas-8395574.pages
$ python kas-structure.py dr examples/kas-7977468.pages
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

       BACK       0.93      0.97      0.95       304
       BODY       1.00      0.99      0.99      2255
      FRONT       0.99      0.99      0.99       328

avg / total       0.99      0.99      0.99      2887

[[ 296    8    0]
 [  24 2229    2]
 [   0    3  325]]
...
```

### Master theses

```
$ python train_main.py train.mag
...
             precision    recall  f1-score   support

       BACK       0.98      0.69      0.81       647
       BODY       0.94      1.00      0.97      3535
      FRONT       1.00      0.95      0.97       432

avg / total       0.95      0.95      0.95      4614

[[ 445  202    0]
 [   8 3526    1]
 [   0   22  410]]
...
```

### PhD theses

```
$ python train_main.py train.dr
...
             precision    recall  f1-score   support

       BACK       0.99      0.65      0.79      1732
       BODY       0.91      1.00      0.95      6626
      FRONT       0.98      0.94      0.96       555

avg / total       0.93      0.93      0.92      8913

[[1130  602    0]
 [  12 6604   10]
 [   0   33  522]]
...
```

### All theses

```
$ python train_main.py train.all
...
             precision    recall  f1-score   support

       BACK       0.98      0.73      0.84      2637
       BODY       0.94      1.00      0.97     12392
      FRONT       1.00      0.96      0.98      1434

avg / total       0.95      0.95      0.95     16463

[[ 1924   713     0]
 [   43 12349     0]
 [    0    51  1383]]
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

     Abs-en       0.88      0.91      0.89        23
     Abs-se       0.89      0.62      0.73        13
     Abs-sl       0.79      0.83      0.81        23
       Dict       0.00      0.00      0.00         1
          O       0.92      0.98      0.95       168
        Tnx       0.96      0.93      0.94        27
        ToC       0.97      0.88      0.92        73

avg / total       0.92      0.92      0.92       328

[[ 21   0   1   0   0   0   1]
 [  2   8   2   0   1   0   0]
 [  1   0  19   0   3   0   0]
 [  0   0   0   0   1   0   0]
 [  0   0   1   0 165   1   1]
 [  0   0   1   0   1  25   0]
 [  0   1   0   0   8   0  64]]
...
```

### Master theses

```
$ python train_front.py train.mag
...
             precision    recall  f1-score   support

     Abs-en       0.91      0.86      0.89        37
     Abs-se       0.50      0.38      0.43         8
     Abs-sl       0.71      0.84      0.77        38
          O       0.92      0.88      0.90       240
        Tnx       0.84      0.81      0.83        32
        ToC       0.77      0.86      0.81        77

avg / total       0.86      0.85      0.85       432

[[ 32   1   2   1   0   1]
 [  0   3   1   2   1   1]
 [  1   0  32   3   0   2]
 [  1   2   8 210   4  15]
 [  0   0   1   4  26   1]
 [  1   0   1   9   0  66]]
...
```

### PhD theses

```
$ python train_front.py train.dr
...
     Abs-en       0.90      0.92      0.91        72
     Abs-se       0.00      0.00      0.00         4
     Abs-sl       0.77      0.90      0.83        67
         CV       0.00      0.00      0.00         1
       Dict       0.00      0.00      0.00         5
          O       0.91      0.90      0.90       267
        Tnx       0.80      0.80      0.80        25
        ToC       0.85      0.85      0.85       114

avg / total       0.86      0.87      0.86       555

[[ 66   0   1   0   0   2   2   1]
 [  1   0   0   0   1   1   0   1]
 [  3   0  60   0   0   3   0   1]
 [  0   0   1   0   0   0   0   0]
 [  0   0   0   0   0   5   0   0]
 [  2   0  11   0   0 239   3  12]
 [  0   0   3   0   0   0  20   2]
 [  1   0   2   0   0  14   0  97]]
...
```

### All theses

```
$ python train_front.py train.all
...
             precision    recall  f1-score   support

     Abs-en       0.84      0.89      0.86       127
     Abs-se       0.94      0.75      0.83        20
     Abs-sl       0.85      0.88      0.86       130
       Dict       0.00      0.00      0.00        10
          O       0.92      0.94      0.93       788
        Tnx       0.91      0.86      0.89        81
        ToC       0.89      0.85      0.87       278

avg / total       0.89      0.90      0.90      1434

[[113   0   2   0   4   2   6]
 [  1  15   0   0   2   0   2]
 [  8   0 114   0   7   0   1]
 [  0   0   0   0  10   0   0]
 [ 11   1  10   1 740   4  21]
 [  1   0   4   0   6  70   0]
 [  1   0   4   0  36   1 236]]
...
```

On this level of processing it seems most reasonable to use a single model as it (1) covers all possible classes and (2) performs best.

## Training discriminators between fine categories in the BACK

### Diploma theses

```
$ python train_back.py train.dipl
...
             precision    recall  f1-score   support

     Abs-en       0.60      0.60      0.60         5
     Abs-sl       0.67      0.40      0.50         5
       Bibl       0.91      0.97      0.94       133
         CV       0.00      0.00      0.00         2
       Dict       0.00      0.00      0.00         1
          O       0.95      0.93      0.94       153
        Tnx       1.00      0.80      0.89         5

avg / total       0.91      0.92      0.91       304

[[  3   1   1   0   0   0   0]
 [  2   2   0   0   0   1   0]
 [  0   0 129   0   0   4   0]
 [  0   0   1   0   0   1   0]
 [  0   0   0   0   0   1   0]
 [  0   0  11   0   0 142   0]
 [  0   0   0   0   0   1   4]]
...
```

### Master theses

```
$ python train_back.py train.mag
...
             precision    recall  f1-score   support

     Abs-en       0.83      0.71      0.77         7
     Abs-sl       0.00      0.00      0.00         5
       Bibl       0.91      0.95      0.93       231
         CV       0.00      0.00      0.00         3
          O       0.96      0.95      0.95       399
        Tnx       0.67      1.00      0.80         2

avg / total       0.93      0.94      0.93       647

[[  5   0   2   0   0   0]
 [  1   0   0   0   4   0]
 [  0   0 220   0  11   0]
 [  0   0   1   0   2   0]
 [  0   0  19   0 379   1]
 [  0   0   0   0   0   2]]
...
```

### PhD theses

```
$ python train_back.py train.dr
...
             precision    recall  f1-score   support

     Abs-en       1.00      0.73      0.84        33
     Abs-sl       0.95      1.00      0.97        18
       Bibl       0.98      0.97      0.98       634
         CV       0.84      0.75      0.79        36
       Dict       0.67      0.33      0.44         6
          O       0.97      0.98      0.98       996
        Tnx       1.00      1.00      1.00         9

avg / total       0.97      0.97      0.97      1732

[[ 24   1   0   0   0   8   0]
 [  0  18   0   0   0   0   0]
 [  0   0 618   1   0  15   0]
 [  0   0   1  27   1   7   0]
 [  0   0   0   0   2   4   0]
 [  0   0  11   4   0 981   0]
 [  0   0   0   0   0   0   9]]
...
```

### All theses

```
$ python train_back.py train.all
...
             precision    recall  f1-score   support

     Abs-en       0.98      0.94      0.96        66
     Abs-sl       0.92      0.81      0.86        43
       Bibl       0.94      0.96      0.95       995
         CV       0.52      0.69      0.60        36
       Dict       0.00      0.00      0.00        14
          O       0.95      0.94      0.95      1464
        Tnx       1.00      1.00      1.00        19

avg / total       0.94      0.94      0.94      2637

[[  62    1    3    0    0    0    0]
 [   1   35    0    0    0    7    0]
 [   0    0  955    1    0   39    0]
 [   0    0    5   25    0    6    0]
 [   0    0    0    0    0   14    0]
 [   0    2   58   22    2 1380    0]
 [   0    0    0    0    0    0   19]]
...
```

Similar as with the annotator of the front, on the level of processing the back, although the dedicated models for master and doctoral theses have better results as they deal with a smaller number of classes, it seems most reasonable to use a single model as it (1) covers all possible classes and (2) has good performance.
