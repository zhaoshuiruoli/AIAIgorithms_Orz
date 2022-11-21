import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import math
import random


class GA():
    def __init__(self, num, data, iter_num, retain_rate, select_rate, mutation_rate, gailiang_num):
        self.num = num
        self.data = data
        self.length = len(self.data)
        self.dis = self.get_distance()
        self.itet_num = iter_num
        self.retain_rate = retain_rate
        self.select_rate = select_rate
        self.mutation_rate = mutation_rate
        self.gailiang_num = gailiang_num
        self.initialize_population = self.initialize_population()

    def get_init(self):
        return self.get_best(self.initialize_population)

    def evolve(self):
        population = self.initialize_population
        distance_list = []
        # 得到种群中最好的个体
        cur_best_res, cur_best_dis = self.get_best(population)
        distance_list.append(cur_best_dis)
        for i in range(self.itet_num):
            # print("*******************************"+str(i)+"********************************")
            # print(self.length,self.num)
            # 自然选择
            parents = self.nature_select(population)

            # 繁殖
            children = self.crossover(parents)

            # 变异
            self.mutation(children)

            # 更新种群
            population = parents + children  # 调整顺序
            # print(len(population))



            # 将当前更新的种群中最优的添加进来
            cur_best_res, cur_best_dis = self.get_best(population)
            distance_list.append(cur_best_dis)

        return cur_best_res, cur_best_dis, distance_list

    def initialize_population(self):
        """
        初始化种群，一共num个个体,基因长度为self.length
        :return:
        """
        population = []
        index = [i for i in range(self.length)]
        for i in range(self.num):
            x = index.copy()
            random.shuffle(x)
            self.gailiang(x)
            population.append(x)
        return population

    def total_distance(self, x):
        """
        计算每个个体的所经过的总长度
        :param x:
        :return:
        """
        dis = 0
        for i in range(len(x)):
            if i == len(x) - 1:
                dis += self.dis[x[i]][x[0]]
            else:
                dis += self.dis[x[i]][x[i + 1]]
        return dis

    def gailiang(self, x):
        """
        对初始的种群进行优化,避免初始种群中存在个体太弱
        :param x:
        :return:
        """
        distance = self.total_distance(x)
        gailiang_num = 0
        while gailiang_num < self.gailiang_num:
            # 随机选择x中的两个位置，进行交换
            while True:
                a = random.randint(0, len(x) - 1)
                b = random.randint(0, len(x) - 1)
                if a != b:
                    break
            new_x = x.copy()
            temp_a = new_x[a]
            new_x[a] = new_x[b]
            new_x[b] = temp_a
            # 如果交换后的距离小于之前的距离，就更新
            if self.total_distance(new_x) < distance:
                x = new_x.copy()
            # 一共尝试改良gailiang_N次
            gailiang_num += 1

    def nature_select(self, population):
        """
        自然选择代码，按照一定的概率淘汰掉弱的个体
        :param population:
        :return:
        """
        grad = [[x, self.total_distance(x)] for x in population]
        grad = [x[0] for x in sorted(grad, key=lambda x: x[1])]
        # 强者
        retain_length = int(self.retain_rate * len(grad))
        parents = grad[: retain_length]
        # 生存下来的弱者
        for other in grad[retain_length:]:
            if random.random() < self.select_rate:
                parents.append(other)
        return parents

    # 交叉繁殖
    def crossover(self, parents):
        """

        :param parents: 父代个体
        :return: 生成的新的子代个体
        """
        # 需要繁殖的孩子数量
        target_count = self.num - len(parents)
        children = []
        while len(children) < target_count:
            # 选择两个不同的父亲与母亲下标
            while True:
                male_index = random.randint(0, len(parents) - 1)
                female_index = random.randint(0, len(parents) - 1)
                if male_index != female_index:
                    break
            male = parents[male_index]
            female = parents[female_index]
            # 随机选择父亲与母亲基因交叉点
            left = random.randint(0, len(male) - 2)
            right = random.randint(left, len(male) - 1)
            # 截取父亲与母亲的left与right之间的基因
            gen_male = male[left:right]
            gen_female = female[left:right]
            child_a = []
            child_b = []

            len_ca = 0
            for g in male:
                # 当child_a中已经存在left个基因时，加上截取的母亲中间的基因
                if len_ca == left:
                    child_a.extend(gen_female)
                    len_ca += len(gen_female)
                # 从父亲基因中选择left个不在gen_female中存在的基因
                if g not in gen_female:
                    child_a.append(g)
                    len_ca += 1

            len_cb = 0
            for g in female:
                # 当child_b中已经存在left个基因时，加上截取的父亲中间的基因
                if len_cb == left:
                    child_b.extend(gen_male)
                    len_cb += len(gen_male)
                # 从母亲基因中选择left个不在gen_male中存在的基因
                if g not in gen_male:
                    child_b.append(g)
                    len_cb += 1
            if len(children) + 1 == target_count:
                children.append(child_a)
            else:
                children.append(child_a)
                children.append(child_b)

        return children

    # 变异操作
    def mutation(self, population):
        """
        :param parents: 种群中的所有个体进行编译
        :return: 无
        变异，对种群的所有个体，以一定概率随机改变某个个体中的某个基因，这里改变基因是交换两个点
        """
        for i in range(len(population)):
            if random.random() < self.mutation_rate:
                while True:
                    u = random.randint(0, len(population[i]) - 1)
                    v = random.randint(0, len(population[i]) - 1)
                    if u != v:
                        break
                temp = population[i][u]
                population[i][u] = population[i][v]
                population[i][v] = temp

    def get_best(self, population):
        """得到当前种群中最优的个体"""
        grad = [[x, self.total_distance(x)] for x in population]
        grad = sorted(grad, key=lambda x: x[1])
        return grad[0][0], grad[0][1]

    def get_distance(self):
        distance = np.zeros((self.length, self.length))
        for i in range(self.length):
            for j in range(self.length):
                distance[i, j] = distance[j, i] = np.linalg.norm(self.data[i] - self.data[j])
        return distance
