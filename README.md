# Polynomial_integration
This script can perform integration on given polynomial. Library used with this script can be used to disect strings into s-expression style nested lists.

Provided files are: 
-Integration.py: this is a library of functions performing integration using graphs in form of s-expressions.
-integrate.py: script that performs integration.
-input.txt: input file with example of polynomial prepared for primitive integration.
-inputD.txt: input file with example of polynomial prepared for definite integration.

Running script:
Script can be run in pattern: python3 integrate.py -i \[input file\] (defines path to input file, default path: 'input.txt'), -I (primitive integral), -D (definite integral)").
Only one type of integration can be set at one time.

Rules on writing input files:

1) File prepared to perform primitive integration contains two parts: polynomial and variables according to which integration will be performed. Correct will be: "1+(1/2)*x*y-2*x^2+1*x^3*y^2 dxdy". Worth noting is that i order to integrate variable name must be wirte in pattern 'd+"name of variable"' and all variables must be written together.

2)File prepared to perform definitive integration contains three parts: polynomial, limits, variable according to which integration will be performed. Correct will be: "1+(1/2)*x-2*x^2+1*x^3 3,9 dx". Library functions calculate definitive integration only for one variable.


