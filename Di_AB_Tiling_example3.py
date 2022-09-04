import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,pi,acos,atan
from Graph_Calc_Print import graph_calc_print
from AB_Tiling import AB_tiling
from G_ex import get_AB_tiling_kasteleyn_orientation_graph_calc_print

AB1 = AB_tiling()
#AB1.print_tiling()
AB2 = AB1.inflate()
#AB2.print_tiling()
AB3 = AB2.inflate()
#AB3.print_tiling()
#AB4 = AB3.inflate()
#AB5 = AB4.inflate()
#Di_AB5 = get_AB_tiling_kasteleyn_orientation_graph_calc_print(AB5)
#Di_AB4.Di_print(node_size = 10, labels = False)

Di_AB3 = get_AB_tiling_kasteleyn_orientation_graph_calc_print(AB3)

Di_AB3.Di_print()

Di_sub_test = Di_AB3.sub_graph(0,1)

Di_sub_test.Di_print()

#r = 5
#while r < 15:
#    Di_part_AB = Di_AB5.part_graph(node_index = 0, radius = r, drop_non_connected_nodes = True)
#    eigenvalues,eigenvectors,zero_indecies = Di_part_AB.get_graph_zero_modes()
#    if len(eigenvalues) == 1:
#        print('r = ' + str(r) + ' has a single zero mode')
#    r += 1
    
#Di_part_AB.Di_print(node_size = 10, labels = True)

#Di_part_AB_R9 = Di_AB4.part_graph(node_index = 0, radius = 9, drop_non_connected_nodes = True)

#Di_part_AB_R9.Di_print(node_size = 10, labels = True)
#zero_eigenvalues,zero_eigenvectors,zero_indecies = Di_part_AB.get_graph_zero_modes()

#print('zero_eigenvectors = ' + str(zero_eigenvectors))
#print('zero_indecies = ' + str(zero_indecies))

#eigenvalues, eigenvectors = Di_part_AB_R9.get_graph_eigenpairs(return_edge_weight_matrix = False)

#print('eigenvalues = ' + str(eigenvalues))

#i = input()

#while i != 'exit':
#    Di_part_AB_R9.Di_print_modes(vector_index = int(i),labels = False)
#    i = input()