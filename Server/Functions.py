from mainGA import walkability,structure,hamming_dist,sort_pop,mutate,tournament,mate
from myLib import Individual

def evolve(pop_size,ind_size,gens,problem,pop=[]):
# def evolve(pop_size, ind_size, gens, problem, pop=[]):
    _gens = gens
#     pop = []
    ### check population size
    gens=int(gens)
    pop_size=int(pop_size)
    ind_size=eval(ind_size)
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
        # print "test~~~~~~~~~~~~``"
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

    # return pareto_fronts_out
    return srtd_pop
    # print 'there are ', len(full_pop_out), 'in the pareto front'
    # print pareto_fronts_out
    # print values_out
    # print full_pop_out