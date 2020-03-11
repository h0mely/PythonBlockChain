#!/usr/bin/python3

import copy
import struct
import binascii

K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
     0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
     0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
     0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
     0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
     0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
     0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
     0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
     0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
     0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
     0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
     0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]


def rightRotate(x, y):
    return ((x >> y) | (x << (32 - y))) & 0xFFFFFFFF


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def ch(x, y, z):
    return (x & y) ^ ((~x) & z)


class SHA256:
    def __init__(self, message=None):
        message = message.encode('utf-8')
        self.K = copy.deepcopy(K)  # 深复制
        self.H = copy.deepcopy(H)
        self.preProccess(message)

    '''
    循环处理每部分
    '''

    def mainLoop(self, c):
        w = [0] * 64
        w[0:16] = struct.unpack('!16L', c)  # 拆成16个unsigned long 一个有32位

        for i in range(16, 64):
            s0 = rightRotate(w[i - 15], 7) ^ rightRotate(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = rightRotate(w[i - 2], 17) ^ rightRotate(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = self.H

        for i in range(64):
            s0 = rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)
            t2 = s0 + maj(a, b, c)
            s1 = rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)
            t1 = h + s1 + ch(e, f, g) + self.K[i] + w[i]
            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF
        for i, (x, y) in enumerate(zip(self.H, [a, b, c, d, e, f, g, h])):  # enumerate()函数创建索引值
            # print(i,x,y)
            # zip（）函数用于将多个可迭代对象作为参数，依次将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象。
            self.H[i] = (x + y) & 0xFFFFFFFF

    '''
    预处理，将message补全1，n个0和长度
    '''

    def preProccess(self, message):
        message = bytearray(message)
        length = (8 * len(message)) & 0xffffffffffffffff
        message.append(0x80)
        while len(message) % 64 != 56:  # 56*8 = 448
            message.append(0)
        message += length.to_bytes(8, byteorder='big')
        for i in range(0, len(message) // 64):  # //在python中，这个叫“地板除”，3//2=1
            self.mainLoop(message[64 * i:64 * (i + 1)])

    '''
    返回值：最后的十六进制sha256
    '''

    def getData(self):
        data = [struct.pack('!L', i) for i in self.H[:8]]
        finaData = binascii.hexlify(b''.join(data)).decode('utf-8')
        return finaData


if __name__ == '__main__':
    A = '刘伟asddajgksdjkasdjasbj*(jdlasbdljasbdjlasdbashgdasdvashdvshlJL_(d-aw0eqw;nask;njkas;gcJLGupdwqt812hdakw;dnask;fho[urqwhwkafbasjbdsa;kdbqwiorpyqwipdcbas'
    print(SHA256(A).getData())
