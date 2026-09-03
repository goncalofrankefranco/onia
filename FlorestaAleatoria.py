import pandas as pd
from numpy import nan
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV

data = pd.read_csv('Data/diabetes.csv')
X = data.iloc[:, 0:8]
change_columns = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction"]
X[change_columns] = X[change_columns].replace({0:nan})
y = data.iloc[:, 8]

X_training, X_test, y_training, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, shuffle = True)
imputer = SimpleImputer(missing_values = nan, strategy = 'mean') # Create the variable to apply sequentially
X_training = imputer.fit_transform(X_training)
X_test = imputer.transform(X_test)

param_grid = [{'max_depth' : [4, 6, 8, None],
               'min_samples_leaf' : [2, 4, 6],
               'min_samples_split' : [2, 4, 6],
               'class_weight' : ['balanced', 'balanced_subsample', None]}]

model = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='f1', n_jobs=-1)
grid_search.fit(X_training, y_training)
best_model = grid_search.best_estimator_
prediction = best_model.predict(X_training)
answer = best_model.predict(X_test)

print("TRAINING:")
print(f"Accuracy: {accuracy_score(y_training, prediction)*100}%")
print(f"Precision: {precision_score(y_training, prediction)*100}%")
print(f"Recall: {recall_score(y_training, prediction)*100}%")
print(f"F1: {f1_score(y_training, prediction)*100}%")
print(f"Confusion Matrix: {confusion_matrix(y_training, prediction)}\n")
print("TEST:")
print(f"Accuracy: {accuracy_score(y_test, answer)*100}%")
print(f"Precision: {precision_score(y_test, answer)*100}%")
print(f"Recall: {recall_score(y_test, answer)*100}%")
print(f"F1: {f1_score(y_test, answer)*100}%")
print(f"Confusion Matrix: {confusion_matrix(y_test, answer)}")
