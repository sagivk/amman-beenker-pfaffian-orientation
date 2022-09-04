import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,pi,acos,atan
from Square import square
from Rhombus import rhombus
from Half_Square import half_square

edge_length_rate = 1/(1+2**0.5) #the inflation is actualy making smaller shapes, with the edges getting shortter by edge_length_rate

def square_inflate(the_square): #using the known inflation template to retrun an inflated square
    left_bottom_right_half_square = half_square(the_square.get_location('back'), 'deg', the_square.get_direction() - pi/4, 'from', 'left', the_square.edge_length * edge_length_rate)
    #print('1')
    left_bottom_left_half_square =  half_square(the_square.get_location('back'), 'deg', the_square.get_direction() + pi/4, 'from', 'right', the_square.edge_length * edge_length_rate)
    #print('2')
    bottom_right_rhombus = rhombus(the_square.get_location('right'), 'pos' , left_bottom_right_half_square.get_location('right'), the_square.edge_length * edge_length_rate)
    #print('3')
    center_square = square(left_bottom_left_half_square.get_location('left'), 'deg', the_square.get_direction(), 'from', the_square.edge_length * edge_length_rate)
    #print('4')
    top_left_rhombus = rhombus(left_bottom_right_half_square.get_location('right'), 'pos' , the_square.get_location('left'), the_square.edge_length * edge_length_rate)
    #print('5')
    top_left_half_square = half_square(the_square.get_location('left'), 'deg', the_square.get_direction() - pi/4, 'from', 'right', the_square.edge_length * edge_length_rate)
    #print('6')
    top_right_left_rhombus = rhombus(the_square.get_location('front'), 'pos', center_square.get_location('right'), the_square.edge_length * edge_length_rate)
    top_right_right_rhombus = rhombus(the_square.get_location('front'), 'pos', center_square.get_location('left'), the_square.edge_length * edge_length_rate)
    bottom_right_half_square = half_square(the_square.get_location('right'), 'deg', the_square.get_direction() + pi/4, 'from', 'left', the_square.edge_length * edge_length_rate)
    return [left_bottom_right_half_square, left_bottom_left_half_square, bottom_right_rhombus, center_square, top_left_rhombus, top_left_half_square, top_right_left_rhombus, top_right_right_rhombus, bottom_right_half_square]

def half_square_inflate(the_half_square): #using the known inflation template to retrun an inflated half_square, the function seperates cases by which half of the square it got
    #print('0')
    side = the_half_square.half_square_side
    #print('1')
    if side == 'left':
        #print('2')
        left_bottom_left_half_square = half_square(the_half_square.get_location('back'), 'deg', the_half_square.get_direction() + pi/4, 'from', 'right', the_half_square.edge_length * edge_length_rate)
        #print('3')
        center_half_square = half_square(left_bottom_left_half_square.get_location('left'), 'deg', the_half_square.get_direction(), 'from', 'left', the_half_square.edge_length * edge_length_rate)
        #print('4')
        top_left_rhombus = rhombus(left_bottom_left_half_square.get_location('left'), 'pos' , the_half_square.get_location('left'), the_half_square.edge_length * edge_length_rate)
        #print('5')
        top_left_half_square = half_square(the_half_square.get_location('left'), 'deg', the_half_square.get_direction() - pi/4, 'from', 'right', the_half_square.edge_length * edge_length_rate)
        #print('6')
        top_right_left_rhombus = rhombus(the_half_square.get_location('front'), 'pos', center_half_square.get_location('right'), the_half_square.edge_length * edge_length_rate)
        #print('7')
        return [left_bottom_left_half_square, center_half_square, top_left_rhombus, top_left_half_square, top_right_left_rhombus]
    if side == 'right':
        #print('8')
        left_bottom_right_half_square = half_square(the_half_square.get_location('back'), 'deg', the_half_square.get_direction() - pi/4, 'from', 'left', the_half_square.edge_length * edge_length_rate)
        #print('9')
        center_half_square = half_square(left_bottom_right_half_square.get_location('right'), 'deg', the_half_square.get_direction(), 'from', 'right', the_half_square.edge_length * edge_length_rate)
        #print('10')
        bottom_right_rhombus = rhombus(the_half_square.get_location('right'), 'pos' , left_bottom_right_half_square.get_location('right'), the_half_square.edge_length * edge_length_rate)
        #print('11')
        bottom_right_half_square = half_square(the_half_square.get_location('right'), 'deg', the_half_square.get_direction() + pi/4, 'from', 'left', the_half_square.edge_length * edge_length_rate)
        #print('12')
        top_right_right_rhombus = rhombus(the_half_square.get_location('front'), 'pos', center_half_square.get_location('left'), the_half_square.edge_length * edge_length_rate)
        #print('13')
        return [left_bottom_right_half_square, center_half_square, bottom_right_rhombus, bottom_right_half_square, top_right_right_rhombus]

def rhombus_inflate(the_rhombus): #using the known inflation template to retrun an inflated rhombus
    left_rhombus = rhombus(the_rhombus.sharp_left_pos, 'deg', the_rhombus.deg, the_rhombus.edge_length * edge_length_rate)
    right_rhombus = rhombus(the_rhombus.sharp_right_pos, 'deg', the_rhombus.deg + pi, the_rhombus.edge_length * edge_length_rate)
    down_half_square = half_square(the_rhombus.obtuse_down_pos, 'deg', the_rhombus.deg + (7*pi)/8, 'from', 'right', the_rhombus.edge_length * edge_length_rate)
    left_half_square = half_square(the_rhombus.obtuse_up_pos, 'deg', the_rhombus.deg + (9*pi)/8, 'from', 'left', the_rhombus.edge_length * edge_length_rate)
    right_half_square = half_square(the_rhombus.obtuse_down_pos, 'deg', the_rhombus.deg + pi/8, 'from', 'left', the_rhombus.edge_length * edge_length_rate)
    up_half_square = half_square(the_rhombus.obtuse_up_pos, 'deg', the_rhombus.deg - pi/8, 'from', 'right', the_rhombus.edge_length * edge_length_rate)
    center_rhombus = rhombus(the_rhombus.obtuse_down_pos, 'pos', the_rhombus.obtuse_up_pos, the_rhombus.edge_length * edge_length_rate)
    return [left_rhombus, right_rhombus, down_half_square, left_half_square, right_half_square, up_half_square, center_rhombus]




