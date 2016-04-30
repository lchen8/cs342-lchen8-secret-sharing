from operator import mul

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

def main():
    print solve_system([1, 2, 3, 4], [5, 7, 9, 11]), "Answer should be 1731"
    print solve_system([6, 4], [7, 8]), "Answer should be 20"
if __name__ == "__main__":
    main()
