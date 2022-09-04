import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,pi,acos,atan

class half_square:
        
    def __init__(self, pos_a, deg_or_pos, deg_or_pos_value, square_direction, side, edge_length = 1): #the function returns an nx.Graph() with a half_square shape.
        '''the function get a starting position, pos_a, and allows to get the half_square with the 4 vertices according to the degree
        between pos_a and the opposite vertex or the position of the opposite vertex, deg_or_pos_value.
        the function require the user to specify if deg_or_pos_value is degree of position in the deg_or_pos.
        'pos' if deg_or_pos_value is position and 'deg' if deg_or_pos_value is degree.
        since the half_square is inflatable it has to have direction, square_direction, square_direction needs to be in ['from','to',right','left'].
        if square_direction == 'from' then the direction of the half_square will be to pos_a, if square_direction == 'right', then when looking from pos_a to pos_b the square direction will be to the right vertex
        if square_direction == 'to' the direction will be to pos_b and if square_direction == 'left' it is the same as 'right' but to the left vertex
        the side is the side of the square remaining when looking from pos_a to pos_b
        can define a custom edge_length, 1 by default'''
        self.nodes = nx.Graph()
        self.direction = 0
        self.edge_length = edge_length
        self.back_direction = (0,0)
        pos_a_x = pos_a[0]
        pos_a_y = pos_a[1]
        if deg_or_pos in ('deg','Deg','DEG','pos','Pos','POS'):
            if deg_or_pos in ('deg','Deg','DEG'):
                deg = deg_or_pos_value
                square_longest = (2**0.5)*edge_length
                pos_b_x = float(format(pos_a_x + square_longest * cos(deg), '.15f')[:-1])
                pos_b_y = float(format(pos_a_y + square_longest * sin(deg), '.15f')[:-1])
            else:
                pos_b_x = deg_or_pos_value[0]
                pos_b_y = deg_or_pos_value[1]
                if abs(pos_b_x - pos_a_x) < (10**-12):
                    if pos_b_y < pos_a_y:
                        deg = float(format((3/2)*pi, '.15f')[:-1])
                    if pos_b_y > pos_a_y:
                        deg = float(format((1/2)*pi, '.15f')[:-1])
                else:
                    deg = float(format(atan((pos_b_y - pos_a_y)/(pos_b_x - pos_a_x)), '.15f')[:-1])
            pos_c_x = float(format(pos_a_x + edge_length*cos(deg - pi/4), '.15f')[:-1])
            pos_c_y = float(format(pos_a_y + edge_length*sin(deg - pi/4), '.15f')[:-1])
            pos_d_x = float(format(pos_a_x + edge_length*cos(deg + pi/4), '.15f')[:-1])
            pos_d_y = float(format(pos_a_y + edge_length*sin(deg + pi/4), '.15f')[:-1])
            if side == 'left':
                self.nodes.add_node((pos_a_x,pos_a_y), pos = (pos_a_x,pos_a_y))
                self.nodes.add_node((pos_d_x, pos_d_y), pos = (pos_d_x, pos_d_y))
                self.nodes.add_node((pos_b_x , pos_b_y), pos = (pos_b_x , pos_b_y))
                self.nodes.add_edge((pos_a_x,pos_a_y),(pos_d_x, pos_d_y))
                self.nodes.add_edge((pos_d_x, pos_d_y), (pos_b_x , pos_b_y))
                self.half_square_side = 'left' if square_direction == 'to' else 'right'
            elif side == 'right':
                self.nodes.add_node((pos_a_x,pos_a_y), pos = (pos_a_x,pos_a_y))
                self.nodes.add_node((pos_c_x, pos_c_y), pos = (pos_c_x, pos_c_y))
                self.nodes.add_node((pos_b_x , pos_b_y), pos = (pos_b_x , pos_b_y))
                self.nodes.add_edge((pos_a_x , pos_a_y),(pos_c_x, pos_c_y))
                self.nodes.add_edge((pos_c_x, pos_c_y),(pos_b_x , pos_b_y))
                self.half_square_side = 'right' if square_direction == 'to' else 'left'
        if square_direction == 'from':
            self.direction = deg + pi
            self.back_location = (pos_b_x, pos_b_y)
            self.right_location = (pos_d_x, pos_d_y)
            self.front_location = (pos_a_x, pos_a_y)
            self.left_location = (pos_c_x, pos_c_y)
        elif square_direction == 'to':
            self.direction = deg
            self.back_location = (pos_a_x, pos_a_y)
            self.right_location = (pos_c_x, pos_c_y)
            self.front_location = (pos_b_x, pos_b_y)
            self.left_location = (pos_d_x, pos_d_y)
    
    def print_the_half_square(self):
        plt.figure(figsize=(1, 1), dpi=80)
        pos = nx.get_node_attributes(self.nodes,'pos')
        nx.draw(self.nodes, pos, with_labels=True)
        plt.show()
    
    def get_edge_length(self):
        return self.edge_length
    
    def get_direction(self):
        return self.direction
    
    def get_location(self,the_direction):
        if the_direction == 'back':
            return self.back_location
        elif the_direction == 'front':
            return self.front_location
        elif the_direction == 'left':
            return self.left_location
        elif the_direction == 'right':
            return self.right_location
        else:
            return False