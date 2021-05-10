import networkx as nx
import matplotlib.pyplot as plt
from textwrap import fill
import random

# 该程序里的时间方向严格意义指的因到果的方向（或者key到value的方向，min path里右箭头的方向）
# 因此就算考虑到时间倒流或某人穿越回过去，即时间不单调，该程序的输出不受影响，因为因果链不变（逻辑关系不变）
# 所以宏观经济中的a导致b到底是什么？如果是因果链，那么a+导致a-不就矛盾了吗，正如因为a白所以a黑？
# 如果是时间，即a+后经过了t时间长度发生b+，那么如何能保证这个时间系统是自洽的呢？方程组(所有存在的路径)的个数大于未知数(edge)的个数不能保证这一点
# 若每个量随时间的变化是连续的，也即len(jargons)元微分方程组，那参数（每个量的变化受其他量的变化的影响的权重）该如何设才能保证方程组存在解呢？
graph = {'reserve require ratio -': ['money supply +'],
         'money supply +': ['nominal interest rate -'],
         'real interest rate -': ['nominal interest rate -', 'consumption +', 'investment +'],  # real?
         'nominal interest rate -': ['supply of currency +'],  # real?
         'supply of currency +': ['exchange rate -'],
         'exchange rate -': ['net exports +'],
         'net exports +': ['aggregate demand +'],
         'aggregate demand +': ['GDP +', 'price level +'],
         'GDP +': ['unemployment -', 'money demand +'],
         'consumption +': ['aggregate demand +'],
         'investment +': ['aggregate demand +'],
         'government spending +': ['aggregate demand +'],
         'tax -': ['consumption +', 'investment +'],
         'price level +': ['money demand +', 'nominal interest rate +'],
         'money demand +': ['nominal interest rate +'],
         'government borrowing +': ['demand for loanable funds +'],
         'demand for loanable funds +': ['real interest rate +'],
         'discount rate -': ['money supply +'],  # ?
         'labor +': ['aggregate supply +'],
         'capital stock +': ['aggregate supply +'],
         'technology +': ['aggregate supply +'],
         'aggregate supply +': ['price level -'],
         }


# spending multiplier
# government deficit + → government borrowing + 或许不能添加到里面，或由于这是直接人为干涉，而graph里的据假设都是自然会发生的；这两个变量并不构成因果


def DrawDiGraph(data, start, end):
    print("condition: {}, result: {}".format(start, end))
    fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
    g_nx = nx.DiGraph()
    nodes = []
    edges = []
    width = 10
    # jargons=[]
    for key in data:
        # print(key)
        # print(data[key])
        # nodes.append(key)
        nodes.append(fill(key, width))
        # jargons.append(key[:-2])
        for v in data[key]:
            # edges.append((key,v))
            edges.append((fill(key, width), fill(v, width)))
            # jargons.append(v[:-2])

    # print(nodes)
    # print(edges)
    # print(set(jargons))
    g_nx.add_nodes_from(nodes)
    g_nx.add_edges_from(edges)
    nx.draw(g_nx, with_labels=True, node_color='r', node_size=500, font_size=6.5)
    path = findShortestPath(graph, start, end)

    if path:
        plt.title(fill("min path : " + ' → '.join(path), 100))
    else:
        plt.title("No path from {} to {}".format(start, end))
    plt.show()


# 找到所有从start到end的路径
def findAllPath(graph, start, end, path=[]):
    # print(path)
    path = path + [start]  # 用于这个函数内的递归，传递path变量
    if start == end:
        return [path]

    paths = []  # 存储所有路径
    if start in graph:
        for node in graph[start]:
            if node not in path:
                newpaths = findAllPath(graph, node, end, path)
                # print("node:{}".format(node))
                # print("newpaths:{}\n".format(newpaths))
                for newpath in newpaths:
                    paths.append(newpath)

    return paths


# 查找最短路径
def findShortestPath(graph, start, end, path=[]):
    all_path = findAllPath(graph, start, end, path)
    min_len = -1
    min_path = []
    for p in all_path:
        print(p)
        if min_len == -1:
            min_len = len(p)
            min_path = p
        elif len(p) < min_len:
            min_len = len(p)
            min_path = p
    print("min path:{}".format(min_path))
    return min_path


def opposite(change):
    if change[-1] == '+':
        altern = change[:-1] + '-'
    else:
        altern = change[:-1] + '+'
    return altern


# 将graph据自己作镜像，对每个以±结尾的key和value添加以∓结尾的镜像
# 之所以可以这么做，是因为graph中没有随时间单调增减的变量（如时间）
# 之所以没有单调变量，或因为宏观经济中讨论单调变量没有意义
def mirror_graph():
    for key in list(graph.keys()):  # 不用global graph是因为list是可变数据类型
        altern = opposite(key)
        if altern not in graph:
            graph[altern] = []
            for item in graph[key]:
                graph[altern] += [opposite(item)]


# 生成术语表
def generate_jargons(data):
    global jargons
    for key in data:
        jargons.append(key[:-2])
        for v in data[key]:
            jargons.append(v[:-2])
    jargons = list(set(jargons))


def generate_Macro_jargons():
    generate_jargons(graph)


def print_Macro_jargons():
    print("jargons: {}".format(jargons))
    # print("number: {}".format(len(jargons)))
    print()


# 据输入的condition和result生成图像和最短路径
def receive_input():
    example_condition = "money supply +"
    example_result = "GDP"
    print_Macro_jargons()

    print('example of condition (default): {}'.format(example_condition))
    condition = input('condition: ').strip()
    while not ((condition[-2:] == " +" or condition[-2:] == " -") and condition[:-2] in jargons):
        if condition == "":
            condition = example_condition
        elif condition[-2:] != " +" and condition[-2:] != " -":
            condition = input('condition must end in " +" or " -": ').strip()
        elif condition[:-2] not in jargons:
            condition = input('condition must be in jargons: ').strip()

    print('example of result (default): {}'.format(example_result))
    result = input('result: ').strip()
    while not (result[-1:].isalpha() and result in jargons):
        if result == "":
            result = example_result
        elif not result[-1:].isalpha():
            result = input('result must end in letter: ').strip()
        elif result not in jargons:
            result = input('result must be in jargons: ').strip()

    print()
    DrawDiGraph(graph, condition, result + ' +')
    print()
    DrawDiGraph(graph, condition, result + ' -')


def two_random_variables():
    DrawDiGraph(graph, random.choice(jargons) + random.choice([" +", " -"]),
                random.choice(jargons) + random.choice([" +", " -"]))


def one_random_variable():
    random_variable = random.choice(jargons)
    DrawDiGraph(graph, random_variable + " +", random_variable + " -")


def crowding_out():
    DrawDiGraph(graph, 'government borrowing +', 'investment -')


jargons = []
generate_Macro_jargons()
# print_Macro_jargons()
mirror_graph()

print("0. Show min path between two inputs, one for the condition and one for the result.")
print("1. Show min path between two random changes.")
print("2. Show min path between the increase and decrease of a random variable.")
print("3. Show the path of the Crowding Out Effect.")
print("4. Show all variables.")

function_list = [receive_input, two_random_variables, one_random_variable, crowding_out, print_Macro_jargons]
function_number = len(function_list)
choice = input("Enter your choice (integer between 0 to {}): ".format(function_number - 1))
while not (choice.isnumeric() and 0 <= int(choice) <= function_number - 1):
    choice = input("Enter your choice (integer between 0 to {}): ".format(function_number - 1))
print()
function_list[int(choice)]()

# 不够简洁的代码（while循环就可以解决）


# 使用户输入有效的condition，递归写法，无返回值，问题在于如果不解开注释一行，则进入while后即使condition为空字符串也不行
# 之所以要在外面给空字符串赋值，是因为在循环里面赋值的话，每次循环都需要重新更改一下example的值；否则就要global example_condition
# def loop_condition():
#     global condition
#     condition = condition.strip()
#     print(condition)
#     if condition == "":
#         pass
#         # condition=example_condition
#
#     else:
#         while condition[-2:] != " +" and condition[-2:] != " -":
#             condition = input('condition must end in " +" or " -": ')
#             loop_condition()
#         if condition[:-2] not in jargons:
#             condition = input('condition must be in jargons: ')
#             loop_condition()


# loop_condition的返回值的递归写法，免去global condition，但每次递归需要传递参数；无需把第一次输入提示放在其他函数中，但第一次后还需额外判断输入是不是None
# def loop_condition(condition=None, example="money supply +"):
#     # global condition
#
#     if condition is None:
#         print('example of condition: {}'.format(example))
#         condition = input('condition: ')
#
#     condition = condition.strip()
#
#     if condition == "":
#         condition = example
#     else:
#         while condition[-2:] != " +" and condition[-2:] != " -":
#             condition = input('condition must end in " +" or " -": ')
#             return loop_condition(condition=condition)
#         if condition[:-2] not in jargons:
#             condition = input('condition must be in jargons: ')
#             return loop_condition(condition=condition)
#     print("condition{}".format(condition))
#     return condition
