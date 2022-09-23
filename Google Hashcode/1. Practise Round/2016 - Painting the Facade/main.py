import multiprocessing

import argparse
import importlib

enableMultiprocessing = False

baseSolver = None
output = None


def solve(file):
	global baseSolver
	global output
	# solver init with filepath
	solver = baseSolver.Solver(file)

	try:
		# solve the problem with given input
		solver.solve()
	except KeyboardInterrupt:
		print('Interrupted')

	# maybe save create a solution file
	solver.write(output)


def main():
	global baseSolver, output, enableMultiprocessing
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


if __name__ == '__main__':
	main()
