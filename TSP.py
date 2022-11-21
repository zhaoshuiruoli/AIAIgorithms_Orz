import matplotlib.pyplot as plt
# from GA_TSP import GA
from homework.homework1.homework.TSP.utils.GA_TSP import GA
from homework.homework1.homework.TSP.utils.SA_TSP import SA_TSP
import numpy as np


def plt_show(data, path):
    fig, ax = plt.subplots()
    x = data[:, 0]
    y = data[:, 1]
    ax.scatter(x, y, linewidths=0.1)
    for i, txt in enumerate(range(1, len(data) + 1)):
        ax.annotate(txt, (x[i], y[i]))
    x0 = x[path]
    y0 = y[path]
    for i in range(len(data) - 1):
        plt.quiver(x0[i], y0[i], x0[i + 1] - x0[i], y0[i + 1] - y0[i], color='r', width=0.005, angles='xy', scale=1,
                   scale_units='xy')
    plt.quiver(x0[-1], y0[-1], x0[0] - x0[-1], y0[0] - y0[-1], color='r', width=0.005, angles='xy', scale=1,
               scale_units='xy')
    plt.show()


if __name__ == '__main__':
    np.random.seed(10)
    data = np.random.rand(50, 2) * 30

    ga = GA(num=500, data=data, iter_num=1000, retain_rate=0.3, select_rate=0.5, mutation_rate=0.1, gailiang_num=300)

    individual, distance = ga.get_init()

    # print(individual)
    # print(distance)
    plt_show(data, individual)
    print("GA初始路径距离：", distance)
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    plt.rcParams['axes.unicode_minus'] = False

    cur_best_res, cur_best_dis, distance_list = ga.evolve()
    plt_show(data, cur_best_res)
    print("GA最后路径距离", cur_best_dis)
    plt.figure(2)
    plt.plot(np.array(distance_list))
    plt.title('优化过程')
    plt.ylabel('最优值')
    plt.xlabel('代数({}->{})'.format(0, 1000))
    plt.show()

    sa = SA_TSP(data=data, T=1000, T_end=1e-3, L=1000, r=0.95)
    cur_path, distance = sa.get_init()
    plt_show(data, cur_path)
    print("SA初始路径距离：", distance)
    cur_best_path, cur_best_dis = sa.simulated_annealing()
    plt_show(data, cur_best_path[-1])
    print("SA最后路径距离", cur_best_dis[-1])
    plt.figure(3)
    plt.plot(np.array(cur_best_dis))
    plt.title('优化过程')
    plt.ylabel('最优值')
    plt.xlabel('代数({}->{})'.format(0, len(cur_best_dis)))
    plt.show()
