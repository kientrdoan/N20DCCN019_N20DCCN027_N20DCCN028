"""
Trương Thái Hoàng - N20DCCN019
Đoàn Trung Kiên - N20DCCN027
Lê Ngọc Tuấn Kiệt - N20DCCN028  
"""
import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy

def read_districts():
    input_districs = []
    with open("districts.txt", "r", encoding= "utf-8") as f:
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

def goInto(node, leng):
    if leng>=len(G.nodes):
        return True
    if not any(G.nodes[node]["color_available"]):
        return False
    for color in range(len(colors)):
        if G.nodes[node]["color_available"][color]:
            G.nodes[node]['color'] = color
            leng+=1
            for neighbor in G.neighbors(node):
                G.nodes[neighbor]["color_available"][color]=False
            noMoreNode=True
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]['color'] is None:
                    noMoreNode=False
                    isColorUsable = goInto(neighbor, leng)
                    if not isColorUsable:
                        for neighborRevert in G.neighbors(node):
                            G.nodes[neighborRevert]["color_available"][color]=True
                        leng-=1
                        G.nodes[node]['color']=None
                        G.nodes[node]["color_available"][color]=False
                        break
            if noMoreNode:
                return True
    return False

def GenerateAndTest():
    for node in G.nodes():
        color_available=[True]* len(colors)
        for nodeChange in G.nodes():
            G.nodes[nodeChange]["color_available"] = deepcopy(color_available)
        G.nodes[node]['color'] = 0
        leng=1
        for neighbor in G.neighbors(node):
            G.nodes[neighbor]["color_available"][0]=False
        for neighbor in G.neighbors(node):
            possible = goInto(neighbor, leng)
            if not possible:
                for nodeRevert in G.nodes:
                    G.nodes[nodeRevert]['color']=None
                break
            else: return True
    return False

if __name__ =="__main__":
    possible = GenerateAndTest()
    if possible:
        pos = nx.spring_layout(G)
        # # nx.draw(G, pos, node_color=node_colors, with_labels=True)
        nx.draw(G, with_labels=True, node_color=[colors[G.nodes[node]["color"]] for node in G.nodes()])
        plt.show()
    else:
        print("Khong the to mau")