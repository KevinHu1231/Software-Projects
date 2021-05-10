#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
from itertools import product
from itertools import combinations
from itertools import permutations

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''

    tenner_csp = CSP("Tenner CSP")
    input_array = list(initial_tenner_board[0])
    variable_array = []
    n = len(input_array)
    cols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    for row in range(0,n):
        row_list = []
        for col in range(0,10):
            if input_array[row][col] == -1:
                var = Variable("Row: " + str(row) + " Column: " + str(col))
                var.add_domain_values(cols)
                tenner_csp.add_var(var)
                row_list.append(var)
            else:
                var = Variable("Row: " + str(row) + " Column: " + str(col))
                var.add_domain_values([input_array[row][col]])
                var.assign(input_array[row][col])
                tenner_csp.add_var(var)
                row_list.append(var)
        variable_array.append(row_list)
    #Constraints

    #n-ary sum constraints

    last_row = list(initial_tenner_board[1])

    for col in range(0,10):
        scope = []
        for row in range(0,n):
            scope.append(variable_array[row][col])

        c = Constraint("Sum: Column: " + str(col), scope)

        var_domains = []
        for var in scope:
            var_domains.append(var.cur_domain())

        satisfying_tuples = []
        for comb in product(*var_domains):
            if sum(comb) == last_row[col]:
                satisfying_tuples.append(comb)

        c.add_satisfying_tuples(satisfying_tuples)
        tenner_csp.add_constraint(c)

    #Row not equals constraints

    for row in range(0,n):
        for pair in combinations(cols,2):

            var1 = variable_array[row][pair[0]]
            var2 = variable_array[row][pair[1]]

            scope = [var1, var2]
            c = Constraint("Row NE: Row: " + str(row) + " Column 1: " + str(pair[0]) + " Column 2: " + str(pair[1]), scope)

            not_equals=[]
            for i in var1.cur_domain():
                for j in var2.cur_domain():
                    if i!=j:
                        not_equals.append((i,j))

            c.add_satisfying_tuples(not_equals)
            tenner_csp.add_constraint(c)

    #Adjacent not equals constraints

    for row in range(0,n):
        for col in range(0,10):

            var1 = variable_array[row][col]

            if row - 1 >= 0:
                up = 1
            else:
                up = 0
            if col - 1 >= 0:
                left = 1
            else:
                left = 0
            if row + 1 < n:
                down = 1
            else:
                down = 0
            if col + 1 < 10:
                right = 1
            else:
                right = 0

            if up == 1:
                var2 = variable_array[row-1][col]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Up", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

            if down == 1:
                var2 = variable_array[row + 1][col]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Down", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

            if up == 1 and left == 1:
                var2 = variable_array[row-1][col-1]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Upper Left", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

            if up == 1 and right == 1:
                var2 = variable_array[row-1][col+1]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Upper Right", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

            if down == 1 and left == 1:
                var2 = variable_array[row+1][col-1]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Lower Left", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

            if down == 1 and right == 1:
                var2 = variable_array[row+1][col+1]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Lower Right", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)
#IMPLEMENT
    return tenner_csp, variable_array #CHANGE THIS
##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary 
       all-different constraints: all-different constraints for the variables in
       each row, and sum constraints for each column. You may use binary 
       contstraints to encode contiguous cells (including diagonally contiguous 
       cells), however. Each -ary constraint is over more 
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''

    tenner_csp = CSP("Tenner CSP")
    variable_array = list(initial_tenner_board[0])

    n = len(variable_array)
    cols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    for row in range(0, n):
        for col in range(0, 10):
            if variable_array[row][col] == -1:
                var = Variable("Row: " + str(row) + " Column: " + str(col), cols)
                tenner_csp.add_var(var)
                variable_array[row][col] = var

            else:
                var = Variable("Row: " + str(row) + " Column: " + str(col), [variable_array[row][col]])
                var.assign(variable_array[row][col])
                tenner_csp.add_var(var)
                variable_array[row][col] = var

    # Constraints

    # n-ary sum constraints

    last_row = list(initial_tenner_board[1])

    for col in range(0, 10):

        scope = []
        for row in range(0, n):
            scope.append(variable_array[row][col])

        c = Constraint("Sum: Column: " + str(col), scope)

        var_domains = []
        for var in scope:
            var_domains.append(var.cur_domain())

        satisfying_tuples = []
        for combination in product(*var_domains):
            if sum(combination) == last_row[col]:
                satisfying_tuples.append(combination)

        c.add_satisfying_tuples(satisfying_tuples)
        tenner_csp.add_constraint(c)

    # Row all-different constraints

    # Calculate values satisfying all-different constraints

    for row in range(0, n):
        scope = []
        for col in range(0, 10):
            scope.append(variable_array[row][col])
        c = Constraint("All-Different: Row: " + str(row), scope)

        all_differents = []
        for i in permutations(cols, 10):
            if (scope[0].in_cur_domain(i[0]) is True) and (scope[1].in_cur_domain(i[1]) is True) and (scope[2].in_cur_domain(i[2]) is True) and (scope[3].in_cur_domain(i[3]) is True) and (scope[4].in_cur_domain(i[4]) is True) and (scope[5].in_cur_domain(i[5]) is True) and (scope[6].in_cur_domain(i[6]) is True) and (scope[7].in_cur_domain(i[7]) is True) and (scope[8].in_cur_domain(i[8]) is True) and (scope[9].in_cur_domain(i[9]) is True):
                all_differents.append(i)

        c.add_satisfying_tuples(all_differents)
        tenner_csp.add_constraint(c)

    # Adjacent not equals constraints

    for row in range(0, n):
        for col in range(0, 10):

            var1 = variable_array[row][col]

            if row - 1 >= 0:
                up = 1
            else:
                up = 0
            if col - 1 >= 0:
                left = 1
            else:
                left = 0
            if row + 1 < n:
                down = 1
            else:
                down = 0
            if col + 1 < 10:
                right = 1
            else:
                right = 0

            if up == 1:
                var2 = variable_array[row - 1][col]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Up", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

            if down == 1:
                var2 = variable_array[row + 1][col]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Down", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

            if up == 1 and left == 1:
                var2 = variable_array[row - 1][col - 1]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Upper Left", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

            if up == 1 and right == 1:
                var2 = variable_array[row - 1][col + 1]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Upper Right", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

            if down == 1 and left == 1:
                var2 = variable_array[row + 1][col - 1]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Lower Left", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

            if down == 1 and right == 1:
                var2 = variable_array[row + 1][col + 1]
                scope = [var1, var2]
                c = Constraint("Adjacent: Row: " + str(row) + " Column: " + str(col) + " Lower Right", scope)

                not_equals = []
                for i in var1.cur_domain():
                    for j in var2.cur_domain():
                        if i != j:
                            not_equals.append((i, j))

                c.add_satisfying_tuples(not_equals)
                tenner_csp.add_constraint(c)

    # IMPLEMENT
    return tenner_csp, variable_array  # CHANGE THIS
