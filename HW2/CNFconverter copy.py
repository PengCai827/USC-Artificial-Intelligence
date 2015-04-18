__author__ = 'Peng Cai'
import sys
NOT = "not"
OR = "or"
AND = "and"
"""Changing the format of input file to a flattened format, which is a nested list,makes a list of conjuncts of lists of disjuncts;
   returns a list of lists of props  """
def flat(prop):
    flat_result = []
    if isinstance(prop, str):
        negList = []
        negList.append(prop)
        flat_result.append(negList)
    else:
        if prop[0] == AND:
            size = len(prop)
            for i in range(1, size):
                each = prop[i]
                if each[0] == OR:
                    tuple = []
                    size2 = len(each)
                    for j in range(1, size2):
                        if len(each[j]) == 1:
                            tuple.append(each[j])
                        else:
                            neg = '-' + str(each[j][1])# Changing ["not","B"] into "-B"
                            tuple.append(neg)
                    flat_result.append(tuple)
                else:
                    if len(each) == 1:
                        negList = []
                        negList.append(each)
                        flat_result.append(negList)
                        # flat_result.append(each)
                    else:
                        neg = '-' + str(each[1])
                        negList = []
                        negList.append(neg)
                        flat_result.append(negList)
        if prop[0] == OR:
            size = len(prop)
            for i in range(1, size):
                each = prop[i]
                if len(each) == 1:
                    negList = []
                    negList.append(each)
                    flat_result.append(negList)
                    # flat_result.append(each)
                else:
                    neg = '-' + str(each[1])
                    negList = []
                    negList.append(neg)
                    flat_result.append(negList)
                    # flat_result.append(neg)
        else:
            if prop[0] == 'not':
                neg = '-' + str(prop[1])
                negList = []
                negList.append(neg)
                flat_result.append(negList)

    return flat_result


def is_prop_symbol(s):
    """A proposition logic symbol is an initial-uppercase string other than
    TRUE or FALSE."""
    return is_symbol(s) and s[0].isupper() and s != 'TRUE' and s != 'FALSE'


def is_symbol(s):
    "A string s is a symbol if it starts with an alphabetic char."
    return isinstance(s, str) and s[:1].isalpha()


def pl_true(exp, model):
    """Return True if the propositional logic expression is true in the model,
    and False if it is false. If the model does not specify the value for
    every proposition, this may return None to indicate 'not obvious';
    this may happen even when the expression is tautological."""
    if exp == True:
        return True
    elif exp == False:
        return False
    if len(exp) == 1:
        if not is_prop_symbol(exp[0]):
            item = exp[0]
            p = pl_true(item[1], model)
            if p is None:
                return None
            else:
                return not p
        else:
            return model.get(exp[0])
    else:
        result = False
        for arg in exp:
            if arg == '-':#
                p = pl_true(exp[1], model)
                if p is None:
                    return None
                else:
                    return not p
            p = pl_true(arg,model)
            if p is True:
                return True
            if p is None:
                result = None
        return result

def dpll(clauses, symbols, model):
    unknown_clauses = []  ## clauses with an unknown truth value
    for c in clauses:
        val = pl_true(c, model)
        if val == False:
            return False
        if val != True:
            unknown_clauses.append(c)
    if not unknown_clauses:
        return model

    P, value = find_pure_symbol(symbols, unknown_clauses)
    if P:
        symbols.remove(P)
        if len(P) == 2:# To make sure the symbols list only store pure letter without '-'
            P = P[1]
        model = extend(model, P, value)
        return dpll(clauses, symbols, model)
    P, value = find_unit_clause(clauses, model)
    if P:
        symbols.remove(P)
        #symbols = filter(lambda a: a == P, symbols)
        model = extend(model, P, value)
        return dpll(clauses, symbols, model)
    P, symbols = symbols[0], symbols[1:]
    return (dpll(clauses, symbols, extend(model, P, True)) or
            dpll(clauses, symbols, extend(model, P, False)))


def extend(s, var, val):
    """Copy the substitution s and extend it by setting var to val;
    return copy.
    """
    s2 = s.copy()
    s2[var] = val
    return s2


def find_pure_symbol(symbols, clauses):
    """Find a symbol and its value if it appears only as a positive literal
    (or only as a negative) in clauses.
    """
    for s in symbols:
        found_pos, found_neg = False, False
        for c in clauses:
            if len(s) == 2:
                if not found_neg and s in c: found_neg = True
                if not found_pos and s[1] in c: found_pos = True
            else:
                if not found_pos and s in c: found_pos = True
                if not found_neg and '-' + s in c: found_neg = True
        if found_pos != found_neg: return s, found_pos
    return None, None


def find_unit_clause(clauses, model):
    """A unit clause has only 1 variable that is not bound in the model.
    """
    for clause in clauses:
        num_not_in_model = 0
        true_literal_in_clause = False  # CTM
        for literal in clause:
            sym = literal_symbol(literal)
            if sym in model:
                val = model.get(sym)
                if (not val and literal[0] == '-') or (val and literal[0] != '-'):
                    true_literal_in_clause = True
            else:
                num_not_in_model += 1
                P, value = sym, (literal[0] != '-')
        if num_not_in_model == 1 and not true_literal_in_clause:
            return P, value
    return None, None


def literal_symbol(literal):
    """The symbol in this literal (without the negation).
    """
    if literal[0] == '-':
        return literal[1:]
    else:
        return literal

""" READ THE INPUT FILE """
inputFile = open(sys.argv[2], 'r')
lines = [line.strip() for line in inputFile]
linesNum = lines[0]
linesNum = int(linesNum)
result = []
for i in range(1, linesNum+1):
#for i in range(1, 2):
    symbols = []
    eachList = eval(lines[i])
    flatted = flat(eachList)
    symbols = list(set(sum(flatted, [])))
    symbols_cp = symbols[:]
    res = dpll(flatted, symbols, {})
    each_result =[]
    """Making the format of the result be the format in the direction of the homework """
    if not res:
        each_result.append("false")
        result.append(each_result)
    else:
        for item in symbols_cp:
            if len(item) == 1:
                neg_item = '-'+item
                res.pop(neg_item, None)
            else:
                neg_item = item[1]
                res.pop(item, None)
        for item in symbols_cp:
            if len(item) == 2:
                one = item[1]
                if not one in res.keys():
                    res[one] = True
            else:
                if not item in res.keys():
                    res[item] = True
        for key in res.keys():
            value = res.get(key)
            if value:
                pair = key + '='+ "true"
                each_result.append(pair)
            else:
                pair = key + '='+ "false"
                each_result.append(pair)
        each_result.insert(0, "true")
        result.append(each_result)
print result

""" WRITE TO THE OUTPUT FILE """
fp = open('CNF_satisfiability.txt', "w")
for i in range(len(result)):
    fp.write(str(result[i]))
    fp.write('\n')
fp.close()
