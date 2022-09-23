import multiprocessing

import argparse
import importlib

enableMultiprocessing = False
selectSolverViaMemory = True
MaxMemory = 8 * 10 ** 9 # 8GB RAM

baseSolver = None
output = None

score = 0


def solve(file):
	global baseSolver, output, score, selectSolverViaMemory, MaxMemory
	# solver init with filepath
	if not selectSolverViaMemory:
		solver = baseSolver.Solver(file)
	else:
		baseSolver = importlib.import_module('.'.join(["solver", 'basesolver']))
		solver = baseSolver.BaseSolver(file)
		if solver.PizzaTypesNum * solver.MaxSlices * 4 > MaxMemory:
			baseSolver = importlib.import_module('.'.join(["solver", 'sorting']))
		else:
			baseSolver = importlib.import_module('.'.join(["solver", 'knapsack']))
		solver = baseSolver.Solver(file)

	try:
		# solve the problem with given input
		solver.solve()
		score += solver.compute_score()
	except KeyboardInterrupt:
		print('Interrupted')

	# maybe save create a solution file
	solver.write(output)


def main():
	global baseSolver, output, enableMultiprocessing, score
	parser = argparse.ArgumentParser()

	# need to be
	parser.add_argument("input", help="input file", nargs='+')

	parser.add_argument("--output", help="output directory", default="output/")
	parser.add_argument("--solver", type=str, default="example")
	parser.add_argument("--multiprocessing", action='store_true')
	args = parser.parse_args()

	baseSolver = None
	# try load the given solver
	try:
		baseSolver = importlib.import_module('.'.join(["solver", args.solver]))
	except ImportError:
		parser.print_help()
		print()
		print("ERROR: Solver '{0}' not available. Create a solver in file 'solver/{0}.py'.".format(args.solver))
		exit(1)
	output = args.output

	if args.multiprocessing:
		print('Multiprocessing')
		p = multiprocessing.Pool()
		p.map(solve, args.input)
		p.close()
		p.join()
	else:
		for file in args.input:
			solve(file)
	print("Total Score: ", score)


if __name__ == '__main__':
	main()
