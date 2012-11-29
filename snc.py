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
    print list
    if len(list[2]) > 3:
        return list[1] + "_" + toString(list[2][1]) + "_" + parsePrep(list[2][3])
    else:
        return list[1] + "_" + toString(list[2][1])

def answer(first, second, third):

    if first == '?' and second == '?' and third == '?':
        for role in data:
            if role == 'INANIMATE-CAUSE':
                for verb in data[role]:
                        for theme in data[role][verb]:
                            print topic, verb, theme        
            else:
                for verb in data[role]:
                        for theme in data[role][verb]:
                            print theme, verb, topic                                                        

    if first == topic and second == '?' and third == '?':
        for role in ['INANIMATE-CAUSE']:
            for verb in data[role]:
                    for theme in data[role][verb]:
                        print first, verb, theme
                        
    if first == topic and second != '?' and third == '?':
        for role in ['INANIMATE-CAUSE']:
            for verb in data[role]:
                if second == verb:
                    for theme in data[role][verb]:
                        print first, second, theme                

    if first == topic and second == '?' and third != '?':
        for role in ['INANIMATE-CAUSE']:
            for verb in data[role]:
                    for theme in data[role][verb]:
                        if third == theme:
                            print first, verb, theme                     

    if first == '?' and second == '?' and third == topic:
        for role in ['THEME', 'EXPERIENCE']:
            for verb in data[role]:
                    for theme in data[role][verb]:
                        print theme, verb, topic
                        
    if first == '?' and second != '?' and third == topic:
        for role in ['THEME', 'EXPERIENCE']:
            for verb in data[role]:
                if second == verb:
                    for theme in data[role][verb]:
                        print theme, verb, topic                

    if first != '?' and second == '?' and third == topic:
        for role in ['THEME', 'EXPERIENCE']:
            for verb in data[role]:
                    for theme in data[role][verb]:
                        if first == theme:
                            print theme, verb, topic   

    if first != '?' and second != '?' and third != '?':
        exists = False
        if first == topic:
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
    
    topic = sys.argv[1]
    filename = topic+".int"
    topic = topic.upper()
    print topic
    file = open(filename, 'r')
    
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
    sexpGroups = ZeroOrMore(sexp)
    #print sentences[0]
    #print sexpGroups.parseString(sentences[0]).asList()
    
    data = {"INANIMATE-CAUSE":{}, "THEME":{}, "EXPERIENCE":{}}
    
    count = 0
    ierr = 0
    terr = 0
    perr = 0
    for sentence in sentences:
        try:
            #print sexpGroups.parseString(sentence).asList()
            parse = sexpGroups.parseString(sentence).asList()
            semantic_role_list = findListLevels(3, parse, topic+'1')
            if semantic_role_list != -1 and semantic_role_list[len(semantic_role_list)-1][0] in ['THEME', 'INANIMATE-CAUSE', 'EXPERIENCE']: 
                semantic_role = semantic_role_list[len(semantic_role_list)-1][0]
            else:
                semantic_role = None

            if semantic_role == 'INANIMATE-CAUSE':
                #print findListLevels(2, parse, 'THEME')
                verb = findListLevels(1, parse, 'MAIN-VERB')[1]
                if verb not in data[semantic_role]:
                    data[semantic_role] .update({verb:[]})
                
                themeList = findListLevels(2, parse, 'THEME')
                if themeList != -1:
                    if len(themeList) < 4:
                        pass
                    else:
                        other = toString(themeList[1])          
                        if other not in data[semantic_role][verb]:
                            data[semantic_role][verb].append(other)                  
                        
                        sense = findListLevels(2, parse, 'THEME')[2][0][0].rstrip("01234567890- ")
                        #print parse[0][0], sense
                        if sense not in data[semantic_role][verb]:
                            data[semantic_role][verb].append(sense)             
                #print parse[0][0], verb, other, sense
            
            if semantic_role == "EXPERIENCE":
                verb = findListLevels(1, parse, 'MAIN-VERB')[1]
                if verb not in data[semantic_role]:
                    data[semantic_role] .update({verb:[]})
                
                other = toString(findListLevels(2, parse, 'EXPERIENCER')[1])      
                if other not in data[semantic_role][verb]:
                    data[semantic_role][verb].append(other)                  
                
                sense = findListLevels(2, parse, 'EXPERIENCER')[2][0][0].rstrip("01234567890- ")
                #print parse[0][0], sense
                if sense not in data[semantic_role][verb]:
                    data[semantic_role][verb].append(sense)                     
                #print parse[0][0], verb, other, sense        
                
            if semantic_role == "THEME":
                #print findListLevels(1, parse, 'VERB')
                verb = findListLevels(1, parse, 'MAIN-VERB')[1]
                if verb not in data[semantic_role]:
                    data[semantic_role] .update({verb:[]})              
           
                otherList = findListLevels(2, parse, 'INANIMATE-CAUSE')
                if otherList != -1:                    
                    if len(otherList) > 4 and otherList[0] == 'PREP':
                        #print "otherList",otherList
                        other = toString(otherList[1]) + "_" + parsePrep(otherList[4])
                    else:
                        other = toString(otherList[1])
                    if other not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(other)   
                    
                    sense = findListLevels(2, parse, 'INANIMATE-CAUSE')[2][0][0].rstrip("01234567890- ")
                    #print parse[0][0], sense
                    if sense not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(sense)             
                else:
                    otherList = findListLevels(2, parse, 'AGENT')
                    if otherList != -1:
                        if len(otherList) > 4:
                            other = toString(otherList[1]) + "_" + parsePrep(otherList[4])
                        else:
                            other = toString(otherList[1])
                        if other not in data[semantic_role][verb]:
                            data[semantic_role][verb].append(other)  
                        sense = findListLevels(2, parse, 'AGENT')[2][0][0].rstrip("01234567890- ")
                        #print parse[0][0], sense
                        if sense not in data[semantic_role][verb]:
                            data[semantic_role][verb].append(sense)             
                #print parse[0][0], verb, other, sense
            count += 1                        
        except IndexError as e:
            ierr += 1
            #print e
            #parse = sexpGroups.parseString(sentence).asList()
            #print parse
            #semantic_role = findListLevels(3, parse, topic+'1')
            #if semantic_role[len(semantic_role)-1][0] in ['THEME', 'INANIMATE-CAUSE', 'EXPERIENCE']: 
            #semantic_role = semantic_role[len(semantic_role)-1][0]
            #print parse[0][0], semantic_role, len(semantic_role)
            #print
            
        #except TypeError:
            terr += 1
            
            #parse = sexpGroups.parseString(sentence).asList()
            #print parse
            #semantic_role = findListLevels(3, parse, topic+'1')
            #print parse[0][0], semantic_role
            #print
        except ParseException:
            perr += 1
            #print "Could not parse: "
            #print sentence
            #print
        #print sentence
    #print data
    print ierr, "index errors"
    print terr, "type errors"
    print perr, "parse errors"
    print count, "out of", len(sentences), "sentences parsed\n"
    p = 1
    while p == 1:
        p = prompt()