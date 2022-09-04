import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin,pi,acos,atan
from Graph_Calc_Print import graph_calc_print
from AB_Tiling import AB_tiling

'''in order to get a kasteleyn orientation it is need to go face by face and give them kasteleyn orientation without leaving holes in the middle (the oriented zone must be simply connected).
the approach of the code is to go to a node and orient all the faces it is linked to.
then the code goes to the neighbors of the original node and orient all the faces linked to all the neighbors. the code will continue to do so for all the nodes.
worth mention is the fact that in order to that the code creates a list with the center node as the first node, than adds the node neighbors to the list, after that the neighbors neighbors are add.
the orienting of faces around nodes is done in the order of the list so all the nearst neighbors are being mapped be any next nearst neighbors are mapped.
when the code refers to node radius it is the index of amount of edges between a node and the original node, (0,0).
so the nearst neighbors are of radius 1 and the next nearst neighbors are radius 2. the radius of a face is the minimal radius of any of its nodes.
to keep the 8-fold symmetry the code gives each face a radius value, and check if there is a face with that radius that is already mapped,
if there is, it will copy that face orientation'''



def get_AB_tiling_kasteleyn_orientation_graph_calc_print(AB_tiling, err = 10**-10, start_from = (0,0) ,test = False): #the function gets AB_tiling object and return graph_calc_print of it with kasteleyn orientation
    G = AB_tiling.get_graph()
    radius_to_faces,radius_to_nodes,face_to_radius,node_to_radius = get_radius_to_faces_and_nodes_and_face_and_node_to_radius(G, start_from)
    face_radius = 0
    oriented_G = graph_calc_print()
    while face_radius < len(radius_to_faces):
        if test: print('radius is ' + str(face_radius))
        map_all_faces_in_radius(oriented_G, radius_to_faces[face_radius], err, test)
        face_radius += 1
    return oriented_G

def get_AB_graph_kasteleyn_orientation(G, err = 10**-10, start_from = (0,0),test = False): #the function gets networkx (haven't debugged for a case where the graph isn't the generic AB_tiling one or an inflation of it) object and return graph_calc_print of it with kasteleyn orientation
    radius_to_faces,radius_to_nodes,face_to_radius,node_to_radius = get_radius_to_faces_and_nodes_and_face_and_node_to_radius(G, start_from)
    face_radius = 0
    oriented_G = graph_calc_print()
    while face_radius < len(radius_to_faces):
        if test: print('radius is ' + str(face_radius))
        map_all_faces_in_radius(oriented_G, radius_to_faces[face_radius], err, test)
        face_radius += 1
    return oriented_G

def rotate_vertex(vertex, theta): #get a vertex and rotate it by theta around (0,0)
    new_vertex_x = vertex[0]*cos(theta) - vertex[1]*sin(theta)
    new_vertex_y = vertex[0]*sin(theta) + vertex[1]*cos(theta)
    return [new_vertex_x,new_vertex_y]

def get_vertex_dist(node1, node2):
    return ((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)**0.5

def get_edge_dist(edge1, edge2): #get 2 edges and return the sum of distances between the edges
    dist1 = get_vertex_dist(edge1[0], edge2[0]) + get_vertex_dist(edge1[1], edge2[1])
    dist2 = get_vertex_dist(edge1[0], edge2[1]) + get_vertex_dist(edge1[1], edge2[0])
    if min(dist1,dist2) == dist1:
        return (dist1,1)
    else:
        return (dist2,2)

def map_all_faces_in_radius(oriented_G, faces_in_radius, err = 10**-10, test = False): #the function get all faces in a specific radius and add orientation to them. if a face has a rotated duplicate they will be oriented in the same way
    faces_to_map_like_for_radius = []
    for face in faces_in_radius:
        map_like = has_similar_face_in(face, faces_to_map_like_for_radius, err)
        if map_like:
            for edge in face:
                oriented_G.add_vertex(edge[0])
            map_face_like(face, map_like, oriented_G, test)
        else:
            if test: print('using add face')
            add_face(oriented_G, face, test)
            faces_to_map_like_for_radius.append(face)

def has_similar_face_in(face, faces_to_map_like_for_radius, err = 10**-10): #the function checks if exists a face with the same radius as face in order for map_all_faces_in_radius to map them with the same orientation
    if len(faces_to_map_like_for_radius) == 0:
        return False
    for face_to_map_like in faces_to_map_like_for_radius:
        map_like = []
        for edge in face:
            similar_edge = has_similar_edge_in(edge, face_to_map_like, err)
            if similar_edge:
                map_like.append(similar_edge)
        if len(map_like) == 4:
            return map_like
    return False

def map_face_like(face, map_like, oriented_G, test = False): #the function get face that need orientation and map it the same way as map_like, keeping the 8-fold symmetry
    edge_index = 0
    while edge_index < len(face):
        if map_like[edge_index][1] == oriented_G.get_edge_direction(map_like[edge_index][0], map_like[edge_index][1]):
            oriented_G.add_connection(face[edge_index][0], face[edge_index][1])
            if test: oriented_G.Di_print(False)
        elif map_like[edge_index][0] == oriented_G.get_edge_direction(map_like[edge_index][0], map_like[edge_index][1]):
            oriented_G.add_connection(face[edge_index][1], face[edge_index][0])
            if test: oriented_G.Di_print(False)
        else:
            print('for some reason the edge ' + str (map_like[edge_index]) + 'is in map_like but does not apear in oriented_G')
        edge_index += 1


def has_similar_edge_in(edge, face, err = 10**-10): #the function get an edge and rotate it by muliples of pi/4 around the center and checks if there is an edge in face to match that edge up to rotation
    rotate_index = 1
    while rotate_index < 8:
        theta = (1/4)*pi*rotate_index
        new_edge = [rotate_vertex(edge[0], theta) , rotate_vertex(edge[1], theta)]
        for edge1 in face:
            dist,kind = get_edge_dist(new_edge, edge1)
            if dist < 2*err and kind == 1:
                return edge1
            if dist < 2*err and kind == 2:
                return (edge1[1],edge1[0])
        rotate_index += 1
    return False


'''get_radius_to_faces_and_nodes_and_face_and_node_to_radius function gets the graph return:
1) radius_to_faces, a list that gets an index and returns a list with faces with that radius
2) radius_to_nodes, a list that gets an index and returns a list with nodes of that index
3) face_to_radius, dictionary, like radius_to_faces but the other way
4) node_to_radius, dictionary'''

def get_radius_to_faces_and_nodes_and_face_and_node_to_radius(G, start_from = (0,0)):
    node_run_order = [start_from]
    node_index = 0
    face_to_radius = {}
    radius_to_faces = []
    node_to_radius = {start_from: 0}
    radius_to_nodes = [[start_from]]
    while node_index < len(node_run_order):
        curr_node = node_run_order[node_index]
        add_node_attached_objects_to_run_lists(G, curr_node, node_run_order, node_to_radius, radius_to_nodes, face_to_radius, radius_to_faces)
        node_index += 1
    return radius_to_faces,radius_to_nodes,face_to_radius,node_to_radius

'''add_node_attached_objects_to_run_lists function get a node and the list from get_radius_to_faces_and_nodes_and_face_and_node_to_radius
 and add the faces it is part of and the node neighbors to the lists'''
def add_node_attached_objects_to_run_lists(G, curr_node, node_run_order, node_to_radius, radius_to_nodes, face_to_radius, radius_to_faces):
    curr_node_radius = node_to_radius[curr_node]
    #print('here')
    (curr_node_attached_faces,curr_node_attached_nodes) = get_node_attached_nodes_and_faces(G,curr_node)
    #print ('here')
    for curr_node_attached_node in curr_node_attached_nodes:
        add_node_attached_node_to_run_order_and_radius(curr_node_radius, curr_node_attached_node, node_run_order, node_to_radius, radius_to_nodes)
    for curr_node_attached_face in curr_node_attached_faces:
        add_face_attached_node_to_run_order_and_radius(curr_node_radius, curr_node_attached_face, face_to_radius, radius_to_faces, node_to_radius)

def add_node_attached_node_to_run_order_and_radius(curr_node_radius, curr_node_attached_node, node_run_order, node_to_radius, radius_to_nodes): #the function gets a node and its raduis and add it to node_run_order, node_to_radius and radius_to_nodes 
    if curr_node_attached_node not in node_run_order and curr_node_radius + 1 == len(radius_to_nodes):
        node_run_order.append(curr_node_attached_node)
        radius_to_nodes.append([curr_node_attached_node])
        node_to_radius[curr_node_attached_node] = curr_node_radius + 1
    elif curr_node_attached_node not in node_run_order and curr_node_radius + 2 == len(radius_to_nodes):
        node_run_order.append(curr_node_attached_node)
        radius_to_nodes[curr_node_radius + 1].append(curr_node_attached_node)
        node_to_radius[curr_node_attached_node] = curr_node_radius + 1
    elif curr_node_attached_node not in node_run_order:
        print ('for curr_node_attached_node = ' + str(curr_node_attached_node) + ' it seems to have radius of ' + str(curr_node_radius + 1) + 'but there are no nodes with radius of ' + str(curr_node_attached_node))


def add_face_attached_node_to_run_order_and_radius(curr_node_radius, curr_node_attached_face, face_to_radius, radius_to_faces, node_to_radius): #the function get a face, find its raduis and add it to face_to_radius and radius_to_faces
    #print ('type(curr_node_attached_face)) = ' + str(type(curr_node_attached_face)))
    #print ('curr_node_attached_face = ' + str(curr_node_attached_face))
    #print ('type(face_to_radius)) = ' + str(type(face_to_radius)))
    #print ('face_to_radius = ' + str(face_to_radius))
    #print ('curr_node_attached_face in face_to_radius = ' + str(curr_node_attached_face in face_to_radius))
    if (curr_node_attached_face in face_to_radius):
        return False
    #print ('node_to_radius = ' + str(node_to_radius))
    face_radii = [node_to_radius[face_edge[0]] for face_edge in curr_node_attached_face if face_edge[0] in node_to_radius]
    face_radius = min(face_radii)
    if face_radius == len(radius_to_faces):
        radius_to_faces.append([curr_node_attached_face])
        face_to_radius[curr_node_attached_face] = face_radius
        face_to_radius[(curr_node_attached_face[1],curr_node_attached_face[2],curr_node_attached_face[3],curr_node_attached_face[0])]= face_radius
        face_to_radius[(curr_node_attached_face[2],curr_node_attached_face[3],curr_node_attached_face[0],curr_node_attached_face[1])]= face_radius
        face_to_radius[(curr_node_attached_face[3],curr_node_attached_face[0],curr_node_attached_face[1],curr_node_attached_face[2])]= face_radius
    elif face_radius + 1 == len(radius_to_faces):
        radius_to_faces[face_radius].append(curr_node_attached_face)
        face_to_radius[curr_node_attached_face] = face_radius
        face_to_radius[(curr_node_attached_face[1],curr_node_attached_face[2],curr_node_attached_face[3],curr_node_attached_face[0])]= face_radius
        face_to_radius[(curr_node_attached_face[2],curr_node_attached_face[3],curr_node_attached_face[0],curr_node_attached_face[1])]= face_radius
        face_to_radius[(curr_node_attached_face[3],curr_node_attached_face[0],curr_node_attached_face[1],curr_node_attached_face[2])]= face_radius
    elif face_radius == len(radius_to_faces) + 1:
        radius_to_faces.append([])
        radius_to_faces.append([curr_node_attached_face])
        face_to_radius[curr_node_attached_face] = face_radius
        face_to_radius[(curr_node_attached_face[1],curr_node_attached_face[2],curr_node_attached_face[3],curr_node_attached_face[0])]= face_radius
        face_to_radius[(curr_node_attached_face[2],curr_node_attached_face[3],curr_node_attached_face[0],curr_node_attached_face[1])]= face_radius
        face_to_radius[(curr_node_attached_face[3],curr_node_attached_face[0],curr_node_attached_face[1],curr_node_attached_face[2])]= face_radius
    else:
        print ('for face ' + str(curr_node_attached_face) + ' the face radius is ' + str(face_radius))
        print ('radius_to_faces[face_radius:] = ' + str(radius_to_faces[face_radius:]))
        print ('len(radius_to_faces) = ' + str(len(radius_to_faces)))
        print ('curr_node_radius = ' + str(curr_node_radius))
        input()




def add_face(oriented_G, face, test = False):#get the calc print graph and adds the oriented edges to it. the nodes of the face are assumed to be in oriented_G before the run!
    #print('the face is: ' + str(face))
    list_face = list(face)
    face_direction = [] #creates an array to check the directions of the edges already mapped
    for edge in list_face: #adds the direction of the edges to face_direction, False if the edge isn't mapped yet
        #if test: print('edge = ' + str(edge))
        edge_direction = oriented_G.get_edge_direction(edge[0], edge[1])
        #if test: print('edge_direction = ' + str(edge_direction))
        oriented_G.add_vertex(edge[0],edge[0])
        oriented_G.add_vertex(edge[1],edge[1])
        if edge_direction == edge[0]:
            #if test: print('if')
            face_direction.append('from')
        elif edge_direction == edge[1]:
            #if test: print('elif')
            face_direction.append('to')
        else:
            #if test: print('else')
            face_direction.append(False)
    
    count_false = face_direction.count(False) #the decision tree to direct the edges start from how many edges aren't directed yet
    #if test: print(face_direction)
    #if test: print('face = ' + str(face))
    #long decision tree to direct the edges of the face, may still have issues (worked in testing, will print if a face can't be mapped)
    #will get the kasteleyn orientation but may have problem with the 8-fold symmetry
    if count_false == 4: #only the first face goes in here so it's custom mapping
        oriented_G.add_connection(list_face[0][1], list_face[0][0])
        if test: oriented_G.Di_print(False)
        oriented_G.add_connection(list_face[1][0], list_face[1][1])
        if test: oriented_G.Di_print(False)
        oriented_G.add_connection(list_face[2][0], list_face[2][1])
        if test: oriented_G.Di_print(False)
        oriented_G.add_connection(list_face[3][0], list_face[3][1])
        if test: oriented_G.Di_print(False)
    elif count_false == 3:
        if face_direction == ['from',False,False,False]:
            place = face_direction.index('from')
            oriented_G.add_connection(list_face[(place+1)%4][0],list_face[(place+1)%4][1])
            if test: oriented_G.Di_print(False)
            oriented_G.add_connection(list_face[(place+2)%4][0],list_face[(place+2)%4][1])
            if test: oriented_G.Di_print(False)
            oriented_G.add_connection(list_face[(place+3)%4][0],list_face[(place+3)%4][1])
            if test: oriented_G.Di_print(False)
        elif face_direction == [False,False,False,'to']:
            oriented_G.add_connection(list_face[0][1],list_face[0][0])
            if test: oriented_G.Di_print(False)
            oriented_G.add_connection(list_face[1][0],list_face[1][1])
            if test: oriented_G.Di_print(False)
            oriented_G.add_connection(list_face[2][0],list_face[2][1])
            if test: oriented_G.Di_print(False)
            
            
        elif 'to' in face_direction:
            place = face_direction.index('to')
            oriented_G.add_connection(list_face[(place+1)%4][1],list_face[(place+1)%4][0])
            if test: oriented_G.Di_print(False)
            oriented_G.add_connection(list_face[(place+2)%4][1],list_face[(place+2)%4][0])
            if test: oriented_G.Di_print(False)
            oriented_G.add_connection(list_face[(place+3)%4][1],list_face[(place+3)%4][0])
            if test: oriented_G.Di_print(False)
        else:
            place = face_direction.index('from')
            oriented_G.add_connection(list_face[(place+1)%4][0],list_face[(place+1)%4][1])
            if test: oriented_G.Di_print(False)
            oriented_G.add_connection(list_face[(place+2)%4][0],list_face[(place+2)%4][1])
            if test: oriented_G.Di_print(False)
            oriented_G.add_connection(list_face[(place+3)%4][0],list_face[(place+3)%4][1])
            if test: oriented_G.Di_print(False)
    elif count_false == 2:
        #if test: print(face)
        if 'to' in face_direction and 'from' in face_direction:
            if face_direction == ['to', False,False,'from']:
                to_index = face_direction.index('to')
                from_index = face_direction.index('from') if face_direction.index('from') < to_index else face_direction.index('from')-1
                list_face.pop(to_index)
                list_face.pop(from_index)
                oriented_G.add_connection(list_face[0][1], list_face[0][0])
                if test: oriented_G.Di_print(False)
                oriented_G.add_connection(list_face[1][1], list_face[1][0])
                if test: oriented_G.Di_print(False)
            elif face_direction == ['from', False,False,'to']:
                to_index = face_direction.index('to')
                from_index = face_direction.index('from') if face_direction.index('from') < to_index else face_direction.index('from')-1
                list_face.pop(to_index)
                list_face.pop(from_index)
                oriented_G.add_connection(list_face[0][0], list_face[0][1])
                if test: oriented_G.Di_print(False)
                oriented_G.add_connection(list_face[1][0], list_face[1][1])
                if test: oriented_G.Di_print(False)
            elif face_direction == [False, False, 'to', 'from']:
                oriented_G.add_connection(list_face[0][0], list_face[0][1])
                if test: oriented_G.Di_print(False)
                oriented_G.add_connection(list_face[1][0], list_face[1][1])
                if test: oriented_G.Di_print(False)
            elif face_direction == ['from', 'to', False, False]:
                oriented_G.add_connection(list_face[2][1], list_face[2][0])
                if test: oriented_G.Di_print(False)
                oriented_G.add_connection(list_face[3][1], list_face[3][0])
                if test: oriented_G.Di_print(False)
            elif face_direction == ['to', 'from', False, False]:
                oriented_G.add_connection(list_face[2][0], list_face[2][1])
                if test: oriented_G.Di_print(False)
                oriented_G.add_connection(list_face[3][0], list_face[3][1])
                if test: oriented_G.Di_print(False)
            elif face_direction == [False, False, 'from', 'to']:
                oriented_G.add_connection(list_face[0][1], list_face[0][0])
                if test: oriented_G.Di_print(False)
                oriented_G.add_connection(list_face[1][1], list_face[1][0])
                if test: oriented_G.Di_print(False)
            else:
                print('both from and to for face:\n' + str(face))
                print('just in case you missed face_direction = ' + str(face_direction))
            
        else:
            index = 0
            w = 0
            while index < len(face_direction):
                if face_direction[index] == False:
                    oriented_G.add_connection(list_face[index][(1 + w) % 2], list_face[index][(0 + w) % 2])
                    if test: oriented_G.Di_print(False)
                    w = 1
                index += 1
    elif count_false == 1:
        false_index = face_direction.index(False)
        if face_direction.count('to') == 3:
            oriented_G.add_connection(list_face[false_index][1], list_face[false_index][0])
            if test: oriented_G.Di_print(False)
        elif face_direction.count('to') == 2:
            oriented_G.add_connection(list_face[false_index][0], list_face[false_index][1])
            if test: oriented_G.Di_print(False)
        elif face_direction.count('to') == 1:
            oriented_G.add_connection(list_face[false_index][1], list_face[false_index][0])
            if test: oriented_G.Di_print(False)
        else:
            oriented_G.add_connection(list_face[false_index][0], list_face[false_index][1])
            if test: oriented_G.Di_print(False)

def get_node_attached_nodes_and_faces(G,orig_node, test = False): #get a graph G, and a node and returns the nodes connected to it by edges and the faces it is a part of
    #attached_nodes G.neighbors(orig_node)
    attached_nodes = tuple([edge[1] for edge in list(G.edges(orig_node))]) #G.edges(orig_node) are the edges orig_node is connected by, the list only takes the second value of each edge, which is the node other than orig_node
    attached_faces = [] #each face if and array of 4 edges, edge is represnted by 2 node locations, the attached_faces will have the faces of each node
    second_level_attached_nodes = {} #a dict with the nodes attached to attached_nodes as keys and an array containing the nodes from attached_nodes attached to them
    for node in attached_nodes:
        #node_attached_nodes = G.neighbors(node)
        node_attached_nodes = [edge[1] for edge in G.edges(node)] #like attached_nodes will get the nodes attached to node in attached_nodes
        node_attached_nodes.remove(orig_node) #removes the orig_node from the array so it won't be counted in second_level_attached_nodes
        for node2 in node_attached_nodes:
            if node2 in second_level_attached_nodes: #adds the node to node2 array if the array exists or creates the array if it isn't created yet
                second_level_attached_nodes[node2].append(node)
            else:
                second_level_attached_nodes[node2] = [node]
    for node in second_level_attached_nodes:
        if len(second_level_attached_nodes[node]) > 1: #if a node is attached to 2 of the attached_nodes it means it along the 2 nodes and orig_node are a face 
            first_edge = (tuple(orig_node),tuple(second_level_attached_nodes[node][0]))
            second_edge = (tuple(second_level_attached_nodes[node][0]), tuple(node))
            third_edge = (tuple(node), tuple(second_level_attached_nodes[node][1]))
            fourth_edge = (tuple(second_level_attached_nodes[node][1]), tuple(orig_node))
            #collecting the edges
            new_face = (first_edge,second_edge,third_edge,fourth_edge)
            if is_clockwise(new_face): #the add_face function needs the face to be oriented counter clockwise to get 8 fold symmetry so this section sets the edges in this way
                #if test: print('si')
                if test: print('new_face = ' + str(new_face))
                first_edge = (tuple(orig_node), tuple(second_level_attached_nodes[node][1]))
                second_edge = (tuple(second_level_attached_nodes[node][1]), tuple(node))
                third_edge = (tuple(node), tuple(second_level_attached_nodes[node][0]))
                fourth_edge = (tuple(second_level_attached_nodes[node][0]), tuple(orig_node))
                new_face = (first_edge,second_edge,third_edge,fourth_edge)
                if test: print('new new_face = ' + str(new_face))
            attached_faces.append(new_face) #adds the face
        if len(second_level_attached_nodes[node]) > 2: #for test cases since we shouldn't get more than 2 connections
            print('node : ' + str(node) + '\nis attached to: ' + str(len(second_level_attached_nodes[node])) + ' nodes.\n the orig_node is: ' + str(orig_node))
            print('the nodes are: ' + str(second_level_attached_nodes[node]))
    return (tuple(attached_faces), attached_nodes)

def is_clockwise(face): #the function gets a face, return True if the nodes of the face are in clockwise order and else return False
    clockwise_sum = 0
    for edge in face:
        x_1 = edge[0][0]
        y_1 = edge[0][1]
        x_2 = edge[1][0]
        y_2 = edge[1][1]
        clockwise_sum += (x_2-x_1)*(y_2 + y_1)
    if clockwise_sum > 0:
        return True
    elif clockwise_sum < 0:
        return False
    else:
        print('is clockwise had a very very big mistake!')
        print('face = ' + str(face))
        print('gets clockwise_sum = ' + str(clockwise_sum))