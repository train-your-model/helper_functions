# Imports
import numpy as np

# Handle Missing Values (Integer)
# Handle Missing Values (Object)

# Pearson Correlation - Numpy
def pearson_corr(x,y):
    """
    Function to determine the correlation between 2 1-D variables.
    Checks for Linear Relationship for assumed Normal Distribution of the variables.
    """
    r = np.corrcoef(x,y)
    r_value = r[0][1]

    if r_value == 0:
        print("NO Correlation")
    elif (r_value == 1) | (r_value == -1):
        print(f'PERFECT Correlation Exists - {r_value}')
    elif (0<r_value<1) | (-1<r_value<0):
        print(f'Correlation Exists - {r_value}')
