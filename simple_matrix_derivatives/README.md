This lecture covers the basics of implementing analytic derivatives for simple vectorized components --- components that use basic numpy vectorization. 
When working with basic numpy vectorization the partial derivative Jacobian will be a diagonal matrix. 


Two methods of declaring derivatives are discussed: 
1) Dense partials - solar_cell_dense.py 
2) Sparse partials - solar_cell_sparse.py

Dense Partials use a lot more memory and are slower. In practice you should avoid them for components that are easy to provide sparsity for. 
However, you may find them useful as a learning tool. 
Sparse partials are the preferred method, since they are faster and use less memory. 
For simple vectorizations, they are not any harder than dense partials. 


Read the (docs on sparse partials)[http://openmdao.org/twodocs/versions/3.0.0/features/core_features/working_with_derivatives/sparse_partials.html] for more information. 