from sympy import randprime
import random
from math import gcd
import os
import json

def generate_prime(bits: int):
    """
    Generate a prime number with the specified number of bits.

    Parameters:
    ----------------
    bits: int
        The number of bits the prime number should have.

    Returns:
    ----------------
    prime : int
        A prime number with the specified number of bits.
    """
    min_value = 2 ** (bits - 1)
    max_value = (2 ** bits) - 1
    prime = randprime(min_value, max_value)
    return prime

def find_e(phi_n):
    """
    Find a number e such that 1 < e < phi_n and gcd(e, phi_n) = 1.

    Parameters:
    ----------------
    phi_n : int
        The value of Euler's totient function for n.
    
    Returns:
    ----------------
    e : int
        A number that satisfies the conditions.
    """
    while True:
      e = random.randint(2, phi_n-1)
      if gcd(e, phi_n) == 1:
          return e
      
def find_d(e, phi_n):
    """
    Find the modular inverse d of e modulo phi_n.

    Parameters:
    ----------------
    e : int
        The public exponent.
    phi_n : int
        The value of Euler's totient function for n.
    
    Returns:
    ----------------
    d : int
        The modular inverse of e modulo phi_n.
    """
    # Using the extended Euclidean algorithm to find the modular inverse
    def extendedEuclid(a, b):
        if b == 0:
            return a, 1, 0
        else:
            d2, x2, y2 = extendedEuclid(b, a % b)
            d, x, y = d2, y2, x2 - (a // b) * y2
        return d, x, y
    # The modular inverse of e is the d that satisfies the equation e * d ≡ 1 (mod phi(n))
    d = extendedEuclid(e, phi_n)[1] % phi_n
    
    return d

def generate_keys(bits: int):
    """
    Generate public and private keys using the RSA algorithm.

    Parameters:
    ----------------
    bits : int
        The number of bits the key should have.

    Returns:
    ----------------
    public_key : tuple
        The public key.
    private_key : tuple
        The private key.
    """
    p = generate_prime(bits//2)
    # make sure they are not the same    
    while True:
        q = generate_prime(bits//2)
        if p != q:
            break
    # calculate phi_n : totient function
    phi_n = (p - 1) * (q - 1)

    # determine e and d
    public_exponent = find_e(phi_n)
    private_exponent = find_d(public_exponent, phi_n)

    modulus = p * q
    
    public_key = (public_exponent, modulus)
    private_key = (private_exponent, modulus)

    return public_key, private_key

def encrypt(message, public_key):
    """
    Encrypt a message using the RSA algorithm.

    Parameters:
    ----------------
    message : str
        The message to encrypt.
    public_key : tuple
        The public key to use for encryption.

    Returns:
    ----------------
    encrypted_message : list
        The encrypted message.
    """

    # unpack the public key
    e, n = public_key

    # convert the message to a list of integers
    message = [ord(char) for char in message]

    # encrypt the message
    encrypted_message = [pow(char, e, n) for char in message]

    return encrypted_message

def decrypt(encrypted_message, private_key):
    """
    Decrypt a message using the RSA algorithm.

    Parameters:
    ----------------
    encrypted_message : list
        The encrypted message.
    private_key : tuple
        The private key to use for decryption.

    Returns:
    ----------------
    message : str
        The decrypted message.
    """
    # unpack the public key
    d, n = private_key

    # decrypt the message
    decrypted_message = [pow(char, d, n) for char in encrypted_message]

    # convert the decrypted message to a string
    message = ''.join([chr(char) for char in decrypted_message])

    return message

def shor_algorithm(public_key: list):
    """
    Break RSA algorithm by finding the private key for a given public key.

    Parameters:
    ----------------
    public_key : list
        The public key to break.
    
    Returns:
    ----------------
    private_key : list
        The private key for the given public key.
    """
    n = public_key[1]
    e = public_key[0]
    p = 0
    q = 0
    # choose a random number g
    g = random.randint(2, n-1)
    if g % n == 0: # if g is a multiple of n, then we have found a factor
        print("*Found a factor randomly: ", g)
        p = g
        q = n // g
    else:
        # find the period r of g^x mod n
        r = 1
        print(f"*Trying to find a period r for the given g : {g}...")
        while True:
            if r > n:
                print("*Could not find a period. Trying again...")
                return shor_algorithm(public_key)
            if pow(g, r, n) == 1:
                break
            r += 1
        if r % 2 != 0:
            print(f"*Found an odd period r : {r} for the given g : {g}. Trying again...")
            return shor_algorithm(public_key)
        else:
            print(f"*Found a suitable r : {r} for the given g : {g}")
            candidate = pow(g, r // 2) - 1
            p = gcd(candidate, n)
            if p != 1 and p != n:
                q = n // p
            else:
                print("*Period gave trivial factor, trying again...")
                return shor_algorithm(public_key)
    
    phi_n = (p - 1) * (q - 1)
    d = find_d(e, phi_n)
    private_key = [d, n]
    return private_key


def IO(file, input=None, output=None):
    """
    Read or write data to a JSON file.

    Parameters:
    ----------------
    file : str
        The file to read or write to.
    input : str
        The data to write to the file.
    output : str
        The data to extract from the file.

    Returns:
    ----------------
    data : str
        The data read from the file.
    """
    if input != None:
        # Create file if not exists
        if not os.path.exists(file):
            print(f"File {file} does not exist. Creating a new file...")
            with open(file, "w") as f:
                f.write("{}")
        # Read the file and update the data
        with open(file, "r") as f:
            data = json.load(f)
        for key in input.keys():
            data[key] = input[key]
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
        return
    elif output != None:
        assert os.path.exists(file), f"File {file} does not exist."
        with open(file, "r") as file:
            data = json.load(file)
        value = data.get(output)
        if output == "public_key" or output == "private_key":
            assert value != None, f"Please generate keys first using -a generate_keys."
        else:
            assert value != None, f"Please encrypt a message first using -a encrypt."
        return value
    else:
        assert "You must specify either input or output argument."
