from gf import *

def make_field(prim, c_exp):
    global gf_log, gf_exp, field_char
    gf_log, gf_exp, field_char = init_tables(prim, c_exp)

def rs_generator_poly(nsym, fcr):
    #Generate an irreducible generator polynomial
    g = [1]
    for i in range(0, nsym):
        g = gf_poly_mul(g, [1, gf_pow(2, i+fcr)])
    return g

def rs_encode_msg(msg_in, nsym, fcr):
    #Reed-Solomon main encoding function

    # compute generator polynomial
    gen = rs_generator_poly(nsym, fcr)

    # compute remaind
    _, remainder = gf_poly_div(msg_in + [0] * (len(gen)-1), gen)
    msg_out = msg_in + remainder
    return msg_out