from bitarray import bitarray

# Extends Bitarray adding shifting functionality
# Reference: https://stackoverflow.com/questions/20665821/how-to-left-shift-a-bitarray-in-python


class ExtendedBitArray(bitarray):
    def __lshift__(self, count):
        result = self.copy()
        for x in range(count):
            result.pop(0)

        result._pad_end(count)
        return result

    def __rshift__(self, count):
        result = self.copy()
        for x in range(count):
            result.pop()
        result._pad_front(count)
        return result

    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.to01())

    def __str__(self):
        return self.to01()

    def __sub__(self, arg):
        if isinstance(arg, bitarray):

            temp = int(self.to01(), 2) - int(arg.to01(), 2)
            if (temp < 0):
                temp = bin(temp)[3:]
            else:
                temp = bin(temp)[2:]

            return ExtendedBitArray(temp)
        elif isinstance(arg, int):
            temp = int(self.to01(), 2) - arg
            if (temp < 0):
                temp = bin(temp)[3:]
            else:
                temp = bin(temp)[2:]

            return ExtendedBitArray(temp)
    def __add__(self, arg):
        if isinstance(arg, bitarray):

            temp = int(self.to01(), 2) + int(arg.to01(), 2)
            temp = bin(temp)[2:]

            return ExtendedBitArray(temp)
        elif isinstance(arg, int):
            temp = int(self.to01(), 2) + arg
            temp = bin(temp)[2:]

            return ExtendedBitArray(temp)

    def __mul__(self, arg):
        if isinstance(arg, bitarray):

            temp = int(self.to01(), 2) * int(arg.to01(), 2)
            temp = bin(temp)[2:]
            return ExtendedBitArray(temp)
        elif isinstance(arg, int):
            temp = int(self.to01(), 2) * arg
            temp = bin(temp)[2:]
            return ExtendedBitArray(temp)

    def _pad_front(self, count):
        for x in range(count):
            self.insert(0, False)

    def _pad_end(self, count):
        for x in range(count):
            self.append(False)

    def resize(self, size):
        diff = self.length() - size
        if diff < 1:
            self._pad_front(-diff)
        elif diff > 1:
            for i in range(diff):
                self.pop(0)

    def twos_complement(self):
        complement = self.copy()
        complement.invert()
        temp = int(complement.to01(), 2) + 1
        temp = str(bin(temp)[2:])
        complement = ExtendedBitArray(temp)
        return complement

