1.  Before running the script, make sure that  `DJIA_Price201306_201806.xslx` is in **the same directory** with `HW2.jl`.
2. Run the following commands to get `Resuli.csv`.
```console
$ julia --optimize=3 HW2.jl
```
3. To evaluate the proformace of this script, you could use the following command.
```console
$ julia
julia> using BenchmarkTools
julia> @benchmark include("HW2.jl") samples=25 seconds=600
```
4. The number of assets, data range, and risk-free rate are hard-coded in the script, you can modified them through changing the variables `NumOfAssets`, `NumOfDataRange`, and `RiskFreeRate`.
