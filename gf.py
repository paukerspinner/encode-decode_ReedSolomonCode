def gf_pow(x, power):
    return gf_exp[(gf_log[x] * power) % field_char]

def gf_mul(x,y):
    if x==0 or y==0:
        return 0
    return gf_exp[(gf_log[x] + gf_log[y]) % field_char]

def gf_sub(x, y):
    return x ^ y
    
def gf_div(x,y):
    if y==0:
        raise ZeroDivisionError()
    if x==0:
        return 0
    return gf_exp[(gf_log[x] + field_char - gf_log[y]) % field_char]

def gf_poly_mul(p,q):
    #Multiply two polynomials, inside Galois Field
    r = [0] * (len(p)+len(q)-1)
    for j in range(0, len(q)):
        for i in range(0, len(p)):
            r[i+j] ^= gf_mul(p[i], q[j])
    return r

def gf_poly_eval(poly, x):
    #Evaluates a polynomial in GF(2^p) given the value for x.
    y = poly[0]
    for i in range(1, len(poly)):
        y = gf_mul(y, x) ^ poly[i]
    return y

def gf_poly_scale(p,x):
    r = [0] * len(p)
    for i in range(0, len(p)):
        r[i] = gf_mul(p[i], x)
    return r

def gf_inverse(x):
    return gf_exp[field_char - gf_log[x]]

def gf_poly_add(p,q):
    r = [0] * max(len(p),len(q))
    for i in range(0,len(p)):
        r[i+len(r)-len(p)] = p[i]
    for i in range(0,len(q)):
        r[i+len(r)-len(q)] ^= q[i]
    return r

def gf_poly_div(dividend, divisor):
    #Polynomial division
    msg_out = list(dividend)
    for i in range(0, len(dividend) - (len(divisor)-1)):
        coef = msg_out[i]
        if coef != 0: 
            for j in range(1, len(divisor)):
                if divisor[j] != 0: # log(0) is undefined
                    msg_out[i + j] ^= gf_mul(divisor[j], coef)

    separator = -(len(divisor)-1)
    return msg_out[:separator], msg_out[separator:] # return quotient, remainder.

# list default primitive elements
prims = [0,0x3,0x7,0xB,0x13,0x25,0x43,0x83,0x11D, 0x211, 0x409, 0x805, 0x1052]

def gf_get_prim_of_field(exp):
    return prims[exp]

def gf_get_suitable_field(n):
    exp = 1
    while (n >= 2**exp and exp < 12):
        exp += 1
    return exp

def init_tables(prim=0x11D, c_exp = 8):
    # create log table and anti-log table
    global gf_exp, gf_log, field_char
    field_char = 2**c_exp - 1
    gf_log = [0] * ( field_char + 1) # log table
    x = 1
    gf_exp = [x]
    for i in range(1, 2**c_exp - 1):
        x = x << 1
        if (x >= 2**c_exp): x = x ^ prim
        gf_exp += [x]
    gf_exp *= 2
    for i in range(1, 2**c_exp - 1):
        gf_log[gf_exp[i]] = i
    return [gf_log, gf_exp, field_char]