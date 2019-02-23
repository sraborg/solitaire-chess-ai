from bitarray import bitarray

# Extends Bitarray adding shifting functionality
# Reference: https://stackoverflow.com/questions/20665821/how-to-left-shift-a-bitarray-in-python


class ExtendedBitArray(bitarray):
    def __lshift__(self, count):
        return self[count:] + type(self)('0') * count

    def __rshift__(self, count):
        return type(self)('0') * count + self[:-count]

    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.to01())

    def __str__(self):
        return self.to01()

    def __sub__(self, arg):
        if isinstance(arg, bitarray):

            bit_length = arg.length()

            temp = int(self.to01(), 2) - int(arg.to01(), 2)
            if (temp < 0):
                temp2 = bin(temp)[3:]
            else:
                temp2 = bin(temp)[2:]

            diff = bit_length - len(temp2)

            result = ExtendedBitArray(temp2)
            for x in range(diff):
                result.insert(0, False)
            return result

    def __add__(self, arg):
        if isinstance(arg, bitarray):

            bit_length = arg.length()

            temp = int(self.to01(), 2) + int(arg.to01(), 2)
            temp2 = bin(temp)[2:]

            result = temp2[-self.length():]
            return result

    def twos_complement(self):
        complement = self.copy()
        complement.invert()
        temp = int(complement.to01(), 2) + 1
        temp = str(bin(temp)[2:])
        complement = ExtendedBitArray(temp)
        return complement

