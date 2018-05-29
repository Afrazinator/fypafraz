#!usr/bin/env python

# Please note that where used % denotes the modulo operator

#As defined in section 2 of the paper a robust extractor takes in input
#an integer modulo q, a signal sigma defined in the 'signal' function and a prime number q

from random import *
import numpy
from numpy import *
import datetime

#NB: x is a numpy array so conversion required, x is KA or KB

def print_time(s, instance):
    #s: seconds, instance: Reference in program execution
    s = s*1000 #Conversion to milliseconds

    print(instance + str(s) + " milliseconds.")

#This function must return either a 0 or a 1
def robust_extractor(x, sigma, q):
    return int((int(x)%q + sigma*((q-1)/2)%q)%2) #---> Because of the mod 2 operation

#b will determine what type of signal function you require, inputs are x as an integer mod q, q as a prime number and b (signal case)
def signal_functions(y, b, q):
    #print(y)
    if b == 0:
        if y >= -q/4 and y <= q/4:
            return 0
        else:
            return 1
    elif b == 1:
        if y >= -q/4 + 1 and y <= q/4 + 1:
            return 0
        else:
            return 1

def check_robust_extractor(x,y,q):
    delta = q/4 - 2
    if (x-y)%2 == 0 and abs(x-y) <= delta:
        return True
    else:
        return False

#This function makes an n x n matrix of integers mod q
def generate_matrix_M(n, q):
    return numpy.random.randint(q, size=(n,n))

def generate_gaussian_matrix(n):
    gaussian_matrix = numpy.zeros((n,n))
    # parameter selection, n = lambda, q = lambda ^ 4, alpha = (lambda)^(-3)
    q = n**4
    alpha = (1/float(n))**3
    mu = 0 #page 5 of the paper
    sigma = alpha*q
    return numpy.random.normal(mu,sigma,size=(n,n)).astype(int)

def generate_gaussian_vector(n):
    # parameter selection, n = lambda, q = lambda ^ 4, alpha = (lambda)^(-3)
    q = n**4
    alpha = (1/float(n))**3
    mu = 0 #page 5 of the paper
    sigma = alpha*q
    return numpy.random.normal(mu,sigma,n).astype(int)

def generate_gaussian_scalar():
    # parameter selection, n = lambda, q = lambda ^ 4.
    q = 1
    alpha = 1
    mu = 0
    sigma = alpha*q
    return numpy.random.normal(mu,sigma,1).astype(int)

def generate_alice_params(M,n,q):
    start_time = datetime.datetime.now()
    SA = generate_gaussian_matrix(n)
    EA = generate_gaussian_matrix(n)
    PA = (M.dot(SA) + 2*EA)
    end_time = datetime.datetime.now()
    print((end_time - start_time).total_seconds())
    return PA,SA

def generate_single_alice_params(M,n,q):
    sA = generate_gaussian_vector(n)
    eA = generate_gaussian_vector(n)
    pA = (M.dot(sA) + 2*eA)%q
    return pA, sA

def generate_bob_params(M,n,q):
    sB = generate_gaussian_vector(n)
    eB = generate_gaussian_vector(n)
    pB = (numpy.transpose(M).dot(sB) + 2*eB)%q
    return pB,sB

def generate_signal(n, KB, q):
    signal = []
    for i in range(0, n):
        signal.append(signal_functions(KB[i],0,q))
    return signal

def run_key_exchange(n,q):
    #M is a matrix of integers mod q and has dimensions n x n
    start_time = datetime.datetime.now()
    M = generate_matrix_M(n,q)
    end_time = datetime.datetime.now()
    print_time((end_time-start_time).total_seconds(), "Generating M took ")
    start_time = datetime.datetime.now()
    SA = generate_gaussian_matrix(n)
    EA = generate_gaussian_matrix(n)
    edashA = generate_gaussian_vector(n)
    end_time = datetime.datetime.now()
    print_time((end_time-start_time).total_seconds(), "Alice's parameters took ")
    start_time = datetime.datetime.now()
    pB,sB = generate_bob_params(M,n,q)
    edashB = 2 * generate_gaussian_vector(n)
    end_time = datetime.datetime.now()
    print_time((end_time-start_time).total_seconds(), "Bob's parameters took ")

    #Setup variables to reduce complexity
    m_dot = numpy.transpose(M).dot(sB)
    ea_transpose = numpy.transpose(2 * EA)
    sa_transpose = numpy.transpose(SA)

    #Generate the Keys
    start_time = datetime.datetime.now()
    KA = (numpy.transpose(SA).dot(pB) + 2*edashA)%q
    KB = ((sa_transpose.dot(m_dot) + (ea_transpose.dot(sB))) + edashB) % q
    end_time = datetime.datetime.now()
    print_time((end_time-start_time).total_seconds(), "KA and KB took ")
    #---------ensuring Robust extractor property is preserved--------

    start_time = datetime.datetime.now()
    i = 0 #INDEX REQUIRED FOR INCREMENTAL ROBUST EXTRACTOR
    #Keep on generating the parameters until robust extractor condition 3 is preserved

    while(i < n):
        if(not check_robust_extractor(KA[i], KB[i], q)):
            #Redo single params
            pA,sA = generate_single_alice_params(M,n,q)
            pB,sB = generate_bob_params(M,n,q)
            edash_single_A = generate_gaussian_scalar()
            edash_single_B = generate_gaussian_scalar()

            #Get KA[i]
            KA[i] = (numpy.transpose(sA).dot(pB) + 2*edash_single_A)%q
            KB[i] = (numpy.transpose(pA).dot(sB) + 2*edash_single_B)%q

        else:
            i += 1
    end_time = datetime.datetime.now()
    print_time((end_time - start_time).total_seconds(), "This while loop took ")
    signal = generate_signal(n, KB, q)
    #---------------Generating shared keys------
    SKA = []
    SKB = []
    for i in range(0, n):
        SKA.append(robust_extractor(KA[i],signal[i],q))
        SKB.append(robust_extractor(KB[i],signal[i],q))

    #-----------------Results-------------------
    if SKA == SKB:
        print("Alice and Bob share the same key!")

    #Comment this part underneath to get the correct results data from graphresults.py 
    """
    SKA = ''.join(map(str, SKA))
    SKB = ''.join(map(str, SKB))
    SKA = int(SKA)
    SKB = int(SKB)
    print("Alices Shared Key is:")
    print format(SKA, 'x')
    print("Bobs Shared Key is:")
    print format(SKB, 'x')
    """

def main():

    #Change the parameters here:
    n = 512
    q = 2**31 - 1
    start_time = datetime.datetime.now()
    run_key_exchange(n,q)
    end_time = datetime.datetime.now()
    print_time((end_time - start_time).total_seconds(), "This program took ")

#initialisation
if __name__ == "__main__":
    main()
