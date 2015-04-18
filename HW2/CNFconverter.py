__author__ = 'Peng Cai'
import sys
import re
IMPLIES = "implies"
NOT = "not"
OR = "or"
AND = "and"


def removeImplications(prop):
    """removeImplications replaces every implication in  prop
       [IMPLIES, A, B]  is replaced by  [OR, [NOT, A], B]
    """
    if isinstance(prop, str):
        answer = prop
    else:  # isinstance(prop,list)
        """{ assert: prop  is a compound proposition }"""
        op = prop[0]
        if op == NOT:
            tree = removeImplications(prop[1])
            """{ assert: tree has all implications removed }"""
            answer = [NOT, tree]
        else:  # op  is a binary operator
            tree1 = removeImplications(prop[1])
            tree2 = removeImplications(prop[2])
            """{ assert: tree1 and tree2 have all implications removed }"""
            if op == IMPLIES:
                answer = [OR, [NOT, tree1], tree2]
            else:  # op is  AND  or  OR
                answer = [op, tree1, tree2]
    return answer


def moveNegations(prop):
    """moveNegations moves all negations inwards until they rest against
       primitive propositions.
    """
    if isinstance(prop, str):
        """{ assert: prop  is a primitive proposition }"""
        answer = prop
    else:  # isinstance(prop,list)
        """{ assert: prop  is a compound proposition }"""
        op = prop[0]
        if op == NOT:
            """{ assert:  prop = [NOT, arg] }"""
            # descend one more level of structure to see what to do with NOT:
            arg = prop[1]
            if isinstance(arg, str):
                """{ assert:  prop = [NOT, P] }"""
                answer = "-" + arg    # negation is attached to primitive prop
            else:  # isinstance(prop,list)
                """{ assert: prop = [NOT, [inner_op, ...]] }"""
                inner_op = arg[0]
                if inner_op == NOT:
                    """{ assert: prop = [NOT, [NOT, rest]] }"""
                    # the two negations cancel, so...
                    answer = moveNegations(arg[1])
                else: # inner_op is AND or OR
                    """{ assert: prop = [NOT, [op, arg1, arg2]] }"""
                    tree1 = moveNegations([NOT, arg[1]])
                    tree2 = moveNegations([NOT, arg[2]])
                    """{ assert:  tree1 and tree2 are the values of arg1 and
                           arg2  where all negations are moved inwards }"""
                    # finally, flip  AND to OR,  OR to AND:
                    dual = {AND: OR,  OR: AND}  # a python dictionary
                    answer = [dual[inner_op], tree1, tree2]
        else: # op is AND or OR
            """{ assert: prop = [op, prop1, prop2] }"""
            tree1 = moveNegations(prop[1])
            tree2 = moveNegations(prop[2])
            """{ assert:  tree1 and tree2 are the values of arg1 and arg2
                   where all negations are moved inwards }"""
            answer = [op, tree1, tree2]

    return answer


def makeIntoCNF(prop):
    """makeIntoCNF moves the ORs within the AND clauses.
    """
    if isinstance(prop, str):  # prop has form "P" or "-P"
        answer = prop
    elif prop[0] == NOT:
        answer = prop
    else:  # prop  has form  [op, prop1, prop2]
        op = prop[0]
        tree1 =  makeIntoCNF(prop[1])
        tree2 =  makeIntoCNF(prop[2])
        if op == AND :
            answer = [AND, tree1, tree2]
        else: # op == OR
            answer = distribute_Or(tree1, tree2)
    return answer


def flattenCNF(prop):
    """makes a list of conjuncts of lists of disjuncts;
       returns a list of lists of props
    """
    def flattenDisjuncts(prop):
        """makes a list of primitive props from  prop, a nested disjunction.
        """
        if isinstance(prop, str):
            ans = [prop]
        else :  # prop  has form  [OR, p1, p2]
            ans = flattenDisjuncts(prop[1]) + flattenDisjuncts(prop[2])
        return ans


    if isinstance(prop, str) :  # prop is "P" or "-P"
        answer = [ [prop] ]
    else :  # prop  has form  [op, p1, p2]
        op = prop[0]
        if op == OR :
            answer = [ flattenDisjuncts(prop[1]) + flattenDisjuncts(prop[2]) ]
        else : # op == AND
            answer = flattenCNF(prop[1]) + flattenCNF(prop[2])
    return answer


def distribute_Or(p1, p2):
    """distribute_Or  converts a proposition of form,   p1 v p2,
       where  p1  and  p2  are already in cnf,  into an answer in cnf
    """
    if isinstance(p1, list) and p1[0] == AND:
        """{ assert:  p1 = P11 & P12 }"""
        answer = [AND, distribute_Or(p1[1], p2), distribute_Or(p1[2], p2)]
    elif  isinstance(p2, list) and p2[0] == AND:
        """{ assert:  p2 = P21 & P22 }"""
        answer = [AND, distribute_Or(p1, p2[1]), distribute_Or(p1, p2[2])]
    else:
        """{ assert: since  p1 and p2 are both in cnf, then both are
             disjunctive clauses, which can be appended }"""
        answer = [OR, p1, p2]
    return answer


def removeDuplicates(prop):
    """removeDuplicates  removes from each disjunctive clause duplicate
       occurrences of any "P" or "-P".
    """
    answer = []
    for disjunct in prop:
        removed=[removeDuplicate(disjunct)]
        answer = answer + removed
        answer.sort()
    b_set = set(map(tuple,answer))
    answer = map(list,b_set)
    return answer


def removeDuplicate(d):
    """removes all duplicate strings from list  d"""
    if d == []:
        ans = d
    else:
        p = d[0]
        rest = removeDuplicate(d[1:])
        if p in rest:
            ans = rest
        else:
            ans = [p] + rest
    return ans


def deflate(prop): # Making the format be the example given by direction of homework
    if len(prop) == 1: #In case prop has only one element, so there is no "and"
        if len(prop[0]) == 1: # For the case that the this one element of prop only has one literal.
            answer = prop[0]
            answer.insert(0, 'not')
            newline = str(answer[1])
            list = re.findall("[-]\w+", newline)# Making the result nested in a bracket
            result = re.split("\W+", list[0])
            del answer[1]
            answer.insert(1, result[1]) #Changing "-B" into the format of ['not','B']
        else:
            answer = prop[0]
            for m in range(len(answer)):# For the case that prop has many clauses
                newline = str(answer[m])
                list = re.findall("[-]\w+", newline)
                if list:
                    for i in range(len(list)):  # For the case that each clauses has several literals
                        result = re.split("\W+", list[0])
                        newlist = []
                        newlist.append('not')
                        newlist.append(result[1])
                        del answer[m]
                        answer.insert(m, newlist)
            answer.insert(0, 'or')
    else: # In case prop has more than one element, so there is an "and"
        answer = prop[:]
        """For each clauses, insert an "or" at the front of the clauses as well as adding 'not' at the front of negative literal  """
        for j in range(len(answer)):
            tuple = answer[j]
            if len(tuple) >= 2:
                for n in range(len(tuple)):
                    newline = str(tuple)
                    list = re.findall("[-]\w+", newline)
                    if list:
                        result = re.split("\W+", list[0])
                        newlist = []
                        newlist.append('not')
                        newlist.append(result[1])
                        del tuple[n]
                        tuple.insert(n, newlist)
            tuple.insert(0, "or")
        answer.insert(0, "and")
    return answer

""" READ THE INPUT FILE """
inputFile = open(sys.argv[2], 'r')
lines = [line.strip() for line in inputFile] # Remove whitespace in inputfile
linesNum = lines[0]
linesNum = int(linesNum)
result = []

for i in range(1, linesNum+1):
    eachList = eval(lines[i])
    res = removeImplications(eachList)
    res = moveNegations(res)
    res = makeIntoCNF(res)
    res = flattenCNF(res)
    res = removeDuplicates(res)
    res = deflate(res)
    result.append(res)
    print res
    print '\n'

""" WRITE TO THE OUTPUT FILE """
fp = open('sentences_CNF.txt', "w")
for i in range(len(result)):
    fp.write(str(result[i]))
    fp.write('\n')
fp.close()


