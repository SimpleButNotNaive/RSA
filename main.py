from values import *
from RSA import RSA

if __name__ == "__main__":
    rsa = RSA(p, q, a)
    rsa.decrypt(rsa.encrypt(message))
    