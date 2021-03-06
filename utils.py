from operator import mul
from fractions import gcd
from random import randint

# Checks if n is pairwise relatively prime with every number in a list
def is_rel_prime(n, numlist):
    for m in numlist:
        if not n == m and not gcd(n, m) == 1:
            return False
    return True

# Helper funtions to return the multiplicative inverse of a mod m
# This is the Extended Euclidean algorthm code from wikibooks
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# Following the Generalized Chinese Remainder Thm,
# this function takes in a list of remainders [r_1,...,r_s]
# and moduli [m_1,...,m_s] and solves the system of the form
# x = r_1 (mod m_1),..., x = r_s (mod m_s) for the unique solution
# that is the least residue of x (mod m_1*...*m_s).
def solve_system(remainders, moduli):
    if not len(remainders) == len(moduli):
        raise Exception('The number of remainders must match the number of moduli')
    M = reduce(mul, moduli, 1) # M is the product of the moduli
    M_k = []
    for m in moduli:
        M_k.append(M/m)
    # print M_k
    y_k = []
    for i in range(0, len(M_k)):
        y_k.append(modinv(M_k[i], moduli[i]))
    # print y_k
    x = 0
    for i in range(0, len(M_k)):
        # print "adding the product of ", remainders[i], M_k[i], y_k[i]
        x += remainders[i]*M_k[i]*y_k[i]
    # print x
    return (x % M)

# The following is the Miller Rabin primality test, from rosettacode.org
# It uses predetermined values of a so that it will give correct answers 
# for n less than 341550071728321.

def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True # n  is definitely composite
 
def is_prime(n, _precision_for_huge_n=16):
    if n in _known_primes or n in (0, 1):
        return True
    if any((n % p) == 0 for p in _known_primes):
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467: 
        if n == 3215031751: 
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s) 
                   for a in _known_primes[:_precision_for_huge_n])
 
_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if is_prime(x)]


# tries different numbers until it succesfully finds a prime number
def randprime(minimum=2, size="medium"):
    if size == "small":
        maximum = 1000
    if size == "medium":
        maximum = 1000000
    if size == "large":
        maximum = 1000000000
    if size == "xlarge":
        maximum=341550071728321
    n = randint(minimum, maximum)
    while not is_prime(n):
        n = randint(minimum, maximum)
    return n

# Generate a list of moduli such that none are divisible by p,
# they are relatively prime to each other, and the product of the
# s smallest moduli is greater than p * the s-1 greatest moduli
# This is done by trial and error and isn't very efficient.

def generate_m(p, s, ms):
    if ms == []:
        return p*s + 1
    m = randint(ms[-1], int(ms[-1]*1.5))
    while not is_rel_prime(m, ms) or m % p == 0:
        m = randint(ms[-1], int(ms[-1]*1.5))
    return m

def generate_moduli(p, s, r):
    ms = []
    while len(ms) < r:
        ms.append(generate_m(p, s, ms))
    while reduce(mul, ms[:s], 1) <= p*(reduce(mul, ms[-(s-1):], 1)):
        ms.pop(0)
        ms.append(generate_m(p, s, ms))
    return ms

def main():
    print solve_system([1, 2, 3, 4], [5, 7, 9, 11]), "Answer should be 1731"
    print solve_system([6, 4], [7, 8]), "Answer should be 20"
    print is_prime(100)
    print is_prime(109)
    print is_prime(23473804293)
    print is_prime(4658303019)

    p = randprime()
    print p
    print generate_moduli(p, 2, 5)

if __name__ == "__main__":
    main()
