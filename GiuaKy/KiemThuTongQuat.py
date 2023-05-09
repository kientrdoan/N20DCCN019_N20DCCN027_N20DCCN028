"""
Trương Thái Hoàng - N20DCCN019
Đoàn Trung Kiên - N20DCCN027
Lê Ngọc Tuấn Kiệt - N20DCCN028  
"""
import random
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product as cwr

def read_districts():
    input_districs = []
    # with open("districts.txt", "r", encoding= "utf-8") as f:
    with open("cityustralia.txt", "r", encoding= "utf-8") as f:
    # with open("city.txt", "r", encoding= "utf-8") as f:
        while True:           
            line = f.readline().strip()
            if not line:
                break
            district = (line, {'color': None})
            input_districs.append(district)
            # print(line)
            
    return input_districs

def read_edges():
    input_egdes = []
    # with open("Edges.txt", "r", encoding= "utf-8") as f:
    with open("edgescityustralia.txt", "r", encoding= "utf-8") as f:
    # with open("edgescity.txt", "r", encoding= "utf-8") as f:
        while True:           
            line = f.readline().strip()
            if not line:
                break
            line = line.split(', ')
            edge = tuple(line)
            input_egdes.append(edge)
            
    return input_egdes

# print(read_districts())

districts = read_districts()
edges = read_edges()
# print(edges)

# print(districts)

# Khởi tạo đồ thị
G = nx.Graph()
G.add_nodes_from(districts)  # districts là danh sách các huyện


G.add_edges_from(edges)

# Khởi tạo danh sách các màu có thể sử dụng
colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'black', 'brown', 'grey']
# colors = ['red', 'green']

node_colors = {}




def generate_and_test(graph, list_colors):
    
    # tô màu bất kỳ cho các đỉnh
    coloring = {v: None for v in G.nodes()}
    
    # thỏa mãn các ràng buộc không
    index_combine = 0
    while is_valid_coloring(graph, coloring) == False:
        index_color = 0
        if index_combine >= len(list_colors):
            return False
           
        for v in G.nodes:
            coloring[v] = list_colors[index_combine][index_color]
            index_color += 1
            # print(v, coloring[v])
        index_combine += 1
    # print(is_valid_coloring(graph, coloring), list_colors[7])
        
    return coloring
    
def is_valid_coloring(graph, coloring):
    # Kiểm tra xem phép tô màu của đồ thị có thỏa mãn các ràng buộc không
    for vertex in graph:
        for neighbor in graph[vertex]:
            if coloring[vertex] == coloring[neighbor]:
                return False
    return True




if __name__ =="__main__":
    list_colors = list(cwr(colors,repeat= len(G.nodes())))
    # # node_colors = [node_colors[n] for n in G.nodes]
    coloring = generate_and_test(G, list_colors)
    if coloring:
        pos = nx.spring_layout(G)
        # nx.draw(G, pos, node_color=node_colors, with_labels=True)
        nx.draw(G, with_labels=True, node_color=[coloring[node] for node in G.nodes()])
        plt.show()
    else:
        print("Khong the to mau")
   
