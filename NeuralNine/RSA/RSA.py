import random
import math

def is_prime (number):

    if number < 2:
        return False
    
    #On vérife si la première motié des chiffres divise notre chiffre
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return  False
    
    return True

def generate_prime(min_val, max_val):
    prime = random.randint(min_val, max_val)
    while not is_prime(prime):
        prime = random.randint(min_val, max_val)

    return prime

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d*e) % phi == 1:
            return d
    
    raise ValueError("mod_inverse doesn't exist")

#Main

#Generate two primes number
p, q = generate_prime(1_000, 5_000), generate_prime(1_000, 5_000)

#If it's the same change
while p == q:
    q = generate_prime(1_000, 5_000)

#N is the factor of two primes number, and it will serve as a modulo
n = p * q
#Euler totient function, count the number between 1 and n-1, are prime with n
phi_n = (p-1) * (q-1)

#Generate public key
e = random.randint(3, phi_n-1)
#If the public key and the 
while math.gcd(e, phi_n) != 1:
    e = random.randint(3, phi_n-1)

#Generate a private key
d = mod_inverse(e, phi_n)

print("")
print("Public key: ", e)
print("Private key: ", d)
print("Phi_n: ", phi_n)
print("p: ", p)
print("q: ", q)

#Public 
#e

#Private
#d, phi_n, p, q

#Message
message = "Hello world"
print("message to  send: ", message)
message_encoded = [ord(c) for c in message]

#Crypt
# (m**e) mod n = c
crypt_message =  [pow(c, e, n) for c in message_encoded]
print(crypt_message)

#Decrypt
# (c**d) mod n = m
decrypt_message =  [pow(ch, d, n) for ch in crypt_message]
new_message = "".join(chr(ch) for ch in decrypt_message)

print("message decrypt: ", new_message)