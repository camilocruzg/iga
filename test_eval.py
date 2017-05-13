from Init_Ind import Individual

s = (2,4,4)

ind_01 = Individual(s)

def structure(ind):
    cols = []
    for i in range(int((ind.s[0] + 1) * (ind.s[1] + 1))):
        cols.append(0)
    for i, col in enumerate(cols):
        x = int(i % (ind.s[0] + 1))
        y = int(i // (ind.s[0] + 1))
        neigh = []  # right, front, left, back
        if x < ind.s[0]:  # right
            neigh.append(int(x + ind.xy + (y * (ind.s[0] * ind.s[2]))))
        if y < ind.s[1]:
            neigh.append(int(y + ind.xy + ind.xz + (x * (ind.s[1] * ind.s[2]))))
        if x > 0:
            neigh.append(int(x - 1 + ind.xy + (y * (ind.s[0] * ind.s[2]))))
        if y > 0:
            neigh.append(int(y - 1 + ind.xy + ind.xz + (x * (ind.s[1] * ind.s[2]))))
        z = 0
        while z < int(ind.s[2]):
            n = []
            for j in neigh:
                if j < (ind.xy + ind.xz):
                    n.append(ind[j + (z * int(ind.s[0]))])
                else:
                    n.append(ind[j + (z * int(ind.s[1]))])
            if sum(n) > 0:
                cols[i] += 1
            z += 1
    print len(cols)
    print cols
    for i in range(len(cols)):
        if cols[i] == ind.s[2]:
            cols[i] = 1
        else:
            cols[i] = 0
    print cols
    ind.values['structure'] = "%.3f" % (sum(cols) / float(len(cols)))
    return ind.values['structure']

### returns Depth first search for graphs (returns sub-graphs of connected nodes)
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

### returns the clusters from a graph
def clusters(g):
    clust = []
    for node in g:
            c = dfs(g,node)
            if c not in clust:
                clust.append(c)
    return clust

def spaces(ind):
    g = ind.graph()
    c = clusters(g)
    print 'there are %s clusters' % len(c)
    possible_clusters = ind.s[0]*ind.s[1]*ind.s[2]
    print 'there could be %s clusters' % possible_clusters
    # spaces_index = float(possible_clusters)/float(len(c))
    # print 'the spaces index is %s' %spaces_index
    ind.values['space'] = "%.3f" %((float(len(c)) - 1.0)/(float(possible_clusters)-1.0))

    return ind.values['space']

print spaces(ind_01)
print structure(ind_01)