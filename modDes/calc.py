import sympy as sp

# Define the variable and the function
x = sp.symbols('x')
f = (16 * (1 + x)**2 - 16) / (1 + x - 1)

# Compute the limit as x approaches 1
limit_value = sp.limit(f, x, 0)

# Display the result
print(limit_value)