import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

df=pd.read_csv('student_perform.csv')

#EDA
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
df['Extra Activities']=le.fit_transform(df['Extra Activities'])
df['Parental Education']=le.fit_transform(df['Parental Education'])
df['Result (Pass/Fail)']=le.fit_transform(df['Result (Pass/Fail)'])

#train test split
from sklearn.model_selection import train_test_split
X=df.drop('Result (Pass/Fail)',axis=1)
y=df['Result (Pass/Fail)']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

#modelfitting
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
model=LogisticRegression()
model.fit(X_train,y_train)

#brain for the model
joblib.dump(model,'student_perform.pkl')