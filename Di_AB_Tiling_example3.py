import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,pi,acos,atan
from Graph_Calc_Print import graph_calc_print
from AB_Tiling import AB_tiling
from G_ex import get_AB_tiling_kasteleyn_orientation_graph_calc_print

AB1 = AB_tiling()
AB2 = AB1.inflate()
AB3 = AB2.inflate() #a 3 times inflated ab tiling star graph

Di_AB3 = get_AB_tiling_kasteleyn_orientation_graph_calc_print(AB3) #makes if an oriented graph calc print

Di_AB3.Di_print() #shows the graph

Di_sub_test = Di_AB3.sub_graph(0,0) #the function returns the graph without the central vertex (the 0 vertex and every neighbor of degree 0 of it, meaning only it)

Di_sub_test.Di_print() #shows the graph

Di_sub_test = Di_AB3.sub_graph(0,1) #the function returns the graph without the central vertex and nearest neighbors to it

Di_sub_test.Di_print() #shows the graph


'''need to note that the returned graph is not reoriented after the remove of the nodes, which can make the returned graph to have a non kasteleyn orientation'''

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