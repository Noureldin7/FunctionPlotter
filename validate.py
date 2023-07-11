priority = {'^':2, '*':1, '/':1, '+':0, '-':0}
ops = {'^', '*', '/', '+', '-'}
nums = {'0','1','2','3','4','5','6','7','8','9'}
def validate(eqn:str,min,max):
    try:
        min_val = int(min)
        max_val = int(max)
        if min_val >= max_val:
            return False, "Invalid range"
    except:
        return False, "Invalid range"
    bracket_stack = list()
    state = 0
    for char in eqn:
        if char == '(':
            bracket_stack.append(char)
        elif char == ')':
            if len(bracket_stack) == 0:
                return False, "Unbalanced brackets"
            bracket_stack.pop()
        elif char=='X':
            match state:
                case 0:
                    state = 1
                case 2:
                    state = 4
                case _:
                    return False, "Invalid syntax near " + char
        elif char in nums:
            match state:
                case 0:
                    state = 1
                case 2:
                    state = 3
        elif char == '-' and state==0:
            state = 2
        elif char in ops:
            match state:
                case 1:
                    state = 2
                case 3:
                    state = 2
                case 4:
                    state = 2
                case _:
                    return False, "Invalid syntax near " + char
        elif char == '(':
            if state == 0 or state == 2:
                state = 0
            else:
                return False, "Invalid syntax near " + char
        elif char == ')':
            if state==3 or state==1 or state==4:
                state = 0
            else:
                return False, "Invalid syntax near " + char
        else:
            return False, "Unexpected character " + char
    if len(bracket_stack) > 0:
        return False, "Unbalanced brackets"
    if state == 2:
        return False, "Invalid syntax near " + eqn[-1]
    return True, "Valid"