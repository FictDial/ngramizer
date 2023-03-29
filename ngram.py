#!/usr/bin/python
import sys
import re
import csv

nodict = False
test = False
testdirsize = 1000000
logtitle = ">>>"

def build_dict(xgram):
  dict = {}
  if (nodict == True):
    return dict
  name = "unigram" if xgram == 1 else "bigram" if xgram == 2 else "trigram"
  print(f"Building {name.capitalize()} Dictionary", end="", flush=True)
  with open(ngram_dir + f"ngram{xgram}-1.frk", encoding="ansi", mode="r") as f:
    lines = f.readlines()
    for line in lines:
      elements = line.strip().split(" ",1)
      try:
        key = elements[1]
      except IndexError:
        continue
      dict[key] = elements[0]
      if (len(dict) % 500000 == 0):
        print(".", end="", flush=True)
      if (test & (len(dict) == testdirsize)):
        break
    print("\nDictionary built with", f"{len(dict):,}", name + "s.")
    f.close()
    return dict

if __name__ == "__main__":
  ver = "0.1"
  print("nGramIzer (nGI) v" + ver)
  print("Using Python " + sys.version + "\n")


  def error_exit(error):
    print("(nGI Error): " + error)
    sys.exit()

  if sys.version_info[0] < 3:
    error_exit("Must be using Python 3. Try py -3!")
  
  inputfiles = sys.argv[1:]
  
  try:
    inputfiles[0]
  except BaseException:
    error_exit("Specify at least one input file in the arguments.")

  print(f"{logtitle} Checking Files.")
  for index, inputfile in enumerate(inputfiles):
    outputfile = inputfile + "_result.csv"
    try:
      f = open(inputfile, 'r')
    except BaseException:
      error_exit('Cannot open input file for reading: ' + inputfile)
    else:
      print(f"Input file  {index}: {inputfile}")
      f.close()
    try:
      f = open(outputfile, 'w')
    except BaseException:
      error_exit('Cannot open output file for writing: ' + outputfile + ' (Maybe open?)')
    else:
      print(f"Output file {index}: {outputfile}")
      f.close()

  print(f"\n{logtitle} Building Dictionaries.", flush=True)

  ngram_dir = "bokm/"
  unigrams = build_dict(1)
  bigrams = build_dict(2)
  trigrams = build_dict(3)
  print("Dictionaries Ready.")
  
  for inputfile in inputfiles:
    outputfile = inputfile + "_result.csv"
    sentences = []
    with open(inputfile, 'r', encoding='utf-8') as inputf:
      with open(outputfile, 'w', encoding='utf-8',  newline='') as outputf:

        print(f"\n{logtitle} Analyizing {inputfile}...")
        
        text = inputf.read()
        # Split the text into sentences
        sentence_regex = r"[A-ZÆØÅ][^\.!?]*[\.!?]"
        sentences_raw = re.findall(sentence_regex, text)
        
        results = [['Sentence Number', 'Word Number', 'Word', 'Forward Probability', 'Backward Probability']]
        ngram_count = 0
    
        # Tokenize the sentences
        for sentence_number, sentence_raw in enumerate(sentences_raw):
          sentence = ("<s> " + re.sub('(?<! )(?=[.,!?()])|(?<=[.,!?()])(?! )', r' ', sentence_raw)).strip().split()
          for word_number, word in enumerate(sentence):
            # Check that we have at least two previous words for the 3-gram
            if word_number >= 2:
              word1 = sentence[word_number - 2].lower()
              word2 = sentence[word_number - 1].lower()
              word3 = sentence[word_number].lower()
              
              trigram = " ".join([word1, word2, word3])
              bigram = " ".join([word1, word2])
              unigram = word3
                          
              forward_probability = '{0:.16f}'.format(int(trigrams[trigram]) / int(bigrams[bigram])) if (trigram in trigrams) & (bigram in bigrams) else "NA"
              backward_probability = '{0:.16f}'.format(int(trigrams[trigram]) / int(unigrams[unigram])) if (trigram in trigrams) & (unigram in unigrams) else "NA"
              results.append([sentence_number + 1, word_number, word, forward_probability, backward_probability])
              ngram_count = ngram_count + 1

        print(f"{len(sentences_raw)} sentences and {ngram_count} ngrams analyized.")
        # Write the results to a CSV file
        writer = csv.writer(outputf)
        writer.writerows(results)
        print(f"File written: {outputfile}.")
        f.close()
