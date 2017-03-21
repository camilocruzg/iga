__author__ = 'ccruz'
import numpy as np
import random as rand
from math import log
import math

###Depth-First search (from eddmann.com)
def dfs(g, start):
    visited = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(g[vertex] - visited)
    v_dict = {}
    for i in visited:
        v_dict[i]=g[i]
    return v_dict

def dfs2(g, start):
    visited = []
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(g[vertex] - visited)
    v_dict = {}
    for i in visited:
        v_dict[i]=g[i]
    return v_dict

### Makes a list of clusters in a graph using dfs
def clusters(g):
    clust = []
    for node in g:
            c = dfs(g,node)
            if c not in clust:
                clust.append(c)
    return clust

def clusters2(g):
    clust = []
    for node in g:
            c = dfs(g,node)
            if c not in clust:
                clust.append(c)
    return clust

def clust_count(gr):
    return len(clusters(gr))

### Finds cycles of 4 nodes in a graph. Returns a list of top left coordinates
### for each cycle found.
def find_cycle(graph):
    cycles = []
    for node in graph:
        if (node[0],node[1]+1) in graph[node]:
            node = (node[0],node[1]+1)
            if (node[0]+1,node[1]) in graph[node]:
                node = (node[0]+1,node[1])
                if (node[0],node[1]-1) in graph[node]:
                    node = (node[0],node[1]-1)
                    if (node[0]-1,node[1]) in graph[node]:
                        node = (node[0]-1,node[1])
                        cycles.append(node)
        else:
            pass
    return cycles

### implementation of find_cycle using number based graphs (instead of coordinate based ones)
def find_cycle2(graph,s):
    v_dif = s[0]+2
    cycles = []
    for node in graph:
        if (node+1) in graph[node]:
            node = (node+1)
            if (node+v_dif) in graph[node]:
                node = (node+v_dif)
                if (node-1) in graph[node]:
                    node = (node-1)
                    if (node-v_dif) in graph[node]:
                        node = (node-v_dif)
                        cycles.append(node)
        else:
            pass
    return cycles

### Finds clusters of 4 node cycles
### Using algorithm found on the following link (Answer posted by user: Howard 30/01/2011):
### http://stackoverflow.com/questions/4842613/merge-lists-that-share-common-elements
def cycle_cluster(gr):
    cy = find_cycle(gr)
    l = []
    for c in cy:
        a = [c,(c[0],c[1]+1),(c[0]+1,c[1]+1),(c[0]+1,c[1])]
        l.append(a)
    out = []
    while len(l)>0:
        first, rest = l[0] , l[1:]
        first = set(first)

        lf = -1
        while len(first)>lf:
            lf = len(first)

            rest2 = []
            for r in rest:
                if len(first.intersection(set(r)))>0:
                    first |= set(r)
                else:
                    rest2.append(r)
            rest = rest2

        out.append(first)
        l = rest
    return list(out)

### Finds shortest path between two points
def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return []
    shortest = []
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


###Following set of functions look for boundaries around a cell

def top(k,s):
    x = k%s[0]
    y = k/s[0]
    return (x-1)+(s[0]*(y-1))

def bottom(k,s):
    return top(k,s)+s[0]

def left(k,s):
    s2=(s[0]+2,s[1]+2)
    x = k%s2[0]
    y = k / s2[0]
    return ((y-1)+(s[1]*(x-1)))+(s[0]*(s[1]+1))

def right(k,s):
    return left(k,s)+s[1]

### Function looks at which cells are connected
def connected2(chr,s):
    connected = []
    for i in range(len(chr)):
        if i < s[0]*(s[1]+1):
            n = ((s2[0]*(i/s[0]))+((i%s[0])+1)) #Finds top neighbour of horizontal bits
            if chr[i] == 0:
                connected.append((n,n+s2[0]))
        else:
            sp = i-(s[0]*(s[1]+1))
            pos = ((sp/s[1]),sp%s[1])
            n = (pos[0]+s2[0])+(pos[1]*s2[0])
            if chr[i] == 0:
                connected.append((n,n+1))
    return connected

### Connected 3D
def connected3D(chr,s):
    s2 = (s[0]+2,s[1]+2,s[2]+2)
    connected = []
    for i in range(len(chr)):
        if i < (s[0] * s[1] * (s[2]+1)):
            n = ((s2[0]*(i/s[0]))+((i%s[0])+1)) #Finds top neighbour of horizontal bits
            if chr[i] == 0:
                connected.append((n,n+s2[0]))
        else:
            sp = i-(s[0]*(s[1]+1))
            pos = ((sp/s[1]),sp%s[1])
            n = (pos[0]+s2[0])+(pos[1]*s2[0])
            if chr[i] == 0:
                connected.append((n,n+1))
    return connected

### Represent a binary chromosome as a graph
def chr_graph(chr,s):
    s2 = (s[0]+2,s[1]+2)
    c = connected(chr,s)
    g = {}
    tot_cells = s2[0]*s2[1]
    for i in range(tot_cells):
        if (0<i%s2[0]<=s[0]) and (0<i/s2[0]<s[1]+1):
            g[i] = []
    for i in g.keys():
        for cell in c:
            if cell[0] == i:
                g[i].append(cell[1])
            elif cell[1] == i:
                g[i].append(cell[0])
        g[i] = set(g[i])
        new_items = {}
        for k in g:
            for v in g[k]:
                if v not in g.keys():
                    new_items[v] = []
                    n = (k)
                    new_items[v].append(n)
                    new_items[v] = set(new_items[v])
        g.update(new_items)

    return g

### Represent a binary string as a graph, without considering connections to the outside

def chr_graph2(chr,s):
    g = {}
    tot_cells = s[0]*s[1]
    rows = []
    for i in range(s[1]):
        rows.append([])
    for i in range(tot_cells):
        rows[i/s[0]].append(i)
    for i in range(tot_cells):
        g[i] = []
    for i in g.keys():
        x = i%s[0]
        y = i/s[0]
        if chr[i] == 0 and i-s[0] >= 0:
            g[i].append(i-s[0])
        if chr[i+s[0]] == 0 and i+s[0]<tot_cells:
            g[i].append(i+s[0])
        # print i, (s[0]*(s[1]+1))+y+(x*s[1]), rows[y]
        if (chr[(s[0]*(s[1]+1))+y+(x*s[1])] == 0):
            if (i-1 in rows[y]):
                g[i].append(i-1)
        if chr[(s[0]*(s[1]+1))+y+(x*s[1])+s[1]] == 0:
            if i+1 in rows[y]:
                g[i].append(i+1)
        g[i]=set(g[i])

    return g

def chr_graph3D(chr,s):
    g = {}
    tot_cells = s[0]*s[1]*s[2]
    xy_plane = s[0]*s[1]*(s[2]+1)
    xz_plane = s[0]*(s[1]+1)*s[2]
    yz_plane = (s[0]+1)*s[1]*s[2]
    for cell in range(tot_cells):
        g[cell] = []
    for i in g.keys():
        z = i / (s[0] * s[1])
        x = i%s[0]
        y = (i/s[0])-(s[1]*z)
        bot = (y*s[0])+x+(z*(s[0]*s[1]))
        top = bot + (s[0]*s[1])
        front = xy_plane + x + (y*(s[0]*s[2])) + (z*s[0])
        back = front + (s[0]*s[2])
        left = xy_plane + xz_plane + (x*(s[1]*s[2])) + y + (z*s[1])
        right = left + (s[1]*s[2])
        if z > 0 and chr[bot] == 0:
            g[i].append(i-(s[0]*s[1]))
        if z < (s[2]-1) and chr[top] == 0:
            g[i].append(i+(s[0]*s[1]))
        if y > 0 and chr[front] == 0:
            g[i].append(i-s[0])
        if y < (s[1]-1) and chr[back] == 0:
            g[i].append(i+s[0])
        if x > 0 and chr[left] == 0:
            g[i].append(i-1)
        if x < (s[0]-1) and chr[right] == 0:
            g[i].append(i+1)
        g[i] = set(g[i])



    return g

###Evaluation functions

### General tools:
### Define grid:
def grid(size):
    grd = []
    tot_cells = ((size[0] + 2) * (size[1] + 2))
    for i in range(tot_cells):
        if (0 < i % (size[0] + 2) <= size[0]) and (0 < i / (size[0] + 2) < size[1] + 1):
            grd.append(i)
    return grd

### Get list of open clsuters
def op_clstrs(g,size):
    grd = grid(size)
    clstrs = clusters(g)
    op = []
    for clst in clstrs:
        if next((k for k in clst.keys() if k not in grd), None):
            op.append(clst)
    return op

### Get list of closed clusters:
def cl_clstrs(g,size):
    grd = grid(size)
    clstrs = clusters(g)
    cl = []
    for clst in clstrs:
        if next((k for k in clst.keys() if k not in grd), None):
            pass
        else:
            cl.append(clst)
    return cl

### Objective: Measure Wakable surface
### Method: Count the number of horizontal elements in a chromosome
### bm represents a benchmark to be attained.
### Objective is set up as minimisation. If working on maximisation return as 1/
def walkable_surf(chr,size,bm):
    ws = []
    for i in range(size[0]*(size[1]+1)):
        ws.append(chr[i])
    tot_ws = float(sum(ws))
    if bm > 1:
        bm = 1
    output = abs((bm*(size[0]*(size[1]+1))) - tot_ws)
    return output

def walkability(g,chr,size,bm):
    size2 = (size[0]+2,size[1]+2)
    w_graph = {}
    w_nodes = [] #Walkable nodes
    w_edges = [] #Walkable edges
    for node in g:
        loc = (node%size2[0],node/size2[0])
        pos = (loc[0]-1)+(size[0]*(loc[1]-1))
        if chr[pos+size[0]]==1:
            w_nodes.append(node)
        w_graph['w_nodes'] = w_nodes
    standing_space_index = float(len(w_nodes))/float(len(g.keys()))
    for i in range(len(w_nodes)-1):
        if w_nodes[i+1] in g[w_nodes[i]]:
            w_edges.append((w_nodes[i],w_nodes[i+1]))
        w_graph['edges'] = w_edges
    w_index = 0
    if len(w_graph['w_nodes']) - 1 > 0:
        w_index = standing_space_index*float((len(w_graph['edges']))/float((len(w_graph['w_nodes']) - 1)))
    else:
        w_index = 0
    return round(abs(bm - w_index),3)

### Objective: Measure number of vertical subdivisions
### Method: Count the number of vertical elements in a chromosome
### bm represents a benchmark to be attained.
### Objective is set up as minimisation. If working on maximisation return as 1/
def subdiv(chr,size,bm):
    sd = []
    for i in range(size[0]*(size[1]+1),((size[0]+1)*size[1])+size[0]*(size[1]+1)):
        sd.append(chr[i])
    tot_sd = float(sum(sd))
    if bm > 1:
        bm = 1
    output = abs((bm - (tot_sd/((size[0]+1)*size[1]))))
    return output

### Objective: Number of clusters
def count_clust(g,bm):
    clust = clusters(g)
    return abs(bm - len(clust))

### Objective: measure proportion of closed clusters:
def count_closed_clust(g, size, bm):
    tot_clust = len(clusters(g))
    closed = len(cl_clstrs(g, size))
    return abs(bm - (float(closed)/tot_clust))

### Objective: Bias the avg size of clusters by type
### looking to minimise the std for a given cluster size
# def bias_cl_size(g,size,type,bm):
#     tot_cells = ((size[0] + 2) * (size[1] + 2))
#     calc_bm = round(bm*tot_cells)
#     if type == 'open':
#         op = op_clstrs(g,size)
#         op_size = []
#         for i in op:
#             op_size.append(len(i))
#         var = []
#         for i in op_size:
#             var.append(pow((i-calc_bm),2))
#             if len(var)>0:
#                 variance = sum(var)/len(var)
#                 return math.sqrt(variance)
#             else:
#                 return calc_bm
#     if type == 'closed':
#         cl = cl_clstrs(g,size)
#         cl_size = []
#         for i in cl:
#             cl_size.append(len(i))
#         var = []
#         for i in cl_size:
#             var.append(pow((i-calc_bm),2))
#         if len(var) > 0:
#             variance = sum(var)/len(var)
#             return math.sqrt(variance)
#         else:
#             return calc_bm

def bias_cl_size(g, size, type, bm):
    tot_cells = ((size[0] + 2) * (size[1] + 2))
    if type == 'open':
        op = op_clstrs(g, size)
        op_size = []
        for i in op:
            op_size.append(len(i))
        if len(op_size) > 0:
            avg_op_size = sum(op_size)/len(op_size)
        else:
            avg_op_size = 0
        var = []
        for i in op_size:
            var.append(pow((i - avg_op_size), 2))
            if len(var) > 0:
                variance = sum(var) / len(var)
                return round(abs(bm - math.sqrt(variance)),3)
            else:
                return 5
    if type == 'closed':
        cl = cl_clstrs(g, size)
        cl_size = []
        for i in cl:
            cl_size.append(len(i))
        if len(cl_size)>0:
            avg_cl_size = sum(cl_size)/len(cl_size)
        else:
            avg_cl_size = 0
        var = []
        for i in cl_size:
            var.append(pow((i - avg_cl_size), 2))
        if len(var) > 0:
            variance = sum(var) / len(var)
            return round(abs(bm - (math.sqrt(variance))),3)
        else:
            return 5

### Objective: Bias the number of cross ventilation lines to match a benchmark
# def cross_vent(g,size,bm):
#     gr = grid(size)
#     op = op_clstrs(g,size)
#     cv = []
#     for i in range(len(op)):
#         cv.append(0)
#         for j in op[i]:
#             if j not in gr and j%(size[0]+2)==0:
#                 shrt_path = find_shortest_path(op[i],j,(j+(size[0]+1)))
#                 if len(shrt_path) == size[0]+2:
#                     cv[i]+=1
#     return abs(bm- float(sum(cv))/len(cv))

def cross_vent(g,size,bm):
    gr = grid(size)
    op = op_clstrs(g,size)
    cv = []
    for i in range(len(op)):
        cv.append(0)
        for j in op[i]:
            if j not in gr and j%(size[0]+2)==0:
                n = 0
                for node in range(j,j+size[0]+2):
                    if node in g.keys() and node+1 in g[node]:
                        n+=1
                if n == size[0]+1:
                    cv[i]+=1
    return abs(bm - float(sum(cv)) / len(cv))

### Objective: Avg Number of conections per node
### can be applied to whole graph or to dif types
def avg_degree(g,size,type,bm):
    if type == 'all':
        deg = []
        for node in g:
            deg.append(len(g[node]))
        return abs(bm - (float(sum(deg))/len(deg)))
    elif type == 'open':
        op = op_clstrs(g,size)
        deg = []
        for c in op:
            deg2=[]
            for node in c:
                deg2.append(float(len(c[node])))
            deg.append(sum(deg2)/len(deg2))
        return abs(bm - (float(sum(deg)) / len(deg)))
    elif type == 'closed':
        cl = cl_clstrs(g,size)
        deg = []
        for c in cl:
            deg2=[]
            for node in c:
                deg2.append(float(len(c[node])))
            deg.append(sum(deg2)/len(deg2))
        return abs(bm - (float(sum(deg)) / len(deg)))

def perimeter(g,s):
    per = []
    for i in g.keys():
        x = i%s[0]
        y=i/s[0]
        per.append(i)
        per.append(i+s[0])
        per.append((s[0]*(s[1]+1))+y+(x*s[1]))
        per.append((s[0]*(s[1]+1))+y+(x*s[1])+s[1])
    p = [i for i in per if per.count(i)==1]
    return p


def is_open(chr,g,s):
    p = perimeter(g,s)
    count = 0
    for i in p:
        if chr[i] == 0:
            count+=1
        else:
            pass
    if count > 0:
        return True
    else:
        return False

### 3D functions start here!!!!!!

###Generates the graph of connected spaces from a binary chromosome
def chr_graph3D(chr,s):
    g = {}
    tot_cells = s[0]*s[1]*s[2]
    xy_plane = s[0]*s[1]*(s[2]+1)
    xz_plane = s[0]*(s[1]+1)*s[2]
    yz_plane = (s[0]+1)*s[1]*s[2]
    for cell in range(tot_cells):
        g[cell] = []
    for i in g.keys():
        z = i / (s[0] * s[1])
        x = i%s[0]
        y = (i/s[0])-(s[1]*z)
        bot = (y*s[0])+x+(z*(s[0]*s[1]))
        top = bot + (s[0]*s[1])
        front = xy_plane + x + (y*(s[0]*s[2])) + (z*s[0])
        back = front + (s[0]*s[2])
        left = xy_plane + xz_plane + (x*(s[1]*s[2])) + y + (z*s[1])
        right = left + (s[1]*s[2])
        if z > 0 and chr[bot] == 0:
            g[i].append(i-(s[0]*s[1]))
        if z < (s[2]-1) and chr[top] == 0:
            g[i].append(i+(s[0]*s[1]))
        if y > 0 and chr[front] == 0:
            g[i].append(i-s[0])
        if y < (s[1]-1) and chr[back] == 0:
            g[i].append(i+s[0])
        if x > 0 and chr[left] == 0:
            g[i].append(i-1)
        if x < (s[0]-1) and chr[right] == 0:
            g[i].append(i+1)
        g[i] = set(g[i])

    return g

### Finds the outer shell for a 3D graph
def outer_shell(g,s):
    shell = []
    xy_plane = s[0] * s[1] * (s[2] + 1)
    xz_plane = s[0] * (s[1] + 1) * s[2]
    for i in g.keys():
        z = i / (s[0] * s[1])
        x = i % s[0]
        y = (i / s[0]) - (s[1] * z)
        bot = (y * s[0]) + x + (z * (s[0] * s[1]))
        top = bot + (s[0] * s[1])
        front = xy_plane + x + (y * (s[0] * s[2])) + (z * s[0])
        back = front + (s[0] * s[2])
        left = xy_plane + xz_plane + (x * (s[1] * s[2])) + y + (z * s[1])
        right = left + (s[1] * s[2])
        shell.extend([bot,top,front,back,left,right])
    s = [i for i in shell if shell.count(i)==1]
    return s

### Openness of outer shell. If bm == 0, returns the ratio of open walls
def os_open(chr,g,s,bm):
    os = outer_shell(g,s)
    count = 0
    for i in os:
        if chr[i]==0:
            count+=1
    return abs(bm-(float(count)/len(os)))

### Walkable space. Returns indicator that combines ratio of spaces in a
### cluster that have 'floor' and the number of spaces that are 'accessible'
def walkability3D(chr,g,s,bm):
    floor = 0
    w = []
    for i in g.keys():
        z = i / (s[0] * s[1])
        x = i % s[0]
        y = (i / s[0]) - (s[1] * z)
        pot = 4
        deg = 0
        if x == 0 or x == s[0]-1:
            pot-=1
        if y == 0 or y == s[1]-1:
            pot-=1
        if chr[i] == 1:
            floor+=1
            for j in g[i]:
                zj = j/(s[0]*s[1])
                if zj == z:
                    deg+=1
        w.append(float(deg)/pot)
    wfr = float(floor)/len(g.keys()) #Walkable floor ratio
    ar = sum(w)/len(w) #accessibility ratio (how much of the potential accessibility is reached
    return abs(bm-(wfr*ar))