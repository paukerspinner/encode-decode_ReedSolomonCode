import random
from math import sqrt, exp, pi, sin, inf, log
from scipy.integrate import quad
import numpy.random
from scipy.stats import norm

def make_random_noise(messcc, proba_error):     # probability of error
    out_messcc = list(messcc)
    for i in range(0, len(messcc)):
        if random.random() < proba_error:
            out_messcc[i] = make_error(messcc[i], 0, len(messcc) - 1)
    
    num_error = 0
    for i in range(0, len(messcc)):
        if messcc[i] != out_messcc[i]: num_error += 1
    return out_messcc, num_error

def get_random_indexes(num, start, end):  # from [start] to [end-1]
    array = []
    for i in range(0, num):
        index = random.randint(start, end - 1)
        while (index in array):
            index = random.randint(start, end - 1)
        array.append(index)
    return array

def make_error(value, min, max):
    # make random another value
    new_value = random.randint(min, max)
    while (new_value == value):
        new_value = random.randint(min, max)
    return new_value

def make_n_noise(mesecc, num_error):
    # make n errors in mesecc
    out_mesecc = mesecc
    error_indexes = get_random_indexes(num_error, 0, len(mesecc) - 1)
    for i in error_indexes:
        out_mesecc[i] = make_error(mesecc[i], 0, len(mesecc) - 1)
    return out_mesecc

def modulate_binary_amplitude(mesecc, elem_bits):
    mesecc_bin = []
    for elem in mesecc:
        elem_bin = list(bin(elem)[2:].zfill(elem_bits))
        mesecc_bin += elem_bin
    return [1 if x == '1' else -1 for x in mesecc_bin]

def genarate_vector_noise_binary(mesecc, elem_bits, loc, scale):
    noise_bin = [0] * len(mesecc) * elem_bits
    for i in range(len(noise_bin)):
        noise_bin[i] = round(norm.rvs(loc, scale), 1)
    return noise_bin

def get_mesecc_with_noise_bin(mesecc_bin, vector_noise_bin):
    sum_vector = [mesecc_bin[i] + vector_noise_bin[i] for i in range(len(mesecc_bin))]
    return ['0' if y <= 0 else '1' for y in sum_vector]

def get_received_mesecc(mesecc_noise_bin, elem_bits):
    mesecc_out = []
    for i in range(0, len(mesecc_noise_bin), elem_bits):
        elem = mesecc_noise_bin[i:i+elem_bits:1]
        mesecc_out.append(int(''.join(elem), 2))
    return mesecc_out

def make_gaussian_noise(mesecc, loc, scale):
    elem_bits = int(log(len(mesecc) + 1, 2))
    vector_x = modulate_binary_amplitude(mesecc, elem_bits)
    vector_e = genarate_vector_noise_binary(mesecc, elem_bits, loc, scale)
    vector_y = get_mesecc_with_noise_bin(vector_x, vector_e)
    received_mesecc = get_received_mesecc(vector_y, elem_bits)
    num_errors = 0
    for i in range(len(mesecc)):
        if mesecc[i] != received_mesecc[i]:
            num_errors += 1
    return received_mesecc, num_errors
