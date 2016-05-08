This is a secret sharing program written by me (Lily Chen) for my CS342 Computer Security final project. Last edited: May 2016

# Usage
(shadow generation) python secretsharing.py generate_shadows <output filename> <key> <threshold> <total shadows>
(key recovery) python secretsharing.py recover_key <input filename> <indices of available shadows>

# Example
python secretsharing.py generate_shadows mysecret 10 2 5
(break 10 into 5 shadows with threshold 2. This generates mysecret.key which holds the original key,
mysecret.shared which stores the threshold and the randomly generated p and t values, and
mysecret-<1,2,3,4,5>.txt which hold the (shadow, modulus) pairs from the algorithm.)

python secretsharing.py recover_key mysecret 3 4
(recover the key using mysecret-3.shadow and mysecret-4.shadow)

# The Algorithm
To create the shadows

1. Decide on a key K and a threshold scheme (s, r).
2. Choose prime p and pairwise co-prime m_1,...,m_r such that the product of the s smallest m’s is greater than p times the (s-1) largest m’s.
3. Let M be the product of the s smallest m’s.
4. Choose a random t such that 0 < t < (M/p). Let k_0 = K + t*p
5. Produce the shadows k_1, … , k_s via the equation k_i = k (mod m_i) for each i

To decrypt the key, you need to know p, t, and at least s of the (key, modulus) pairs.

1. By the Chinese Remainder Theorem, this system has a unique solution
2. Solve it using the Extended Euclidean Algorithm
3. Then K = x - t*p

Additionally, I referenced the following functions in utils.py:
Primality checking: https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test#Python 
Euclidean algorithm for multiplicative inverse modulo n: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
