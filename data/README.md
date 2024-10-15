# Instance format

The provided instances are saved as JSON files with the following attributes:

 * __Coordinates__: list of all location coordinates in the problem, each location is a two-element list
 * __Matrix__: Euclidean 2D matrix of distances between all pairs of locations (symmetric), locations are indexed from 0
 * __GlobalBest__: globally optimal solution, sequence of locations in the route, locations are indexed from 0
 * __GlobalBestVal__: cost of the globally optimal solution
 * __Timeout__: timeout in seconds for the given instance

# Notes to instance contents


## Global best solution

The instance files contain globally optimal solutions and their costs. This information was added for your convenience so that you know the gap between yours and the optimal solution and may compare them visually (see the visualization tool README for more details). Note that you must not use this solution nor its value within the logic of your solver.

## Timeout

In order to make the evaluation of your homework possible, it is necessary to cap the available time for your solvers. Since instances are of different sizes, each is limited by a different timeout. Please respect the specified values. Solvers exceeding this limit by a larger margin will be terminated during the evaluation.

# Solution format

Your solver should produce a single JSON file containing one solution. The JSON file must contain a list in the same format as described for the __GlobalBest__ attribute of input instances.

