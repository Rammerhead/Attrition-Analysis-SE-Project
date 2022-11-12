import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from IPython.display import Image
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
#%matplotlib inline 
#%config InlineBackend.figure_format = 'retina' 
pd.set_option('display.max_columns', None) 
warnings.filterwarnings('ignore')

df = pd.read_csv("attrition_data.csv")
st.dataframe(df.head())

def predict_ready(dframe):
    dframe = dframe.drop(columns=['Over18', 'EmployeeCount', 'StandardHours', 'EmployeeNumber'])
    for cate_features in dframe.select_dtypes(include='object').columns:
        le = preprocessing.LabelEncoder()
        dframe[cate_features] = le.fit_transform(dframe[cate_features])
        #st.write("Origin Classes:", list(le.classes_))

    dummies = ['Department', 'EducationField', 'JobRole', 'MaritalStatus']
    dframe = pd.get_dummies(data=dframe, columns=dummies)
    #st.dataframe(df.head())
    numerical_list = ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 'MonthlyIncome', 'MonthlyRate',
                  'NumCompaniesWorked', 'PercentSalaryHike', 'TotalWorkingYears', 'TrainingTimesLastYear',
                  'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']

    std = preprocessing.StandardScaler()
    scaled = std.fit_transform(dframe[numerical_list])
    scaled = pd.DataFrame(scaled, columns=numerical_list)
    for i in numerical_list:
        dframe[i] = scaled[i]
    std = preprocessing.StandardScaler()
    scaled = std.fit_transform(dframe[numerical_list])
    scaled = pd.DataFrame(scaled, columns=numerical_list)
    for i in numerical_list:
        dframe[i] = scaled[i]
    #st.dataframe(df.head())
    dframe = dframe.drop(columns=['Attrition'])
    return dframe



preprocessedData = predict_ready(df)
st.dataframe(preprocessedData.head())

file = open('decisiontree1.pkl', "rb")
dt = pickle.load(file)

results = dt.predict(preprocessedData)
#my_confusion_matrix(y_test, y_test_pred_tree1) # Defined before
#tree1_auc = roc_auc_score(y_test, y_test_pred_tree1)
#st.write("AUC:", tree1_auc)

res = list(results)
exit = res.count(1)
stay = res.count(0)
st.write('Number of employees predicted to be leaving the company:',exit)
st.write('Number of employees predicted to stay in the company:',stay)
st.write('Attrition rate = ', (exit / stay) * 100)
