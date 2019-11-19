import struct
import hashlib
top = 0xffffffff


def sha1(msg):

    msg = pad(msg)
    h0 = 0x67452301
    h1 = 0xefcdab89
    h2 = 0x98badcfe
    h3 = 0x10325476
    h4 = 0xc3d2e1f0

    for j in range(len(msg) // 64):
        chunk = msg[j * 64: (j+1) * 64]

        w = {}
        for i in range(16):
            # 将一个chunk分为16个字
            word = chunk[i*4: (i+1)*4]
            (w[i],) = struct.unpack(">i", word)
            # 按照大端序，将word(bytes类型)转换为int类型

        for i in range(16, 80):
            # 按照之前已有的字生成新的字
            w[i] = rotl((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]) & top, 1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(0, 80):
            if 0 <= i <= 19:
                f = (b & c) | ((~ b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = add([rotl(a, 5), f, e, k, w[i]])
            e = d
            d = c
            c = rotl(b, 30)
            b = a
            a = temp

        h0 = add([h0, a])
        h1 = add([h1, b])
        h2 = add([h2, c])
        h3 = add([h3, d])
        h4 = add([h4, e])

    h_list = [h0, h1, h2, h3, h4]
    h_bytes_list = []

    for h in h_list:
        h_bytes_list.append(h.to_bytes(4, "big", signed=False))

    return b"".join(h_bytes_list)


def pad(msg):
    sz = len(msg)
    bits_number = sz * 8
    padding = 512 - ((bits_number + 8) % 512) - 64

    return msg + bytes.fromhex("80")\
        + (padding // 8) * bytes.fromhex("00") + struct.pack(">Q", bits_number)


def rotl(i, n):
    # 循环左移
    lmask = top << (32-n)
    rmask = top >> n
    # 由于python的int没有长度限制，因此不能简单地移位
    l = i & lmask
    r = i & rmask
    newl = r << n
    newr = l >> (32-n)
    return newl + newr


def add(l):
    # 将列表l中的元素模2^32加
    ret = 0
    for e in l:
        ret = (ret + e) & top
        # 通过与top相与保证结果的范围在0-2^32-1之内
    return ret


if __name__ == "__main__":
    sha_1_hash = hashlib.sha1()
    data = "12345".encode("utf-8")

    sha_1_hash.update(data)
    print(sha1(data))
    print(sha_1_hash.digest())
