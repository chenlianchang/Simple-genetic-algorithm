#encoding=utf8
"""
@author: chenlianchang
@email: zhengyi.clc@taobao.com, qiyingjita@126.com
@log:2012-12-01 create
"""
import random
import math
from ga_base import GA

class TestGa(GA):
    def __init__(self):
        self.scale = 8
        self.length = 7

    def cal_fit(self, fitsig):
        """计算个体的目标函数值"""
        fit = 100000 - ((fitsig-10)**2)
        return float(fit)

    def randnum(self):
        return random.random()

    def choose(self, fittup, num):
        """fittup是各个个体的适应度，num是个体个数， num_randrom是产生的随机数， 
        随机数落在什么范围则返回个体的下标"""
        l = []
        while len(l)< self.scale / 2:
            num_random = self.randnum()
            all = 0
            for i in xrange(0, num):
                all += fittup[i]
                if num_random < all:
                    if i in l:
                        break
                    else:
                        l.append(i)
                        break
        return l
    
    def cross(self, singletup):
        #pdb.set_trace()
        random.shuffle(singletup)
        for i in xrange(0, len(singletup), 2):
            n = random.randint(0, len(singletup[0])-1)
            temp_front_1 = singletup[i][0:n]
            temp_tail_1 = singletup[i+1][n:]
            temp_front_2 = singletup[i+1][0:n]
            temp_tail_2 = singletup[i][n:]
            singletup[i] = temp_front_1 + temp_tail_1
            singletup[i+1] = temp_front_2 + temp_tail_2
        return singletup

    def variation(self, singletup):
        n = random.randint(0, len(singletup)-1)
        m = random.randint(0, len(singletup[0])-1)
        new = '0' if singletup[n][m] == '1' else '1'
        singletup[n] = singletup[n][0:m] + new + singletup[n][m+1:]
        return singletup
    
    def entropy(self, singletup):
        """计算种群敛熵"""
        fit_value_tup = [self.cal_fit(self.decode_gray(j)) for j in singletup]
        fit_tup = [i/sum(fit_value_tup) for i in fit_value_tup]
        fit_percent_tup = [i/sum(fit_tup) for i in fit_tup]

        print fit_percent_tup
        entro = 0 
        for x in fit_percent_tup:
            entro += (- (x * math.log(x)))
        print entro
        return entro

    def monotone_coefficient(self, singletup):
        """每一位的单调系数"""
        l = []
        value = []
        for i in xrange(0, len(singletup[0])):
            num = 0
            for n in xrange(0, self.scale): 
                num += int(singletup[n][i])
            u = abs(num / self.scale - 0.5) * 2
            l.append(u)
            value.append(num)
        return l, value
            
    def allelic_variation(self, mono_tup, value, singletup):
        """mono_tup是单调系数数组"""
        variation_probability = 0
        for i in xrange(0, len(mono_tup)):
            if mono_tup[i] > 0.5 and value[i] >= 6:
                for s in xrange(0, len(singletup)):
                    if variation_probability > 2:
                        break
                    if singletup[s][i] == '1':
                        singletup[s] = singletup[s][0:i] + '0' + singletup[s][(i+1):]
                        variation_probability += 1
            elif mono_tup[i] > 0.5 and value[i] <= 2:
                for s in xrange(0, len(singletup)):
                    if variation_probability > 2:
                        break
                    if singletup[s][i] == '0':
                        singletup[s] = singletup[s][0:i] + '1' + singletup[s][(i+1):]
                        variation_probability += 1
        return singletup

    def fitness(self, fitall):
        """判断是否有个体满足适应度，有则返回个体值"""
        for i in xrange(len(fitall)):
            data = self.decode_gray(fitall[i])
            if 100000 - (float(data) - 10) ** 2 > 99999:
                return data
        return 0

if __name__ == '__main__':
    obj = TestGa()
    singletup = []
    
    #产生4个初始个体 
    num = [obj.encode_gray(i, obj.length) for i in xrange(0, 128)]
    singletup = random.sample(num, obj.scale)
    fit_value_tup = [obj.cal_fit(obj.decode_gray(j)) for j in singletup]
    fit_percent_tup = [i/sum(fit_value_tup) for i in fit_value_tup]
    result = obj.fitness(singletup)
    
    if result:
        print "result = %s" %result
        print singletup
    else:
        for i in xrange(0, 10000):
            print "第 %s 代" % i
            
            #if obj.entropy(singletup) > 0.9 and not obj.fitness(singletup):
            mono_tup, value = obj.monotone_coefficient(singletup)
            singletup = obj.allelic_variation(mono_tup, value, singletup)
            singletup_new = []#新一代的个体
            choose_list = obj.choose(fit_percent_tup, len(fit_percent_tup))
            temp_1 = singletup[choose_list[0]]
            temp_2 = singletup[choose_list[1]]
            temp_3 = singletup[choose_list[2]]
            temp_4 = singletup[choose_list[3]]
            singletup_new.append(temp_1)
            singletup_new.append(temp_2)
            singletup_new.append(temp_3)
            singletup_new.append(temp_4)
            singletup_new = obj.cross(singletup_new)
            singletup_new.append(temp_1)
            singletup_new.append(temp_2)
            singletup_new.append(temp_3)
            singletup_new.append(temp_4)
           
            print "新种群=%s" % singletup_new
            single_digist = [obj.decode_gray(j) for j in singletup_new]
            print single_digist
            
            file = open('ga_data.txt', 'a')
            ss = ''
            for s in single_digist:
                ss += (str(s) + ' ' )
            file.write(ss)
            file.write('\n')
            file.close()
           
            fit_value_tup = [obj.cal_fit(obj.decode_gray(j)) for j in singletup_new]
            fit_percent_tup = [i/sum(fit_value_tup) for i in fit_value_tup]
            result = obj.fitness(singletup_new)
            singletup = [i for i in singletup_new]
            if result:
                print "result = %s" % result
                break
            else:
                continue

