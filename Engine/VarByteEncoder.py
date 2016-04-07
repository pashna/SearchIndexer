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
        #return bytes
        return pack('%dB' % len(bytes), *bytes)


    def encode(self, numbers):
        bytes = ""
        for n in numbers:
            bytes += self.encode_number(n)
        return bytes
        #return pack('%dB' % len(bytes), *bytes)


    def decode(self, bytestream):
        bytestream = unpack('%dB' % len(bytestream), bytestream)
        old_radix = 0
        numbers = []

        for byte in bytestream:
            if byte < 128:
                old_radix = byte
            else:
                n = 128 * old_radix + (byte - 128)
                numbers.append(n)
                old_radix = 0
        return numbers