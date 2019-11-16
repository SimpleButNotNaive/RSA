from random import getrandbits
from hashlib import sha1
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class RSA:
    def __init__(self, p, q, a):
        self.p = p
        self.q = q
        self.a = a
        self.n = p*q
        self.phi_n = (p - 1)*(q - 1)
        self.b = RSA.calc_inverse(self.phi_n, self.a)
        logging.info("RSA初始化完毕")
        logging.info("私钥：")
        logging.info("p:\n%d", self.p)
        logging.info("q:\n%d", self.q)
        logging.info("a:\n%d", self.a)
        logging.info("公钥：")
        logging.info("b:\n%d", self.b)
        logging.info("n:\n%d", self.n)

        self.q_inv = RSA.calc_inverse(p, q)
        self.p_inv = RSA.calc_inverse(q, p)
        self.dp = self.a % (p - 1)
        self.dq = self.a % (q - 1)

    def encrypt(self, plain_text):
        logging.info("明文：\n%s", plain_text)
        M = RSA.padding(plain_text)
        logging.info("明文填充后的2048比特数：\n%d", M)
        cipher = RSA.modular_exponent(M, self.b, self.n)
        logging.info("密文：\n%d", cipher)
        return cipher

    def decrypt(self, cipher):
        logging.info("待解密密文：\n%d", cipher)
        M = self.do_decrypt(cipher)
        logging.info("解密得到的2048比特数：\n%d", M)
        plaint_text = RSA.strip(M)
        logging.info("去除填充后得到的明文：\n%s", plaint_text)
        return plaint_text

    def do_decrypt(self, cipher):
        c_1 = RSA.modular_exponent(cipher, self.dp, self.p)
        c_2 = RSA.modular_exponent(cipher, self.dq, self.q)

        return ((c_1*self.q_inv*self.q % self.n) + (c_2*self.p_inv*self.p % self.n)) % self.n

    @staticmethod
    def calc_inverse(n, ele):
        a = n
        b = ele % n
        t_0 = 0
        t = 1
        q = a // b
        r = a % b
        while r > 0:
            temp = (t_0 - q*t) % n
            t_0 = t
            t = temp
            a = b
            b = r
            q = a // b
            r = a % b

        return t

    @staticmethod
    def modular_exponent(a, b, n):
        mask = 1
        result = 1
        while mask <= b:
            if mask & b:
                result = (result * a) % n
            a = (a * a) % n
            mask = mask << 1
        return result

    @staticmethod
    def padding(message: str):
        assert len(message) <= 128

        message_bytes = RSA.integer_to_bytes(
            RSA.bytes_to_integer(message.encode("utf-8")))
        random_integer_bytes = RSA.integer_to_bytes(getrandbits(1024))

        left_part = RSA.bytes_xor(message_bytes, RSA.H(random_integer_bytes))
        right_part = RSA.bytes_xor(RSA.H(left_part), random_integer_bytes)

        result = RSA.bytes_to_integer(left_part)
        result = result << 1024
        result += RSA.bytes_to_integer(right_part)

        return result

    @staticmethod
    def strip(big_integer: int):
        bit_integer_bytes = RSA.integer_to_bytes(big_integer, 2048)
        left_part = bit_integer_bytes[0:128]
        right_part = bit_integer_bytes[128:256]

        random_integer_bytes = RSA.bytes_xor(RSA.H(left_part), right_part)
        message_bytes = RSA.bytes_xor(left_part, RSA.H(random_integer_bytes))

        message = message_bytes.decode("utf-8")
        return message

    @staticmethod
    def bytes_xor(a: bytes, b: bytes):
        assert len(a) == 128
        assert len(b) == 128
        result = bytearray(128)
        for i in range(128):
            result[i] = a[i] ^ b[i]
        return result

    @staticmethod
    def bytes_to_integer(b: bytes):
        return int.from_bytes(b, byteorder="big", signed=False)

    @staticmethod
    def integer_to_bytes(i: int, size=1024):

        return i.to_bytes(size//8, byteorder="big", signed=False)

    @staticmethod
    def H(data):
        hash_func = sha1()
        hash_func.update(data)
        data = hash_func.digest()

        data_array = bytearray(128)
        for i in range(6):
            for j in range(20):
                data_array[127 - (20*i + j)] = data[j]

        result = RSA.integer_to_bytes(RSA.bytes_to_integer(data_array))

        assert len(result) == 128
        return result
