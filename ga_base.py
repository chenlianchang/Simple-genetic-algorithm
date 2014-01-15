#encoding=utf8
import pdb
import random

class GA(object):
    def __init__(self):
        pass

    def encode_binary(self, chron_data, chron_len):
        """code form digest to 0/1"""
        d = ''
        dd = ''
        while chron_data/2 or chron_data % 2:
            d += str(chron_data % 2)
            chron_data = chron_data / 2
        for i in xrange(len(d)-1, -1, -1):
            dd = dd + d[i]
        prefix = (chron_len - len(dd)) * '0'
        return prefix + dd

    def encode_gray(self, chron_data, chron_len):
        binary = self.encode_binary(chron_data, chron_len)
        gray = ''
        for i in xrange(0, len(binary)):
            if i == 0:
                gray += binary[i]
            else:
                gray += str(int(binary[i]) ^ int(binary[i-1]))
        return gray


    def decode_binary(self, chron_data):
        """decode from 0/1 to digest"""
        d = 0
        for i in xrange(len(chron_data)):
            d += int(chron_data[i]) * (2**(len(chron_data)-(i+1)))
        return d


    def decode_gray(self, chron_data):
        binary = ''
        for i in xrange(0, len(chron_data)):
            if i == 0:
                binary += chron_data[i]
            else:
                binary += str(int(binary[len(binary)-1]) ^ int(chron_data[i]))
        digist = self.decode_binary(binary)
        return digist

    def fitness(self, fitsig):
        pass

    def choose(self, fittup, num_individual, num_random):
        pass

    def cross(self, singletup, num):
        pass

    def variation(self, singletup):
        pass 
        
    def fitfun(self, singletup):
        pass

#test
if __name__ == '__main__':
    obj = GA()
    print obj.decode('11011')
    print obj.encode(10, 5)
