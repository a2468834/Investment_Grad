1. Please convert `DJIA_Price201306_201806.xlsx` into `DJIA_Price201306_201806.csv`.
2. Before running the script, make sure that  `DJIA_Price201306_201806.csv` is in **the same directory** with `HW2.jl` or `HW2_python.py`.
3. There are two versions of HW2 with different languages. Please make sure that you already have installed the completed environment to run the script.
    * Julia-1.1.0
        * Run the following commands to get `Result.csv`.
        ```console
        $ julia HW2.jl
        ```
    * Python-3.7.3
        * Run the following commands to get `Result_python.csv`.
        ```console
        $ python -B HW2_python.py
        ```
4. The number of assets, data range, and risk-free rate are **hard-coded** in the script, you can modified them through changing the variables `NumOfAssets`, `NumOfDataRange`, and `RiskFreeRate`.

5. To evaluate the proformace of this script, you could use the following command.
    * Julia-1.1.0
        ```julia
        $ julia
        julia> using BenchmarkTools
        julia> @benchmark include("HW2.jl") samples=25 seconds=600
        ```
    * Python-3.7.3
        ```console
        $ python -m cProfile HW2_python.py
        ```
