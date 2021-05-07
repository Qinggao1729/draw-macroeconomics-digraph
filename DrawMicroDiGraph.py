import networkx as nx
import matplotlib.pyplot as plt
import json
import re
from textwrap import fill
import random

graph = {'reserve require ratio -': ['money supply +'],
         'money supply +': ['nominal interest rate -'],
         'real interest rate -': ['nominal interest rate -', 'consumption +', 'investment +'],  # real?
         'nominal interest rate -': ['supply of currency +'],  # nominal?
         'supply of currency +': ['exchange rate -'],
         'exchange rate -': ['net exports +'],  # ?
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
         'aggregate supply +': ['price level +'],

         }



# spending multiplier


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
            # jargons.append(key[:-2])

    # print(nodes)
    # print(edges)
    # print(set(jargons))
    g_nx.add_nodes_from(nodes)
    g_nx.add_edges_from(edges)
    nx.draw(g_nx, with_labels=True, node_color='r', node_size=500, font_size=6.5)
    path = findShortestPath(graph, start, end)
    # 这句改成path = findShortestPath(graph,start,end,path=[start,end])后，图上显示no path，findShortestPath里的path变量没变，一直是['A', 'G']
    if path:
        plt.title(fill("min path : " + ' →'.join(path), 100))
    else:
        plt.title("No path from {} to {}".format(start, end))
    plt.show()


# 找到一条从start到end的路径
def findPath(graph, start, end, path=[]):
    path = path + [start]  # 即把start一项添加到path末尾

    if start == end:
        return path
    for node in graph[start]:
        if node not in path:
            newpath = findPath(graph, node, end, path)
            if newpath:
                return newpath
    return None


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
    # 传进来的path的赋值确定了每个路径的前几项，若path为空，则路径的前几项为空，然后继续运算（将start添加到path末尾，即path第一项都是'A'）
    # 若传进来的path=[start,end]，则path前两项是'A'和'G'，第三项（把start添加进来）是'A'，然后再搜索
    # 这么传的问题是，有一句if node not in path的限制，G已经出现了一次，就无法再在末尾出现，所以找不到符合条件的路径
    all = findAllPath(graph, start, end, path)
    # print(all)
    # print("all:{}".format(all))
    # print([x.__str__()+"\n" for x in all])
    # print(list, end="\n")
    for x in all:
        print(x)
    min_len = -1
    min_path = []
    # print("path:{}".format(path))
    for pathh in all:
        if min_len == -1:
            min_len = len(pathh)
            min_path = pathh
        elif len(pathh) < min_len:
            min_len = len(pathh)
            min_path = pathh
    # print("path:{}".format(path))
    print("min path:{}".format(min_path))
    return min_path


def opposite(change):
    if change[-1] == '+':
        altern = change[:-1] + '-'
    else:
        altern = change[:-1] + '+'
    return altern


for key in list(graph.keys()):
    altern = opposite(key)

    if altern not in graph:
        graph[altern] = []
        for item in graph[key]:
            graph[altern] += [opposite(item)]
        # result=re.search(r'^(.+)[+]$',item)
        # result.group(1)


def print_jargons(data):
    global jargons
    for key in data:
        jargons.append(key[:-2])
        for v in data[key]:
            jargons.append(v[:-2])
    jargons = list(set(jargons))
    print("jargons: {}".format(jargons))
    #print(len(jargons))
    print()


def loop_condition():
    global condition
    condition = condition.strip()
    if condition == "":
        condition = "money supply +"
    else:
        while condition[-2:] != " +" and condition[-2:] != " -":
            condition = input('condition must end in " +" or " -": ')
            loop_condition()
        if condition[:-2] not in jargons:
            condition = input('condition must be in jargons: ')
            loop_condition()


def loop_result():
    global result
    result = result.strip()
    if result == "":
        result = "GDP"
    else:
        while not result[-1].isalpha():
            result = input('result must end in letter: ')
            loop_result()
        if result not in jargons:
            result = input('result must be in jargons: ')
            loop_result()


def receive_input():
    global condition
    global result

    print('example of condition: money supply +')
    condition = input('condition: ')
    loop_condition()

    print('example of result: GDP')
    result = input('result: ')
    loop_result()
    print()

    DrawDiGraph(graph, condition, result + ' +')
    print()
    DrawDiGraph(graph, condition, result + ' -')


jargons = []
condition = ""
result = ""
print_jargons(graph)

receive_input()
# DrawDiGraph(graph,'government borrowing +', 'investment -')# crowding out

# DrawDiGraph(graph, random.choice(jargons)+random.choice([" +"," -"]), random.choice(jargons)+random.choice([" +"," -"]))
