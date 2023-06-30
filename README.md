# PyCorrelationMatrixManager

A manager for correlation matrices.  The input is a set of operators and some information about 
the computation of correlation functions, and a list of files containing numeric values of the
diagrams composing the correlators.  If all the necessary numeric value exists, it outputs 
files containing the correlation function values as a function of time.  If some data is missing
then it outputs several files for computing those numerical values with a LQCD package.


## Installation

Install locally in a conda environment with `pip install -e .`  Then
due to a bug that I am working on download the [WickContractions library](github.com/chrisculver/WickContractions),
enter the directory and type `pip install -e .`. 


## Running

TODO: Simple pion example

For more advanced use see [su4workflow](github.com/chrisculver/su4workflow).


## TODO

* Dont pass in gammas, those are in the ops already...  but need to do correctly for indexing [easy]
* When crashing, give minimal computation required [easy]
* When generating computation - integrate CSE & DC [hard]
* Unit tests [easy]