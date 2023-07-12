priority = {'^':2, '*':1, '/':1, '+':0, '-':0}
ops = {'^', '*', '/', '+', '-'}
nums = {'0','1','2','3','4','5','6','7','8','9'}
# 0 => Start State (Accepts open bracket, number, X, negative sign) 
# 1 => Building a Number
# 2 => Got an Operator
# 3 => Got X
# 4 => Got decimal point (Accepts only a number)
# 5 => State Following state 4 similar to state 1 but doesn't accept decimal point
def validate(eqn:str,min,max):
    valid, msg = validate_eqn(eqn)
    if not valid:
        return valid, msg
    valid, msg = validate_range(min,max)
    return valid, msg
def validate_range(min,max):
    # Check min
    valid, msg = validate_numeric(min,"min")
    if not valid:
        return valid, msg
    # Check max
    valid, msg = validate_numeric(max,"max")
    if not valid:
        return valid, msg
    # Check if min <= max
    min_val = float(min)
    max_val = float(max)
    if min_val >= max_val:
        return False, "Invalid range: min can't be greater than max"
    return True, "Valid"
def validate_numeric(string,name):
    if len(string) == 0:
        return False, "Invalid range: "+name+" is empty"
    i = 0
    if string[0] == '-':
        i = 1
    point_flag = False
    valid = False
    msg = "Invalid range: Invalid "+name+" value"
    while i < len(string):
        if string[i] == '.':
            if point_flag:
                valid = False
                msg = "Invalid range: Unexpected decimal point in "+name+" value"
                break 
            else:
                point_flag = True
        elif string[i] == '-':
            valid = False
            msg = "Invalid range: Unexpected negative sign in "+name+" value"
            break  
        else:
            valid = True
            msg = "Valid"
        i+=1
    return valid,msg
def validate_eqn(eqn:str):
    if len(eqn) == 0:
        return False, "No Function is provided"
    bracket_stack = list()
    state = 0
    for char in eqn:
        if char=='X':
            match state:
                case 0:
                    state = 3
                case 2:
                    state = 3
                case _:
                    return False, "Invalid syntax near " + char
        elif char in nums:
            match state:
                case 0:
                    state = 1
                case 1:
                    state = 1
                case 2:
                    state = 1
                case 4:
                    state = 5
                case 5:
                    state = 5
                case _:
                    return False, "Invalid syntax near " + char
        elif char == '.':
            match state:
                case 1:
                    state = 4
                case _:
                    return False, "Invalid syntax near " + char
        elif char == '-' and state==0:
            state = 2
        elif char in ops:
            match state:
                case 1:
                    state = 2
                case 3:
                    state = 2
                case 5:
                    state = 2
                case _:
                    return False, "Invalid syntax near " + char
        elif char == '(':
            bracket_stack.append(char)
            if state == 0 or state == 2:
                state = 0
            else:
                return False, "Invalid syntax near " + char
        elif char == ')':
            if len(bracket_stack) == 0:
                return False, "Unbalanced brackets"
            bracket_stack.pop()
            if state == 1 or state == 3 or state == 5:
                state = 3
            else:
                return False, "Invalid syntax near " + char
        else:
            return False, "Unexpected character " + char
    if len(bracket_stack) > 0:
        return False, "Unbalanced brackets"
    if state == 2:
        return False, "Invalid syntax near " + eqn[-1]
    return True, "Valid"