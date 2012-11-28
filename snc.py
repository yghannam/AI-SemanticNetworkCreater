"""
Author: Yazen Ghannam
CAP 5636
Fall 2012
Semantic Network Creater
"""

import sys, re
from pyparsing import *


def findList(inList, item):
    if item in inList:
        return inList
    else:
        for x in inList:
            if isinstance(x, list):
                result = findList(x, item)
                if result != -1:
                    return result
                
    return -1
    
def findListLevels( levels, inList, item):
    result = item
    for x in range(levels):
        result = findList(inList, result)
    
    return result

if __name__ == '__main__':
    print 'Hello\n'
    
    file = open(sys.argv[1], 'r')
    
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
    
    #parse = sexp.parseString( sentences[1] )
    #print parse
    #t = {'test':[1, 2, 3, [5]]}
    #t['test'].append(5)
    #print t['test']
    #parse.dump(indent='True', depth=5)
    #findWord(parse.asList(), 'FAMINE1')
    
    for sentence in sentences:
        try:
            parse = sexp.parseString(sentence).asList()
            semantic_role = findListLevels(3, parse, 'FAMINE1')[3][0]
            if semantic_role == 'INANIMATE-CAUSE':
                verb = findListLevels(1, parse, 'MAIN-VERB')[1]
                theme = findListLevels(2, parse, 'THEME')[2][0][0]
                print "FAMINE " + verb + " " + theme
        except IndexError:
            pass
        except TypeError:
            pass
        except ParseException:
            pass
            #print "Could not parse: "
            #print sentence
            #print
        #print sentence
        #print
    
    #contents = file.read()
    #print len(re.findall('famine', contents))