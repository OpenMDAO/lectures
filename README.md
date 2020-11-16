# Gradient Based Optimization for Practitioners

A collection of notes and associated scripts for online lectures on OpenMDAO. 
These lectures are the beginnings of a MDO training course that I am building. 
I am just at the early stages of laying out the course and for now this is mostly a collection of scattered lectures on topics that I develop as I need to teach them. 

The full collection of lectures can be found on the [OpenMDAO youtube channel](https://www.youtube.com/playlist?list=PLPusXFXT29sWLpp5A8yOt6AYiW7kus56q)

If you're new to OpenMDAO and looking for help getting started, check out the [User Guide](http://openmdao.org/twodocs/versions/latest/index.html) in the docs.
Thats the best place to get started. 


# Course Outline

## Introduction 
### Three Critical MDO skill sets 

* Optimization Problem Formulation 
* Model Building 
* Model Differentiation 

### Additional Important Skill sets 
* Version control: Git and Github 
* Coding best practices: test driven development 



### Optimization Problem Formulation 

* An optimizer is a solver for underdefined problems
* Types of optimizers and why gradient based should be your first choice
* Basic optimization problem formulation: objective, ieq constraint, eq constraint
* Constrained optimization can be turned into a nonlinear solve (derive the KKT conditions)
* Getting optimization problem formulation right
* Basic scaling techniques for optimization 
* Advanced optimization problem formulation
    * bound constraint vs ieq constraints
    * slack variables for improved stability 
    * eq constraints vs solver balance
    * MDF vs IDF vs SAND 
    * Re-parameterizing a design space (need to develop good examples here)
* Dealing with multiple objectives: weighted sum vs epsilon-constraint
* Understanding what controls the compute cost for optimization
    * Cost of a nonlinear solve at start of opt vs at end
    * time to compute derivatives 
* Weird Optimization Situations
    * Singular objective function (possible optimal-control, example)
    * Separable objectives 
    * constraint relaxation 
* Nested optimization techniques for bumpy problems 
* Why Optimization convergence is important --- so you get smooth trends


### Model Building 

* Basic implicit and explicit functions
* Pseudo explicit functions: implicit functions hiding inside explicit ones 
* Hierarchical model construction and visualization
* Implicit Model Structure: Cyclic Dependency -- example: 2D airfoils on translational and rotational spring
* Implicit Model Structure: Balance Equation -- example: modular truss solver 
* Common Modeling Pattern: Node-resistance (circuit analysis, thermal analysis, truss solver)
* How to debug when a solver is not converging
* Basic solvers: fixed point iteration vs Newton-like methods
* Nested Solvers: when and how to use them
* adding curve fits into your model in a differentiable way -- Collocation example 
* Using a newton solver to tackle nested optimizations -- L2 norm minimization 
* (advanced topic) Advanced Solvers: Gradient Free (Bracketing, Brent, NLBGS, Jacobi) vs Gradient Based (Newton, Broyden)
* (advanced topic) Understanding Newton's method
* (advanced topic) What is a line search and why should you care about it? 
* (advanced topic) Unbalanced nonlinearity and its relationship to nested solver structure
* (advanced topic) Matrix free linear solver methods for use with Newton solver



### Model Differentiation 
* Computing derivatives of explicit functions: FD, chain rule 
* computing derivatives of implicit functions: FD, analytic derivatives
* What to do with pseudo explicit functions? 
* advanced methods for derivative computations: CS, AD
* dealing with vector valued functions 
    * diagonal 
    * non-diagonal 
    * sparse
* How to structure your code to be easily differentiable
* Common gotchas
    * conditionals 
    * for loops 
    * singularities 
* Computing derivatives as cheaply as possible 
    * Forward vs Reverse derivatives 
    * UDE 

