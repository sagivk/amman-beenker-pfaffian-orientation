import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,pi,acos,atan
from Graph_Calc_Print import graph_calc_print
from AB_Tiling import AB_tiling
from G_ex import get_AB_tiling_kasteleyn_orientation_graph_calc_print

AB1 = AB_tiling()
AB2 = AB1.inflate()
AB3 = AB2.inflate()
AB4 = AB3.inflate()
AB5 = AB4.inflate()
Di_AB5 = get_AB_tiling_kasteleyn_orientation_graph_calc_print(AB5)

r = 5
while r < 20:
    Di_part_AB = Di_AB5.part_graph(node_index = 0, radius = r, drop_non_connected_nodes = True)
    eigenvalues,eigenvectors,zero_indecies = Di_part_AB.get_graph_zero_modes()
    if len(eigenvalues) == 1:
        print('r = ' + str(r) + ' has a single zero mode')
    r += 1

Di_part_AB.Di_print(node_size = 10, labels = False)