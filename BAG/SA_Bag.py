import random
from math import exp

import numpy as np


class SA_Bag(object):
    def __init__(self, data, price, C=269, T=200, T_end=1, L=100, r=0.95):
        self.T = T  # 初始温度
        self.T_end = T_end  # 终止温度
        self.L = L
        self.data = data  # 物品的重量
        self.price = price  # 物品的价值
        self.C = C  # 背包容量
        self.num = len(data)  # 物品个数
        self.r = r  # 退火率

        self.best_ways = np.array([0] * self.num)  # 初始化最优
        self.now_ways = np.array([0] * self.num)  # 初始化当前

        self.best = -1
        self.sum_weight = 0
        self.best_weight = -1

    def get_total_price(self, ways):
        sum_price = 0
        sum_weight = 0
        for i in range(self.num):
            sum_price += ways[i] * self.price[i]
            sum_weight += ways[i] * self.data[i]
        self.sum_weight = sum_weight
        return sum_price

    def get_init(self):
        while True:
            for k in range(self.num):
                if random.random() < 0.5:
                    self.now_ways[k] = 1
                else:
                    self.now_ways[k] = 0
            self.get_total_price(self.now_ways)
            if self.sum_weight <= self.C:
                break
        self.best = self.get_total_price(self.now_ways)
        self.best_ways = self.now_ways.copy()
        self.best_weight = self.sum_weight

    def get(self, x):  # 随机将背包中已经存在的物品取出
        while True:
            ob = random.randint(0, self.num - 1)
            if x[ob] == 1:
                x[ob] = 0
                break

    def put(self, x):  # 随机放入背包中不存在的物品
        while True:
            ob = random.randint(0, self.num - 1)
            if x[ob] == 0:
                x[ob] = 1
                break

    def simulated_annealing(self):

        best_value = []
        best_weight = []

        while self.T > self.T_end:
            # # 存储最退火过程中的最优路径变化
            # now = 0
            # test = np.array([0] * self.num)

            for i in range(self.L):
                now_price = self.get_total_price(self.now_ways)
                new_ways = self.now_ways.copy()
                # 随机取值
                seed_obj = random.randint(0, self.num - 1)
                # 在背包中则将其拿出，并加入其它物品
                if new_ways[seed_obj] == 1:
                    self.put(new_ways)
                    new_ways[seed_obj] = 0
                else:
                    if random.random() < 0.5:
                        new_ways[seed_obj] = 1
                    else:
                        self.get(new_ways)
                        new_ways[seed_obj] = 1

                new_price = self.get_total_price(new_ways)
                if self.sum_weight > self.C:
                    # print(self.sum_weight)
                    continue

                # print(self.sum_weight)
                if new_price > self.best:  # 更新全局最优
                    self.best = new_price
                    self.best_ways = new_ways.copy()
                    self.best_weight = self.sum_weight

                if new_price > now_price:  # 直接接受新解
                    self.now_ways = new_ways.copy()
                else:  # 概率接受劣解
                    g = 1.0 * (new_price - now_price) / self.T
                    if random.random() < exp(g):
                        self.now_ways = new_ways.copy()

            best_value.append(self.best)
            best_weight.append(self.best_weight)
            self.T *= self.r
            # print("best:%d" % self.best)

        return self.best_ways, self.best, best_weight, best_value
