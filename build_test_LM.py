#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
import re
import nltk
import sys
import getopt
import math

LANGUAGES = ["malaysian", "tamil", "indonesian"]

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print("building language models...")
    
    #storage
    model_table = {}
    language_counter = {l:0 for l in LANGUAGES} 

    #working with the file
    with open(in_file, "r") as file:
        for line in file:
            language,text = line.strip().split(' ',1)
            language_counter[language] += 1

            #fix fourgram computation
            fourgram = [text[i: i+4] for i in range(len(text) - 5)]
            for gram in fourgram:
                if not gram in model_table:
                    model_table[gram] = {lang:1 for lang in LANGUAGES}
                    for lang in LANGUAGES:
                        model_table[gram][lang] = 1
                        language_counter[lang]+=1
                
                model_table[gram][language] += 1
                language_counter[language] +=1

    #generate the probabilities
    for gram, table in model_table.items():
        for language, num in table.items():
            table[language] = num / language_counter[language]
  
    #sum_of_language_values = sum(language_p.values())
    #P_L = {l: language_p[l] / sum_of_language_values for l in LANGUAGES}
    return model_table


def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    #extract
    model_table = LM 

    with open(in_file, "r") as r_file, open(out_file, "w") as out:
        for line in r_file:
            P_L = {language: 0 for language in LANGUAGES}
            n_missing = 0 #shld count missing values 

            fourgram = [line[i: i+4] for i in range(len(line) - 5)] 
            for each in fourgram:
                if not each in model_table:
                    n_missing += 1
                    continue
                for language in LANGUAGES:
                    P_L[language] += math.log(model_table[each][language])
            
            
            #argmax
            missing_prop = n_missing/float(len(fourgram))
            if missing_prop > 0.6:
                most_probable_language = "unknown"
            else:
                most_probable_language = max(P_L, key=P_L.get)
            out.write(f"{most_probable_language} {line}")


def usage():
    print(
        "usage: "
        + sys.argv[0]
        + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"
    )


input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "b:t:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-b":
        input_file_b = a
    elif o == "-t":
        input_file_t = a
    elif o == "-o":
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
