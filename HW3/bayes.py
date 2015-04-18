__author__ = 'Bruce'
import sys
import re
from copy import deepcopy
import itertools
import decimal
"""function block"""
# Get P(D)
def getPD(disease_group, j, i):
    return disease_group[j][0][2]


def getSize(disease_group, j, i):
    return disease_group[j][0][1]


def getEachPTrue(disease_group, j, i):
    return disease_group[j][2][i]


def getEachPFalse(disease_group, j, i):
    return disease_group[j][3][i]


def getDiseaseName(disease_group, j, i):
    return disease_group[j][0][0]


def calProb(description_patient, i, j, divident, divisor,D_group):
     for i in range(0, len(description_patient)):
        diease_name = getDiseaseName(D_group, j, i)
        PD = float(getPD(D_group, j, i))
        if description_patient[i] == 'T':
            symp_num = getSize(D_group, j, i)
            each_P_true = getEachPTrue(D_group, j, i)
            each_P_false = getEachPFalse(D_group, j, i)
            divident *= each_P_true
            divisor *= each_P_false
        elif description_patient[i] == 'F':
            each_P_true = getEachPTrue(D_group, j, i)
            each_P_false = getEachPFalse(D_group, j, i)
            deductByOneTrue = 1 - each_P_true
            deductByOneFalse = 1 - each_P_false
            divident *= deductByOneTrue
            divisor *= deductByOneFalse
     reversedPD = 1 - PD
     divident *= PD
     divisor *= reversedPD
     divisor += divident
     res = divident / divisor
     res = round(res, 4)
     #res = ("%.4f" % res)
     #res = float(res)
     res = decimal.Decimal("%.4f" % float(res))
     return res,diease_name


def getComb(description_patient):
    loc = []
    for i in range(len(description_patient)):
        if description_patient[i] == 'U':
            loc.append(i)
    size = len(loc)
    res = []
    for j in range(0, 2**size):
        res.append(j ^ (j >> 1))
    sum_each = []
    for i in range(0,len(res)):
        item = res[i]
        count = size
        each = []
        while count != 0:
            bit = item & 1
            if bit == 0:
                each.append('F')
            elif bit == 1:
                each.append('T')
            item >>= 1
            count -= 1
        sum_each.append(each)
    total_new_cmb = []
    for m in range(len(sum_each)):
        one_cmb = sum_each[m]
        new_each = []
        idx = 0
        for i in range(len(description_patient)):
            if description_patient[i] == 'U':
               new_each.append(one_cmb[idx])
               idx += 1
            else:
                new_each.append(description_patient[i])
        total_new_cmb.append(new_each)
    return total_new_cmb


def combWithU(description_patient):
    loc = []
    dp_copy = []
    each = []
    total_combination= []
    for i in range(len(description_patient)):
        if description_patient[i] == 'U':
            dp_copy = deepcopy(description_patient)
            dp_copy[i] = 'T'
            total_combination.append(dp_copy)
            dp_copy = deepcopy(description_patient)
            dp_copy[i] = 'F'
            total_combination.append(dp_copy)
            loc.append(i)
    return total_combination

def findDiff(original, modified ):
    for i in range(len(original)):
        if original[i] != modified[i]:
            return i, modified[i]
    return None, None
""" READ THE INPUT FILE """
inputFile = open(sys.argv[2], 'r')
lines = [line.strip() for line in inputFile]  # Remove whitespace in inputfile
firstLine = lines[0].split()
num_disease = firstLine[0]
num_patient = firstLine[1]
"""READ DISEASE LIST INTO LISTS """
disease_group = []
num_disease = int(num_disease)
num_patient = int(num_patient)
j = 1
i = int(num_disease)
while i != 0:
    eachLine = []
    each_disease = []
    eachLine = lines[j].split()
    each_disease.append(eachLine)
    j += 1
    for k in range(0, 3):
        eachLine = eval(lines[j])
        each_disease.append(eachLine)
        j += 1
    disease_group.append(each_disease)
    i -= 1

i = int(num_disease)
k = int(num_patient)

patient_group = []
while k != 0:
    k -= 1
    each_patient = []
    while i != 0:
        i -= 1
        each_patient.append(lines[j])
        j += 1
    i = int(num_disease)
    patient_group.append(each_patient)

"""Question 1"""
res_q1_group = []
for k in range(0, num_patient):
    res_q1 = {}
    for j in range(0, num_disease):
        diease_name = None
        PD = 0
        divident = 1
        divisor = 1
        description_patient = eval(patient_group[k][j])
        res, diease_name = calProb(description_patient, i, j, divident, divisor, disease_group)
        res_q1[diease_name] = str(res)
    res_q1_group.append(res_q1)
print res_q1_group


"""Question 2 """
res_q2_group = []
for k in range(0, num_patient):
        res_q2 = {}
        each = []
        for j in range(0, num_disease):
            diease_name = None
            PD = 0
            divident = 1
            divisor = 1
            description_patient = eval(patient_group[k][j])
            total_combination = getComb(description_patient)
            res_max = 0
            res_min = 1
            for n in range(len(total_combination)):
                res,diease_name = calProb(total_combination[n], i, j, divident, divisor, disease_group, )
                if res > res_max:
                    res_max = res
                if res < res_min:
                    res_min = res
            res_q2[diease_name] = list() #saving list as value in dictionary
            res_q2[diease_name].append(str(res_min))
            res_q2[diease_name].append(str(res_max))
        res_q2_group.append(res_q2)
print res_q2_group


"""Question 3 """
res_q3_group = []
for k in range(0, num_patient):
        res_q3 = {}
        each = []
        for j in range(0, num_disease):
            diease_name = None
            PD = 0
            divident = 1
            divisor = 1
            description_patient = eval(patient_group[k][j])
            total_combination = combWithU(description_patient)
            res_max = 0
            res_min = 1
            choosedFindMax = None
            choosedFindMin = None
            TFMax = None
            TFMin = None
            for n in range(len(total_combination)):
                res,diease_name = calProb(total_combination[n], i, j, divident, divisor, disease_group )
                comb = total_combination[n]
                if res > res_max:
                    res_max = res
                    MaxLoc, TFMax = findDiff(description_patient, total_combination[n])
                    choosedFindMax = disease_group[j][1][MaxLoc]
                if res < res_min:
                    res_min = res
                    MinLoc, TFMin = findDiff(description_patient, total_combination[n])
                    choosedFindMin = disease_group[j][1][MinLoc]
            res_q3[diease_name] = list() #saving list as value in dictionary
            res_q3[diease_name].append(choosedFindMax)
            res_q3[diease_name].append(str(TFMax))
            res_q3[diease_name].append(choosedFindMin)
            res_q3[diease_name].append((TFMin))
        res_q3_group.append(res_q3)
print res_q3_group



""" WRITE TO THE OUTPUT FILE """
fp = open('sample_input_inference.txt', "w")
for i in range(1, num_patient+1):
    num = str(i)
    title = 'Patient-' + num + str(':')
    fp.write(title)
    fp.write('\n')
    fp.write(str(res_q1_group[i-1]))
    fp.write('\n')
    fp.write(str(res_q2_group[i-1]))
    fp.write('\n')
    fp.write(str(res_q3_group[i-1]))
    fp.write('\n')

