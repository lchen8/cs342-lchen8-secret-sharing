import os
import sys
import utils
from fractions import gcd
from random import randint
from operator import mul

__author__ = "Lily Chen"

# Given k (the master key), s (the threshold), p (prime number) and 
# ms (a list of integers), output len(ms) shadows such that any s of them
# can recover the master key. Note that the ms must satisfy the following:
# (product of s smallest ms) > p*(product of s-1 largest ms)
def generate_shadows(k, s, p, ms, check=True):
    ms.sort()
    r = len(ms)
    #check if values meet requirements
    if check:
        if s > len(ms):
            raise Exception("Threshold cannot exceed the number of shadows.")
        if not utils.is_prime(p):
            raise Exception("p is not prime")
        for m in ms:
            if not utils.is_rel_prime(m, ms):
                raise Exception("The moduli must be pairwise relatively prime.")

    M = 1
    for i in range(0, s):
        M *= ms[i]
    largest = p
    for i in range(0, s-1):
        largest *= ms[r-1-i]
    if M <= largest:
        raise Exception("The product of the smallest s moduli must be greater than the product of the s-1 largest moduli times p.")

    #print "M = ", M
    t = randint(0, int(M/p))
    k0 = k + t*p 
    #print k0

    shadows = []
    for m in ms:
        shadows.append(k0 % m)

    return t, shadows

# This will recover the master key given the chosen values of p and t
# as well as a list shadows and the correspoding moduli
def recover_master(p, t, shadows, moduli):
    k0 = utils.solve_system(shadows, moduli)
    return k0 - t*p

# Usage:
# python secretsharing.py generate_shadows <filename> <key> <s> <r> <size='small','medium','large','xlarge'>(optional)
# python secretsharing.py recover_key <filename> <shadow index 1> <shadow index 2> ...
def main():
    print "* * * * *"
    mode = sys.argv[1] # "generate_shadows" or "recover_key"
    filename = sys.argv[2] # filename to read from or write to

    # generate shadows for key accoring to (s, r) threshold scheme
    if mode == "generate_shadows":
        # we do not want leftover files from previous sessions
        os.system("rm {}*".format(filename)) 
        k = int(sys.argv[3])
        s = int(sys.argv[4])
        r = int(sys.argv[5])
        if len(sys.argv) == 7:
            p = utils.randprime(k, sys.argv[6])
        else:
            p = utils.randprime(k)
        ms = utils.generate_moduli(p, s, r)
        # the generation process ensures that criteria are met; no need to check
        t, shadows = generate_shadows(k, s, p, ms, False)
        
        keyfile = open(filename+".key", 'w')
        keyfile.write(str(k))

        sharedfile = open(filename+".shared", 'w')
        sharedfile.write(str(s)+"\n"+str(p)+"\n"+str(t))

        print "Generating", r, "shadows for key =", k
        print "Randomized values for p and t are", p, "and", t
        print "The threshold is", s
        for i in range(0, r):
            shadowfile = open(filename+"-"+str(i+1)+".shadow", 'w')
            shadowfile.write(str(shadows[i]) + "\n" + str(ms[i]))
            print "Shadow",str(i+1),": s =", str(shadows[i]),", m =", str(ms[i])

        print "Done writing to files"

    #recover a key given at least s number of shadows
    if mode == "recover_key":
        with open(filename+".shared", 'r') as sharedfile:
            s = int(sharedfile.readline())
            p = int(sharedfile.readline())
            t = int(sharedfile.readline())

        if len(sys.argv) < (s+3):
            raise Exception("Cannot recover key without at least {} shadows".format(s))
        shadows = []
        ms = []
        for i in sys.argv[3:]:
            with open(filename+"-"+str(i)+".shadow") as shadowfile:
               shadows.append(int(shadowfile.readline()))
               ms.append(int(shadowfile.readline()))

        k = recover_master(p, t, shadows, ms)
        print "The master key is", k

    print "* * * * *"

if __name__ == "__main__":
    main()
