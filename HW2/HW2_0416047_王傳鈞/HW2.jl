using LinearAlgebra
using DataFrames
using CSV
using Statistics
using DelimitedFiles


# declaration of constant variables
NumOfAssets = 30
NumOfDataRange = 61
RiskFreeRate = 0.5*0.01/12	# i.e., 'monthly' R_f = 0.5%
IniValue = -0.1
FinValue = 0.3
Increment = 0.005
NumOfSample = 1 + convert(Int64, round( (FinValue - IniValue) / Increment ))


# import raw data
RawInput = CSV.read("Source.csv")


# extract price data from 'RawInput'
PriceMatrix = zeros(Float64, NumOfDataRange, NumOfAssets)	# initialization of 'PriceMatrix'
PriceMatrix = convert( Array{Float64}, Matrix(RawInput[1:NumOfDataRange, 2:NumOfAssets+1]) )	# the first column is date


# calculate history rate of return matrix from 'PriceMatrix'
# note that the number of rate of return equals the number of data range minus one
ReturnMatrix = zeros(Float64, NumOfDataRange-1, NumOfAssets)	# initialization
for i = 1:NumOfAssets
    for j = 1:(NumOfDataRange-1)
        ReturnMatrix[j, i] = ( PriceMatrix[j+1, i] - PriceMatrix[j, i] ) / PriceMatrix[j, i]
    end
end


# calculate expected return matrix from 'ReturnMatrix'
ExpectedReturn = zeros(Float64, NumOfAssets, 1)	# initialization
ExpectedReturn = transpose( mean(ReturnMatrix, dims = 1) )


# calculate variance covariance matrix from 'ReturnMatrix'
VarCovMatrix = zeros(Float64, NumOfAssets, NumOfAssets)	# initialization
for i = 1:NumOfAssets
	for j = 1:NumOfAssets
		VarCovMatrix[i, j] = cov(ReturnMatrix[1:end, i], ReturnMatrix[1:end, j])
	end
end


# calculate inverse matrix of 'VarCovMatrix'
InvVarCovMatrix = zeros(Float64, NumOfAssets, NumOfAssets)	# initialization
InvVarCovMatrix = inv(VarCovMatrix)


# calculate the efficient frontier
# step 1: calculate some constants (read more in class lectures about Markowitz procedures)
OneVector = ones(Float64, NumOfAssets, 1)
A = det( transpose(ExpectedReturn) * InvVarCovMatrix * OneVector )
B = det( transpose(ExpectedReturn) * InvVarCovMatrix * ExpectedReturn )
C = det( transpose(OneVector) * InvVarCovMatrix * OneVector )
D = (B * C) - (A * A)
H = B - (2 * A * RiskFreeRate) + (C * RiskFreeRate * RiskFreeRate)
# note that the return value of 'det()' is Float64, so we can use it to turn 'Array{Float64, 2}' to 'Float64'


# step 2: enumerate the E(r)=y-coordinate and find out the corresponding SD=x-coordinate wrt efficient frontier
EffcntFrntr = zeros(Float64, NumOfSample, 2)
IndexItr = 1
for y_coor in IniValue:Increment:FinValue
	x_coor = sqrt( (C/D) * (y_coor-(A/C)) * (y_coor-(A/C)) + (1/C) )
	
	global EffcntFrntr[IndexItr, 1] = x_coor
	global EffcntFrntr[IndexItr, 2] = y_coor
	global IndexItr += 1
end


# step 3: enumerate the E(r) and find out the corresponding SD wrt CAL(optimal risky portfolio)
CAL = zeros(Float64, NumOfSample, 2)
IndexItr = 1
for y_coor in IniValue:Increment:FinValue
	if y_coor >= RiskFreeRate
		x_coor = ( y_coor - RiskFreeRate ) / sqrt(H)
	else
		x_coor = ( RiskFreeRate - y_coor ) / sqrt(H)
	end
	
	global CAL[IndexItr, 1] = x_coor
	global CAL[IndexItr, 2] = y_coor
	global IndexItr += 1
end


# step 4: calculate the minimum-variance portfolio
MinVarPortMu = A / C
MinVarPortSigma = sqrt(1 / C)
MinVarPortWeightMatrix = zeros(Float64, NumOfAssets, 1)
MinVarPortWeightMatrix = (1/C) * InvVarCovMatrix * OneVector


# step 5: calculate the intersection point of efficient frontier and CAL (i.e., optimal risky portfolio)
OptRiskyMu = (B - A*RiskFreeRate) / (A - C*RiskFreeRate)
OptRiskySigma = sqrt( H / ( (A - C*RiskFreeRate)*(A - C*RiskFreeRate) ) )
OptRiskyWeightMatrix = zeros(Float64, NumOfAssets, 1)
OptRiskyWeightMatrix =	begin
						    ( 1 / ( A - C * RiskFreeRate ) )
						    *
						    ( InvVarCovMatrix * ( ExpectedReturn - RiskFreeRate * OneVector ) )
						end


# print out all of results above
# open a file in write mode
Result = open("Result.csv", "w");

write(Result, "Price Matrix\n")
writedlm(Result, PriceMatrix, ',')
write(Result, "\n")

write(Result, "Rate of Return Matrix\n")
writedlm(Result, ReturnMatrix, ',')
write(Result, "\n")

write(Result, "Expected Return Vector\n")
writedlm(Result, ExpectedReturn, ',')
write(Result, "\n")

write(Result, "Variance-Covariance Matrix\n")
writedlm(Result, VarCovMatrix, ',')
write(Result, "\n")

write(Result, "Efficient Frontier\n")
writedlm(Result, EffcntFrntr, ',')
write(Result, "\n")

write(Result, "CAL\n")
writedlm(Result, CAL, ',')
write(Result, "\n")

write(Result, "Minimum Variance Portfolio\n")
writedlm(Result, MinVarPortSigma, ',')
writedlm(Result, MinVarPortMu, ',')
write(Result, "\n")
writedlm(Result, MinVarPortWeightMatrix, ',')
write(Result, "\n")

write(Result, "Optimal Risky Portfolio\n")
writedlm(Result, OptRiskySigma, ',')
writedlm(Result, OptRiskyMu, ',')
write(Result, "\n")
writedlm(Result, OptRiskyWeightMatrix, ',')
write(Result, "\n")

write(Result, "Some Scalars\n")
write(Result, "Risk Free Rate\n")
writedlm(Result, RiskFreeRate, ',')
write(Result, "A\n")
writedlm(Result, A, ',')
write(Result, "B\n")
writedlm(Result, B, ',')
write(Result, "C\n")
writedlm(Result, C, ',')
write(Result, "D\n")
writedlm(Result, D, ',')
write(Result, "H\n")
writedlm(Result, H, ',')

close(Result)
