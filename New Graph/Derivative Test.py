# import sympy 
from sympy import * 
  
x = symbols('x')
expr = cos(x)
print("Expression : {} ".format(expr))
   
# Use sympy.Derivative() method 
expr_diff = Derivative(expr, x)  
      
print("Derivative of expression with respect to x : {}".format(expr_diff))  
print("Value of the derivative : {} ".format(expr_diff.doit()))
