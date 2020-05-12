import numpy as np

nn = 3

data = np.empty(nn*3)
nl_vec = {}
nl_vec['x'] = data[:3]
nl_vec['y'] = data[3:6]
nl_vec['z'] = data[6:9]

data_o = np.empty(nn*3)
ln_o = {}
ln_o['x'] = data_o[:3]
ln_o['y'] = data_o[3:6]
ln_o['z'] = data_o[6:9]

data_r = np.empty(nn*3)
ln_r = {}
ln_r['x'] = data_r[:3]
ln_r['y'] = data_r[3:6]
ln_r['z'] = data_r[6:9]


def X(inputs, outputs): 
    outputs['x'][:] = [2,3,4]

def Y(inputs, outputs): 
    outputs['y'][:] = 5 * inputs['x']

def Z(inputs, outputs): 
    outputs['z'][:] = inputs['y']**2 + inputs['x']**3

# UDE Form
# Rx = x - \hat{x}
# Ry = y - Y(x)
# Rz = z - Z(x,y)

# OM Form
# Rx = \hat{x} - x
# Ry = Y(x) - y
# Rz = Z(x,y) - z

def dY__dx(inputs): 
    return np.eye(nn)*5

def dZ__dx(inputs): 
    return np.diag(3*inputs['x']**2)

def dZ__dy(inputs): 
    return np.diag(2*inputs['y'])


def X_apply_linear(inputs, outputs, d_i, d_o, d_r, mode='fwd', sign="pos"): 

    # if sign == "pos": 
    #     if mode == "fwd": 
    #         if 'x' in d_r: 
    #             d_r['x'] += d_o['x']

    #     else: # rev
    #         if 'x' in d_r: 
    #             d_o['x'] += d_r['x']
    # else: #neg 
    #     if mode == "fwd": 
    #         if 'x' in d_r: 
    #             d_r['x'] -= d_o['x']

    #     else: # rev
    #         if 'x' in d_r: 
    #             d_o['x'] -= d_r['x']

    pass
    
def X_solve_linear(rhs_vec, sol_vec): 
    sol_vec['x'][:] = rhs_vec['x']


def Y_apply_linear(inputs, outputs, d_i, d_o, d_r, mode='fwd', sign='pos'): 

    if sign == "pos": 
        if mode == 'fwd': 
            if 'x' in d_r: 
                d_r['y'] += -5*d_i['x'] # (np.eye(nn)*5).dot(d_i['x'])
            # if 'y' in d_r: 
            #     d_r['y'] += d_o['y']
        
        else: # rev
            pass
    else: # neg 
        if mode == 'fwd': 
            if 'x' in d_r: 
                d_r['y'] -= -5*d_i['x'] # (np.eye(nn)*5).dot(d_i['x'])
            # if 'y' in d_r: 
            #     d_r['y'] -= d_o['y']
        
        else: # rev
            pass
     
def Y_solve_linear(rhs_vec, sol_vec): 
    sol_vec['y'][:] = rhs_vec['y']


def Z_apply_linear(inputs, outputs, d_i, d_o, d_r, mode='fwd', sign='pos'): 

    if sign == "pos":
        if mode == "fwd": 
            d_r['z'] += -3*inputs['x']**2 * d_i['x'] # np.diag(3*inputs['x']**2).dot(d_i['x'])

            d_r['z'] += -2*inputs['y'] * d_i['y']

            # if 'z' in d_r: 
            #     d_r['y'] += d_o['y']
        else: # rev
            pass
    else: # neg

        if mode == "fwd": 
            d_r['z'] -= -3*inputs['x']**2 * d_i['x'] # np.diag(3*inputs['x']**2).dot(d_i['x'])

            d_r['z'] -= -2*inputs['y'] * d_i['y']

        else: # rev
            pass

def Z_solve_linear(rhs_vec, sol_vec): 
    sol_vec['z'][:] = rhs_vec['z']

if __name__ == "__main__": 

    print(50*'#')
    print('# Nonlinear run')
    print(50*'#')
    print('init:', data)
    print()


    X(nl_vec, nl_vec)
    print('after X:', data)
    print()

    Y(nl_vec, nl_vec)
    print('after Y:', data)
    print()

    Z(nl_vec, nl_vec)
    print('after Z:', data)
    print()

    print()
    print()


    print(50*'#')
    print('# Linear run')
    print(50*'#')

    data_r[:] = 0
    data_o[:] = 0

    # ln_r['x'][:3] = 1.
    ln_r['x'][0] = 1.

    print('init rhs', data_r)
    print('.       ', data_o)

    print('X block')
    X_apply_linear(nl_vec, nl_vec, ln_o, ln_o, ln_r, mode='fwd', sign='neg')
    print('  X apply', data_r)
    X_solve_linear(ln_r, ln_o)
    print('  X solve', data_r)
    print('         ', data_o)

    print('Y block')
    Y_apply_linear(nl_vec, nl_vec, ln_o, ln_o, ln_r, mode='fwd', sign='neg')
    print('  Y apply', data_r)
    Y_solve_linear(ln_r, ln_o)
    print('  Y solve', data_r)
    print('         ', data_o)

    print('Z block')
    Z_apply_linear(nl_vec, nl_vec, ln_o, ln_o, ln_r, mode='fwd', sign='neg')
    print('  Z apply', data_r)
    Z_solve_linear(ln_r, ln_o)
    print('  Z solve', data_r)
    print('         ', data_o)


    print('CS check')
    data_r[:] = data
    print(data_r)
    data_r[0] += .000001
    print(data_r)

    # X(ln_r, ln_r)
    Y(ln_r, ln_r)
    Z(ln_r, ln_r)


    fd_check = (ln_r['z'] - nl_vec['z'])/.000001
    print('fd ', fd_check)


    # want dz/dx








