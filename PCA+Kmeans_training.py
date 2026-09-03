import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

data = pd.read_csv("Data/Country-data.csv", index_col="country")
data = data.drop('health', axis=1)
#print((data == 0).sum()) # Data is clean

scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

X_reduced = PCA(n_components=3).fit_transform(X_scaled)
#print(X_reduced.shape) # (167, 3)

kmeans = KMeans(n_clusters=10, random_state=42)
clusters = kmeans.fit_predict(X_reduced)
data['Cluster'] = clusters



fig = plt.figure(1, figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d", elev=-150, azim=110)
scatter = ax.scatter(
    X_reduced[:, 0],
    X_reduced[:, 1],
    X_reduced[:, 2],
    c=clusters,
    s=40,
)

ax.set(
    title="First three principal components",
    xlabel="1st Principal Component",
    ylabel="2nd Principal Component",
    zlabel="3rd Principal Component",
)
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])
ax.zaxis.set_ticklabels([])

handles, labels = scatter.legend_elements()

legend1 = ax.legend(
    handles,
    labels,
    loc="upper right",
    title="Classes",
)
ax.add_artist(legend1)

print(data.groupby('Cluster').mean().to_string())
print(data[(data['Cluster'] == 2) | (data['Cluster'] == 7)])
plt.show()


