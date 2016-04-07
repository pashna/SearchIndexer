# coding: utf-8
from struct import pack, unpack

class Simple9():

    max_values = [1, 3, 7, 15, 31, 127, 511, 16383, 268435455]
    max_length = [28, 14, 9, 7, 5, 4, 3, 2, 1]
    shift = [1, 2, 3, 4, 5, 7, 9, 14, 28]
    margin = [0, 0, 1, 0, 3, 0, 1, 0, 0]
    value_mask = (1<<28)-1
    max_int = 268435455

    """
    schemes = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    length = [28, 14, 9, 7, 5, 4, 3, 2, 1]
    """

    def __init__(self):
        self._decoders = [self._decode_number_0, self._decode_number_1, self._decode_number_2, self._decode_number_3, self._decode_number_4, self._decode_number_5, self._decode_number_6, self._decode_number_7, self._decode_number_8]

    def encode(self, numbers):
        i = 0
        encoded = ""
        while(i < len(numbers)):
            scheme, count_of_numbers = self._choice_type(numbers[i:])

            encoded += self.encode_numbers(numbers[i:i+count_of_numbers], scheme)
            i += count_of_numbers

        return encoded

    def encode_numbers(self, numbers, scheme):
        encoded = scheme

        length = Simple9.shift[scheme]
        for n in numbers:
            if n > Simple9.max_int:
                n = 0
            encoded = encoded << length
            encoded += n
        encoded = encoded << Simple9.margin[scheme]
        return pack('=I', encoded)


    def decode(self, bytestream):
        numbers = unpack('%dI' % (len(bytestream)/4), bytestream)
        decoded = []
        for n in numbers:
            scheme = n >> 28
            decoded.extend(self._decoders[scheme](n))

        return decoded


    def decode_number(self, number):
        scheme = number >> 28


        n = number & Simple9.value_mask
        shift = Simple9.shift[scheme]
        length = Simple9.max_length[scheme]
        result = []
        for i in range(length):
            n = n >> (length-i-1)*shift
            result.append(n)

        return result


    def _decode_number_0(self, number):
        return [(number&134217728)>>27, (number&67108864)>>26, (number&33554432)>>25, (number&16777216)>>24, (number&8388608)>>23, (number&4194304)>>22, (number&2097152)>>21, (number&1048576)>>20, (number&524288)>>19, (number&262144)>>18, (number&131072)>>17, (number&65536)>>16, (number&32768)>>15, (number&16384)>>14, (number&8192)>>13, (number&4096)>>12, (number&2048)>>11, (number&1024)>>10, (number&512)>>9, (number&256)>>8, (number&128)>>7, (number&64)>>6, (number&32)>>5, (number&16)>>4, (number&8)>>3, (number&4)>>2, (number&2)>>1, (number&1)>>0, ]

    def _decode_number_1(self, number):
        return [(number&201326592)>>26, (number&50331648)>>24, (number&12582912)>>22, (number&3145728)>>20, (number&786432)>>18, (number&196608)>>16, (number&49152)>>14, (number&12288)>>12, (number&3072)>>10, (number&768)>>8, (number&192)>>6, (number&48)>>4, (number&12)>>2, (number&3)>>0, ]

    def _decode_number_2(self, number):
        return [(number&234881024)>>25, (number&29360128)>>22, (number&3670016)>>19, (number&458752)>>16, (number&57344)>>13, (number&7168)>>10, (number&896)>>7, (number&112)>>4, (number&14)>>1, ]

    def _decode_number_3(self, number):
        return [(number&251658240)>>24, (number&15728640)>>20, (number&983040)>>16, (number&61440)>>12, (number&3840)>>8, (number&240)>>4, (number&15)>>0, ]

    def _decode_number_4(self, number):
        return [(number&260046848)>>23, (number&8126464)>>18, (number&253952)>>13, (number&7936)>>8, (number&248)>>3, ]

    def _decode_number_5(self, number):
        return [(number&266338304)>>21, (number&2080768)>>14, (number&16256)>>7, (number&127)>>0, ]

    def _decode_number_6(self, number):
        return [(number&267911168)>>19, (number&523264)>>10, (number&1022)>>1, ]

    def _decode_number_7(self, number):
        return [(number&268419072)>>14, (number&16383)>>0, ]

    def _decode_number_8(self, number):
        return [(number&268435455)>>0, ]


    def _choice_type(self, n_lst):
        current_scheme = 0
        i = 0
        max_length = 28

        while(i < max_length):
            if i < len(n_lst):
                number = n_lst[i]
            else:
                # Если не удается закодировать все - кодируем только одно число
                return 8, 1

            if number > Simple9.max_int:
                number = 0

            result_index = next((Simple9.max_values.index(n) for n in Simple9.max_values if n >= number), len(Simple9.max_values))
            if result_index > current_scheme:
                current_scheme = result_index
                max_length = Simple9.max_length[current_scheme]

            i += 1
            #print current_scheme

        return current_scheme, max_length


def simple9_script_generator():
    for j in range(9):
        max_value = Simple9.max_values[j]
        shift = Simple9.shift[j]
        max_length = Simple9.max_length[j]
        margin = Simple9.margin[j]
        script = "def _decode_number_{}(self, number):\n".format(j)
        script += "    return ["
        for i in reversed(range(max_length)):
            script += "(number&{})>>{}, ".format(max_value << shift*i+margin, shift*i+margin)
        script += "]\n"
        print script

if __name__ == "__main__":
    s = Simple9()
    enc = s.encode([5523123, 123, 12, 32])
    print s.decode(enc)
    simple9_script_generator()