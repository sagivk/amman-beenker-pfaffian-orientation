import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,pi,acos,atan
from Graph_Calc_Print import graph_calc_print
from AB_Tiling import AB_tiling
from G_ex import get_AB_tiling_kasteleyn_orientation_graph_calc_print

AB1 = AB_tiling() #creating ab tiling of 8 rhombuses
AB2 = AB1.inflate()
AB3 = AB2.inflate()
AB4 = AB3.inflate() #inflating the original tiling 4 times
Di_AB4 = get_AB_tiling_kasteleyn_orientation_graph_calc_print(AB4) #get the kasteleyn oriented version of the graph (takes some time since assembling the graph is n^2 and orienting it is n
Di_AB4.Di_print(node_size = 10, labels = False) #shows to the user the graph created
r = 2
while r < 10:
    Di_part_AB = Di_AB4.part_graph(node_index = 0, radius = r, drop_non_connected_nodes = True) #the function takes only a part of the graph, around the center vertex, with r jumps from vertex to vertex. the drop_non_connected_nodes = True makes the returned graph to have no nodes that are not part of a rectangle
    eigenvalues,eigenvectors,zero_indecies = Di_part_AB.get_graph_zero_modes() #get_graph_zero_modes creates the graphs matrix and diagonalize it numercly. eigenvalues that are smaller (abs) than 10^-3 are considered 0
    if len(eigenvalues) == 1: #the code check if there are multiple 0 states
        print('r = ' + str(r) + ' has a single zero mode')
    r += 1
    
Di_part_AB.Di_print(node_size = 10, labels = True) #shows to the user the graph around the center vertex, as created by the last run of the while loop

Di_part_AB_R9 = Di_AB4.part_graph(node_index = 0, radius = 9, drop_non_connected_nodes = True) #gets a graph around the center vertex of radius 9 without vertexes not part of a closed shape 

Di_part_AB_R9.Di_print(node_size = 10, labels = True) #show to the user the radius 9 shape
zero_eigenvalues,zero_eigenvectors,zero_indecies = Di_part_AB.get_graph_zero_modes() #get the radius 9 zero modes

print('zero_eigenvectors = ' + str(zero_eigenvectors))
print('zero_indecies = ' + str(zero_indecies))

eigenvalues, eigenvectors = Di_part_AB_R9.get_graph_eigenpairs(return_edge_weight_matrix = False) #diagonalize metrix

print('eigenvalues = ' + str(eigenvalues))

i = input()

while i != 'exit': #the while loop allows printing the radius 9 graph zero modes
    Di_part_AB_R9.Di_print_modes(vector_index = int(i),labels = False)
    i = input()