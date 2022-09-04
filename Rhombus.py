import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,pi,acos,atan

class rhombus:
        
    def __init__(self, pos_a, deg_or_pos, deg_or_pos_value, required_edge_length = 1): #the function returns an nx.Graph() with a rhombus shape.
        '''the function get a starting position, pos_a, and allows to get the rhombus with the 4 vertices according to the degree
        between pos_a and the opposite vertex or the position of the opposite vertex, deg_or_pos_value.
        the function require the user to specify if deg_or_pos_value is degree of position in the deg_or_pos.
        'pos' if deg_or_pos_value is position and 'deg' if deg_or_pos_value is degree
        can define a custom edge_length, 1 by default'''
        self.nodes = nx.Graph() #defining the graph
        self.edge_length = required_edge_length #the edge_length is a property of the graph
        pos_a_x = pos_a[0]
        pos_a_y = pos_a[1]
        if deg_or_pos  in ('deg','Deg','DEG'): #if deg_or_pos_value is pos the opposite vertex position is calculted by it
            self.deg = deg_or_pos_value
            rhombus_longest = (2*(self.edge_length**2) - 2*(self.edge_length**2)*cos((pi/180)*135))**0.5
            pos_b_x = float(format(pos_a_x + rhombus_longest * cos(self.deg), '.15f')[:-1])
            pos_b_y = float(format(pos_a_y + rhombus_longest * sin(self.deg), '.15f')[:-1])
        if deg_or_pos in ('pos','Pos','POS'): #the code needs pos_a to left to pos_b so this part makes sure of it
            pos_b_x = deg_or_pos_value[0]
            pos_b_y = deg_or_pos_value[1]
            if pos_a_x > pos_b_x:
                keep = pos_a_x
                pos_a_x = pos_b_x
                pos_b_x = keep
                keep = pos_a_y
                pos_a_y = pos_b_y
                pos_b_y = keep
            if abs(pos_b_x - pos_a_x) < (10**-12):
                if pos_b_y < pos_a_y:
                    self.deg = float(format((3/2)*pi, '.15f')[:-1])
                if pos_b_y > pos_a_y:
                    self.deg = float(format((1/2)*pi, '.15f')[:-1])
            else:
                self.deg = float(format(atan((pos_b_y - pos_a_y)/(pos_b_x - pos_a_x)), '.15f')[:-1])
        #the 2 other positions calcultations
        pos_c_x = float(format(pos_a_x + self.edge_length*cos(self.deg - pi/8), '.15f')[:-1])
        pos_c_y = float(format(pos_a_y + self.edge_length*sin(self.deg - pi/8), '.15f')[:-1])
        pos_d_x = float(format(pos_a_x + self.edge_length*cos(self.deg + pi/8), '.15f')[:-1])
        pos_d_y = float(format(pos_a_y + self.edge_length*sin(self.deg + pi/8), '.15f')[:-1])
        #adding the nodes and the edges
        self.nodes.add_node((pos_a_x, pos_a_y), pos = (pos_a_x, pos_a_y))
        self.nodes.add_node((pos_c_x, pos_c_y), pos = (pos_c_x, pos_c_y))
        self.nodes.add_node((pos_d_x, pos_d_y), pos = (pos_d_x, pos_d_y))
        self.nodes.add_node((pos_b_x, pos_b_y), pos = (pos_b_x, pos_b_y))
        self.nodes.add_edge((pos_a_x,pos_a_y), (pos_c_x, pos_c_y))
        self.nodes.add_edge((pos_a_x,pos_a_y), (pos_d_x, pos_d_y))
        self.nodes.add_edge((pos_b_x, pos_b_y), (pos_c_x, pos_c_y))
        self.nodes.add_edge((pos_b_x, pos_b_y), (pos_d_x, pos_d_y))
        #saves a few settings to help with the calcultations in tile_inflate
        self.sharp_left_pos = (pos_a_x, pos_a_y)
        self.sharp_right_pos = (pos_b_x, pos_b_y)
        self.obtuse_down_pos = (pos_c_x, pos_c_y)
        self.obtuse_up_pos = (pos_d_x, pos_d_y)
    
    
    def print_the_rhombus(self): #print function, mostly for testing
        plt.figure(figsize=(1, 1), dpi=80)
        pos = nx.get_node_attributes(self.nodes,'pos')
        nx.draw(self.nodes, pos, with_labels=True)
        plt.show()
    
    def get_nodes(self):
        return self.nodes
    
    def get_edge_length(self):
        return self.edge_length