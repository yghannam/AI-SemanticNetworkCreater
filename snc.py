"""
Author: Yazen Ghannam
CAP 5636
Fall 2012
Semantic Network Creater
"""

import sys, re
from pyparsing import *

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
            
    """        
    fileOut = open("famine.out", 'w')
    for x in sentences:
        fileOut.write(x)
        fileOut.write("\n\n")
    fileOut.close()    
    #print sentences[0]
    """
    
    
    # define grammar
    # define punctuation literals
    LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR = map(Suppress, "()[]{}|")
    
    sexp = Forward()
    sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
    sexp << ( Word(alphanums+"-_*/") | sexpList )

    """
    gElement = "(" + Word( alphanums ) + ")"
    gPhrase = "(" + Word( alphanums ) + ZeroOrMore( gPhrase ) + ")"
    gDT = "(DT" + Word(alphanums) + ")"
    gADJ = "(ADJ" + Word(alphanums) + ")"
    gNOUN = "(NOUN" + Word(alphanums) + ")"
    gNP = "(" + ZeroOrMore(gDT) + ZeroOrMore(gADJ) + ZeroOrMore(gNOUN) + ")"
    gSemanticRole = "(" + "THEME" + ")"
    gSense = "(" + OneOrMore(gElement) + ")"
    #gPrep = "(PREP" + 
    gSubj = "(SUBJ" + gNP + gSense + gSemanticRole + gPrep + ")"
    gSentence = "(" + Word(alphanums) + OneOrMore( gElement ) +")"
    """
    print sexp.parseString( sentences[0] )
    
    #contents = file.read()
    #print len(re.findall('famine', contents))