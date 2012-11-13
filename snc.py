"""
Author: Yazen Ghannam
CAP 5636
Fall 2012
Semantic Network Creater
"""

import sys, re

if __name__ == '__main__':
    print 'Hello'
    
    file = open(sys.argv[1], 'r')
    #fc = file.read()
    #sentences = str.split(fc, "NEXT-SENTENCE")
    #print str.split(sentences[1], "(********** INTERPRETATION STARTS *************)")[1]
    
    sentences = []
    i = -1
    parsing = False
    for line in file:
        if re.search("NEXT-SENTENCE", line):
            i += 1
            sentences.append("")
            parsing = False
        elif re.search("INTERPRETATION STARTS", line):
            parsing = True
        elif parsing:
            sentences[i] += line.strip("\t\n ")
            
    print list(sentences[0])
    
    #contents = file.read()
    #print len(re.findall('famine', contents))