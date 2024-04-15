import argparse
from sympy import randprime
import random
from math import gcd

def generate_prime(bits):
    min_value = 2 ** (bits - 1)
    max_value = (2 ** bits) - 1
    return randprime(min_value, max_value)

def find_e(phi_n):
    while True:
      e = random.randint(2, phi_n-1)
      if gcd(e, phi_n) == 1:
          return e
      
def find_d(e, phi_n):
    # Using the extended Euclidean algorithm to find the modular inverse
    def extendedEuclid(a, b):
        if b == 0:
            return a, 1, 0
        else:
            d2, x2, y2 = extendedEuclid(b, a % b)
            d, x, y = d2, y2, x2 - (a // b) * y2
        return d, x, y
    # The modular inverse of e is the d that satisfies the equation e * d ≡ 1 (mod phi(n))
    def multiplicativeInverse(e, phi_n):
        return extendedEuclid(e, phi_n)[1] % phi_n
    
    return multiplicativeInverse(e, phi_n)


# initialize the parser
parser = argparse.ArgumentParser(description="A script to generate keys using RSA algorithm.")

# add the arguments
parser.add_argument('--bits', type=int, default=2048, help='How muh bits the key should have.')

# parse the arguments
args = parser.parse_args()

# generate the primes
p = generate_prime(args.bits//2)
# make sure they are not the same    
while True:
    q = generate_prime(args.bits//2)
    if p != q:
        break
    
phi_n = (p - 1) * (q - 1)

# determine e and d
public_exponent = find_e(phi_n)
private_exponent = find_d(public_exponent, phi_n)

modulus = p * q

public_key = [public_exponent, modulus]
private_key = [private_exponent, modulus]

# save the keys to files
with open('keys.json', 'w') as f:
    f.write(f'{{\n\t"public_key": {public_key},\n\t"private_key": {private_key}\n}}')