from struct import pack, unpack

class Simple9():

    max_values = [1, 3, 7, 15, 31, 127, 511, 16383, 268435455]
    max_length = [28,14,9,7,5,4,3, 2, 1]
    shift = [1,2,3,4,5,7,9,14,28]
    value_mask = (1<<28)-1

    """
    schemes = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    length = [28, 14, 9, 7, 5, 4, 3, 2, 1]
    """

    def __init__(self):
        pass

    def encode(self, numbers):
        i = 0
        encoded = ""
        while(i < len(numbers)):
            scheme, count_of_numbers = self._choice_type(numbers[i:])
            print scheme, count_of_numbers
            encoded += self.encode_numbers(numbers[i:i+count_of_numbers], scheme)
            i += count_of_numbers

        return encoded

    def encode_numbers(self, numbers, scheme):
        encoded = scheme

        length = Simple9.shift[scheme]
        for n in numbers:
            encoded = encoded << length
            encoded += n

        return pack('=I', encoded)


    def decode(self, bytestream):
        numbers = unpack('%dI' % (len(bytestream)/4), bytestream)
        decoded = []
        for n in numbers:
            decoded.extend(self.decode_number(n))

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

    def decode_number_0(self, number):
        return [(number&134217728)>>54, (number&67108864)>>52, (number&33554432)>>50, (number&16777216)>>48, (number&8388608)>>46, (number&4194304)>>44, (number&2097152)>>42, (number&1048576)>>40, (number&524288)>>38, (number&262144)>>36, (number&131072)>>34, (number&65536)>>32, (number&32768)>>30, (number&16384)>>28, (number&8192)>>26, (number&4096)>>24, (number&2048)>>22, (number&1024)>>20, (number&512)>>18, (number&256)>>16, (number&128)>>14, (number&64)>>12, (number&32)>>10, (number&16)>>8, (number&8)>>6, (number&4)>>4, (number&2)>>2, (number&1)>>0, ]

    def decode_number_1(self, number):
        return [(number&201326592)>>26, (number&50331648)>>24, (number&12582912)>>22, (number&3145728)>>20, (number&786432)>>18, (number&196608)>>16, (number&49152)>>14, (number&12288)>>12, (number&3072)>>10, (number&768)>>8, (number&192)>>6, (number&48)>>4, (number&12)>>2, (number&3)>>0, ]

    def decode_number_2(self, number):
        return [(number&117440512)>>16, (number&14680064)>>14, (number&1835008)>>12, (number&229376)>>10, (number&28672)>>8, (number&3584)>>6, (number&448)>>4, (number&56)>>2, (number&7)>>0, ]

    def decode_number_3(self, number):
        return [(number&251658240)>>12, (number&15728640)>>10, (number&983040)>>8, (number&61440)>>6, (number&3840)>>4, (number&240)>>2, (number&15)>>0, ]

    def decode_number_4(self, number):
        return [(number&32505856)>>8, (number&1015808)>>6, (number&31744)>>4, (number&992)>>2, (number&31)>>0, ]

    def decode_number_5(self, number):
        return [(number&266338304)>>6, (number&2080768)>>4, (number&16256)>>2, (number&127)>>0, ]

    def decode_number_6(self, number):
        return [(number&133955584)>>4, (number&261632)>>2, (number&511)>>0, ]

    def decode_number_7(self, number):
        return [(number&268419072)>>2, (number&16383)>>0, ]

    def decode_number_8(self, number):
        return [(number&268435455)>>0, ]

    def _choice_type(self, n_lst):
        current_scheme = 0
        i = 0
        max_length = 28

        while(i < max_length):
            if len(n_lst) == i:
                pass
            number = n_lst[i]
            result_index = next((Simple9.max_values.index(n) for n in Simple9.max_values if n >= number), len(Simple9.max_values))
            if result_index > current_scheme:
                current_scheme = result_index
                max_length = Simple9.max_length[current_scheme]

            i += 1
            #print current_scheme

        return current_scheme, max_length


s = Simple9()
#print s.decode_number_0(262974714)
#print s._choice_type([1, 3, 142, 24, 412])
#ec = s.encode([1000, 2000, 25000, 30000])
#print s.decode(ec)
max_values = [1, 3, 7, 15, 31, 127, 511, 16383, 268435455]
max_length = [28,14,9,7,5,4,3, 2, 1]
shift = [1,2,3,4,5,7,9,14,28]

def simple9_script_generator():
    for j in range(9):
        max_value = Simple9.max_values[j]
        shift = Simple9.shift[j]
        max_length = Simple9.max_length[j]
        script = "def decode_number_{}(self, number):\n".format(j)
        script += "    return ["
        for i in reversed(range(max_length)):
            script += "(number&{})>>{}, ".format(max_value << shift*i, 2*i)
        script += "]\n"
        print script


simple9_script_generator()