# tagger-tester

This repository contains a Python utility for training and testing
part-of-speech taggers from a provided training file.

## Usage

Train a Brill tagger on a provided training file:

```Python
import taggertester
btt = taggertester.TTBrillTaggerTrainer(file_name='uyghurtagger.train',
                                        language='Uyghur')
btt.train(verbose=True)
```

Train and test Stanford log-linear taggers from a provided training file
using ten-fold cross-validation:

```Python
import taggertester
tst = taggertester.TaggerTester(file_name='uyghurtagger.train',
                                language='Uyghur')
tst.split_groups()
tst.estimate_tagger_accuracy()
tst.print_results()
```

## Requirements

The `tagger-tester` package requires NLTK 3.0+.

## Support
This Python package is being written to support the work of the **Annotating
Turki Manuscripts Online** project (Principal Investigators: Arienne M. Dwyer
and C.M. Sperberg-McQueen), sponsored by the
[Luce Foundation](http://www.hluce.org). The support of the Luce Foundation
is gratefully acknowledged.
