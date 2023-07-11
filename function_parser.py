import numpy as np
from eqn_structs import expression, symbol
priority = {'^':2, '*':1, '/':1, '+':0, '-':0}
ops = {'^', '*', '/', '+', '-'}
nums = {'0','1','2','3','4','5','6','7','8','9'}
def parse(eqn:str,min,max):
    start_expr = expression([])
    parse_rec(eqn, start_expr)
    return funcCalc(start_expr,min,max)
def funcCalc(func:expression,min,max):
    pts = 1000
    step = (max-min)/pts
    x = np.arange(min,max,step)
    y = []
    for i in x:
        y.append(func.calc(i))
    return x,y
def parse_rec(eqn:str, expr:expression, index=0, parent_op:str = '+'):
    last_op = parent_op
    while index < len(eqn):
        if eqn[index] == "(":
            new_expr = expression([])
            expr.expr_list.append(new_expr)
            index = parse_rec(eqn, new_expr, index+1, "+")
        elif eqn[index] == ")":
            return index+1
        elif eqn[index] in ops:
            if priority[eqn[index]] > priority[last_op]:
                new_expr = expression([expr.expr_list.pop(), symbol(1, eqn[index])])
                expr.expr_list.append(new_expr)
                index = parse_rec(eqn, new_expr, index+1, eqn[index])
            elif priority[eqn[index]] < priority[last_op]:
                return index
            else:
                expr.expr_list.append(symbol(1, eqn[index]))
                last_op = eqn[index]
                index+=1
        elif eqn[index] == 'X':
            expr.expr_list.append(symbol(2, eqn[index]))
            index+=1
        else:
            num = ""
            while index<len(eqn) and eqn[index] in nums:
                num += eqn[index]
                index+=1
            expr.expr_list.append(symbol(0, num))
    return index