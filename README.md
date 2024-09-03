# nGramIzer
created by Károly Füzessi and Lilla Magyari

This program calculates the forward conditional probability and backward conditional probability of Norwegian Bokmål words in sentences in a text file. The probability calculation is based the formulae in [Onnis et al. (2022)](https://onlinelibrary.wiley.com/doi/full/10.1111/cogs.13201) and uses data from the n-gram database from the National Library of Norway.

## Prerequisites

### Database of N-grams in Norwegian Bokmål

1. Download the [Norwegian Bokmål n-gram database from the National Library of Norway](https://www.nb.no/sbfil/tekst/ngram_nob.tar.gz) to the project directory.
2. Decompress the archive, e.g. by opening a command line and issuing the command: `tar xf ngram_nob.tar.gz`

You should have a `bokm` folder in the project directory after some minutes.

### Python

[Download Python 3.x](https://www.python.org/downloads/)

## Run

Run the nGramIzer on any number of text files with the command

```
py -3 ngram.py input_file [input_file_2]...
```

Output files will be generated with a `_result.csv` postfix.

Note: building the dictionaries takes some time before the actual analysis runs.

### Output format

The generated CSV will contain the following columns:

- Sentence Number
- Word Number
- Word
- Forward Probability
- Backward Probability

### Funding statement
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No. 845343.
Project's website: https://www.uis.no/nb/lesesenteret/fictdial
