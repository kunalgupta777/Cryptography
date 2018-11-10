## Merkle-Hellman Knapsack Cryptosystem - Kunal Gupta - 735 IT 15 - NSIT Delhi
### Quick Intro to the Merkle - Hellman Knapsack Cryptosystem

### The Merkle - Hellman Knapsack Cryptosystem is a public-key cryptosystem which relies on the NP-complete subset sum problem
### It has 3 parts:
### 1.) Key Generation
### 2.) Encryption 
### 3.) Decryption

### As it happens in asymmetric cryptography algorithms, Merkle Hellman Knapsack uses the public key to encrypt the data and the
### private key to decrypt it. Both the "keys" as we call them are nothing but some mathematical objects that are related to each 
### other via some mathematical relationship. This relationship is generally hard to figure out if we dont know certain parameters
### Read on for more details
'''
    1.) Key Generation
    We will construct a public key and a private key
    Before constructing the keys, let's first see how will use our plaintext message and convert it to a suitable form
    The plaintext message consists of standard characters which can be represented by 8-bit ASCII code.
    So we will convert each character into its 8bit ASCII equivalent and encrypt those 8 bits
    
    So, let's set n = 8, the chunk size
    Now, we will build a superincreasing sequence of 'n' nonzero natural numbers
    w = (w1, w2, w3, ...., wn)
    A superincreasing sequence is a sequence in which each element wi is strictly greater than the sum of all previous elements
    
    Next step, now select a random integer 'q', such that:
        q > sum(w)
    Now, select another random integer 'r' such that:
        gcd(q,r) = 1
    Finally, calculate the sequence:
    beta = (b1, b2, b3, ...., bn)
    where 
        bi = (r*wi) mod q
    
    The public key is beta, and the private key is the tuple (w, q, r)
    
    2.) Encryption
    To encrypt a character, as mentioned before, we use its ASCII 8-bit representation
    Let the general 'n' bit representation be called as alpha
    or
        alpha = (a1, a2, a3, ....., an)
    We encrypt the plaintext character to a ciphertext character given by
        c = sum(i = 1 to n) ai*bi
    
    3.) Decryption
    Finally, to decrypt the ciphertext, normally, a cracker would have to solve the subset sum problem, i.e. 
    given 
        c = ai*bi for i = 1 to n
    and we know beta, we would have to find alpha = (a1, a2, ... an)
    This is an NP hard problem.
    Here is where, our private key comes into action.
    Recall that our private key was : (w, q, r)
    Also, we constructed beta, the public key, in a special way, so that we can retrieve alpha more efficiently.
    The key to decrypt is an integer 's' such that:
        r*s = 1 mod q 
        OR
        r*s mod q = 1
    This integer 's' can be found out using the Extended Euclidean Algorithm efficiently
    After we compute 's', we calculate
    c' = cs mod q
    OR
    c' = sum(ai*bi*s mod q for i =1 to n)
    OR
    c' = sum(ai*wi*r*s mod q for i = 1 to n)
    But since, r*s mod q = 1
    So,
    c' = sum(ai*wi for i =1 to n)
    So, now we converted our subset sum problem to a simpler version where w is a supersequence
    Hence alpha can now be found out efficiently in linear time.
    Hence we can decrypt the message!
    :)
    
'''
### Having described all the necessary steps, let's dive in straight into the code! :)

import math
import random
import fractions


def generate_keys(n=8):
    
    ## first create a superincreasing sequence of length 'n'
    seed = random.randint(2,10)
    super_sequence = [seed]
    
    for i in range(n-1):
        sum_so_far = sum(super_sequence)
        element = random.randint(sum_so_far+1, 2*sum_so_far)
        super_sequence.append(element)
    
    ## now select a random integer q such that q > sum(super_sequence)
    q = random.randint(sum(super_sequence)+1, 2*sum(super_sequence))
    
    ## now select another random integer 'r' such that gcd(q,r) = 1
    r = 2
    while True:
        r = random.randint(2,q-1)
        if fractions.gcd(q,r) == 1:
            break
    ## Finally, calculate beta - the public key
    
    beta = tuple( (r*super_sequence[i])%q for i in range(n) ) ## making beta as a tuple, as tuples are immutable 
    
    private_key = (super_sequence, q, r)
    
    return beta, private_key

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

##The below function finds alpha as a part of decryption
def getalpha(c,w):
    w = w[::-1]
    alpha = []
    for number in w:
        if number > c:
            alpha.append(0)
        else:
            alpha.append(1)
            c = c - number
    return alpha[::-1]
            

def encrypt(plaintext_message, public_key):
    ## Now, we encrypt the message character by character and use the 8bit ASCII representation to encrypt the bytes
    ciphertext = []
    print "Character\tASCII in Decimal\tASCII in Binary\t\tCiphertext Number"
    for character in plaintext_message:
        binary = bin(ord(character))
        binary = binary[0]+binary[2:]
        l = len(binary)
        binary = (8-l)*"0"+binary
        print character+"\t\t"+str(ord(character))+"\t\t\t"+binary,
        binary = map(int,binary)
        # now, binary is an 8 element list, containing bits of binary representation of the character
        # ciphertext 'c' is calculated now
        c = sum([ binary[i]*public_key[i] for i in range(len(public_key)) ])
        print "\t\t",c
        ciphertext.append(c)
    return ciphertext

def decrypt(ciphertext, private_key):
    #First, we calculate the integer 's' , which has the property that:
    # r*s = 1 mod q
    
    #unpack private key
    super_sequence, q, r = private_key
    s = invmod(r, q)
    print "s = ",s
    # finding c' = modified ciphertext
    modified_ciphertext = [ (ciphertext[i]*s)%q for i in range(len(ciphertext)) ]
    
    decrypted_text = []
    ## Now, for each modified ciphertext, we will find the actual alpha sequence 
    print "Ciphertext Number \t Modified Ciphertext Number \t Computed Alpha \t ASCII character equivalent"
    i = 0
    for c in modified_ciphertext:
        alpha = getalpha(c,super_sequence)
        alpha = "".join(map(str, alpha))
        decrypted_text.append(chr(int(alpha,2)))
        print str(ciphertext[i])+"\t\t\t "+str(c)+"\t\t\t\t "+alpha+"\t\t "+chr(int(alpha,2))
        i+=1
    
    return "".join(decrypted_text)

if __name__ == "__main__":
    
    print "---------------------KNAPSACK CRYPTOSYSTEM-----------------------"
    public_key, private_key = generate_keys()
    message = str(raw_input("Enter the message to be encrypted:"))
    
    print "------------------------------------------------------------------"
    print "The Randomly Generated Public Key for the Encryption is:",public_key
    ciphertext = encrypt(message, public_key)
    print "-------------------------------------------------------------------"
    print "Cipher Text after Encryption is:\n\n","".join(map(str,ciphertext))
    
    print "\n------------------------------------------------------------------"
    print "The Equivalent Private Key used for Decryption is:(w, q, r)", private_key
    plaintext = decrypt(ciphertext, private_key)
    print "------------------------------------------------------------------"
    print "Decrypted Ciphertext is:\n\n\t",plaintext
    print "\n------------------------------------------------------------------"
    
        
    
    
    
        
    
    