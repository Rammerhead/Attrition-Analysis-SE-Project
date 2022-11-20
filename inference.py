import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
from sklearn import preprocessing
from IPython.display import Image
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, roc_auc_score
from subprocess import call
from IPython.display import Image 
import pickle
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
#%matplotlib inline 
#%config InlineBackend.figure_format = 'retina' 
pd.set_option('display.max_columns', None) 
warnings.filterwarnings('ignore')


def dt(data):
    df = data
    st.dataframe(df.head())

    st.write("""By overview of data set, it can be found that this data set includes {} observations and {} features.\n 
    But features 'Over18', 'EmployeeCount' and 'StandardHours' are exactly same in every rows and 'EmployeeNumber' is the number that tag employees so we decide to drop these columns.""".format(df.shape[0],df.shape[1]))

    df = df.drop(columns=['Over18', 'EmployeeCount', 'StandardHours', 'EmployeeNumber'])

    st.write("Next, we move on to converting some categorical data to numeric by encoding the labels")

    education_map = {1: 'Below College', 2: 'College', 3: 'Bachelor', 4: 'Master', 5: 'Doctor'}
    education_satisfaction_map = {1: 'Low', 2:'Medium', 3:'High', 4:'Very High'}
    job_involvement_map = {1: 'Low', 2:'Medium', 3:'High', 4:'Very High'}
    job_satisfaction_map = {1: 'Low', 2:'Medium', 3:'High', 4:'Very High'}
    performance_rating_map = {1: 'Low', 2: 'Good', 3: 'Excellent', 4: 'Outstanding'}
    relationship_satisfaction_map = {1: 'Low', 2:'Medium', 3:'High', 4:'Very High'}
    work_life_balance_map = {1: 'Bad', 2: 'Good', 3: 'Better', 4: 'Best'}
    st.write("Use the pandas apply method to numerically encode our attrition target variable")
    df['Education'] = df["Education"].apply(lambda x: education_map[x])
    df['EnvironmentSatisfaction'] = df["EnvironmentSatisfaction"].apply(lambda x: education_satisfaction_map[x])
    df['JobInvolvement'] = df["JobInvolvement"].apply(lambda x: job_involvement_map[x])
    df['JobSatisfaction'] = df["JobSatisfaction"].apply(lambda x: job_satisfaction_map[x])
    df['PerformanceRating'] = df["PerformanceRating"].apply(lambda x: performance_rating_map[x])
    df['RelationshipSatisfaction'] = df["RelationshipSatisfaction"].apply(lambda x: relationship_satisfaction_map[x])
    df['WorkLifeBalance'] = df["WorkLifeBalance"].apply(lambda x: work_life_balance_map[x])

    st.dataframe(df.head())

    st.write("Missing Value:", df.isnull().any().any())

    st.write("The dataset is found to have no missing values")

    st.write("Preprocessing -")
    #------------------

    st.write("Reload the data")
    df = pd.read_csv("./attrition_data.csv")
    df = df.drop(columns=['Over18', 'EmployeeCount', 'StandardHours', 'EmployeeNumber'])

    for cate_features in df.select_dtypes(include='object').columns:
        le = preprocessing.LabelEncoder()
        df[cate_features] = le.fit_transform(df[cate_features])
        st.write("Origin Classes:", list(le.classes_))

    dummies = ['Department', 'EducationField', 'JobRole', 'MaritalStatus']
    df = pd.get_dummies(data=df, columns=dummies)
    st.dataframe(df.head())

    st.write("Scaling numerical features as the values can be of varying range -")


    numerical_list = ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 'MonthlyIncome', 'MonthlyRate',
                    'NumCompaniesWorked', 'PercentSalaryHike', 'TotalWorkingYears', 'TrainingTimesLastYear',
                    'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']

    plt.figure(figsize=(10, 10))
    for i, column in enumerate(numerical_list, 1):
        plt.subplot(5, 3, i)
        sns.distplot(df[column], bins=20)
    plt.tight_layout()
    st.pyplot(plt)

    std = preprocessing.StandardScaler()
    scaled = std.fit_transform(df[numerical_list])
    scaled = pd.DataFrame(scaled, columns=numerical_list)
    for i in numerical_list:
        df[i] = scaled[i]
    st.dataframe(df.head())

    st.write("split the data set into training set and test set with ratio 8:2")

    def my_confusion_matrix(test, test_pred):
        cf = pd.DataFrame(confusion_matrix(test, test_pred), 
                        columns=['Predicted No', 'Predicted Yes'], 
                        index=['True No', 'True Yes'])
        report = pd.DataFrame(classification_report(test, test_pred, target_names=['No', 'Yes'], 
                                                            output_dict=True)).round(2).transpose()
        st.dataframe(cf)
        st.dataframe(report)

    def plot_roc_curve(model, y, x):
        tree_auc = roc_auc_score(y, model.predict(x))
        fpr, tpr, thresholds = roc_curve(y, model.predict_proba(x)[:,1])
        plt.figure(figsize=(15, 10))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='Decision Tree ROC curve (area = %0.2f)' % tree_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.fill_between(fpr, tpr, color='orange', alpha=0.2)
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")

    #st.write("Decision Tree")


    X = df.drop(columns=['Attrition'])
    y = df['Attrition']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    params = {"criterion": ("gini", "entropy"), 
            "splitter": ("best", "random"), 
            "max_depth": np.arange(1, 20), 
            "min_samples_split": [2, 3, 4], 
            "min_samples_leaf": np.arange(1, 20)}
    tree1_grid = GridSearchCV(DecisionTreeClassifier(random_state=0), params, scoring="roc_auc", n_jobs=-1, cv=5)
    tree1_grid.fit(X_train, y_train)

    st.write("Tree grid best score:", tree1_grid.best_score_)
    st.write("Tree grid best parameters:", tree1_grid.best_params_)
    st.write("Tree grid best estimator:", tree1_grid.best_estimator_)

    tree1_clf = DecisionTreeClassifier(random_state=0, **tree1_grid.best_params_)
    tree1_clf.fit(X_train, y_train)
    tree.export_graphviz(tree1_clf, out_file='tree1.dot', special_characters=True, rounded = True, filled= True,
                        feature_names=X.columns, class_names=['Yes', 'No'])
    call(['dot', '-T', 'png', 'tree1.dot', '-o', 'tree1.png'], shell = True)

    # st.image("tree1.png")

    y_test_pred_tree1 = tree1_clf.predict(X_test)
    my_confusion_matrix(y_test, y_test_pred_tree1) # Defined before
    tree1_auc = roc_auc_score(y_test, y_test_pred_tree1)
    st.write("AUC:", tree1_auc)

    st.write("Importance of Features")

    IP = pd.DataFrame({"Features": np.array(X.columns), "Importance": tree1_clf.feature_importances_})
    IP = IP.sort_values(by=['Importance'], ascending=False)
    plt.figure(figsize=(15, 10))
    sns.barplot(x='Importance', y='Features', data=IP[:10])
    st.pyplot(plt)

    st.write("ROC curve")

    plot_roc_curve(tree1_clf, y_test, X_test)
    st.pyplot(plt)

    st.write("Saving the Decision Tree model")

    import pickle

    m = tree1_grid.best_estimator_

    filename = './decisiontree1.pkl'
    pickle.dump(m, open(filename, 'wb'))


    test = pd.read_csv("./test_data.csv")

    dt = open('./decisiontree1.pkl', "rb")

    m = pickle.load(dt)


