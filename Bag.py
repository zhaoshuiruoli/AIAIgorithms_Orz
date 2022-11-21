import numpy as np
from AI_AIgorithms_Orz.BAG.SA_Bag import SA_Bag
from AI_AIgorithms_Orz.BAG.GA_Bag import GA_Bag
import matplotlib.pyplot as plt

if __name__ == '__main__':
    np.random.seed(10)
    weight = np.random.randint(low=5, high=30, size=300)
    profit = np.random.randint(low=5, high=50, size=300)

    ga = SA_Bag(data=weight, price=profit, C=5000)

    best_ways, best, best_weight, best_value = ga.simulated_annealing()

    print(best_weight)
    print(best_ways)
    print(best)

    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(1)
    plt.plot(np.array(best_weight))
    plt.title('优化过程')
    plt.ylabel('最优值')
    plt.xlabel('代数({}->{})'.format(0, 1000))
    plt.show()

    plt.figure(2)
    plt.plot(np.array(best_value))
    plt.title('优化过程')
    plt.ylabel('最优值')
    plt.xlabel('代数({}->{})'.format(0, 1000))
    plt.show()

    ga = GA_Bag(num=60, weight=weight, profit=profit, W=5000, iter_num=1000, crossover_rate=0.8, mutation_rate=0.05)


    best_value, best_single, best_weight = ga.evolve()


    plt.figure(1)
    plt.plot(np.array(best_weight))
    plt.title('优化过程')
    plt.ylabel('最优值')
    plt.xlabel('代数({}->{})'.format(0, 1000))
    plt.show()

    plt.figure(2)
    plt.plot(np.array(best_value))
    plt.title('优化过程')
    plt.ylabel('最优值')
    plt.xlabel('代数({}->{})'.format(0, 1000))
    plt.show()