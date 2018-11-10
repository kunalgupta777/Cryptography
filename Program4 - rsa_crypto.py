### RSA Algorithm Implementation:- Kunal Gupta - 735 IT 15, NSIT Delhi
### RSA -  Rivest Shamir Adleman cryptography algorithm

### Quick Intro to RSA
### RSA is an asymmetric cryptography system which consists of a public key and a private key
### The public key, as the name suggests is open to all and one can encrypt a plaintext using it.
### The sender uses this public key to encrypt the message and send it to the receiver
### The receiver has a private key which is known only to him. Using that private key, the receiver decrypts the message

### Prime Number Factorisation is a computationally expensive problem, this is what is at the core of RSA
### We take 2 large prime numbers and create keys by applying a bunch of mathematical operations on them
### The cracker has to know the specific factorisation we used while encrypting in order to successfully decrypt the message
### The Algorithm works this way:
'''
    Take any 2 large, distinct prime numbers - p and q
    Let n = p*q
    Let f(n) = lcm(p-1,q-1) also called as Carmichael's Totient Function
    Now, select a number 'e' such that:
        1 < e < f(n)
        gcd(e,f(n)) = 1
    The public key pair is now: (n,e)
    Now, we compute the private key as follows:
    Find a 'd' such that
        d*e mod f(n) = 1
        or d = e^(-1) mod f(n)
    The private key pair is now: (n,d)
    The ciphertext 'c' is generated as:
    c = m^e mod n
    where m the plaintext message
    The plaintext is retrieved as:
    m = c^d mod n
'''

from fractions import gcd
import random 

def isprime(n):
    if n==2:
        return True
    if n%2==0 or n%3==0:
        return False
    i = 4
    while i*i <= n:
        if n%i == 0:
            return False
        i+=2
    return True

def generate_large_prime_number():
    while True:
        x = random.randint(10000,1000000)
        if isprime(x)==True:
            return x

def lcm(x,y):
    return (x*y) / gcd(x,y)

def f(n,p,q):
    return lcm(p-1,q-1)

def invmod(a,m):
    ### We have to find an integer x such that a*x = 1 mod m
    ### Obviously, x can be in between (1, m-1)
    ### The Below code uses the iterative version of the Extended Euclidean Algorithm to compute multiplicative inverse modulus
    m0 = m 
    y = 0
    x = 1
  
    if (m == 1) : 
        return 0
  
    while (a > 1) : 
  
        # q is quotient 
        q = a // m 
  
        t = m 
  
        # m is remainder now, process 
        # same as Euclid's algo 
        m = a % m 
        a = t 
        t = y 
  
        # Update x and y 
        y = x - q * y 
        x = t 
  
  
    # Make x positive 
    if (x < 0) : 
        x = x + m0 
  
    return x 

def get_public_key(fn):
    while True:
        e = random.randint(2,fn-1)
        if gcd(e,fn)==1:
            return e

def get_private_key(e,fn):
    d = invmod(e,fn)
    return d

def rsa_encrypt(message, e, n):
    ciphertext_numbers = []
    ciphertext = []
    for i in range(len(message)):
        m = ord(message[i])
        c = pow(m,e,n)
        ciphertext_numbers.append(c)
        ciphertext.append(chr(c%256))
    return "".join(ciphertext), ciphertext_numbers

    
    

def rsa_decrypt(ciphertext_numbers, ciphertext, d, n):
    plaintext_numbers = []
    plaintext = []
    for i in range(len(ciphertext_numbers)):
        c = ciphertext_numbers[i]
        m = pow(c,d,n)
        plaintext_numbers.append(m)
        plaintext.append(chr(m%256))
    return "".join(plaintext),plaintext_numbers

def print_encryption_parameters(p,q,n,fn,e,d):
    print "-----------------------------Encryption Parameters--------------------------------------"
    print "1st Large Prime Number p:",p
    print "2nd Large Prime Number q:",q
    print "n = p*q = ",n
    print "f(n) = lcm(p-1,q-1) = ",fn
    print "Public Key Pair (e, n): ("+str(e)+","+str(n)+")"
    print "Private Key Pair (d, n): ("+str(d)+","+str(n)+")"
    print "----------------------------------------------------------------------------------------"


if __name__ == "__main__":
    print "-----------------------------RSA Crytography System-------------------------------------"
    message = str(raw_input("Enter a plaintext message you want to encrypt:"))
    
    message_to_numbers = [ ord(message[i]) for i in range(len(message)) ]
    
    print "Message in String:",message
    print "Message in Numbers ( ASCII mapping ):",message_to_numbers
    
    ## generating encryption parameters
    p,q = generate_large_prime_number(), generate_large_prime_number()
    n = p*q  
    fn = f(n,p,q)
    e = get_public_key(fn)
    d = get_private_key(e,fn)
    print_encryption_parameters(p,q,n,fn,e,d)
    
    ## begin with encryption
    ciphertext, ciphertext_numbers = rsa_encrypt(message, e, n)
    print "The Ciphertext Message is:", ciphertext
    print "Ciphertext Numbers:", ciphertext_numbers
    
    ## begin with decryption
    plaintext, plaintext_numbers = rsa_decrypt(ciphertext_numbers, ciphertext, d, n)
    print "The Plain Text decrypted is:", plaintext
    print "Plain Text Numbers: ", plaintext_numbers
    print "Original Message Numbers: ",message_to_numbers

