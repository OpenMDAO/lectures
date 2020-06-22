This lecture covers the process of differentiating a moderately complex vectorized component. 
The component has vector inputs and outputs, but the relationship between them is much more complex than simple numpy vectorization (i.e. the partial derivative Jacobians have many off-diagonal terms). 
The primary goal with this lecture is to get you comfortable working with the `rows`  and `cols` needed for specifying sparse partials on a non-trivial example. 

This lecture is based around the calculation of the bending moment along a cantilevered beam under both distributed and point loading. 
The calculations are discretized and implemented in a for-loop fashion. 
The for-loop structure of the code in this lecture is not how you'd really want to implement this if you were really coding an analysis tool like this, at least not in Python. 
For loops like these are really slow in python, so you'd want to use  Numpy vectorization. 
Those details are not given here though, because the primary goal with this lecture is lean to differentiate the example.

Two differentiation approaches are shown. 
1) Dense Partials -- Slightly easier to code, but a lot slower in practice. 
2) Sparse Partials -- A little harder to code, but much faster in practice. 


