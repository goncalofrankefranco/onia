import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

data = pd.read_csv('Data/Social_Network_Ads.csv')
data = data.drop(['User ID'], axis=1)
data = data.replace({
    "Male":0,
    "Female":1
})

X = data.iloc[:, :3]
y = data.iloc[:, 3:].values
scaler = StandardScaler()

pipeline = make_pipeline(scaler, LogisticRegression())
print(cross_val_score(pipeline, X, y).mean())