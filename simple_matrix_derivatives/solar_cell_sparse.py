import numpy as np

import openmdao.api as om

class SolarCell(om.ExplicitComponent):

    def setup(self):
        
        n = 2
        m = 3

        self.add_input('T', val=np.ones((n,m))*28.,  units='degC')
        self.add_output('eta', val=np.ones((n,m))*0.32, desc='solar cell efficiency with respect to absorbed power')
        
        rows_cols = np.arange(6)
        self.declare_partials('eta', 'T', rows=rows_cols, cols=rows_cols)
    def compute(self, inputs, outputs):
        
        self.alp_sc = 0.91
        T0 = 28. #reference temperature
        eff0 = .285 #efficiency at ref temp
        T1 = -150.
        eff1 = 0.335

        delta_T = inputs['T'] - T0

        self.slope = (eff1 - eff0) / (T1 - T0)
        
        outputs['eta'] = (eff0 + self.slope * delta_T)/self.alp_sc

    def compute_partials(self, inputs, J):


        J['eta', 'T'] = np.ones(6) * self.slope/self.alp_sc


if __name__ == "__main__": 

    p = om.Problem()

    p.model.add_subsystem('sc', SolarCell())

    p.setup()

    p.check_partials()





        
       