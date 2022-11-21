from math import exp
import numpy as np
import matplotlib.pyplot as plt


class SA_TSP(object):
    def __init__(self, data, T=1000, T_end=1e-3, L=200, r=0.9):
        self.T = T  # 初始温度
        self.T_end = T_end  # 终止温度
        self.data = data  # 位置坐标
        self.num = len(data)  # 城市个数
        self.L = L  # 每一个温度下的链长
        self.r = r  # 降温速率
        # 距离矩阵
        self.all_path_distance = self.get_distance()
        self.current_path = np.array([0] * self.num)  # 初始化路径和距离
        self.current_distance = 0

        self.new_path = np.array([0] * self.num)  # 变换后的路径和距离
        self.new_distance = 0

    def get_init(self):
        self.rand_individual()
        return self.current_path, self.current_distance

    def simulated_annealing(self):

        # # 存储最退火过程中的最优路径变化
        best_path = [self.current_path]
        best_distance = [self.current_distance]
        #
        count = 0
        while self.T > self.T_end:
            path_arr = []
            distance_arr = []  # 存储每一个退火过程的路径和距离找寻最优

            for i in range(self.L):
                self.new_way_1()  # 变换产生新路径
                self.metropolis()  # 判断是否接受新路径

                path_arr.append(self.current_path)
                distance_arr.append(self.current_distance)

            # 存储该步迭代后的最优路径,即求最小值的索引
            index = np.argmin(distance_arr)
            if distance_arr[index] >= best_distance[-1]:
                best_distance.append(best_distance[-1])
                best_path.append(best_path[-1])
            else:
                best_path.append(path_arr[index])
                best_distance.append(distance_arr[index])

            # 更新温度
            self.T *= self.r
            count += 1

        print(count)
        return best_path, best_distance

    def rand_individual(self):
        rand_ch = np.array(range(self.num))
        np.random.shuffle(rand_ch)
        self.current_path = rand_ch
        self.current_distance = self.path_distance(rand_ch)

    def get_distance(self):
        distance = np.zeros((self.num, self.num))
        for i in range(self.num):
            for j in range(self.num):
                distance[i, j] = distance[j, i] = np.linalg.norm(self.data[i] - self.data[j])
        return distance

    def path_distance(self, path):
        res = 0
        for i in range(self.num - 1):
            res += self.all_path_distance[path[i], path[i + 1]]
        res += self.all_path_distance[path[-1], path[0]]
        return res

    def new_way_1(self):
        self.new_path = self.current_path.copy()
        r1 = np.random.randint(self.num)
        r2 = np.random.randint(self.num)
        while r2 == r1:
            r2 = np.random.randint(self.num)
        self.new_path[r1], self.new_path[r2] = self.new_path[r2], self.new_path[r1]
        self.new_distance = self.path_distance(self.new_path)

    def metropolis(self):
        ds = self.new_distance - self.current_distance
        if ds < 0:
            # 新路径更短 接受为新解
            self.current_path = self.new_path.copy()  # 数组直接赋值会共享内存 采用copy避免
            self.current_distance = self.new_distance
        else:
            if exp(-ds / self.T) > np.random.rand():
                self.current_path = self.new_path.copy()
                self.current_distance = self.new_distance



