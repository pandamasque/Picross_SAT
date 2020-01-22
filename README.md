# Nonogram Solver

This is a nonogram (or picross) solver with a fully integrated GUI. This nonogram solver however, opposite to most of the others, works using only SAT.

## Using the interface

First of when you launch the app, you will be able to choose the size of your square nonogram. The size will have to be between 5 and 20, because above it will be to long to solve for a python solver and below it would be to easy, even for a human.

Then when the right size is selected you can push the "START" button in order to switch to a resizable window. You will then be able to enter your image's encoding.

In order to do so you can click on the side cells on the right and the bottom of the grid.

+ A right click decreases the number of dots to be aligned
+ A left click increases that same value

Note that a gape (a yellow cell with no number) between to cells with a value is always considered as non solvable.
The same rule is applied if the number of dots is greater than the size of the grid.

### Controls

Once you have entered the encoding of your image some actions are availlable to you:

+ The "***s***" key (for azerty users) allows to launch the solver. If there is a solution, it will be displayed on the grid, if not a message "No solution" will appear.
+ The "***w***" key (for azerty users) allows to clean the grid and remove all the dots andd messages from previous solvings.
+ The "***r***" key allows to reset the board in order to restart from a clean board.
+ The "***q***" key (for azerty users) allows to go back to the selection of the grid's size by closing the board's window.

## How it works

The Picross_SAT class works by taking the constraints from both vertical and horizontal directions. 

It will then, for each row, compute all possible arrangment of dash, and build a disjunctive normal form of all those possible row.

The problem here is that in order for a SAT solver to work we need a conjunctive normal form, that is why the tseitin transformation is used to transform the disjunctive form in conjunctive form. 

Then all those constraints concerning each row are put together in conjunctive form (the conjunction of a conjunction is a conjunction).
This final set of constraints is then given to the python SAT solver, its anwser will be converted to a a grid and returned. 
