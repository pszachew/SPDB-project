import random
import itertools
from deap import base
from deap import creator
from deap import tools


from dbaccess import DbAccess

def find_path(cursor, starting_point, places, starting_time,  transport):
    pass
    print("find_path")
    # all_points =  { i: places[i] for i range(len(places))}

    # print(starting_point)
    # print(places)
    # print(starting_time)
    # print(transport)

    
    closest_points_ids = _get_closest_point_ids(starting_point, places) # ids of closest points in database, used in dijkstra algorithm
    # points_ids = {i: closest_points_ids[i] for i in range(len(closest_points_ids))} # own ids from 0 to 

    # print(closest_points_ids)

    paths = _get_paths(closest_points_ids)
    costs = _extract_costs(paths)

    # print(paths)

    # all points
    points = {i: places[i] for i in range(len(closest_points_ids)-1)} | {len(closest_points_ids)-1: starting_point}
    
    # # print(paths)
    # # print(points)

    # # print(costs)
    # _find_best_path(points, costs)
    # BestPathEvolutionAlgorithm(points, costs, crossing_prob = 0.5, mutation_prob = 0.5, pop_size = 10)
    
    bpea = BestPathEvolutionAlgorithm(points, costs, 10, 0.5, 0.5, 5)
    result = bpea.run()
    best_order = [len(places)] + result[0]
    # print(f"best order : {best_order}")

    shortest_path = _extract_path(paths, best_order)

    return best_order, shortest_path

def _get_closest_point_ids(starting_point, places):
    points = [{'lat': place["lat"], 'lng': place["lng"]} for place in places] + [starting_point] # starting point push back, because it isnt used as variable in permutation

    closest_pids = []

    orig_pid = 0
    for point in points:
        pid, = DbAccess.get_closest_point(point["lng"], point["lat"])
        closest_pids.append((orig_pid, pid))
        orig_pid += 1

    return closest_pids

def _get_paths(pids):
    paths = {}

    for s_orig, source in pids:
        for t_orig, target in [pid for pid in pids if pid != (s_orig, source)]:
            result = DbAccess.get_shortest_path(source, target)
            # result[0] = (*result[0], s_orig) # add original point ids
            # result[-1] = (*result[-1], t_orig)
            # print(type(result[-1][5]))
            paths[(s_orig, t_orig)] = result
    
    return paths

def _extract_costs(paths):
    costs = {key: value[-1][5]  for key, value in paths.items()}
    return costs

def _extract_path(all_paths, points_order):
    pass
    all_points_order = {}
    path = []
    paths = {}
    
    points_paths = [all_paths[(points_order[i], points_order[i+1])] for i in range(len(points_order)-1)]

    i = 0
    for p in points_paths:
        all_points_order[i] = []
        for j in range(len(p)):
            all_points_order[i].append(p[j][2])
        i +=1

    points = list(itertools.chain.from_iterable(all_points_order.values()))
    cords = DbAccess.get_path(points)

    # specify nr of path
    for i in range(len(all_points_order)):
        paths[i] = []
        pts = all_points_order[i]
        for j in range(len(pts)):
            cord = [x[1] for x in cords if x[0] == pts[j]]
            paths[i].append(cord)

    return paths


class BestPathEvolutionAlgorithm:

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    
    # toolbox = base.Toolbox()
    # points = []
    # costs = []

    def __init__(self, points, costs, num_of_gen = 10, crossing_prob = 0.5, mutation_prob = 0.5, pop_size = 10) -> None:
        pass
        self.points = points
        self.costs = costs

        self.IND_SIZE = len(points) - 1
        self.NGEN = num_of_gen # number of generations
        self.POPSIZE = pop_size
        self.CXPB = crossing_prob # crossing probability
        self.MUTPB = mutation_prob # mutation probability

        # sample_elems = list(points.keys())[1:]

        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_permutation", random.sample, range(self.IND_SIZE), self.IND_SIZE)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.attr_permutation)

        self.toolbox.register("mate", tools.cxOrdered)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=self.MUTPB)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self._evaluate)

    def run(self):
        pop = [self.toolbox.individual() for i in range(self.POPSIZE)]#

        # for g in range(1):
        for g in range(self.NGEN):

            # select the next generation individuals
            offspring = self.toolbox.select(pop, len(pop))

            # clone selected individuals
            offspring = list(map(self.toolbox.clone, offspring))

            # apply crossover on the offspring

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                child1 = self.toolbox.clone(child1)
                child2 = self.toolbox.clone(child2)
                if random.random() < self.CXPB:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            # apply mutation on the offspring
            for mutant in offspring:
                if random.random() < self.MUTPB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

        #     # evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)

            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit


            # the population is entirely replaced by the offspring
            pop[:] = offspring

        return tools.selBest(offspring, 3)
        # return 0

    def _evaluate(self, individual):
        distance = 0

        distance += self.costs[(list(self.points.keys())[-1], individual[0])] # distance from starting point to first place
        for i in range(len(individual)-1):
            distance += self.costs[(individual[i], individual[i+1])]

        return distance,
