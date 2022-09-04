import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,pi,acos,atan
from Square import square
from Rhombus import rhombus
from Half_Square import half_square
from tile_inflate import *

'''the AB_tiling object is just an array of squares, half_squares and rhombuses. It can be used to create a networkx graph of the tiling by using get_graph'''

def dist(node_1,node_2): #euclidean distance of 2 nodes
    return ((node_1[0]-node_2[0])**2 + (node_1[1]-node_2[1])**2)**0.5

def composer(tiling): #collects shapes from ab_tiling and retrun the graph they represent
    tile_graph = tiling[0].nodes
    for tile in tiling:
        tile_graph = nx.compose(tile_graph, tile.nodes)
    return tile_graph

def graph_cleaner(graph): #goes over all nodes and checks which of them are duplicates according to having their distance too short, the function delete duplicates so only one remain
    '''this function can be improved in at least one way. the node can be compared to other nodes with approximatly the same radius (making it nlog(n)
    alternativly the values of the nodes position can be muliplied by 10^(large number) and rounded, than the nodes will be unified by having the same coordinates (nore efficient, but may not work)
    maybe in square, half_square and rhombus the locations can be calculated in a way than will make this function unnecessary, but it's probably not easy to do'''
    remove_list = set() #a set with all the nodes that need to be removed from the graph
    for node in graph:
        if node not in remove_list: #if the node is in the remove list the code doesn't check close nodes
            for other_node in graph:
                if node != other_node and dist(node,other_node) < 10**(-13): #if node isn't in remove_list it will check for all other nodes if they are close to it, if they are, it will add them to remove_list
                    other_node_neighbors = list(graph.adj[other_node]) #if the node needs to be removed all the connections it has should be connected to the node remaining
                    for neighbor in other_node_neighbors:
                        graph.add_edge(node, neighbor)
                    remove_list.add(other_node)
    for node in remove_list: #remove the nodes from the remove list
        graph.remove_node(node)


class AB_tiling:
    #print('0')
    
    #print('1')
    def __init__(self, start_type = 8, base_length = 1): #creates an initial shape, currntly has only star
        self.tiles = []
        #print('2')
        if start_type in ('star',8,'8'):
            index = 0
            while index < 8:
                self.tiles.append(rhombus((0,0), 'deg', pi/8 + (pi*index)/4, base_length))
                index += 1
        if type(start_type) == list:
            self.tiles = start_type
    
    def inflate(self): #the function returns ab_tiling of all the shapes in the original ab_tiling inflated
        inflated_tiles = []
        for tile in self.tiles:
            #print(str(type(tile)))
            if type(tile) == square:
                inflated_tiles = inflated_tiles + square_inflate(tile)
            elif type(tile) == rhombus:
                inflated_tiles = inflated_tiles + rhombus_inflate(tile)
            else:
                inflated_tiles = inflated_tiles + half_square_inflate(tile)
        return AB_tiling(inflated_tiles)
        
    def get_graph(self): #return the graph version of the ab_tiling
        graph = composer(self.tiles) #get the 'dirty' graph, meaning that if 2 points are differnt in the 16th digit it will show them as 2 different points
        graph_cleaner(graph) #will choose one point from every points 'cluster'
        return graph
    
    def dirty_print(self,labels = False): #was added for test purposes print the graph with node clusters
        #print (1)
        graph = composer(self.tiles)
        #graph_cleaner(graph)
        #print(2)
        plt.figure(figsize=(1, 1), dpi=80)
        pos = nx.get_node_attributes(graph,'pos')
        nx.draw(graph, pos, with_labels = labels)
        plt.show()
    
    def print_tiling(self, labels = False): #prints the graph 'clean' graph in the ab_tiling
        graph = composer(self.tiles)
        graph_cleaner(graph)
        plt.figure(figsize=(1, 1), dpi=80)
        pos = nx.get_node_attributes(graph,'pos')
        nx.draw(graph, pos, with_labels = labels)
        plt.show()
    
    
    def print_tiling2(self, labels = False): #same as print_tiling, but prints smaller nodes, should be unified if time allows
        graph = composer(self.tiles)
        graph_cleaner(graph)
        plt.figure(figsize=(1, 1), dpi=80)
        pos = nx.get_node_attributes(graph,'pos')
        d = dict(graph.degree)
        nx.draw(graph, pos, with_labels = labels , node_size=[v for v in d.values()])
        plt.show()
    
    def print_from(self,print_index, labels = False): #print a specific shape, there for test purposes
        graph = self.tiles[print_index].nodes
        plt.figure(figsize=(1, 1), dpi=80)
        pos = nx.get_node_attributes(graph,'pos')
        nx.draw(graph, pos, with_labels = labels)
        plt.show()