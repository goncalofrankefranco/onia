import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x = []
x1 = []
for i in range(1,101):
    x.append(i)
y = x.copy()
x1 = x.copy()
for i in x:
    x[i - 1] = x[i - 1] ** 2
    x1[i - 1] = ((x1[i - 1] ** 3)/10) + 100

"""
plt.title("Gráfico BTS")
plt.ylabel("Retorno (MM)")
plt.xlabel("Tempo (Anos)")
plt.grid()
plt.plot(y, x)
plt.plot(y, x1)
plt.show()
"""


# Bar Chart:
categories = ["Grains", "Fruit", "Vegetables", "Protein", "Dairy", "Sweets"]
values = [4, 3, 2, 5, 3, 1]
colors = ["red", "blue", "green", "yellow", "orange", "cyan"]

"""
plt.bar(categories, values, color="red")
#plt.barh(categories, values)
plt.show()
"""

# Pie Chart:
"""
plt.pie(values, labels=categories,
                autopct="%1.1f%%",
                colors=colors,
                explode=[0, 0, 0, 0, 0, 0.3])
plt.show()
"""

# Scatter Graph:
"""
plt.scatter(x, y, color="red")
plt.scatter(x1, y, color="skyblue")
plt.show()
"""

# Histogram Graphs:
scores = np.random.normal(loc=80, scale=10, size=10000)
scores = np.clip(scores, 0, 100)
"""
plt.hist(scores, bins=100,
                 color="skyblue",
                 edgecolor="white")
plt.show()
"""

# Subplots:
""""
figure, axes = plt.subplots(2)
#figure, axes = plt.subplots(2, 2)

axes[0].hist(scores)
axes[0].set_title("Histograma")
axes[1].plot(values)
axes[1].set_title("Gráfico")
plt.show()
"""

# Pandas:
df = pd.read_csv("Data/pokemon.csv")
type_count = df["Type 1"].value_counts()

plt.pie(type_count.values, labels=type_count.index)
plt.show()