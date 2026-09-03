import pandas as pd
from numpy import nan
#import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

def model(first, last, type):
    if type == "train-test-split":
        model_train_test_split(*data_processing(first, last))
    elif type == "cross-validation":
        model_cross_validation(*data_processing(first, last))
    else:
        print("Please enter either 'train-test-split' or 'cross-validation'")

def data_processing(first_collumn, last_collumn):
    # Make data
    data = pd.read_csv('Data/diabetes.csv')
    si = SimpleImputer(missing_values=nan, strategy='mean')
    X = data.iloc[:, first_collumn:last_collumn]  # iloc[row_slicing, column_slicing]
    y = data.iloc[:, 8]

    invalid_zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction']
    active_cols = [col for col in invalid_zero_cols if col in X.columns]
    X[active_cols] = X[active_cols].replace({0: nan})
    return [si, X, y]

def model_train_test_split(si, X, y):
    x_training, x_test, y_training, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

    x_training = si.fit_transform(x_training)
    x_training = StandardScaler().fit_transform(x_training)
    x_test = si.transform(x_test)
    x_test = StandardScaler().fit_transform(x_test)
    k_values = range(5, 50)
    f1_best = 0
    k_best = 0
    for k in k_values:
        model = KNeighborsClassifier(n_neighbors=k, p=2, metric='minkowski')
        model.fit(x_training, y_training)
        prediction = model.predict(x_training)
        answer = model.predict(x_test)
        f1 = (f1_score(y_training, prediction) + f1_score(y_test, answer))/2
        if f1 > f1_best:
            f1_best = f1
            k_best = k

    model = KNeighborsClassifier(n_neighbors=k_best, p=2, metric='minkowski')
    model.fit(x_training, y_training)
    prediction = model.predict(x_training)
    answer = model.predict(x_test)

    print(f"k = {k_best}")
    print(f" Accuracy Train Score: {accuracy_score(y_training, prediction)}")
    print(f"Precision Train Score: {precision_score(y_training, prediction)}")
    print(f"Recall Train Score: {recall_score(y_training, prediction)}")
    print(f" F1 Train Score: {f1_score(y_training, prediction)}")
    print(f"Confusion Train Score: {confusion_matrix(y_training, prediction)}")
    print(f" Accuracy Test Score: {accuracy_score(y_test, answer)}")
    print(f"Precision Test Score: {precision_score(y_test, answer)}")
    print(f"Recall Test Score: {recall_score(y_test, answer)}")
    print(f" F1 Test Score: {f1_score(y_test, answer)}")
    print(f"Confusion Test Score: {confusion_matrix(y_test, answer)}")

def model_cross_validation(si, X, y):
    kf = KFold(n_splits=10, random_state=42, shuffle=True)
    f1_best_of_the_best = 0

    for training, test in kf.split(X):
        x_training = X.iloc[training]
        x_test = X.iloc[test]
        y_training = y.iloc[training]
        y_test = y.iloc[test]
        x_training = si.fit_transform(x_training)
        x_training = StandardScaler().fit_transform(x_training)
        x_test = si.transform(x_test)
        x_test = StandardScaler().fit_transform(x_test)
        k_values = range(5, 50)
        f1_best = 0
        k_best = 0
        for k in k_values:
            model = KNeighborsClassifier(n_neighbors=k, p=2, metric='minkowski')
            model.fit(x_training, y_training)
            prediction = model.predict(x_training)
            answer = model.predict(x_test)
            f1 = (f1_score(y_training, prediction) + f1_score(y_test, answer)) / 2
            if f1 > f1_best:
                f1_best = f1
                k_best = k

        model = KNeighborsClassifier(n_neighbors=k_best, p=2, metric='minkowski')
        model.fit(x_training, y_training)
        prediction = model.predict(x_training)
        answer = model.predict(x_test)
        if f1_best > f1_best_of_the_best:
            f1_best_of_the_best = f1_best

    print(f"f = {f1_best_of_the_best}")
    print(f"k = {k_best}")
    print(f" Accuracy Train Score: {accuracy_score(y_training, prediction)}")
    print(f"Precision Train Score: {precision_score(y_training, prediction)}")
    print(f"Recall Train Score: {recall_score(y_training, prediction)}")
    print(f" F1 Train Score: {f1_score(y_training, prediction)}")
    print(f"Confusion Train Score: {confusion_matrix(y_training, prediction)}")
    print(f" Accuracy Test Score: {accuracy_score(y_test, answer)}")
    print(f"Precision Test Score: {precision_score(y_test, answer)}")
    print(f"Recall Test Score: {recall_score(y_test, answer)}")
    print(f" F1 Test Score: {f1_score(y_test, answer)}")
    print(f"Confusion Test Score: {confusion_matrix(y_test, answer)}")

model(
    int(input("Enter first column: ")),
    int(input("Enter last column: ")),
    input("Enter the model type: "))