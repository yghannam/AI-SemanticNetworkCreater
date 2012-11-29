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
    #print list
    if list[0] == 'PREP':
        if len(list[2]) > 3:
            return list[1] + "_" + toString(list[2][1]) + "_" + parsePrep(list[2][3])
        else:
            return list[1] + "_" + toString(list[2][1])
    else:
        return " "

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
                level = 4
                topicList = findListLevels(level, parse, topic+'1')
                verb = findListLevels(1, topicList, 'MAIN-VERB')
                while verb == -1:
                    level += 1
                    topicList = findListLevels(level, parse, topic+'1')
                    verb = findListLevels(1, topicList, 'MAIN-VERB')
                verb = verb[1]
                if verb not in data[semantic_role]:
                    data[semantic_role] .update({verb:[]})
                
                themeList = findListLevels(2, parse, 'THEME')
                level = 4
                topicList = findListLevels(level, parse, topic+'1')
                themeList = findListLevels(2, topicList, 'THEME')
                while themeList == -1 and topicList != -1:
                    level += 1
                    topicList = findListLevels(level, parse, topic+'1')
                    if topicList != -1:
                        themeList = findListLevels(2, topicList, 'THEME')
                if themeList != -1:
                    themeIndex = themeList.index(['THEME'])
                    if len(themeList) < 4:
                        pass
                    else:
                        other = toString(themeList[themeIndex-2])          
                        if other not in data[semantic_role][verb]:
                            data[semantic_role][verb].append(other)                  
                        
                        sense = themeList[themeIndex-1][0][0].rstrip("01234567890- ")
                        #print parse[0][0], sense
                        if sense not in data[semantic_role][verb]:
                            data[semantic_role][verb].append(sense)             
                #print parse[0][0], verb, other, sense
            
            if semantic_role == "EXPERIENCE":
                level = 4
                topicList = findListLevels(level, parse, topic+'1')
                verb = findListLevels(1, topicList, 'MAIN-VERB')
                while verb == -1:
                    level += 1
                    topicList = findListLevels(level, parse, topic+'1')
                    verb = findListLevels(1, topicList, 'MAIN-VERB')
                verb = verb[1]
                if verb not in data[semantic_role]:
                    data[semantic_role] .update({verb:[]})
                
                exList = findListLevels(2, parse, 'EXPERIENCER')
                level = 4
                topicList = findListLevels(level, parse, topic+'1')
                exList = findListLevels(2, topicList, 'EXPERIENCER')
                while themeList == -1:
                    level += 1
                    topicList = findListLevels(level, parse, topic+'1')
                    exList = findListLevels(2, topicList, 'EXPERIENCER')
                if exList != -1:
                    exIndex = exList.index(['EXPERIENCER'])
                    if len(exList) < 4:
                        pass
                    else:
                        other = toString(exList[exIndex-2])          
                        if other not in data[semantic_role][verb]:
                            data[semantic_role][verb].append(other)                  
                        
                        sense = exList[exIndex-1][0][0].rstrip("01234567890- ")
                        #print parse[0][0], sense
                        if sense not in data[semantic_role][verb]:
                            data[semantic_role][verb].append(sense)             
                #print parse[0][0], verb, other, sense
                
            if semantic_role == "THEME":
                level = 4
                topicList = findListLevels(level, parse, topic+'1')
                verb = findListLevels(1, topicList, 'MAIN-VERB')
                while verb == -1:
                    level += 1
                    topicList = findListLevels(level, parse, topic+'1')
                    verb = findListLevels(1, topicList, 'MAIN-VERB')
                verb = verb[1]
                #verb = findListLevels(1, parse, 'MAIN-VERB')[1]
                if verb not in data[semantic_role]:
                    data[semantic_role] .update({verb:[]})              
           
                level = 4
                topicList = findListLevels(level, parse, topic+'1')
                icList = findListLevels(2, topicList, 'INANIMATE-CAUSE')
                agList = findListLevels(2, topicList, 'AGENT')
                while icList == -1 and agList == -1:
                    level += 1
                    topicList = findListLevels(level, parse, topic+'1')
                    if topicList == -1:
                        break
                    icList = findListLevels(2, topicList, 'INANIMATE-CAUSE')
                    agList = findListLevels(2, topicList, 'AGENT')                
                
                if icList != -1:
                    icIndex = icList.index(['INANIMATE-CAUSE'])
                    if len(icList) == icIndex+2:# and icList[0] != 'PREP':
                        #print "otherList",otherList
                        other = toString(icList[icIndex-2]) + "_" + parsePrep(icList[icIndex+1])
                    else:
                        other = toString(icList[icIndex-2])
                    if other not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(other)   
                    
                    sense = icList[icIndex-1][0][0].rstrip("01234567890- ")
                    if sense not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(sense)   
                    #print parse[0][0], verb, other, sense
                if agList != -1:
                    agIndex = agList.index(['AGENT'])
                    if len(agList) == agIndex+2:# and agList[0] == 'PREP':
                        other = toString(agList[agIndex-2]) + "_" + parsePrep(agList[agIndex+1])
                    else:
                        other = toString(agList[agIndex-2])
                    if other not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(other)  
                    sense = agList[agIndex-1][0][0].rstrip("01234567890- ")
                    if sense not in data[semantic_role][verb]:
                        data[semantic_role][verb].append(sense)             
                    #print parse[0][0], verb, other, sense
            count += 1                        
        except IndexError:
            ierr += 1
            #print e
            #parse = sexpGroups.parseString(sentence).asList()
            #print parse
            #semantic_role = findListLevels(3, parse, topic+'1')
            #if semantic_role[len(semantic_role)-1][0] in ['THEME', 'INANIMATE-CAUSE', 'EXPERIENCE']: 
            #semantic_role = semantic_role[len(semantic_role)-1][0]
            #print parse[0][0], semantic_role, len(semantic_role)
            #print
            
        except TypeError:
            terr += 1
            #print verbList
            #print verb
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