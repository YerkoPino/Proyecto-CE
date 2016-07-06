from pyevolve import *

def eval_func(chromosome):
	score = 0.0
	# iterate over the chromosome
	for value in chromosome:
		if value==0:
			score += 1
	return score

genome = G1DList.G1DList(10)
genome.setParams(rangemin=0, rangemax=1)
genome.evaluator.set(eval_func)
ga = GSimpleGA.GSimpleGA(genome)
ga.setMinimax(Consts.minimaxType["minimize"])
ga.evolve(freq_stats=10)
print ga.bestIndividual()