import numpy as np

nn = 3

data = np.empty(nn*3)
nl_vec = {} # these dictionaries are analagous to the vector objects in OpenMDAO
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

    if sign == "pos": 
        if mode == "fwd": 
            if 'x' in d_r: 
                d_r['x'] += d_o['x']
        else: # rev
            if 'x' in d_o: 
                d_o['x'] += d_r['x']
    else: #neg 
        if mode == "fwd": 
            if 'x' in d_r: 
                d_r['x'] -= d_o['x']
        else: # rev
            if 'x' in d_o: 
                d_o['x'] -= d_r['x']

    
def X_solve_linear(rhs_vec, sol_vec): 
    sol_vec['x'][:] = rhs_vec['x']


def Y_apply_linear(inputs, outputs, d_i, d_o, d_r, mode='fwd', sign='pos'): 

    if sign == "pos": 
        if mode == 'fwd': 
            if 'y' in d_r: 
                if 'x' in d_i: 
                    d_r['y'] += -5*d_i['x'] # (np.eye(nn)*5).dot(d_i['x'])
                if 'y' in d_o: 
                    d_r['y'] += d_o['y']
        else: # rev
            if 'y' in d_r: 
                if 'x' in d_i: 
                    d_i['x'] += -5*d_r['y'] # (np.eye(nn)*5).dot(d_i['x'])
                if 'y' in d_o: 
                    d_o['y'] += d_r['y']
    else: # neg 
        if mode == 'fwd': 
            if 'y' in d_r: 
                if 'x' in d_i: 
                    d_r['y'] -= -5*d_i['x'] 
                if 'y' in d_o: 
                    d_r['y'] -= d_o['y']
        else: # rev
            if 'y' in d_r: 
                if 'x' in d_i: 
                    d_i['x'] -= -5*d_r['y'] 
                if 'y' in d_o: 
                    d_o['y'] -= d_r['y']
     
def Y_solve_linear(rhs_vec, sol_vec): 
    sol_vec['y'][:] = rhs_vec['y']


def Z_apply_linear(inputs, outputs, d_i, d_o, d_r, mode='fwd', sign='pos'): 

    if sign == "pos":
        if mode == "fwd": 
            if 'z' in d_r: 
                if 'x' in d_i: 
                    d_r['z'] += -3*inputs['x']**2 * d_i['x'] # np.diag(3*inputs['x']**2).dot(d_i['x'])
                if 'y' in d_i:
                    d_r['z'] += -2*inputs['y'] * d_i['y']
                if 'z' in d_o: 
                    d_r['z'] += d_o['z']

        else: # rev
            if 'z' in d_r: 
                if 'x' in d_i: 
                    d_i['x'] += -3*inputs['x']**2 * d_r['z'] 
                if 'y' in d_i:
                    d_i['y'] += -2*inputs['y'] * d_r['z']
                if 'z' in d_o: 
                    d_o['z'] += d_r['z']

    else: # neg

        if mode == "fwd": 
            if 'z' in d_r: 
                if 'x' in d_i: 
                    d_r['z'] -= -3*inputs['x']**2 * d_i['x'] # np.diag(3*inputs['x']**2).dot(d_i['x'])
                if 'y' in d_i:
                    d_r['z'] -= -2*inputs['y'] * d_i['y']
                if 'z' in d_o: 
                    d_r['z'] -= d_o['z']

        else: # rev
            if 'z' in d_r: 
                if 'x' in d_i: 
                    print('foo', d_r['z'], inputs['x'])
                    d_i['x'] -= -3*inputs['x']**2 * d_r['z'] 
                    print('bar', d_i['x'], inputs['x'])
                if 'y' in d_i:
                    d_i['y'] -= -2*inputs['y'] * d_r['z']
                if 'z' in d_o: 
                    d_o['z'] -= d_r['z']

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
    print('# Linear FWD run')
    print(50*'#')

    data_r[:] = 0
    data_o[:] = 0

    # put the seed in the dv of interest
    ln_r['x'][0] = 1.

    print('init rhs', 'r:', data_r)
    print('.       ', 'o: ', data_o)

    # note: ln_i is not actually used, instead we re-use ln_o here
    print('X block')
    X_apply_linear(nl_vec, nl_vec, ln_o, ln_o, ln_r, mode='fwd', sign='neg')
    print('  X apply', 'r: ', data_r)
    X_solve_linear(ln_r, ln_o)
    print('  X solve', 'r:', data_r)
    print('         ', 'o: ', data_o)

    print('Y block')
    Y_apply_linear(nl_vec, nl_vec, ln_o, ln_o, ln_r, mode='fwd', sign='neg')
    print('  Y apply', 'r:', data_r)
    Y_solve_linear(ln_r, ln_o)
    print('  Y solve', 'r: ', data_r)
    print('         ', 'o: ', data_o)

    print('Z block')
    Z_apply_linear(nl_vec, nl_vec, ln_o, ln_o, ln_r, mode='fwd', sign='neg')
    print('  Z apply', 'r:', data_r)
    Z_solve_linear(ln_r, ln_o)
    print('  Z solve', 'r:', data_r)
    print('         ', 'o: ', data_o)

    print('dZ/dx[0]', ln_o['z'])


    print(50*'#')
    print('# FD check')
    print(50*'#')

    # use  ln_r as a scratch vector for this check 
    # OpenMDAO does this to avoid allocating more memory for these checks
    data_r[:] = data #copy data into data_r (which is the memory associated with ln_r vector)
    ln_r['x'][0] += .000001

    # X(ln_r, ln_r) # don't call the X function, because it would mess up our increment for the FD
    Y(ln_r, ln_r)
    Z(ln_r, ln_r)


    # looking for dz/dx[0]
    fd_check = (ln_r['z'] - nl_vec['z'])/.000001
    print('fd ', fd_check)


    print(50*'#')
    print('# CS check')
    print(50*'#')

    data_cs = np.empty(nn*3, dtype=complex)
    # swap out the memory for the ln_r vector for a complex array
    ln_r['x'] = data_cs[:3]
    ln_r['y'] = data_cs[3:6]
    ln_r['z'] = data_cs[6:9]


    data_cs[:] = data #copy the nonlinear baseline into the memory for ln_r
    ln_r['x'][0] += complex(0,1e-50)

    Y(ln_r, ln_r)
    Z(ln_r, ln_r)

    # looking for dz/dx[0]
    cs_check = ln_r['z'].imag/1e-50
    print('cs ', cs_check)



    print(50*'#')
    print('# Linear REV run')
    print(50*'#')



    # swap the memory back to the real array (was just used for complex)
    ln_r['x'] = data_r[:3]
    ln_r['y'] = data_r[3:6]
    ln_r['z'] = data_r[6:9]

    data_r[:] = 0
    data_o[:] = 0

    # put the seed into the output of interest
    ln_r['z'][0] = 1.

    print('init rhs', 'r:', data_r)
    print('.       ', 'o: ', data_o)

    print('Z block')
    Z_solve_linear(ln_r, ln_o)
    print('  Z solve', 'r:', data_r)
    print('         ', 'o: ', data_o)
    Z_apply_linear(nl_vec, nl_vec, ln_r, ln_o, ln_r, mode='rev', sign='neg')
    print('  Z apply', 'r:', data_r)
   

    print('Y block')
    Y_solve_linear(ln_r, ln_o)
    print('  Y solve', 'r: ', data_r)
    print('         ', 'o: ', data_o)
    Y_apply_linear(nl_vec, nl_vec, ln_r, ln_o, ln_r, mode='rev', sign='neg')
    print('  Y apply', 'r:', data_r)


    print('X block')
    X_solve_linear(ln_r, ln_o)
    print('  X solve', 'r:', data_r)
    print('         ', 'o: ', data_o)
    X_apply_linear(nl_vec, nl_vec, ln_r, ln_o, ln_r, mode='rev', sign='neg')
    print('  X apply', 'r: ', data_r)


    print('dZ[0]/dx[0], dZ[0]/dx[1], dZ[0]/dx[2]', ln_r['x'])







