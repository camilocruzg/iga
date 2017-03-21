from random import randint, random
from myLib import Individual

###Evaluation functions

###Walkability: this function calculates the ratio of accessible horizontal subdivisions
def walkability(ind):
    ###Get graph representation of individual
    g = ind.graph()
#    floor = 0
    ###Initialise walkability count
    w = []
    for i in g.keys():
        ###Get the coordeantes for each node in the graph
        z = i // (ind.s[0] * ind.s[1])
        x = i % ind.s[0]
        y = (i // ind.s[0]) - (ind.s[1] * z)
        ###Initialise potential connections pot: potential connections
        pot = 4
        ###Initialise counter for degree distribution deg: counter for actual connections
        deg = 0
        ###adjust pot for edges and corners
        if x == 0 or x == ind.s[0]-1:
            pot-=1
        if y == 0 or y == ind.s[1]-1:
            pot-=1
        ###count deg for each node that has a horizontal panel
        if ind[i] == 1:
            if i+1 in g[i] and ind[i+1] == 1:
                deg+=1
            if i-1 in g[i] and ind[i-1] == 1:
                deg+=1
            if i+ind.s[0] in g[i] and ind[i+ind.s[0]] == 1:
                deg+=1
            if i-ind.s[0] in g[i] and ind[i-ind.s[0]] == 1:
                deg+=1
        ###
        w.append(float(deg)/pot)
    ar = sum(w)/len(g.keys()) #accessibility ratio (how much of the potential accessibility is reached
    ind.values['walk'] = ar
    return ind.values['walk']

###Structural elements: this function calculates the ratio of structural lines
def structure(ind):
    cols = []
    for i in range(int((ind.s[0]+1)*(ind.s[1]+1))):
        cols.append(0)
    for i, col in enumerate(cols):
        x = int(i%(ind.s[0]+1))
        y = int(i//(ind.s[0]+1))
        neigh = [] #right, front, left, back
        if x < ind.s[0]: #right
            neigh.append(int(x + ind.xy + (y*(ind.s[0]*ind.s[2]) )))
        if y < ind.s[1]:
            neigh.append(int(y + ind.xy + ind.xz + (x*(ind.s[1]*ind.s[2]))))
        if x > 0:
            neigh.append(int(x - 1 + ind.xy + (y*(ind.s[0]*ind.s[2]) )))
        if y > 0:
            neigh.append(int(y - 1 + ind.xy + ind.xz + (x*(ind.s[1]*ind.s[2]))))
        z = 0
        while z < int(ind.s[2]):
            n = []
            for j in neigh:
                if j < (ind.xy + ind.xz):
                    n.append(ind[j + (z*int(ind.s[0]))])
                else:
                    n.append(ind[j + (z*int(ind.s[1]))])
            if sum(n) > 0:
                cols[i]+=1
            z+=1
    for i in range(len(cols)):
        if cols[i] == ind.s[2]:
            cols[i] = 1
        else:
            cols[i] = 0
    ind.values['structure'] = float(sum(cols)/len(cols))
    return ind.values['structure']



###GA functionality

###Hamming Distance for encouraging diversity
def hamming_dist(pop):
    for i,ind in enumerate(pop):
        hd = []
        for j, other in enumerate(pop):
            if i != j:
                dist = 0
                for b in range(int(ind.getLen())):
                    if ind[b] != other[b]:
                        dist+=1
                hd.append(dist/ind.getLen())
        ind.hd = sum(hd)/(len(pop)-1)
    return pop

###Sorting
def sort_pop(pop,problem):
    new_pop = pop
    fronts = []
    while len(new_pop) > 0:
        fronts.append([])
        dom = []
        dom_by = []
        #Evaluate dominance
        for i ,ind in enumerate(new_pop):
            dom.append([])
            dom_by.append([])
            for j, other in enumerate(new_pop):
                if i != j:
                    if ind.dominates(other,problem):
                        dom[i].append(j)
                    if other.dominates(ind,problem):
                        dom_by[i].append(j)
            ind.dom = dom[i]
            ind.dom_by = dom_by[i]
        rem = []
        for j, ind in enumerate(new_pop):
            if len(ind.dom_by) == 0:
                fronts[-1].append(ind)
                rem.append(j)
        rank = []
        for i in fronts[-1]:
            rank.append(len(i.dom))
        fronts[-1] = [i for (r,i) in sorted(zip(rank,fronts[-1]),reverse = True)]
        new_pop = [i for j,i in enumerate(new_pop) if j not in rem]
    return fronts

###Tournament for selection
def tournament(pop,p_len,problem):
    _pop = pop
    new_pop = []
    while len(new_pop) < p_len:
        r1 = randint(0,len(_pop)-1)
        r2 = randint(0,len(_pop)-1)
        ind = _pop[r1]
        other = _pop[r2]
        if ind.dominates(other,problem) and other.dominates(ind,problem) is False:
            if ind.hd > other.hd:
                new_pop.append(ind)
                _pop.remove(ind)
            else:
                new_pop.append(other)
                _pop.remove(other)
        elif ind.dominates(other,problem):
            new_pop.append(ind)
            _pop.remove(ind)
        else:
            new_pop.append(other)
            _pop.remove(other)
    return new_pop

### Mating
def mate(pop):
    selected = []
    new_pop = []
    ni1 = None
    ni2 = None
    while len(new_pop) < len(pop):
        if len(pop)%2 == 1:
            new_pop.append(pop[0])
            selected.append(0)
            del pop[0]
        else:
            r1 = randint(0,len(pop)-1)
            r2 = randint(0,len(pop)-1)
            if r1 in selected:
                r1 = randint(0,len(pop)-1)
            elif r1 not in selected:
                selected.append(r1)
            if r2 in selected:
                r2 = randint(0,len(pop)-1)
            elif r2 not in selected:
                selected.append(r2)
            p1 = randint(0,pop[r1].getLen()-1)
            p2 = randint(0,pop[r1].getLen()-1)
            p = sorted([p1,p2])
            ni1 = pop[r1][:p[0]] + pop[r2][p[0]:p[1]] + pop[r1][p[1]:]
            ni2 = pop[r2][:p[0]] + pop[r1][p[0]:p[1]] + pop[r2][p[1]:]
        new_ind1 = Individual(pop[0].s,pop[0].p,ni1)
        new_ind2 = Individual(pop[0].s,pop[0].p,ni2)
        new_pop.append(new_ind1)
        new_pop.append(new_ind2)
    return new_pop

### Mutation
def mutate(pop,prob):
    for ind in pop:
        for bit in ind:
            r = random()
            if r < prob:
                bit = abs(bit-1)
    return pop

###K-means algorithm to present alternatives to user
def kmeans(k,points,d,centroids=[]):
    new_centroids = []
    clusters = [[] for n in range(k)]
    maxX = max(zip(*points)[0]) #Maximum value of X in the list of points being analised
    maxY = max(zip(*points)[1]) #Maximum value of Y in the list of points being analised
    ###Generate centroids
    if len(centroids) < k:
        for i in range(k):
            centroid = (random.randrange(maxX),random.randrange(maxY))
            centroids.append(centroid)
    ###Cluster points based on dist to centroids
    for pt in points:
        dists = []
        for c in centroids:
            dists.append(e_dist(pt,c))
        clusters[dists.index(min(dists))].append(pt)
    ###Calculate new centroids
    for cluster in clusters:
        new_centroid = calc_centroid(cluster)
        new_centroids.append(new_centroid)
    cen_dist = [e_dist(centroids[i],new_centroids[i]) for i in range(k)]
    ###If centroids are found...
    if all([i<d for i in cen_dist]):
        closest = []
        for j, c in enumerate(new_centroids):
            d = []
            for pt in clusters[j]:
                d.append(e_dist(c,pt))
            closest.append(clusters[j][d.index(min(d))])
        return closest
    ###If centroids are still to be found...
    else:
        centroids = new_centroids
        return kmeans(k,points,d,centroids)

###The evolutionary process itself
#def evolve(pop,pop_size,gens,problem):
def evolve(pop_size,ind_size,gens,problem,k,pop = []):
    _gens = gens
    pop = []
    ### check population size
    while len(pop) < pop_size:
        pop.append(Individual(ind_size))
    print 'the population has', len(pop), 'individuals'

    ### evaluate population
    new_pop = pop
    for i in new_pop:
        walkability(i)
        structure(i)
    hamming_dist(new_pop)

    ### Pareto front for each generation will be stored in this list
    pareto_fronts_out = []
    ### Values for individuals in pareto fron for each gen will be stored in this list
    values_out = []
    ### Full pop will be stored here
    full_pop_out = []

    ### Evolution starts here
    while gens > 0:
        ### sort population
        fronts = sort_pop(new_pop,problem)
        sorted_pop = [ind for front in fronts for ind in front]

        ### elite population
        e_pop = []
        for ind in sorted_pop:
            if ind not in e_pop and len(e_pop) < int(len(new_pop)/4):
                e_pop.append(ind)

        ### mating pool
        m_pool = tournament(sorted_pop,len(new_pop)-len(e_pop),problem)

        ### operate on mating pool
        off_1 = mate(m_pool)
        offspring = mutate(off_1,0.05)

        ### recompose population
        new_pop = e_pop + offspring
        for ind in new_pop:
            ind.clear_values()

        ### re_evaluate new_pop
        for i in new_pop:
            walkability(i)
            structure(i)
        hamming_dist(new_pop)

        # fronts2 = sort_pop(new_pop,problem)
        # nd_pop = [ind for front in fronts2 for ind in front[0]]
        # print len(nd_pop)
        # pFront = fronts2[0]
        # pFront2 = []
        # for ndf in pFront:
        #     if ndf not in pFront2:
        #         pFront2.append(ndf)
        # pareto_fronts_out.append(pFront2)
        # values_out.append([i.values for i in pFront2])
        # srtd_pop = [ind for front in fronts2 for ind in front]
        # full_pop_out.append(srtd_pop)
        gens-=1
    fronts2 = sort_pop(new_pop,problem)
    nd_pop = fronts2[0]
    d_pop = [indiv for fr in fronts2[1:] for indiv in fr]

    print len(fronts2)
    # print 'the new population has', len(new_pop), 'individuals'
    # print 'there are', len(nd_pop), 'non dominated individuals'
    # print 'there are', len(d_pop), 'dominated individuals'

    # print fronts2[0][0].values['structure']





    # print 'there are', len(full_pop_out), 'in the pareto front'
    # print pareto_fronts_out
    # print values_out
    # print full_pop_out[0]
    prompt1 = raw_input('Terminate? (Y/N): ')
    if prompt1 == 'Y':
        return pareto_fronts_out,values_out,full_pop_out
    elif prompt1 == 'N':
        pts = [(individual['structure'],individual['walk']) for individual in full_pop_out]
        display = kmeans(k,pts,0.0001)
        print display
        prompt2 = raw_input('sellect individuals to seed population')
        seed_pop = [
            full_pop_out[-1][seeded_ind]
            for seeded_ind in [int(ii) for ii in prompt2.split(',')]
        ]
        print 'you have selected', len(seed_pop), 'individuals to seed next gen'
        return evolve(pop_size,ind_size,_gens,problem,k,seed_pop)
    else:
        return 'You have failed!'

s = (2,3,4)

for i in evolve(100, s, 10, 'max', k=5)[1]:
    print i