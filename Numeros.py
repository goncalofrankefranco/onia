import numpy as np
"""
array = np.array([1, 2, 3, 4])
#array[row, column] Can be combined!
array *= 2
print(array)
print(array.ndim)
print(array + 1)
print(np.sqrt(array))

array1 = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print(array1.shape)
print(array1[:, 2:4])

array2 = np.array([2.5, 3.99, 1.2])
print(np.round(array2))

# BROADCASTING: Multiplies array to match another array's size. N. == N. | N. == 1
array3 = np.array([[1, 2, 3, 4]])
array4 = np.array([[1], [2], [3], [4]])
print(array3.shape)
print(array4.shape)
print(array3 * array4)

# FILTERING: Like pandas, expect for this:
array5 = np.array([[20, 56, 14, 23, 24, 26], [98, 40, 67, 19, 21, 27]])
print(np.where(array5 > 20, array5, np.nan))

# RNG
rng = np.random.default_rng(seed=42)
print(rng.integers(1, 7, (3, 2)))
"""