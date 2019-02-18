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
