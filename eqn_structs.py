from abc import abstractmethod, ABC
import math
class parse_tree_node(ABC):
    def __init__(self,type):
        self.type = type
        '''0: Numeric Constant\n1: Operator\n2: x\n3: e'''
    @abstractmethod
    def calc(self, x):
        '''Calculates the value of the node given x'''
        pass
class expression(parse_tree_node):
    '''Non-terminal Node'''
    def __init__(self,node_list:list[parse_tree_node]):
        super().__init__(4)
        self.node_list = node_list
        '''Children Nodes'''
    def calc(self, x):
        i = 1
        left_op = self.node_list[0]
        # Set Result to first operand
        result = left_op.calc(x)
        if len(self.node_list) == 1:
            return result
        # If first symbol is negative, negate the following operand and set result to it
        if result=='-':
            result = -self.node_list[i].calc(x)
            i+=1
        # Accumulate the following operands on the result based on the operator
        while i<len(self.node_list):
            # Get operator
            op = self.node_list[i].calc(x)
            i+=1
            # Get operand
            right_op = self.node_list[i].calc(x)
            # Update result based on operator
            match op:
                case '^':
                    try:
                        result = math.pow(result,right_op)
                    except:
                        # Negative base with a non-integer exponent
                        result = float("inf")
                case '*':
                    result *= right_op
                case '/':
                    if right_op==0:
                        # Division by zero
                        result = float("inf")
                    else:
                        result /= right_op
                case '+':
                    result += right_op
                case '-':
                    result -= right_op
            i+=1
        return result
class symbol(parse_tree_node):
    '''Terminal Node'''
    def __init__(self, type, value):
        super().__init__(type)
        self.value = value
        '''Value of leaf node'''
    def calc(self, x):
        '''Returns the suitable value based on the node type'''
        if self.type==0:
            return float(self.value)
        elif self.type==1:
            return self.value
        elif self.type==2:
            return x
        elif self.type==3:
            return math.e