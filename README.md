# SAT-SOLVER
The challenge is to write a SAT solver, and then use it to solve Sudoku problems.
Writing a SAT solver for Sudoku's requires that you write a SAT solver that can read DIMACS input. See the slides from the first lecture on propositional logic, or here (Links to an external site.); the "p" line will help you to more easily read your input file. 
encode the Sudoku rules as clauses in DIMACS format. You get these for free here. (Links to an external site.)
Suggestion: make sure you understand what the different lines of this file mean. You will need this later. 
encode a given puzzle in DIMACS format. Some examples of puzzle in DIMACS is here as well.
(again, make sure you understand what the different lines mean).
give (2)+(3) as input to (1) and return the solution to the given puzzle. 
This output should again be a DIMACS file, but containing only the truth assignment to all variables (729 for Sudoku, different for other SAT problems). If your input file is called 'filename', then make sure your outputfile is called 'filename.out'. If there is no solution (inconsistent problem), the output can be an empty file. If there are multiple solutions (eg. non-propert Sudoku) you only need to return a single solution.
Your SAT solver should implement at least three different strategies: the DPLL algorithm without any further heuristics, plus two different heuristics of your choice. These can be some of the heuristics discussed in the lectures, or any other heuristic you can find in the literature (or that you make up yourself, for that matter). Points will be awarded for how sophisticated the strategies are that you choose to implement, but you must implement two different strategies as well as the basic DP algorithm itself.

Of course, your SAT solver must be fully general, in the sense that it is an algorithm to solve not only Sudoku's formulated in SAT, but any SAT problem (at least in principle, given enough time and memory).


The SAT Solver has been developed in Python for the course Knowledge Representation.
