'''
    Programming Assignment #2
    
    Course: Investment (Graduated)
    Writer_ID: 0416047
    Writer_Name: Chuan-Chun, Wang
    Environment: Python 3.7.3 on Windows 10(1803) and Intel Core i5-5200U
'''

import numpy
import math
import csv

# declaration of constant variables
NumOfAssets = 30
NumOfDataRange = 61
RiskFreeRate = 0.5*0.01/12                                                                      # i.e., 'monthly' R_f = 0.5%
IniValue = -0.1
FinValue = 0.3
Increment = 0.005
NumOfSample = 1 + int( ( ( FinValue - IniValue ) / Increment ) )


# import raw data
RawInput = []                                                                                   # type: nested list
with open('DJIA_Price201306_201806.CSV', 'r') as InFilePtr:
    CSVReader = csv.reader(InFilePtr, delimiter=',')
    for RowItr in CSVReader:
        RawInput.append(RowItr)


# extract price data from 'RawInput'
PriceMatrix = numpy.zeros([NumOfDataRange, NumOfAssets])                                        # initialization
# discard the first row and first column of 'RawInput'
for i in range(0, NumOfDataRange):
    for j in range(0, NumOfAssets):
        PriceMatrix[i][j] = RawInput[i+1][j+1]


# calculate history rate of return matrix from 'PriceMatrix'
# note that the number of rate of return equals the number of data range minus one
ReturnMatrix = numpy.zeros([NumOfDataRange-1, NumOfAssets])                                     # initialization
for i in range(0, NumOfDataRange-1):
    for j in range(0, NumOfAssets):
        ReturnMatrix[i, j] = ( PriceMatrix[i+1, j] - PriceMatrix[i, j] ) / PriceMatrix[i, j]    # asset j, time i+1 & i


# calculate expected return matrix from 'ReturnMatrix'
ExpectedReturn = numpy.mean(ReturnMatrix, axis=0).reshape((NumOfAssets, 1))


# calculate variance covariance matrix from 'ReturnMatrix'
VarCovMatrix = numpy.cov(ReturnMatrix, rowvar=False)


# calculate inverse matrix of 'VarCovMatrix'
InvVarCovMatrix = numpy.linalg.inv(VarCovMatrix)


# calculate the efficient frontier
# step 1: calculate some constants (read more in class lectures about Markowitz procedures)
OneVector = numpy.ones([NumOfAssets, 1])
A = numpy.linalg.det( numpy.dot( numpy.dot( numpy.transpose(ExpectedReturn), InvVarCovMatrix ), OneVector ) )
B = numpy.linalg.det( numpy.dot( numpy.dot( numpy.transpose(ExpectedReturn), InvVarCovMatrix ), ExpectedReturn ) )
C = numpy.linalg.det( numpy.dot( numpy.dot( numpy.transpose(OneVector), InvVarCovMatrix ), OneVector ) )
D = (B * C) - (A * A)
H = B - (2 * A * RiskFreeRate) + (C * RiskFreeRate * RiskFreeRate)
# note that the return value of 'det()' is Float64, so we can use it to turn 'Array{Float64, 2}' to 'Float64'


# step 2: enumerate the E(r)=y-coordinate and find out the corresponding SD=x-coordinate wrt efficient frontier
EffcntFrntr = numpy.zeros([NumOfSample, 2])
y_coor = IniValue
for IndexItr in range(0, NumOfSample):
    x_coor = math.sqrt( (C/D) * (y_coor-(A/C)) * (y_coor-(A/C)) + (1/C) )
    
    EffcntFrntr[IndexItr, 0] = x_coor
    EffcntFrntr[IndexItr, 1] = y_coor
    y_coor = round(y_coor+Increment, 3)


# step 3: enumerate the E(r) and find out the corresponding SD wrt CAL(optimal risky portfolio)
CAL = numpy.zeros([NumOfSample, 2])
y_coor = IniValue
for IndexItr in range(0, NumOfSample):
    if y_coor >= RiskFreeRate :
        x_coor = ( y_coor - RiskFreeRate ) / math.sqrt(H)
    else:
        x_coor = ( RiskFreeRate - y_coor ) / math.sqrt(H)
    
    CAL[IndexItr, 0] = x_coor
    CAL[IndexItr, 1] = y_coor
    y_coor = round(y_coor+Increment, 3)


# step 4: calculate the minimum-variance portfolio
MinVarPortMu = A / C
MinVarPortSigma = math.sqrt(1 / C)
MinVarPortWeightMatrix = numpy.multiply( (1/C), numpy.dot(InvVarCovMatrix, OneVector) )


# step 5: calculate the intersection point of efficient frontier and CAL (i.e., optimal risky portfolio)
OptRiskyMu = (B - A*RiskFreeRate) / (A - C*RiskFreeRate)
OptRiskySigma = math.sqrt( H / ( (A - C*RiskFreeRate)*(A - C*RiskFreeRate) ) )

Temp1 = 1 / ( A - C * RiskFreeRate )
Temp2 = InvVarCovMatrix
Temp3 = numpy.subtract(ExpectedReturn, numpy.multiply(RiskFreeRate, OneVector))

OptRiskyWeightMatrix =  numpy.multiply(Temp1, numpy.dot(Temp2, Temp3))


# print out all of results above
# open a file in write mode
with open('Result_python.csv', 'w', newline='') as OutFilePtr:
    CSVWriter = csv.writer(OutFilePtr, delimiter=',')

    CSVWriter.writerow(['Price Matrix'])
    CSVWriter.writerows(PriceMatrix)
    CSVWriter.writerow([''])

    CSVWriter.writerow(['Rate of Return Matrix'])
    CSVWriter.writerows(ReturnMatrix)
    CSVWriter.writerow([''])

    CSVWriter.writerow(['Expected Return Vector'])
    CSVWriter.writerows(ExpectedReturn)
    CSVWriter.writerow([''])

    CSVWriter.writerow(['Variance-Covariance Matrix'])
    CSVWriter.writerows(VarCovMatrix)
    CSVWriter.writerow([''])

    CSVWriter.writerow(['Efficient Frontier'])
    CSVWriter.writerows(EffcntFrntr)
    CSVWriter.writerow([''])

    CSVWriter.writerow(['CAL'])
    CSVWriter.writerows(CAL)
    CSVWriter.writerow([''])

    CSVWriter.writerow(['Minimum Variance Portfolio'])
    CSVWriter.writerow(['Mu', MinVarPortMu])
    CSVWriter.writerow(['Sigma', MinVarPortSigma])
    CSVWriter.writerow([''])
    CSVWriter.writerows(MinVarPortWeightMatrix)
    CSVWriter.writerow([''])

    CSVWriter.writerow(['Optimal Risky Portfolio'])
    CSVWriter.writerow(['Mu', OptRiskyMu])
    CSVWriter.writerow(['Sigma', OptRiskySigma])
    CSVWriter.writerow([''])
    CSVWriter.writerows(OptRiskyWeightMatrix)
    CSVWriter.writerow([''])

    CSVWriter.writerow(['Some Scalars'])
    CSVWriter.writerow(['Risk Free Rate', RiskFreeRate])
    CSVWriter.writerow(['A', A])
    CSVWriter.writerow(['B', B])
    CSVWriter.writerow(['C', C])
    CSVWriter.writerow(['D', D])
    CSVWriter.writerow(['H', H])

