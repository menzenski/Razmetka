# Razmetka

This repository contains a Python utility for training and testing
part-of-speech taggers from a provided training file.

## Training Files

This package assumes a training file structured according to the following
rules:

* Each line contains one sentence (i.e., sentences are separated by the
    newline character `\n`)
* Each sentence is white-space delimited---a space should precede every
    punctuation mark.
* Each token in each sentence consists of three parts: the word/punctuation
    mark itself, the separator character, and the associated tag. For example,
    here's a breakdown of a token `Men_PN1s`:
  * `Men` -- the word as it would appear in an untagged sentence.
  * `_` -- the separator character (the underbar `_` is the default, but
      other separators may be specified. The slash `/` is also common).
  * `PN1s` -- the (part-of-speech) tag, here indicating a first-person singular
      pronoun.
* UTF-8 is the default encoding, but other encodings may be specified.

```
Men_PN1s besh_NU minut_N usul_N oynidim_Vt-PST.dir-1s1 ._PUNCT
Sen_PN2si poluni_N-ACC yéding_Vt-PST.dir-2si2 dédi_Vt-PST.dir-3s2 Tursun_Npr ._PUNCT
Xinjiangda_Ntop-LOC turghan_Vi-REL.PST méning_PN1s.GEN ayalim_N-POSS1s qaytip_Vi-CNV keldi_Vdirc-PST.dir-3s2 ._PUNCT
```

## Provided Files

This repository includes a sample file, `uyghurtagger.train`, structured
according to the standards described above. The Uyghur sentences in this
file are taken from the public online corpus of the
[**Uyghur Light Verbs Project**](https://uyghur.ittc.ku.edu/uylvs.html)
(PI Arienne M. Dwyer, NSF BCS-1053152).

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

Repeat the entire ten-fold cross-validation process multiple times:

```Python
import taggertester
taggertester.repeat_tagger_tests(fname='uyghurtagger.train',
                                 number_of_tests=3, language='Uyghur')
```

## Requirements

The `Razmetka` package requires NLTK 3.0+.

## Support
This Python package is being written to support the work of the **Annotating
Turki Manuscripts Online** project (Principal Investigators: Arienne M. Dwyer
and C.M. Sperberg-McQueen), sponsored by the
[Luce Foundation](http://www.hluce.org). The support of the Luce Foundation
is gratefully acknowledged.
