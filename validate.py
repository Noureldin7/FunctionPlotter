from function_parser import nums, ops
nums = nums.difference({'.'})
# 0 => Start State (Accepts open bracket, number, e, X, negative sign) 
# 1 => Building a Number
# 2 => Got an Operator
# 3 => Got X or )
# 4 => Got decimal point (Accepts only a number)
# 5 => State following state 4 similar to state 1 but doesn't accept decimal point
# 6 => e state similar to state 3 but can accept an X
def validate(eqn:str,min,max) -> tuple[bool,str,str]:
    '''Validates the given equation and range'''
    eqn_obj = []
    eqn_obj.append(eqn)
    valid, msg = validate_eqn(eqn_obj)
    if valid:
        valid, msg = validate_range(min,max)
    return valid, msg, eqn_obj[0]
def validate_range(min,max) -> tuple[bool,str]:
    '''Validates the range'''
    valid = True
    msg = "Valid"
    # Check if min is numeric
    valid, msg = validate_numeric(min,"Min")
    # Check if max is numeric
    if valid:
        valid, msg = validate_numeric(max,"Max")
    # Check if min < max
    if valid:
        min_val = float(min)
        max_val = float(max)
        if min_val >= max_val:
            valid = False
            msg = "Min must be smaller than Max" 
    return valid, msg
def validate_numeric(string,name) -> tuple[bool,str]:
    '''Validates if the given string is a valid numeric value'''
    valid = False
    msg = "Invalid "+name+" value"
    if len(string) == 0:
        return False, name+" is empty" 
    i = 0
    # Negative sign is allowed only at the beginning
    if string[0] == '-':
        i = 1
    point_flag = False
    while i < len(string):
        # Only 1 "." is allowed in the string
        if string[i] == '.':
            if point_flag:
                valid = False
                msg = "Unexpected decimal point in "+name+" value"
                break 
            else:
                point_flag = True
        elif string[i] == '-':
            valid = False
            msg = "Unexpected negative sign in "+name+" value"
            break  
        else:
            # At least 1 number is required (.1 => 0.1, 1. => 1.0)
            valid = True
            msg = "Valid"
        i+=1
    return valid,msg
def inject_mul(i,eqn_obj:list[str]):
    '''Splits the string at the given index and injects a multiplication operator'''
    eqn_obj[0] = eqn_obj[0][:i] + '*' + eqn_obj[0][i:]
    return i+1, eqn_obj[0]
def validate_eqn(eqn_obj:list[str]) -> tuple[bool,str]:
    '''Validates the given equation by tracing a finite state machine'''
    eqn = eqn_obj[0]
    if len(eqn) == 0:
        return False, "No Function is provided"
    bracket_stack = list()
    state = 0
    i=0
    while i < len(eqn):
        char = eqn[i]
        if char=='X':
            match state:
                case 0:
                    state = 3
                case 1:
                    state = 3
                    i, eqn = inject_mul(i,eqn_obj)
                case 2:
                    state = 3
                case 5:
                    state = 3
                    i, eqn = inject_mul(i,eqn_obj)
                case 6:
                    state = 3
                    i, eqn = inject_mul(i,eqn_obj)
                case _:
                    return False, "Invalid syntax near " + char
        elif char=='e':
            match state:
                case 0:
                    state = 6
                case 1:
                    state = 6
                    i, eqn = inject_mul(i,eqn_obj)
                case 2:
                    state = 6
                case 5:
                    state = 6
                    i, eqn = inject_mul(i,eqn_obj)
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
                case 6:
                    state = 2
                case _:
                    return False, "Invalid syntax near " + char
        elif char == '(':
            bracket_stack.append(char)
            match state:
                case 0:
                    state = 0
                case 1:
                    state = 0
                    i = inject_mul(i,eqn_obj)
                case 2:
                    state = 0
                case 3:
                    state = 0
                    i = inject_mul(i,eqn_obj)
                case 5:
                    state = 0
                    i = inject_mul(i,eqn_obj)
                case 6:
                    state = 0
                    i = inject_mul(i,eqn_obj)
                case _:
                    return False, "Invalid syntax near " + char
        elif char == ')':
            if len(bracket_stack) == 0:
                return False, "Unbalanced brackets"
            bracket_stack.pop()
            match state:
                case 1:
                    state = 3
                case 3:
                    state = 3
                case 5:
                    state = 3
                case 6:
                    state = 3
                case _:
                    return False, "Invalid syntax near " + char
        else:
            return False, "Unexpected character " + char
        i+=1
    if len(bracket_stack) > 0:
        return False, "Unbalanced brackets"
    if state == 2 or state == 4:
        return False, "Invalid syntax near " + eqn[-1]
    return True, "Valid"