import numpy as np
from AI_AIgorithms_Orz.BAG.SA_Bag import SA_Bag
from AI_AIgorithms_Orz.BAG.GA_Bag import GA_Bag
import matplotlib.pyplot as plt


def plt_show(data, n, title, ylabel, xlebel):
    plt.figure(n)
    plt.plot(data)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlebel)
    plt.show()


if __name__ == '__main__':
    np.random.seed(10)
    weight = np.random.randint(low=5, high=30, size=300)
    profit = np.random.randint(low=5, high=50, size=300)
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    plt.rcParams['axes.unicode_minus'] = False

    ga = SA_Bag(data=weight, price=profit, C=5000)

    best_ways, best, best_weight, best_value = ga.simulated_annealing()

    plt_show(np.array(best_weight), 1, 'SA最优解对应的总重', '每轮对应的总重', '代数({}->{})'.format(0, len(best_weight)))
    plt_show(np.array(best_value), 2,'SA优化过程','每轮最优解','代数({}->{})'.format(0, len(best_value)))


    ga = GA_Bag(num=60, weight=weight, profit=profit, W=5000, iter_num=1000, crossover_rate=0.8, mutation_rate=0.05)

    best_value, best_single, best_weight = ga.evolve()

    plt_show(np.array(best_weight), 3, 'GA最优解对应的总重', '每轮对应的总重', '代数({}->{})'.format(0, len(best_weight)))
    plt_show(np.array(best_value), 4,'GA优化过程','每轮最优解','代数({}->{})'.format(0, len(best_value)))

