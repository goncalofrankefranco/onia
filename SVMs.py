import matplotlib.pyplot as plt
import pandas as pd
from seaborn import scatterplot
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.inspection import DecisionBoundaryDisplay


data = pd.read_csv('Data/cancer-data.csv', index_col="id")
#print((data == 0).sum()) # Data cleaned
data = data[data["concavity_mean"] != 0]
data = data.replace({
    "B":"Benign",
    "M":"Malignant",
})

X = data[["radius_mean", "texture_mean"]]
y = data.iloc[:, 0]#.astype(int) # Removes object type
scaler = StandardScaler()

model = make_pipeline(scaler, SVC(kernel="linear", random_state=42))
model.fit(X, y)
print(cross_val_score(model, X, y).mean())

fig, ax = plt.subplots(figsize=(10, 6))
DecisionBoundaryDisplay.from_estimator(model, X,
                                       response_method="predict",
                                       ax=ax)

scatterplot(
    data=X,
    x="radius_mean",
    y="texture_mean",
    hue=y.values,
    ax=ax
)

ax.set_title("SVM cancer detection malignancy")
ax.set_xlabel("Radius Mean")
ax.set_ylabel("Texture Mean")
plt.show()