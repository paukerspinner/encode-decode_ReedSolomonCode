import test as ts
import encoder, decoder
import gf
from datetime import datetime

# function for set code. For example, set_rs_code(3,2) to set RS(7,3)
def set_rs_code(m, t):
    global n, k
    n = 2**m - 1
    k = n - 2*t
    print("RS(%d, %d)" % (n, k))
    exp_field = gf.gf_get_suitable_field(n)
    encoder.make_field(gf.gf_get_prim_of_field(exp_field), exp_field)
    decoder.make_field(gf.gf_get_prim_of_field(exp_field), exp_field)

# Configuration of the parameters and input message
b = 0
m = 6
t = 16

set_rs_code(m, t)

def test():
	ts.make_one_test(n, k, b)

def ntest():
	N = int(input("Enter number test N = "))
	for i in range(N):
		try:
			print("\nTest %d:" % (i+1))
			ts.make_one_test(n, k, b)
		except:
			pass

test()
ntest()

'''
### For test code

# t0 = (d-1)/2
def getFER_t0():
    arr = []
    for m in range(4, 10):
        fer = ts.getFER(m, 2**(m-2), 0)
        arr.append(fer)
    return arr

# t1 = (d-1)/2+1
def getFER_t1():
    arr = []
    for m in range(4, 10):
        fer = ts.getFER(m, 2**(m-2) + 1, 0)
        arr.append(fer)
    return arr

# create FER diagram
ts.create_diagram_FER(n, k)
'''
