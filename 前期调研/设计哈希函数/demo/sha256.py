#!/usr/bin/python3

import copy
import struct
import binascii
import hashlib

F32 = 0xFFFFFFFF

_k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
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

_h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
      0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]


def _pad(msglen):
    mdi = msglen & 0x3F # 11,1111
    length = struct.pack('!Q', msglen << 3) # Q 表示 unsigned long long  为8*8=64位

    if mdi < 56:
        padlen = 55 - mdi
    else:
        padlen = 119 - mdi

    return b'\x80' + (b'\x00' * padlen) + length # 0x80 = 1000,0000


def _rotr(x, y):
    return ((x >> y) | (x << (32 - y))) & F32


def _maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def _ch(x, y, z):
    return (x & y) ^ ((~x) & z)


class SHA256:
    _output_size = 8
    blocksize = 1
    block_size = 64
    digest_size = 32

    def __init__(self, m=None):
        self._counter = 0
        self._cache = b''
        self._k = copy.deepcopy(_k)  # 深复制
        self._h = copy.deepcopy(_h)

        self.update(m)

    def _compress(self, c):
        w = [0] * 64
        w[0:16] = struct.unpack('!16L', c)  # 拆成16个unsigned long 一个有32位

        for i in range(16, 64):
            s0 = _rotr(w[i - 15], 7) ^ _rotr(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = _rotr(w[i - 2], 17) ^ _rotr(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & F32

        a, b, c, d, e, f, g, h = self._h

        for i in range(64):
            s0 = _rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)
            t2 = s0 + _maj(a, b, c)
            s1 = _rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)
            t1 = h + s1 + _ch(e, f, g) + self._k[i] + w[i]

            h = g
            g = f
            f = e
            e = (d + t1) & F32
            d = c
            c = b
            b = a
            a = (t1 + t2) & F32

        for i, (x, y) in enumerate(zip(self._h, [a, b, c, d, e, f, g, h])):  # enumerate()函数创建索引值
            # zip（）函数用于将多个可迭代对象作为参数，依次将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象。
            self._h[i] = (x + y) & F32

    def update(self, m):
        if not m:
            return

        self._counter += len(m)
        m = self._cache + m

        # 代码将 输入m按照64*8 = 512 位分块处理
        for i in range(0, len(m) // 64):  # //在python中，这个叫“地板除”，3//2=1
            self._compress(m[64 * i:64 * (i + 1)])
        self._cache = m[-(len(m) % 64):]

    def digest(self):
        r = copy.deepcopy(self)
        r.update(_pad(self._counter))
        data = [struct.pack('!L', i) for i in r._h[:self._output_size]]
        return b''.join(data)

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode('ascii')  # hexlify其作用是返回的二进制数据的十六进制表示


def true_sha256(message):
    m = hashlib.sha256()
    m.update(message)
    return m.hexdigest()


def my_sha256(message):
    return SHA256(message).hexdigest()


if __name__ == '__main__':
    demo = ["a", "abc", "message digest", "abcdefghijklmnopqrstuvwxyz",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890",
            "你好，SHA256"]
    for message in demo:
        demo[demo.index(message)] = message.encode('utf-8')
    for message in demo:
        print(my_sha256(message), ' <= "', message.decode('utf-8'), '"', sep='')
        assert true_sha256(message) == my_sha256(message)  # 若和标准库中不同，会抛出异常
    print('\nSHA256测试全部通过')
