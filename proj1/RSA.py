import numpy as np
import math
import random
from Crypto.Util import number
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time


def draw_p_q(bitsnr):
    while True:
        p=number.getRandomNBitInteger(bitsnr)
        if number.isPrime(p):
            break
    while True:
        q=number.getRandomNBitInteger(bitsnr)
        if number.isPrime(q) and q!=p:
            break
    return p,q


def create_keys():
    keylen= 1032
    #keylen=1024
    bitsnr = int(keylen/2)

    while True:
        p,q = draw_p_q(bitsnr)
        n = p*q
        eul=(p-1)*(q-1)
        if eul.bit_length() == keylen:
            break

    while True:
        e=number.getRandomNBitInteger(bitsnr-1)
        if e<eul and number.GCD(e,eul) == 1:
            break

    d = number.inverse(e,eul)

    public_key=(n,e)
    private_key=(n,d)

    return public_key,private_key
    


def encryption(pixels):
    
    public_key,private_key=create_keys()
    block_size=128
    #print(private_key)
    """
    block_size=64
    f = open('mykey.pem','r')
    key=RSA.import_key(f.read())
    public_key=(key.n,key.e)
    private_key=(key.n,key.d)
    #print(key.n)
    #print(key.e)
    #print(key.d)
    """
    encrypted_pixels=[]
    i=0
    start = time.time()
    while (i<len(pixels)):
        block_of_pixels=bytearray(pixels[i:i+block_size])
        cipher=pow(int.from_bytes(block_of_pixels,'big'),public_key[1],public_key[0])
        block_of_encrypted_pixels=cipher.to_bytes(int(public_key[0].bit_length()/8),'big')
        #print(len(block_of_encrypted_pixels))

        for j in range(0,len(block_of_encrypted_pixels)):
            encrypted_pixels.append(block_of_encrypted_pixels[j].to_bytes(1,'big'))
        i=i+block_size
    end=time.time()
    print("Szyfrowanie ECD: "+str(end-start))
    return encrypted_pixels,private_key,block_size


def decryption(pixels,private_key,encryption_block_size,original_size):
    n=private_key[0]
    d=private_key[1]

    block_size=int(n.bit_length()/8)
    decrypted_pixels=[]
    
    i=0
    start = time.time()
    while (i<len(pixels)):
        block_of_pixels=bytearray(pixels[i:i+block_size])
        plain=pow(int.from_bytes(block_of_pixels,'big'),d,n)
        block_of_decrypted_pixels=plain.to_bytes(encryption_block_size,'big')
        #print(block_of_encrypted_pixels[0])
        if (len(decrypted_pixels)+encryption_block_size>original_size):
            last_length=len(decrypted_pixels)+encryption_block_size-original_size
            block_of_decrypted_pixels=block_of_decrypted_pixels[last_length:]
        for j in range(0,len(block_of_decrypted_pixels)):
            decrypted_pixels.append(block_of_decrypted_pixels[j].to_bytes(1,'big'))
        i=i+block_size
    end=time.time()
    print("Deszyfrowanie ECD: "+str(end-start))
    return decrypted_pixels



def encryptionCBC(pixels):
    
    public_key,private_key=create_keys()
    block_size=128
    """
    block_size=64
    f = open('mykey.pem','r')
    key=RSA.import_key(f.read())
    public_key=(key.n,key.e)
    private_key=(key.n,key.d)
    #print(key.n)
    #print(key.e)
    #print(key.d)
    """
    encrypted_pixels=[]

    first_vector=number.getRandomNBitInteger(block_size*8)
    vector=first_vector
    i=0
    start = time.time()
    while (i<len(pixels)):
        block_of_pixels=bytearray(pixels[i:i+block_size])
        cipher=int.from_bytes(block_of_pixels,'big')


        vector=vector.to_bytes(int(public_key[0].bit_length()/8),'big')
        vector = int.from_bytes(vector[0:len(block_of_pixels)],'big')
        cipher=cipher ^ vector

        cipher_block=pow(cipher,public_key[1],public_key[0])
        vector=cipher_block
        block_of_encrypted_pixels=cipher_block.to_bytes(int(public_key[0].bit_length()/8),'big')

        for j in range(0,len(block_of_encrypted_pixels)):
            encrypted_pixels.append(block_of_encrypted_pixels[j].to_bytes(1,'big'))
        i=i+block_size
    end=time.time()
    print("Szyfrowanie CBC: "+str(end-start))
    return encrypted_pixels,private_key,block_size,first_vector


def decryptionCBC(pixels,private_key,encryption_block_size,original_size,first_vector):
    n=private_key[0]
    d=private_key[1]

    block_size=int(n.bit_length()/8)
    decrypted_pixels=[]
    
    vector=first_vector
    i=0
    start = time.time()
    while (i<len(pixels)):
        block_of_pixels=bytearray(pixels[i:i+block_size])
        plain=int.from_bytes(block_of_pixels,'big')
        plain_block=pow(plain,d,n)

        vector=vector.to_bytes(int(n.bit_length()/8),'big')
        vector=int.from_bytes(vector[0:encryption_block_size],'big')
        plain_block=plain_block ^ vector
        block_of_decrypted_pixels=plain_block.to_bytes(encryption_block_size,'big')

        if (len(decrypted_pixels)+encryption_block_size>original_size):
            last_length=len(decrypted_pixels)+encryption_block_size-original_size
            block_of_decrypted_pixels=block_of_decrypted_pixels[last_length:]
            
        for j in range(0,len(block_of_decrypted_pixels)):
            decrypted_pixels.append(block_of_decrypted_pixels[j].to_bytes(1,'big'))
        i=i+block_size
        vector=plain
    end=time.time()
    print("Deszyfrowanie CBC: "+str(end-start))
    return decrypted_pixels


def encrypt_ready(pixels):
    key = RSA.generate(1032)
    f=open('mykey.pem','wb')
    f.write(key.export_key('PEM'))
    f.close()
    encryption=PKCS1_OAEP.new(key.public_key())


    block_size=64
    encrypted_pixels=[]
    
    i=0
    start = time.time()
    while (i<len(pixels)):
        block_of_pixels=bytearray(pixels[i:i+block_size])
        
        block_of_encrypted_pixels=encryption.encrypt(block_of_pixels)

        for j in range(0,len(block_of_encrypted_pixels)):
            encrypted_pixels.append(block_of_encrypted_pixels[j].to_bytes(1,'big'))
        i=i+block_size
    end=time.time()
    print("Szyfrowanie gotowym rozwiązaniem: "+str(end-start))
    return encrypted_pixels,(key.n,key.d),block_size

def decrypt_ready(pixels,encryption_block_size,original_size):
    f = open('mykey.pem','r')
    key=RSA.import_key(f.read())
    f.close
    decryption=PKCS1_OAEP.new(key)
    #print(key.n)
    #print(key.e)
    #print(key.d)
    
    block_size=int((key.n).bit_length()/8)
    decrypted_pixels=[]
    
    i=0
    start = time.time()
    while (i<len(pixels)):
        block_of_pixels=bytearray(pixels[i:i+block_size])
        
        block_of_decrypted_pixels=decryption.decrypt(block_of_pixels)
        #print(block_of_encrypted_pixels[0])
        #if (len(decrypted_pixels)+encryption_block_size>original_size):
            #last_length=len(decrypted_pixels)+encryption_block_size-original_size
            #block_of_decrypted_pixels=block_of_decrypted_pixels[last_length:]
        for j in range(0,len(block_of_decrypted_pixels)):
            decrypted_pixels.append(block_of_decrypted_pixels[j].to_bytes(1,'big'))
        i=i+block_size
    end=time.time()
    print("Deszyfrowanie gotowym rozwiązaniem: "+str(end-start))
    return decrypted_pixels