"""
Trương Thái Hoàng - N20DCCN019
Đoàn Trung Kiên - N20DCCN027
Lê Ngọc Tuấn Kiệt - N20DCCN028  
"""
import random
import networkx as nx
import matplotlib.pyplot as plt

def read_districts():
    input_districs = []
    with open("districts.txt", "r", encoding= "utf-8") as f:
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
    with open("Edges.txt", "r", encoding= "utf-8") as f:
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

def generate_and_test(graph, colors):
    
    #danh sách các đỉnh của đồ thị
    vertices = list(graph.nodes())
    # Sinh ra một tô màu bất kỳ cho các đỉnh
    coloring = {v: colors[0] for v in vertices}
    
    count = 0
    # Kiểm tra thỏa mãn các ràng buộc 
    while not is_valid_coloring(graph, coloring):
        coloring = {v: random.choice(colors) for v in vertices}
        count += 1
        if count >= 1000000:
            return False
    
    return coloring
    
def is_valid_coloring(graph, coloring):
    for vertex in graph.nodes():
        for neighbor in graph.neighbors(vertex):
            if coloring[vertex] == coloring[neighbor]:
                return False
    return True




if __name__ =="__main__":
    
    # node_colors = [node_colors[n] for n in G.nodes]
    coloring = generate_and_test(G, colors)
    if coloring != False:
        pos = nx.spring_layout(G)
        # nx.draw(G, pos, node_color=node_colors, with_labels=True)
        nx.draw(G, with_labels=True, node_color=[coloring[node] for node in G.nodes()])
        plt.show()
    else:
        print("Dữ liệu quá lớn! Dùng thuật toán khác đi")
