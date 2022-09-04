import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,pi,acos,atan

'''the code overall creates 2 graphs. since networkx directed graphs can have 2 values for each edge (one in each direction) we can't create from
them a matrix which is anti-hermitian we can print (since the arrows will point in both ways).
so this object streamlines the fact that we need one graph to act as it is directed both ways, meaning we can create a matrix to calculate
graph properties with and another graph allowing to print the intended graph.
an additional property this object allows is to print number each of the nodes. for the users of the object nodes are added with location,
but the graph is giving them index and uses pos_index_dict to connect between the index and posstion.
the index is given to allow graph cutting in future'''

get_zero_indecies = lambda eigenvalues, err: np.where(np.absolute(eigenvalues)<err)[0]

def set_color_map(vector): #get a vector and returns the color map represnting it, normalised by the vector's maximum value
    color_map = []
    for i in vector:
        color_map.append(number_to_color(i/np.amax(vector)))
    return color_map

def number_to_color(number): #get a number between 1 and 0 and return a color between blue and red in a format that nx.draw can use
    brightness = round(255 * number)
    red = int(brightness)
    green = 0
    blue = int(255 - brightness)
    return '#%02x%02x%02x' % (red, green, blue)

class graph_calc_print:
    
    def __init__(self,setup = False): #creates the 4 properties of the graph, the print graph, calculations graph the index dict and index
        if setup:
            self.G_for_calc = setup[0]
            self.G_for_print = setup[1]
            self.current_index = setup[2] #probably can be cut out of the code since len(G_for_calc.nodes) should be equal to current_index
            self.pos_index_dict = setup[3]
        else:
            self.G_for_calc = nx.DiGraph()
            self.G_for_print = nx.DiGraph()
            self.current_index = 0 #probably can be cut out of the code since len(G_for_calc.nodes) should be equal to current_index
            self.pos_index_dict = {}
    
    def add_vertex(self,node,n_pos = False): #adds the vertex to both graphs
        if node not in self.pos_index_dict: #checks if the node is in the graph, increase current_index if it isn't
                self.pos_index_dict[node] = self.current_index
                self.current_index += 1
        if n_pos: #gives the node posstion if asked for
            self.G_for_calc.add_node(self.pos_index_dict[node], pos = n_pos)
            self.G_for_print.add_node(self.pos_index_dict[node], pos = n_pos)
        elif n_pos == 'no pos': #if asked, the node will have no location
            self.G_for_calc.add_node(self.pos_index_dict[node])
            self.G_for_print.add_node(self.pos_index_dict[node])
        else: #by default the code assumes the node is also the location
            self.G_for_calc.add_node(self.pos_index_dict[node], pos = node)
            self.G_for_print.add_node(self.pos_index_dict[node], pos = node)
    
    def get_matrix(self): #will return the adjacency matrix of the graph
        mid = nx.to_numpy_recarray(self.G_for_calc,dtype=[("weight", float), ("cost", int)]) #gets the matrices
        edge_weight_matrix = mid.weight
        return edge_weight_matrix
        
    
    def export_matrix_to_csv(self, file_name):
        mid = nx.to_numpy_recarray(self.G_for_calc,dtype=[("weight", float), ("cost", int)]) #gets the matrices
        edge_weight_matrix = mid.weight
        np.savetxt(file_name + '.csv', edge_weight_matrix, delimiter=',')
    
    def get_graph_eigenpairs(self,return_edge_weight_matrix = False): #get the eigenpairs, will also return the edge weight matrix if asked
        mid = nx.to_numpy_recarray(self.G_for_calc,dtype=[("weight", float), ("cost", int)]) #gets the matrices
        edge_weight_matrix = mid.weight
        eigenvalues,eigenvectors = np.linalg.eig(edge_weight_matrix) #get the eigenpair
        if return_edge_weight_matrix:
            return (eigenvalues,eigenvectors,edge_weight_matrix)
        else:
            return (eigenvalues,eigenvectors)
    
    def get_graph_zero_modes(self, err = 10**-3,return_edge_weight_matrix = False):
        mid = nx.to_numpy_recarray(self.G_for_calc,dtype=[("weight", float), ("cost", int)]) #gets the matrices
        edge_weight_matrix = mid.weight
        eigenvalues,eigenvectors = np.linalg.eig(edge_weight_matrix) #get the eigenpair
        zero_indecies = get_zero_indecies(eigenvalues, err)
        if return_edge_weight_matrix:
            return (eigenvalues[zero_indecies],eigenvectors[zero_indecies],zero_indecies,edge_weight_matrix)
        else:
            return (eigenvalues[zero_indecies],eigenvectors[zero_indecies],zero_indecies)
    
    def add_connection(self, node_from,node_to, the_weight = 1.0): #get 2 nodes and add the edge between them, can get alternative weight
        if node_from in self.pos_index_dict and node_to in self.pos_index_dict:
            self.G_for_calc.add_edge(self.pos_index_dict[node_to], self.pos_index_dict[node_from], weight = -the_weight, cost = 0, has_dimer = False, color = 'blue')
            self.G_for_calc.add_edge(self.pos_index_dict[node_from], self.pos_index_dict[node_to] , weight = the_weight, cost = 0, has_dimer = False, color = 'blue')
            self.G_for_print.add_edge(self.pos_index_dict[node_from], self.pos_index_dict[node_to], has_dimer = False, color = 'blue')
        elif node_from in self.pos_index_dict:
            print('node ' + str(node_to) + ' has not been inserted to the graph yet')
        else:
            print('node ' + str(node_from) + ' has not been inserted to the graph yet')
    
    def Di_print_modes(self,vector_index,labels = False): #print the graph with colors to point vector dominant points
        mid = nx.to_numpy_recarray(self.G_for_calc,dtype=[("weight", float), ("cost", int)]) #gets the matrices
        edge_weight_matrix = mid.weight
        eigenvalues,eigenvectors = np.linalg.eig(edge_weight_matrix) #get the eigenpair
        vector = eigenvectors[:,int(vector_index)] #takes the asked for vector
        abs_vector = np.absolute(vector)
        color_map = set_color_map(abs_vector) #creating a color map for the graph printing with eigenvectors
        plt.figure(figsize=(1, 1), dpi=80)
        pos = nx.get_node_attributes(self.G_for_print,'pos')
        nx.draw(self.G_for_print, pos, node_color=color_map, with_labels=labels) #setting the graph print
        plt.show()
    
    '''def graph_printer(G_for_print, color_map = False): #get the G_for_print and print it with color_map as a heat map of the nodes
        plt.figure(figsize=(1, 1), dpi=80) #setting up the figure size
        pos = nx.get_node_attributes(G_for_print,'pos') #getting the posstions of the nodes on a 2 dim plane
        if color_map: #if color_map isn't True valued the graph will be printed in one color
            nx.draw(G_for_print, pos, node_color=color_map, with_labels=True) #setting the graph print
        else:
            nx.draw(G_for_print, pos, with_labels=True) #setting the graph print
        plt.show() #graph print'''
    
    def get_edge_direction(self, node_from, node_to): #get 2 nodes and checks which one the edge points to, return False if edge doesn't exist
        if node_from not in self.pos_index_dict or node_to not in self.pos_index_dict:
            return False
        edge_point_to = self.G_for_print.has_edge(self.pos_index_dict[node_from], self.pos_index_dict[node_to])
        #print('edge direction row 1')
        edge_point_from = self.G_for_print.has_edge(self.pos_index_dict[node_to], self.pos_index_dict[node_from])
        #print('edge direction row 2')
        if edge_point_from:
            #print('edge direction row 3')
            return node_from
        elif edge_point_to:
            #print('edge direction row 4')
            return node_to
        else:
            #print('edge direction row 5')
            return False
    
    def part_graph(self, node_index,radius,drop_non_connected_nodes=False):
        nodes_index_by_radius = [{node_index}]
        nodes_for_sub_graph = {node_index}
        j = 0
        while j < radius:
            nodes_index_to_add_for_radius_j = set()
            for index in nodes_index_by_radius[j]:
                #print('for j=' + str(j) + ' with index=' + str(index))
                #print('we get list(self.G_for_print.neighbors(index))=' + str(list(self.G_for_print.neighbors(index))))
                index_neighbors = [neighbor for neighbor in list(self.G_for_calc.neighbors(index)) if neighbor not in nodes_for_sub_graph]
                nodes_index_to_add_for_radius_j.update(index_neighbors)
            nodes_index_by_radius.append(nodes_index_to_add_for_radius_j)
            nodes_for_sub_graph.update(nodes_index_to_add_for_radius_j)
            #print('for j=' + str(j) + ' we got index_neighbors=' + str(index_neighbors))
            #print('and nodes_index_to_add_for_radius_j=' + str(nodes_index_to_add_for_radius_j))
            j+=1
        new_G_for_calc = nx.DiGraph(self.G_for_calc.subgraph(nodes_for_sub_graph))
        if drop_non_connected_nodes:
            remove_set = [n for n in nodes_for_sub_graph if len(list(new_G_for_calc.neighbors(n))) < 2]
            nodes_for_sub_graph.difference_update(remove_set)
            new_G_for_calc = nx.DiGraph(self.G_for_calc.subgraph(nodes_for_sub_graph))  
        new_G_for_print = nx.DiGraph(self.G_for_print.subgraph(nodes_for_sub_graph))
        new_pos_index_dict = {}
        for key in self.pos_index_dict:
            if self.pos_index_dict[key] in nodes_for_sub_graph:
                new_pos_index_dict[key] = self.pos_index_dict[key]
        new_Graph_calc_print = graph_calc_print([new_G_for_calc,new_G_for_print, self.current_index, new_pos_index_dict])
        return new_Graph_calc_print
    
    def sub_graph(self, node_index,radius,drop_non_connected_nodes=False):
        nodes_index_by_radius = [{node_index}]
        nodes_for_sub_graph = {node_index}
        j = 0
        while j < radius:
            nodes_index_to_add_for_radius_j = set()
            for index in nodes_index_by_radius[j]:
                #print('for j=' + str(j) + ' with index=' + str(index))
                #print('we get list(self.G_for_print.neighbors(index))=' + str(list(self.G_for_print.neighbors(index))))
                index_neighbors = [neighbor for neighbor in list(self.G_for_calc.neighbors(index)) if neighbor not in nodes_for_sub_graph]
                nodes_index_to_add_for_radius_j.update(index_neighbors)
            nodes_index_by_radius.append(nodes_index_to_add_for_radius_j)
            nodes_for_sub_graph.update(nodes_index_to_add_for_radius_j)
            #print('for j=' + str(j) + ' we got index_neighbors=' + str(index_neighbors))
            #print('and nodes_index_to_add_for_radius_j=' + str(nodes_index_to_add_for_radius_j))
            j+=1
        new_G_for_calc = nx.DiGraph(self.G_for_calc.subgraph(nodes_for_sub_graph))
        if drop_non_connected_nodes:
            remove_set = [n for n in nodes_for_sub_graph if len(list(new_G_for_calc.neighbors(n))) < 2]
            nodes_for_sub_graph.difference_update(remove_set)
            new_G_for_calc = nx.DiGraph(self.G_for_calc.subgraph(nodes_for_sub_graph))  
        new_G_for_print = nx.DiGraph(self.G_for_print.subgraph(nodes_for_sub_graph))
        new_pos_index_dict = {}
        for key in self.pos_index_dict:
            if self.pos_index_dict[key] in nodes_for_sub_graph:
                new_pos_index_dict[key] = self.pos_index_dict[key]
        diff_G_for_calc = self.G_for_calc.copy()
        diff_G_for_print = self.G_for_print.copy()
        for node in new_G_for_calc.nodes():
            diff_G_for_calc.remove_node(node)
        for node in new_G_for_print:
            diff_G_for_print.remove_node(node)
        new_Graph_calc_print = graph_calc_print([diff_G_for_calc,diff_G_for_print, self.current_index, new_pos_index_dict])
        return new_Graph_calc_print
    
    def Di_print(self, labels = False, node_size = 10): #same as Di_print_modes but without modes printing
        plt.figure(figsize=(1, 1), dpi=80)
        #print ('yes here')
        pos = nx.get_node_attributes(self.G_for_print,'pos')
        #print ('pos = ' + str(pos))
        nx.draw(self.G_for_print, pos, node_size = node_size, with_labels=labels)
        #print (3)
        plt.show()
    
    def add_dimer_to_edge(self,node_from_index,node_to_index): #adds to the edge an attribute 'has_dimer = True' red color, return flase if fails (from the edge not pre-existing or the nodes not pre-existing)
        if node_from_index not in self.G_for_calc or node_to_index not in self.G_for_calc:
            return False
        elif G_for_print.has_edge(node_from_index,node_to_index):
            G_for_print.add_edge(node_from_index, node_to_index, has_dimer = True, color = 'red')
            G_for_calc.add_edge(node_from_index, node_to_index, has_dimer = True, color = 'red')
            G_for_calc.add_edge(node_to_index, node_from_index, has_dimer = True, color = 'red')
        elif G_for_print.has_edge(node_to_index, node_from_index):
            G_for_print.add_edge(node_to_index, node_from_index, has_dimer = True, color = 'red')
            G_for_calc.add_edge(node_from_index, node_to_index, has_dimer = True, color = 'red')
            G_for_calc.add_edge(node_to_index, node_from_index, has_dimer = True, color = 'red')
        else:
            return False