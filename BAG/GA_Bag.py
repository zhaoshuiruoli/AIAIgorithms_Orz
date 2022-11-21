import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import math
import random


class GA_Bag():
    def __init__(self, num, weight, profit, W, iter_num, crossover_rate, mutation_rate):
        self.num = num  # 种群长度
        self.weight = weight
        self.profit = profit
        self.W = W
        self.length = len(profit)  # 染色体长度
        self.itet_num = iter_num
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.initialize_population = self.initialize_population()

    # def get_init(self):
    #     population = self.initialize_population
    #     fitnesses = self.get_fitness(population)
    #     return self.get_best(population, fitnesses)

    def evolve(self):
        population = self.initialize_population

        # fitness_list = []
        # cur_best_res, cur_best_fit = self.get_best(population, fitnesses)
        # fitness_list.append(cur_best_fit)
        best_value = []
        best_single = []
        best_weight = []
        for i in range(self.itet_num):
            # print("***************" + str(i) + "******************")

            fitnesses = self.get_fitness(population)

            population_new, fitnesses_new = self.nature_select(population, fitnesses)
            fitnesses_1 = list(np.array(fitnesses_new)[:, 0])
            # print(fitnesses_new)
            # print(fitnesses_1)
            # print(type(fitnesses_1))

            best_index = fitnesses_1.index(max(fitnesses_1))
            # print(best_index)
            # print("))))))))))))")
            best_value.append(fitnesses_new[best_index][0])
            best_single.append(population_new[best_index])
            best_weight.append(fitnesses_new[best_index][1])

            population_new = self.roulette_wheel(population_new, fitnesses_new)
            fitnesses_new = self.get_fitness(population_new)
            population_new = self.crossover(population_new, fitnesses_new)
            population = self.mutation(population_new)

        return best_value, best_single, best_weight

    def initialize_population(self):
        """
        初始化种群，一共num个个体,基因长度为self.length
        :return:
        """

        population = []
        for i in range(self.num):
            pop = ''
            for j in range(self.length):
                pop = pop + str(np.random.randint(0, 2))
            population.append(pop)
        return population

    # 计算适应度
    def get_fitness(self, population):
        fitnesses = []
        for chromosome_state in population:  # 遍历所有的染色体
            value_sum = 0  # 物品重量
            weight_sum = 0  # 物品价值
            # 将一个可遍历的数据对象组合为一个索引序列，同时列出数据和数据下标
            for i, v in enumerate(chromosome_state):
                # 对染色体中的1，即存在的物品体重和价格求和
                if int(v) == 1:
                    weight_sum += self.weight[i]
                    value_sum += self.profit[i]
            fitnesses.append([value_sum, weight_sum])
        return fitnesses

    def get_fitness_single(self, single):
        protit_single = 0
        for i in range(len(single)):
            if int(single[i]) == 1:
                protit_single += self.profit[i]
        return protit_single

    def nature_select(self, population, fitnesses):
        """
        自然选择代码，按照一定的概率淘汰掉弱的个体
        :param population:
        :return:
        """
        ppopulation_new = []
        fitnesses_new = []
        for i in range(len(population)):
            if fitnesses[i][1] <= self.W:
                ppopulation_new.append(population[i])
                fitnesses_new.append(fitnesses[i])

        return ppopulation_new, fitnesses_new

    def roulette_wheel(self, population, fitnesses):
        fitness_sum = []
        fitnesses_1 = list(np.array(fitnesses)[:, 0])
        value_sum = sum(fitnesses_1)
        fitness = [i / value_sum for i in fitnesses_1]
        for i in range(len(population)):  ##
            if i == 0:
                fitness_sum.append(fitness[i])
            else:
                fitness_sum.append(fitness_sum[i - 1] + fitness[i])
        population_new = []
        for j in range(self.num):
            select_p = np.random.uniform()
            for k in range(len(population)):
                if select_p > fitness_sum[k] and select_p <= fitness_sum[k + 1]:
                    population_new.append(population[k])
        return population_new

    def crossover(self, population, fitnesses):
        population_new = []

        while len(population_new) < self.num:
            while True:
                male_index = random.randint(0, len(population) - 1)
                female_index = random.randint(0, len(population) - 1)
                if male_index != female_index:
                    break
            point = np.random.randint(0, self.length)
            p = np.random.uniform()
            if (p < self.crossover_rate):
                chile_one = population[male_index][:point] + population[female_index][point:]
                chile_two = population[female_index][:point] + population[male_index][point:]
                pro1 = self.get_fitness_single(chile_one)
                pro2 = self.get_fitness_single(chile_two)
                if pro1 > fitnesses[male_index][0] and pro1 > fitnesses[female_index][0]:
                    population_new.append(chile_one)
                else:
                    if fitnesses[female_index][0] > fitnesses[male_index][0]:
                        population_new.append(population[female_index])
                    else:
                        population_new.append(population[male_index])
                if pro2 > fitnesses[male_index][0] and pro2 > fitnesses[female_index][0]:
                    population_new.append(chile_two)
                else:
                    if fitnesses[female_index][0] > fitnesses[male_index][0]:
                        population_new.append(population[female_index])
                    else:
                        population_new.append(population[male_index])
        return population_new

    def mutation(self, population):
        population_new = []
        for pop in population:
            p = np.random.uniform()
            if p < self.mutation_rate:
                point = np.random.randint(0, len(population[0]))
                pop = list(pop)

                if pop[point] == '0':
                    pop[point] = '1'
                elif pop[point] == '1':
                    pop[point] = '0'
                pop = ''.join(pop)
                population_new.append(pop)
            else:
                population_new.append(pop)
        return population_new
