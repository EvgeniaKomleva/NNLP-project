from tqdm import tqdm
import nltk
import os
import xml.etree.ElementTree as ET
import re

path = "Number Normalization/rdf_unregular_eng/train"

files = os.listdir(path)
f = open("dataset/train.txt", "a")
markup_data = set()


for file in tqdm(files):
    tree = ET.parse(f"{path}/{file}")
    root = tree.getroot()

    text = root[-1][0].text
    sents = nltk.tokenize.sent_tokenize(text)
    inp = ''
    sents = nltk.tokenize.sent_tokenize(text)
    #print(len(root))
    for i in range(len(root)-2):
        data = ''
        text = root[-1][0].text
        for be in root[i]:
            print(be.text)
            print(be.tag[38:])

            data = data+" "+be.text
        for s in sents:
            try:
                if re.search(be.text, s) != None:
                    print(be.text)
                    text = s
            except:
                print("ERR")
            #else:

                #text = root[-1][0].text
        data = data+  " : "+ text
        print(data)
        f.write(data)
        f.write("\n")
        print("______")

