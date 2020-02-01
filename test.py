import random
import noise
import decoder
import encoder
import matplotlib.pyplot as plt
import numpy
from scipy.stats import norm
from math import sqrt, log10
from datetime import datetime

def make_random_message(lenth, max_value):
    msg = [0] * lenth
    for i in range(len(msg)):
        msg[i] = random.randint(1, max_value)
    return msg

def make_one_test(n, k, b):
    message = make_random_message(k, n)
    print("Sent random message: %s" % message)
    ecc_number = n - k
    #ecc_number = int(input("Enter number error correcting codes: "))
    # n = k + ecc_number # the remaining n-k symbols will be the ECC code (more is better)

    # Encoding the input message
    mesecc = encoder.rs_encode_msg(message, ecc_number, b)
    print("After encoding:		%s" % mesecc)

    received_messcc, error_number = noise.make_random_noise(mesecc, proba_error = 0.05)
    print("After making noise:	%s" % received_messcc)
    print("Number of error:	%d" % error_number)

    # Decoding/repairing the corrupted message
    corrected_message, corrected_ecc = decoder.rs_correct_msg(received_messcc, ecc_number, b)
    print("Repaired:		%s" % (corrected_message+corrected_ecc))
    print("Restore message: %s" % corrected_message[:k])


def make_test(n, k, b, prob_error):
    message = make_random_message(k, n)
    ecc_number = n - k
    # Encoding the input message
    #print("Message: %s" % message)
    mesecc = encoder.rs_encode_msg(message, ecc_number, b)
    #print("Sent:\t\t%s" % mesecc)
    # Make noise
    received_messcc, num_error = noise.make_random_noise(mesecc, prob_error)
    #print("Received:\t%s" % received_messcc)
    #print("Number ERROR: %d" % num_error)
    message_out, _= decoder.rs_correct_msg(received_messcc, ecc_number, b)
    #print("Corrected: %s" % corrected_message)
    return message == message_out

def make_test_gauss(n, k, b, SNR):
    message = make_random_message(k, n)
    ecc_number = n - k
    # Encoding the input message
    #print("Message: %s" % message)
    mesecc = encoder.rs_encode_msg(message, ecc_number, b)
    #print("Sent:\t\t%s" % mesecc)
    # Make noise
    sigma = sqrt(n / (2 * k * SNR))
    received_messcc, num_error = noise.make_gaussian_noise(mesecc, 0, sigma)
    #print("Received:\t%s" % received_messcc)
    #print("Number ERROR: %d" % num_error)
    message_out, corrected_message = decoder.rs_correct_msg(received_messcc, ecc_number, b)
    #print("Corrected: %s" % corrected_message)

def make_multi_test_gauss(num_test, n, k, b, SNR):
    num_fail_decode = 0
    for i in range(0, num_test):
        try:
            #print("\nTest %d: " % (i+1))
            make_test_gauss(n, k, b, SNR)
        except(Exception):
            num_fail_decode += 1
    return num_fail_decode

def make_multi_test(num_test, n, k, b, prob_error):
    num_fail_decode = 0
    for i in range(0, num_test):
        try:
            #print("\nTest %d: " % (i+1))
            make_test(n, k, b, prob_error)
        except(Exception):
            num_fail_decode += 1
    return num_fail_decode


def make_test_with_n_errors(m, t, b):
    n = 2**m - 1
    k = 2**(m-1) - 1
    message = make_random_message(k, n)
    mesecc = encoder.rs_encode_msg(message, n - k, b)
    received_mess = noise.make_n_noise(mesecc, t)
    decoder.rs_correct_msg(received_mess, n - k, b)

def getFER(m, t, b):
    num_test = 100
    fail_test = 0
    for i in range(0, num_test):
        try:
            make_test_with_n_errors(m, t, b)
        except:
            fail_test += 1
    return fail_test / num_test

# Create graphic FER for AWGN channel, RS(1023, 681)
def create_diagram_FER(n = 1023, k = 681):
    ox = numpy.arange(3, 3.05, 0.1)         # предсказанный размах SNR для РС(1023,681)
    oy = [make_multi_test_gauss(1000, n, k, 0, SNR)/1000 for SNR in ox]
    # delete values 0 (log(0) = infinite)
    ox = ox[0 : oy.index(0) : 1]
    oy = oy[0 : oy.index(0) : 1]
    plt.plot(ox, oy, marker='o')
    plt.xlabel("SNR(Eb/E0)")
    plt.ylabel("FER")
    plt.show()