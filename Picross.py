import numpy as np
from ColunmPossible import generatePossibleColunm
import Tseitin as t
from pysat import Solver
import math




class Picross(object):


    def __init__(self, x_dashs = None, y_dashs = None, size_x = None, size_y = None):

        if not (size_x is None) and not (size_y is None):
            if not isinstance(size_x, int):
                raise TypeError("'size_x' attribut must be an int.")
            if not isinstance(size_y, int):
                raise TypeError("'size_y' attribut must be an int.")
            if size_x < 1:
                raise ValueError("'size_x' must be at least 1.")
            if size_y < 1:
                raise ValueError("'size_y' must be at least 1.")

        if not (x_dashs is None) and not (y_dashs is None):
            self._check_array(x_dashs, y_dashs.shape[0])
            self._check_array(y_dashs, x_dashs.shape[0])
        
        if not (size_x is None) and not (x_dashs is None) :
            raise ResourceWarning("(You don't need to specify size_x if you give x_dash)")
        if not (size_y is None) and not (y_dashs is None) :
            raise ResourceWarning("(You don't need to specify size_y if you give y_dash)")

        if not (size_x is None) and not (size_y is None):
            self._size_x = size_x
            self._size_y = size_y
            self._x_dashs = np.zeros((size_x, math.ceil(size_y/2) + 1))
            self._y_dashs = np.zeros((size_y, math.ceil(size_x/2) + 1))
            
        if not (x_dashs is None) and not (y_dashs is None):
            self._size_x = x_dashs.shape[0]
            self._size_y = y_dashs.shape[0]
            self._x_dashs = x_dashs
            self._y_dashs = y_dashs

        self._board = np.zeros((self._size_y, self._size_x))

        if ((x_dashs is None) or (y_dashs is None)) and ((size_x is None) or (size_y is None)):
            raise RuntimeError("Both sizes or both the arrays must be specified!")


    def _solve(self):
        raise NotImplementedError("This function should be implemented in the childs' classes. \
            It put a solution to the constraints in the attribut board, or None if there is no solution.")


    def getSolution(self):
        self._solve()
        return self._board


    def _changeConstraints(self, colunm, pos, val, array, size):
        if (colunm < 0) or (colunm >= array.shape[0]):
            raise ValueError("The value of 'colunm' must be between 0 and %d.", array.shape[0])
        if (pos < 0) or (pos >= math.ceil(size/2) + 1):
            raise ValueError("The value of 'pos' must be between 0 and the opposite widht / 2 + 1.")
        if pos > 0 and array[colunm][pos-1] < 1:
            raise IndexError("You can't assign a value after the end of the constraints.")

        array[colunm][pos] = val


    def changeXConstraints(self, colunm, pos, val):
        self._changeConstraints(colunm, pos, val, self._x_dashs, self._size_y)


    def changeYConstraints(self, colunm, pos, val):
        self._changeConstraints(colunm, pos, val, self._y_dashs, self._size_x)


    def _check_array(self, array, size):
        if not isinstance(array, np.ndarray) or not(array.dtype == np.dtype('int32')):
                raise TypeError("The 'dash' attribut must be an int numpy array.")
        if (np.max(np.argmin(array, axis = 1) + np.sum(array, axis = 1))-1) > size:
                raise ValueError("The size of the dashs on an axis must be inferior to the size of the other.")
        if (array.shape[1] != math.ceil(size/2) + 1):
                raise ValueError("The second dimension of a dashs must be the other direction widht / 2 + 1.")
        for i in range(array.shape[1]):
            if np.sum(array[i, np.argmin(array[i]):]) > 0:
                raise ValueError("There must be no gap between 2 lines in a dash.")


    def defineXConstraints(self, array):
        self._check_array(array, self._size_y)
        if array.shape[0] != self._size_x:
            raise ValueError("The array's shape[0] must be the x size.")
        
        self._x_dashs = array


    def defineYConstraints(self, array):
        if array.shape[0] != self._size_y:
            raise ValueError("The array's shape[0] must be the y size.")
        self._check_array(array, self._size_x)
        self._y_dashs = array



class Picross_SAT(Picross):


    def __init__(self, x_dashs=None, y_dashs=None, size_x=None, size_y=None):
        super().__init__(x_dashs=x_dashs, y_dashs=y_dashs, size_x=size_x, size_y=size_y)


    def _StartEndToBlackWhite(self, dict, size):#Better algorithme to find
        val = -1
        bw = []
        modif = False
        vals = np.array(list(dict.values()))
        for r in range(size):
            if r in dict.values() and val == -1:
                val*=-1
                modif = True
                
            bw.append(val*(r+1))
            
            if r in dict.values() and val == 1 and not modif:
                val*=-1

            if vals[vals == r].shape[0] > 1:
                val*=-1

            modif = False

        return bw


    def _generatePossibleLine(self, line_Constraints, size):
        constraints = []
        for p,constraint in enumerate(line_Constraints):
            constraints.append([])
            solutions = generatePossibleColunm(constraint,size)
            for sol in solutions:
                constraints[p].append(self._StartEndToBlackWhite(sol, size))
        return constraints
                

    def _toTrueCoord(self, X, i, array):
        sign = array/ np.abs(array)
        array = np.abs(array)
        if X:
            return (sign*((array - 1) * self._size_x + i + 1)).astype(int)
        return (sign*(array + self._size_y * i)).astype(int)

    
    def _generateLineConstraints(self, line_Constraints, X, size):
        possible_line = self._generatePossibleLine(line_Constraints, size)
        constraints = []

        for i in range(line_Constraints.shape[0]):
            colunm_possible_dnf = np.array(self._toTrueCoord(X, i, possible_line[i]))
            colunm_possible_cnf = t.Tseitin(colunm_possible_dnf, self.maxi)
            constraints.extend(colunm_possible_cnf)
            self.maxi += len(colunm_possible_dnf) 

        return constraints


    def _generateXConstraints(self):
        return self._generateLineConstraints(self._x_dashs, True, self._size_y)


    def _generateYConstraints(self):
        return self._generateLineConstraints(self._y_dashs, False, self._size_x)


    def _generateConstraints(self):
        self._board = np.zeros((self._size_y, self._size_x))
        self.maxi = self._size_x * self._size_y
        Y = self._generateYConstraints()
        X = self._generateXConstraints()
        self.clauses = X+Y


    def _solve(self):
        self._generateConstraints()
        solver = Solver()
        for line in self.clauses:
            solver.addClause(line)

        solver.buildDataStructure()
        solver.solve()
        try:
            result = (np.array(solver.finalModel)[:self._size_x*self._size_y]).reshape(self._size_y, self._size_x)
            self._board[result > 0] = 1
        except:
            self._board = None

