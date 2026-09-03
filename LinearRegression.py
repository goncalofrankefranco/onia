from pandas import DataFrame, read_csv
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

data = read_csv("Data/Student_Performance.csv")
X = data.iloc[:, 0:5]
X['Does Extracurricular Activities'] = X['Does Extracurricular Activities'].replace({'Yes':1, 'No':0})
y = data["Performance"]

X_training, X_test, y_training, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, shuffle = True)
model = LinearRegression()
model.fit(X_training, y_training)
prediction = model.predict(X_training)
answer = model.predict(X_test)

print("TRAINING:")
print(f"R2 Score: {r2_score(y_training, prediction)}\n")
print("TEST:")
print(f"R2 Score: {r2_score(y_test, answer)}")

while True:
    X_live = []
    print("\nLIVE:")
    for column in X.columns:
        X_live.append(int(input(f"Enter {column}: ")))
    X_live = DataFrame([X_live], columns = X.columns)
    print(f"Grade: {model.predict(X_live)}")