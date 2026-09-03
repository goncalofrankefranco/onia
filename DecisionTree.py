import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split

# Setup
data = pd.read_csv("Data/pokemon.csv", index_col="Name")
filtered_data = data[(data["Type 1"] == "Grass") | (data["Type 1"] == "Electric")]
filtered_data = filtered_data.drop(columns=["Type 2", "Total", "Generation", "Legendary"])
X = filtered_data[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]]
Y = filtered_data["Type 1"] == "Electric"

# Split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
                                                    test_size=0.2,
                                                    random_state=42)


# Decision Tree
max_depth = 2
tree = DecisionTreeClassifier(max_depth=max_depth).fit(X_train, Y_train)

# Run
plot_tree(tree, feature_names=["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"], class_names=["Grass", "Electric"])
plt.show()

# Predict
prediction = tree.predict(X_train)
answer = tree.predict(X_test)
print(f"Max Depth: {max_depth}")
print(f"Accuracy Train Score: {accuracy_score(Y_train, prediction)}")
print(f"Precision Train Score: {precision_score(Y_train, prediction)}")
print(f"Recall Train Score: {recall_score(Y_train, prediction)}")
print(f"F1 Train Score: {f1_score(Y_train, prediction)}")
print(f"Accuracy Test Score: {accuracy_score(Y_test, answer)}")
print(f"Precision Test Score: {precision_score(Y_test, answer)}")
print(f"Recall Test Score: {recall_score(Y_test, answer)}")
print(f"F1 Test Score: {f1_score(Y_test, answer)}")