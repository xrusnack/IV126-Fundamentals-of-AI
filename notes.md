solution representation: list of indices containing values from 0-n
infeasible solutions: 
	- must be a permutation
	- timeout
initial solutions:
	-random
	-minimal spanning tree algo
destroy:
	-consider Shaw
cost function: incremental
solution acceptance: minimize the cost function
termination condition: iterate until the improvement is small enough
arguments: matrix of the distances

kubo: destroy, initial sol,
kaja: repair, cost function, 
obaja: explore LNS and stopping criteria


### Note edge cases

- empty instance
- instance with single city
- instance with 2 cities
