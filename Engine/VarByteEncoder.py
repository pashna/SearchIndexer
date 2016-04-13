# coding: utf-8

from struct import pack, unpack

class VarByteEncoder():


    def encode_number(self, number):
        bytes = []
        while True:
            bytes.insert(0, number % 128)
            if number < 128:
                break
            number /= 128
        bytes[-1] += 128
        return pack('%dB' % len(bytes), *bytes)


    def encode(self, numbers):
        bytes = ""
        for n in numbers:
            bytes += self.encode_number(n)
        return bytes


    def decode(self, bytestream):
        n = 0
        numbers = []
        bytestream = unpack('%dB' % len(bytestream), bytestream)
        for byte in bytestream:
            if byte < 128:
                n = 128 * n + byte
            else:
                n = 128 * n + (byte - 128)
                numbers.append(n)
                n = 0
        return numbers