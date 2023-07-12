priority = {'^':2, '*':1, '/':1, '+':0, '-':0}
ops = {'^', '*', '/', '+', '-'}
nums = {'0','1','2','3','4','5','6','7','8','9'}
# 0 => Start State (Accepts open bracket, number, X, negative sign) 
# 1 => Building a Number
# 2 => Got an Operator
# 3 => Got X
# 4 => Got decimal point (Accepts only a number)
# 5 => State Following state 4 similar to state 1 but doesn't accept decimal point
# 6 => Dummy state to transform 2X to 2*X goes directly to state 3
# 7 => e state similar to state 3 but can accept an X
def validate(eqn:str,min,max) -> tuple[bool,str,str]:
    eqn_obj = []
    eqn_obj.append(eqn)
    valid, msg = validate_eqn(eqn_obj)
    if valid:
        valid, msg = validate_range(min,max)
    return valid, msg, eqn_obj[0]
def validate_range(min,max) -> tuple[bool,str]:
    valid = True
    msg = "Valid"
    # Check min
    valid, msg = validate_numeric(min,"min")
    # Check max
    if valid:
        valid, msg = validate_numeric(max,"max")
    # Check if min <= max
    if valid:
        min_val = float(min)
        max_val = float(max)
        if min_val >= max_val:
            valid = False
            msg = "Invalid range: min must be smaller than max" 
    return valid, msg
def validate_numeric(string,name) -> tuple[bool,str]:
    valid = False
    msg = "Invalid range: Invalid "+name+" value"
    if len(string) == 0:
        return False, "Invalid range: "+name+" is empty" 
    i = 0
    if string[0] == '-':
        i = 1
    point_flag = False
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
def validate_eqn(eqn_obj:list[str]) -> tuple[bool,str]:
    eqn = eqn_obj[0]
    if len(eqn) == 0:
        return False, "No Function is provided"
    bracket_stack = list()
    state = 0
    i=0
    while i < len(eqn):
        if state == 6:
            eqn = eqn[:i] + '*' + eqn[i:]
            eqn_obj[0] = eqn
            i+=2
            state = 3
            continue
        char = eqn[i]
        if char=='X':
            match state:
                case 0:
                    state = 3
                case 1:
                    state = 6
                    continue
                case 2:
                    state = 3
                case 5:
                    state = 6
                    continue
                case 7:
                    state = 6
                    continue
                case _:
                    return False, "Invalid syntax near " + char
        elif char=='e':
            match state:
                case 0:
                    state = 7
                case 1:
                    state = 7
                case 2:
                    state = 7
                case 5:
                    state = 7
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
                case 7:
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
            if state == 1 or state == 3 or state == 5 or state == 7:
                state = 3
            else:
                return False, "Invalid syntax near " + char
        else:
            return False, "Unexpected character " + char
        i+=1
    if len(bracket_stack) > 0:
        return False, "Unbalanced brackets"
    if state == 2 or state == 4:
        return False, "Invalid syntax near " + eqn[-1]
    return True, "Valid"