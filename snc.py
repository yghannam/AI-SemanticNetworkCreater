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
    
def toString(list):
    string = ""
    for x in list:
        if x[0] != 'DT':
            string += x[1] + "_"
    return string.rstrip("01234567890_ ")
        
def parsePrep(list):
    if len(list[2]) > 3:
        return list[1] + " " + toString(list[2][1]) + " " + parsePrep(list[2][3])
    else:
        return list[1] + " " + toString(list[2][1])

def answer(first, second, third):

    if first == '?' and second == '?' and third == '?':
        for role in data:
            if role == 'INANIMATE-CAUSE':
                for verb in data[role]:
                        for theme in data[role][verb]:
                            print "FAMINE", verb, theme        
            else:
                for verb in data[role]:
                        for theme in data[role][verb]:
                            print theme, verb, "FAMINE"                                                        

    if first == 'FAMINE' and second == '?' and third == '?':
        for role in ['INANIMATE-CAUSE']:
            for verb in data[role]:
                    for theme in data[role][verb]:
                        print first, verb, theme
                        
    if first == 'FAMINE' and second != '?' and third == '?':
        for role in ['INANIMATE-CAUSE']:
            for verb in data[role]:
                if second == verb:
                    for theme in data[role][verb]:
                        print first, second, theme                

    if first == 'FAMINE' and second == '?' and third != '?':
        for role in ['INANIMATE-CAUSE']:
            for verb in data[role]:
                    for theme in data[role][verb]:
                        if third == theme:
                            print first, verb, theme                     

    if first == '?' and second == '?' and third == 'FAMINE':
        for role in ['THEME', 'EXPERIENCE']:
            for verb in data[role]:
                    for theme in data[role][verb]:
                        print theme, verb, 'FAMINE'
                        
    if first == '?' and second != '?' and third == 'FAMINE':
        for role in ['THEME', 'EXPERIENCE']:
            for verb in data[role]:
                if second == verb:
                    for theme in data[role][verb]:
                        print theme, verb, 'FAMINE'                

    if first != '?' and second == '?' and third == 'FAMINE':
        for role in ['THEME', 'EXPERIENCE']:
            for verb in data[role]:
                    for theme in data[role][verb]:
                        if first == theme:
                            print theme, verb, 'FAMINE'   

    if first != '?' and second != '?' and third != '?':
        exists = False
        if first == 'FAMINE':
            for verb in data['INANIMATE-CAUSE']:
                if second == verb:
                    for theme in data['INANIMATE-CAUSE'][verb]:
                        if third == theme:
                            exists = True
        else:
            for role in ['THEME', 'EXPERIENCE']:
                for verb in data[role]:
                        if second == verb:
                            for theme in data[role][verb]:
                                if first == theme:
                                    exists = True
        if(exists):
            print "True"
        else:
            print "False"
        
def prompt():
    input = raw_input("Please enter command: ")
    if input == 'quit':
        return 0
    parameters = input.split(' ')
    answer(parameters[0].upper(), parameters[1].upper(), parameters[2].upper())
    print
    return 1

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
    
    data = {"INANIMATE-CAUSE":{}, "THEME":{}, "EXPERIENCE":{}}
    
    count = 0
    ierr = 0
    terr = 0
    perr = 0
    for sentence in sentences:
        try:
            parse = sexp.parseString(sentence).asList()
            semantic_role = findListLevels(3, parse, 'FAMINE1')[3][0]
            

            if semantic_role == 'INANIMATE-CAUSE':
                verb = findListLevels(1, parse, 'MAIN-VERB')[1]
                if verb not in data[semantic_role]:
                    data[semantic_role] .update({verb:[]})
                 
                other = toString(findListLevels(2, parse, 'THEME')[1])          
                if other not in data[semantic_role][verb]:
                    data[semantic_role][verb].append(other)                  
                
                senses = findListLevels(2, parse, 'THEME')[2][0]
                for x in senses:
                    x = x.rstrip("0123456789 ")
                    if x not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(x)             

            if semantic_role == "EXPERIENCE":
                verb = findListLevels(1, parse, 'MAIN-VERB')[1]
                if verb not in data[semantic_role]:
                    data[semantic_role] .update({verb:[]})
                
                other = toString(findListLevels(2, parse, 'EXPERIENCER')[1])      
                if other not in data[semantic_role][verb]:
                    data[semantic_role][verb].append(other)                  
                
                senses = findListLevels(2, parse, 'EXPERIENCER')[2][0]
                for x in senses:
                    x = x.rstrip("0123456789 ")
                    if x not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(x)        
                        
            if semantic_role == "THEME":
                #print findListLevels(1, parse, 'VERB')
                verb = findListLevels(1, parse, 'MAIN-VERB')[1]
                if verb not in data[semantic_role]:
                    data[semantic_role] .update({verb:[]})              
           
                otherList = findListLevels(2, parse, 'INANIMATE-CAUSE')
                if otherList != -1:                    
                    if len(otherList) > 4:
                        other = toString(otherList[1]) + " " + parsePrep(otherList[4])
                    else:
                        other = toString(otherList[1])
                    if other not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(other)                  
                
                else:
                    otherList = findListLevels(2, parse, 'AGENT')
                    if len(otherList) > 4:
                        other = toString(otherList[1]) + " " + parsePrep(otherList[4])
                    else:
                        other = toString(otherList[1])
                    if other not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(other)  
                """
                senses = findListLevels(2, parse, 'AGENT')[2][0]
                for x in senses:
                    x = x.rstrip("0123456789 ")
                    if x not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(x)                                  
                """
            count += 1                        
        except IndexError:
            ierr += 1
            pass
            """
            parse = sexp.parseString(sentence).asList()
            #print parse
            semantic_role = findListLevels(4, parse, 'FAMINE1')
            print sentence
            print
            print semantic_role
            print
            pass
            """
        except TypeError:
            terr += 1
            pass
        except ParseException:
            perr += 1
            pass
            #print "Could not parse: "
            #print sentence
            #print
        #print sentence
    #print data
    print ierr, "index errors"
    print terr, "type errors"
    print perr, "parse errors"
    print count, "out of", len(sentences), "sentences parsed\n"
    p = 0
    while p == 1:
        p = prompt()