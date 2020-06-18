import numpy as np

import openmdao.api as om 


class BeamMoment(om.ExplicitComponent): 

    def initialize(self): 
        self.options.declare('n_q', types=int, default=3)

        # index of the node to apply the point load F
        self.options.declare('idx_F', types=int, default=2) 

    def setup(self): 
        n_q = self.options['n_q']
        # array of point loads resolved from distributed load to nodes
        self.add_input('Q', val=1, shape=n_q, units='N') 

        self.add_input('F', val=10, units='N') # magnitude of the point load
        self.add_input('alpha', val=0, units='rad') # angle of point load
        self.add_input('l', val=3, units='m') # length of beam

        self.add_output('M', shape=n_q, units='N*m') # bending moment computed at each node
        self.add_output('x', shape=n_q, units='m') # locations of the nodes

        self.x_norm = np.linspace(0, 1, n_q) # normalized array of node locations

        # sub-jac sized (n_q, 1)
        self.declare_partials(of='M', wrt='l')
        self.declare_partials(of='x', wrt='l')

        # sparse sub jac with data of length idx_F+1
        idx_F = self.options['idx_F']
        row_idx = np.arange(idx_F+1)
        col_idx = np.zeros(idx_F+1)
        self.declare_partials(of='M', wrt=['F', 'alpha'], rows=row_idx, cols=col_idx)
        
        # sparse sub jac with data of length n_q*((n_q+1)/2 - 1); upper triangle of sub-jac
        row_idx = []
        col_idx = []
        for i in range(n_q):
            for j in range(i, n_q): 
                row_idx.append(i)
                col_idx.append(j)   
        self.declare_partials(of='M', wrt='Q', rows=row_idx, cols=col_idx)

    def compute(self, inputs, outputs): 

        #use trapezoidal integration for the distributed load 
        n_q = self.options['n_q']
        idx_F = self.options['idx_F']
        
        F = inputs['F']
        Q = inputs['Q']
        alpha = inputs['alpha']

        l = inputs['l']

        M = outputs['M']
        x = outputs['x'] = self.x_norm * l

        M[:] = 0
        for i in range(n_q): 
            # fast numpy method to do trapezoidal integration
            # M[i] = -np.trapz((x[i:]-x[i])*Q[i:], x[i:])

            # trapezoidal integration of Q
            for j in range(i, n_q-1): 
                M[i] -= (Q[j]*(x[j]-x[i]) + Q[j+1]*(x[j+1]-x[i]))/2. * (x[j+1]-x[j])
           
            # account for the point load
            if i <= idx_F: 
                x_k = x[idx_F]
                M[i] += F*np.cos(alpha)*(x_k - x[i])


    def compute_partials(self, inputs, J): 

        n_q = self.options['n_q']
        idx_F = self.options['idx_F']
        
        F = inputs['F']
        Q = inputs['Q']
        alpha = inputs['alpha']
        l = inputs['l'] 

        # M = outputs['M']
        x = self.x_norm * inputs['l'] 
        x_norm = self.x_norm


        J['x', 'l'] = x_norm

        for i in range(n_q):
            for j in range(i, n_q-1):
                term1 = (Q[j]*(x[j]-x[i]) + Q[j+1]*(x[j+1]-x[i]))/2.
                term2 = (x[j+1]-x[j])

                J['M', 'l'][i] -= ((Q[j]*(x_norm[j]-x_norm[i]) + Q[j+1]*(x_norm[j+1]-x_norm[i]))/2. * term2 + 
                                   term1*(x_norm[j+1]-x_norm[j]))
                
                offset = i*(i+1)//2
                
                k = (n_q*i)+ j - offset
                J['M', 'Q'][k] -= (x[j]-x[i])/2. * term2

                k = (n_q*i)+ j+1 - offset
                J['M', 'Q'][k] -= (x[j+1]-x[i])/2. * term2
      
            if i <= idx_F: 
                x_k = x[idx_F]
                J['M', 'alpha'][i] +=  -F*np.sin(alpha)*(x_k-x[i])
                J['M', 'l'][i] +=  F*np.cos(alpha)*(x_norm[idx_F]-x_norm[i])
                J['M', 'F'][i] +=  np.cos(alpha)*(x_k-x[i])





if __name__ == "__main__": 

    import time

    p = om.Problem()

    N = 6
    ivc = p.model.add_subsystem('ivc', om.IndepVarComp(), promotes=['*'])
    ivc.add_output('F', 10, units='N')
    ivc.add_output('alpha', 45, units='deg')
    ivc.add_output('Q', 2*np.ones(N), units='N')
    p.model.add_subsystem('beam', BeamMoment(n_q=N, idx_F=2), promotes=['*'])

    p.model.linear_solver = om.DirectSolver()

    p.setup(force_alloc_complex=True)
 
    p.run_model()

    p.model.list_outputs(print_arrays=True) 

    p.check_partials(method='cs')

