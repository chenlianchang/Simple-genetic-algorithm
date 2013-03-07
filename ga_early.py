#encoding=utf8
"""
@author: chenlianchang
@email: zhengyi.clc@taobao.com, qiyingjita@126.com
@log:2012-12-01 create
"""

import pdb
import random
from ga_base import GA

class TestGa(GA):
    def __init__(self):
        pass

    def cal_fit(self, fitsig):
        """计算个体的目标函数值"""
        fit = 1000 - ((fitsig-10)**2)
        return float(fit)

    def randnum(self):
        return random.random()

    def choose(self, fittup, num):
        """fittup是各个个体的适应度，num是个体个数， num_randrom是产生的随机数， 
        随机数落在什么范围则返回个体的下标"""
        l = []
        while len(l)<4:
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
    
    def fitness(self, fitall):
        """判断是否有个体满足适应度，有则返回个体值"""
        for i in xrange(len(fitall)):
            data = self.decode_gray(fitall[i])
            if 1000 - (float(data) - 10) ** 2 > 999:
                return data
        return 0

if __name__ == '__main__':
    obj = TestGa()
    singletup = []
    
    #产生4个初始个体 
    num = [obj.encode_gray(i, 5) for i in xrange(0, 32)]
    singletup = random.sample(num, 8)
    fit_value_tup = [obj.cal_fit(obj.decode_gray(j)) for j in singletup]
    fit_percent_tup = [i/sum(fit_value_tup) for i in fit_value_tup]
    result = obj.fitness(singletup)
    if result:
        print "result = %s" %result
        print singletup
    else:
        for i in xrange(0, 10000):
            print "第 %s 代" % i
            if i % 10 == 0:
                singletup = obj.variation(singletup)
                print "bianyi"
            else:
                pass
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

