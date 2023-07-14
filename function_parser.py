import numpy as np
from eqn_structs import expression, symbol
priority = {'^':2, '*':1, '/':1, '+':0, '-':0}
ops = {'^', '*', '/', '+', '-'}
nums = {'0','1','2','3','4','5','6','7','8','9','.'}
def parse(eqn:str,min,max):
    '''Constructs a parse tree and uses it to calculate f(x) for given range of x values'''
    parse_tree = expression([])
    parse_rec(eqn, parse_tree)
    return funcCalc(parse_tree,min,max)
def funcCalc(func:expression,min,max):
    '''Calculates f(x) for given range of x values given a parse tree'''
    pts = 5000  # Number of points to calculate
    step = (max-min)/pts
    x_range = np.arange(min,max+step,step)
    x = []
    y = []
    for i in x_range:
        f_x = func.calc(i)
        # Invalid values are not included in the plot (Infinity, imaginary numbers, etc.)
        if f_x != float("inf"):
            x.append(i)
            y.append(f_x)
    return x,y
def parse_rec(eqn:str, expr:expression, index=0, parent_op:str = '+'):
    '''Constructs a parse tree for given eqn string'''
    last_op = parent_op
    while index < len(eqn):
        if eqn[index] == "(":
            # Go 1 level deeper for parenthesis
            new_expr = expression([])
            expr.node_list.append(new_expr)
            index = parse_rec(eqn, new_expr, index+1, "+")
        elif eqn[index] == ")":
            # Step Out on closing parenthesis
            return index+1
        elif eqn[index] in ops:
            if priority[eqn[index]] > priority[last_op]:
                # If current operator has higher priority than the current scope's operator, go 1 level deeper
                new_expr = expression([expr.node_list.pop(), symbol(1, eqn[index])])
                expr.node_list.append(new_expr)
                index = parse_rec(eqn, new_expr, index+1, eqn[index])
            elif priority[eqn[index]] < priority[last_op]:
                # If current operator has lower priority than the current scope's operator, Step Out
                return index
            else:
                # If current operator has the same priority as the current scope's operator, append to current level normally
                expr.node_list.append(symbol(1, eqn[index]))
                last_op = eqn[index]
                index+=1
        elif eqn[index] == 'X':
            expr.node_list.append(symbol(2, eqn[index]))
            index+=1
        elif eqn[index] == 'e':
            expr.node_list.append(symbol(3, eqn[index]))
            index+=1
        else: # Numeric Constant Case
            num = ""
            # Build the number
            while index<len(eqn) and eqn[index] in nums:
                num += eqn[index]
                index+=1
            expr.node_list.append(symbol(0, num))
    return index