"""
    Trương Thái Hoàng - N20DCCN019
    Đoàn Trung Kiên - N20DCCN027
    Lê Ngọc Tuấn Kiệt - N20DCCN028
"""
import networkx as nx
import matplotlib.pyplot as plt
import random
# from networkx.drawing.nx_pydot import graphviz_layout
# from networkx.drawing.nx_pydot import graphviz_layout
# import pygraphviz as pgv

def read_districts():
    input_districs = []
    with open("districts.txt", "r", encoding= "utf-8") as f:
    #with open("cityustralia.txt", "r", encoding= "utf-8") as f:
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
    #with open("edgescityustralia.txt", "r", encoding= "utf-8") as f:
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

# danh sách các huyện
districts = read_districts()
edges = read_edges()
# print(edges)

# print(districts)

# Khởi tạo đồ thị
G = nx.Graph()
G.add_nodes_from(districts) 
G.add_edges_from(edges)

# Khởi tạo danh sách các màu có thể sử dụng
colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'black', 'brown', 'grey']
# colors = ['red', 'blue', 'green']



# Định nghĩa hàm kiểm tra một màu có thể sử dụng cho một nút hay không
# def is_color_valid(node, color):
#     neighbors = list(G.neighbors(node))
#     for neighbor in neighbors:
#         neighbor_color = G.nodes[neighbor].get('color')
#         #neu mau to cho node hien tai trung voi bat ky canh ke voi canh hien tai
#         if neighbor_color == color:
#             return False
#     return True


# hàm tìm nút tiếp theo để tô màu
def next_node():
    max_degree = -1
    max_degree_node = None
    for node in list(G.nodes()):
        if G.nodes[node].get('color') is None:
            #Đầu tiên ưu tiên biên bị ràng buộc nhiều nhất
            degree = len([node for node in G.neighbors(node) if G.nodes[node].get('color') is not None])
            if degree > max_degree:
                max_degree = degree
                max_degree_node = node
            #Hai node có độ ưu tiên biến bị ràng buộc như nhau
            elif degree == max_degree:
               
                degree_neighbors_node = len([node for node in G.neighbors(node) if G.nodes[node].get('color') is None])
                max_degree_neighbors_node = len([node for node in G.neighbors(max_degree_node) if G.nodes[node].get('color') is None])
                #Uư tiên node không chế node lân cận nó chưa tô màu nhiều hơn
                # print(node, degree_neighbors_node, max_degree_node, max_degree_neighbors_node)
                if degree_neighbors_node > max_degree_neighbors_node:
                    max_degree_node = node

    return max_degree_node

#Lay Mien Gia Tri
def lay_mien_gia_tri(node):
    used_color = set()
    for node in list(G.neighbors(node)):
        if G.nodes[node].get('color') is not None:
            used_color.add(G.nodes[node].get('color'))

    # print(set(used_color))
    # domain = list(set(colors)-set(used_color))
    domain = [color for color in colors if color not in used_color]

    # for color in domain:
    #     if color in used_color:
    #         domain.remove(color)
    return domain

def check_neighbors(node):
    for n in G.neighbors(node):
        domain_next_node = lay_mien_gia_tri(n)
        if len(domain_next_node) == 0:
            return True
    return False

# thuật toán tô màu quay lui
def backtrack_coloring(node):
    if node is None:
        return True
    domain = lay_mien_gia_tri(node)
    print(node)
    for color in domain:    
        # if is_color_valid(node, color):
        if check_neighbors(node):
            continue
        G.nodes[node]['color'] = color  
        # print(node, domain, color)     
        if backtrack_coloring(next_node()):
            return True
        # if node is not None and len(lay_mien_gia_tri(next_node())) != 0:
            # backtrack_coloring(next_node())
            # return True
        G.nodes[node]['color'] = None
        
    return False

if __name__ == "__main__":

    if backtrack_coloring(next_node()):
        color_map = [G.nodes[node]['color'] for node in G.nodes()]

        # pos = {
        # 'AG': (0, 0), 'KG': (1, 1), 'CT': (1, -1),
        # 'BL': (2, 0), 'CM': (3, 1), 'ST': (3, -1),
        # 'PQ': (4, 0)
        # }

        # pos = {
        # 'Quận 1': (0, 1), 'Quận 3': (0, 0), 'Quận 4': (0, 2), 
        # 'Quận 5': (1, 1), 'Quận 6': (1, 0), 'Quận 7': (1, -1),
        # 'Quận 8': (2, 2), 'Quận 10': (2, 1), 'Quận 11': (2, 0), 
        # 'Quận 12': (2, -1), 'Thành phố Thủ Đức': (2, -2),
        # 'Quận Bình Tân': (3, 2), 'Quận Bình Thạnh': (3, 1), 
        # 'Quận Gò Vấp': (3, 0), 'Quận Phú Nhuận': (3, -1), 'Quận Tân Bình': (3, -2),
        # 'Quận Tân Phú': (4, 1), 'Huyện Bình Chánh': (4, 0), 
        # 'Huyện Cần Giờ': (4, -1), 'Huyện Củ Chi': (5, 1), 'Huyện Hóc Môn': (5, 0),
        # 'Huyện Nhà Bè': (5, -1)
        # }
        

        # pos = {
        # 'WA': (0, 0), 'NT': (1, 1), 'Q': (2, 1),
        # 'SA': (1, -1), 'NSW': (2, -1), 'V': (2, -2),
        # 'T': (3, 3)
        # }


        # Tạo vị trí ngẫu nhiên cho các node còn lại
        pos = nx.spring_layout(G)
        # Thay thế vị trí của node đầu tiên bằng vị trí mà bạn mong muốn
        pos['Quận 1'] = (-1, 0)

        nx.draw(G, pos,with_labels=True, node_color=color_map)
        plt.show()



