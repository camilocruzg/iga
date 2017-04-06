from random import randint, random
from myLib import Individual
###Evaluation functions

###Walkability
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
        if x == 0 or x == ind.s[0] - 1:
            pot -= 1
        if y == 0 or y == ind.s[1] - 1:
            pot -= 1
        ###count deg for each node that has a horizontal panel
        if ind[i] == 1:
            if i + 1 in g[i] and ind[i + 1] == 1:
                deg += 1
            if i - 1 in g[i] and ind[i - 1] == 1:
                deg += 1
            if i + ind.s[0] in g[i] and ind[i + ind.s[0]] == 1:
                deg += 1
            if i - ind.s[0] in g[i] and ind[i - ind.s[0]] == 1:
                deg += 1
        ###
        w.append(float(deg) / pot)
    ar = sum(w) / len(g.keys())  #accessibility ratio (how much of the potential accessibility is reached
    ind.values['walk'] = "%.3f" % ar
    return ind.values['walk']


###Structural elements
def structure(ind):
    cols = []
    for i in range(int((ind.s[0] + 1) * (ind.s[1] + 1))):
        cols.append(0)
    for i, col in enumerate(cols):
        x = int(i % (ind.s[0] + 1))
        y = int(i // (ind.s[0] + 1))
        neigh = []  #right, front, left, back
        if x < ind.s[0]:  #right
            neigh.append(int(x + ind.xy + (y * (ind.s[0] * ind.s[2]))))
        if y < ind.s[1]:
            neigh.append(int(y + ind.xy + ind.xz + (x * (ind.s[1] * ind.s[2]))))
        if x > 0:
            neigh.append(int(x - 1 + ind.xy + (y * (ind.s[0] * ind.s[2]))))
        if y > 0:
            neigh.append(
                int(y - 1 + ind.xy + ind.xz + (x * (ind.s[1] * ind.s[2]))))
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
    for i in range(len(cols)):
        if cols[i] == ind.s[2]:
            cols[i] = 1
        else:
            cols[i] = 0

    ind.values['structure'] = "%.3f"%(sum(cols) / float(len(cols)))
    return ind.values['structure']

###Hamming Distance for encouraging diversity
def hamming_dist(pop):
    for i, ind in enumerate(pop):
        hd = []
        for j, other in enumerate(pop):
            if i != j:
                dist = 0
                for b in range(int(ind.getLen())):
                    if ind[b] != other[b]:
                        dist += 1
                hd.append(float(dist) / ind.getLen())
        ind.hd = sum(hd) / (len(pop) - 1)
    return pop


###GA functionality
###Sorting
def sort_pop(pop, problem):
    new_pop = pop
    fronts = []
    while len(new_pop) > 0:
        fronts.append([])
        dom = []
        dom_by = []
        #TODO use map funciton to do this
        # map(lambda x,y:)
        #Evaluate dominance
        for i, ind in enumerate(new_pop):
            dom.append([])
            dom_by.append([])
            for j, other in enumerate(new_pop):
                if i != j:
                    if ind.dominates(other, problem):
                        dom[i].append(j)
                    if other.dominates(ind, problem):
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
        fronts[-1] = [i for (r, i) in sorted(zip(rank, fronts[-1]), reverse=True)]
        new_pop = [i for j, i in enumerate(new_pop) if j not in rem]
    return fronts


###Tournament for selection
def tournament(pop, p_len, problem):
    _pop = pop
    new_pop = []
    while len(new_pop) < p_len:
        r1 = randint(0, len(_pop) - 1)
        r2 = randint(0, len(_pop) - 1)
        ind = _pop[r1]
        other = _pop[r2]
        if ind.dominates(other,
                         problem) and other.dominates(ind, problem) is False:
            if ind.hd > other.hd:
                new_pop.append(ind)
                _pop.remove(ind)
            else:
                new_pop.append(other)
                _pop.remove(other)
        elif ind.dominates(other, problem):
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
        if len(pop) % 2 == 1:
            new_pop.append(pop[0])
            selected.append(0)
            del pop[0]
        else:
            r1 = randint(0, len(pop) - 1)
            r2 = randint(0, len(pop) - 1)
            if r1 in selected:
                r1 = randint(0, len(pop) - 1)
            elif r1 not in selected:
                selected.append(r1)
            if r2 in selected:
                r2 = randint(0, len(pop) - 1)
            elif r2 not in selected:
                selected.append(r2)
            p1 = randint(0, pop[r1].getLen() - 1)
            p2 = randint(0, pop[r1].getLen() - 1)
            p = sorted([p1, p2])
            ni1 = pop[r1][:p[0]] + pop[r2][p[0]:p[1]] + pop[r1][p[1]:]
            ni2 = pop[r2][:p[0]] + pop[r1][p[0]:p[1]] + pop[r2][p[1]:]
        new_ind1 = Individual(pop[0].s, pop[0].p, ni1)
        new_ind2 = Individual(pop[0].s, pop[0].p, ni2)
        new_pop.append(new_ind1)
        new_pop.append(new_ind2)
    return new_pop


### Mutation
def mutate(pop, prob):
    for ind in pop:
        for bit in ind:
            r = random()
            if r < prob:
                bit = abs(bit - 1)
    return pop


###The evolutionary process itself
#def evolve(pop,ind_size,generations,problem type):
def evolve(pop_size, ind_size, gens, problem, pop=[]):
    _gens = gens
    # pop = []
    ### check population size
    while len(pop) < pop_size:
        pop.append(Individual(ind_size))
    print 'the population is ', len(pop), 'individuals'

    ### evaluate population
    new_pop = pop
    for i in new_pop:
        walkability(i)
        structure(i)
    print "walkability and structure done"
    hamming_dist(new_pop)
    print "hamming dist done"
    ### Pareto front for each generation will be stored in this list
    pareto_fronts_out = []
    ### Values for individuals in pareto front for each gen will be stored in this list
    values_out = []
    ### Full pop will be stored here
    full_pop_out = []

    ### Evolution starts here
    while gens > 0:
        ### sort population
        fronts = sort_pop(new_pop, problem)
        sorted_pop = [ind for front in fronts for ind in front]
        ### elite population
        e_pop = []
        for ind in sorted_pop:
            if ind not in e_pop and len(e_pop) < int(len(new_pop) / 4):
                e_pop.append(ind)

        ### mating pool
        m_pool = tournament(sorted_pop, len(new_pop) - len(e_pop), problem)

        ### operate on mating pool
        off_1 = mate(m_pool)
        offspring = mutate(off_1, 0.05)

        ### recompose population
        new_pop = e_pop + offspring
        for ind in new_pop:
            ind.clear_values()
        ### re_evaluate new_pop
        for i in new_pop:
            walkability(i)
            structure(i)
        hamming_dist(new_pop)
        fronts2 = sort_pop(new_pop, problem)
        pFront = fronts[0]
        pFront2 = []
        for ndf in pFront:
            if ndf not in pFront2:
                pFront2.append(ndf)
        pareto_fronts_out.append(pFront2)
        values_out.append([i.values for i in pFront2])
        srtd_pop = [ind for front in fronts2 for ind in front]
        full_pop_out.append(srtd_pop)
        gens -= 1
        print "Number %dth loop is done"%(gens)
    print 'there are ', len(full_pop_out), 'in the pareto front'
    print pareto_fronts_out
    print values_out
    print full_pop_out
    prompt1 = raw_input('Terminate? (Y/N): ')
    if prompt1 == 'Y':
        exit()
        # print 'there are ', len(full_pop_out), 'in the pareto front'
        # return pareto_fronts_out, values_out, full_pop_out
    elif prompt1 == 'N':
        # _pop_size = pop_size
        # _ind_size = ind_size
        # _gens = gens
        # _problem = problem
        prompt2 = raw_input('seed population (enter list of indice up to %s): '
                            % (len(full_pop_out[0]) - 1))
        seed_pop = [
            full_pop_out[-1][seeded_ind]
            for seeded_ind in [int(ii) for ii in prompt2.split(',')]
        ]
        print 'you have selected', len(seed_pop), 'individuals to seed next gen'
        return evolve(pop_size, ind_size, _gens, problem, seed_pop)
    else:
        return 'You have failed!'

if __name__ == '__main__':
    s = (2, 3, 4)
    ############################
    # def evolve(pop,ind_size,gens,problem):
    for i in evolve(50, s, 5, 'max')[1]:
        print i


