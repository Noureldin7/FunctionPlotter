import math
class expression:
    def __init__(self,expr_list:list):
        self.expr_list = expr_list
        self.type = 3
    def calc(self, x):
        i = 1
        left_op = self.expr_list[0]
        ans = left_op.calc(x)
        if len(self.expr_list) == 1:
            return ans
        if ans=='-':
            ans = -self.expr_list[i].calc(x)
            i+=1
        while i<len(self.expr_list):
            op = self.expr_list[i].calc(x)
            i+=1
            right_op = self.expr_list[i].calc(x)
            match op:
                case '^':
                    ans = ans ** right_op
                case '*':
                    ans *= right_op
                case '/':
                    ans /= right_op
                case '+':
                    ans += right_op
                case '-':
                    ans -= right_op
            i+=1
        return ans
class symbol:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def calc(self, x):
        if self.type==0:
            return float(self.value)
        elif self.type==1:
            return self.value
        elif self.type==2:
            return x
        elif self.type==3:
            return math.e