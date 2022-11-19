#Importing Python Libraries
import streamlit as st
import pandas as pd
import warnings
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go


#-----------Sample call of the functions below-------------
# data = file_input()
#     if task == "Profile":
#         st.subheader("User Profiles")
#     elif task == "Analytics":
#         st.subheader("Analytics")
#         try:
#             plots(data)
#         except:
#             pass

def file_input():
    csvfile = st.file_uploader("Upload File", type={"csv"})
    df = None
    if csvfile is not None:
        df = pd.read_csv(csvfile)

        init_data = pd.read_csv("attrition_data.csv")

        if(set(df.columns) == set(init_data.columns)):
            st.write(df)
            return df
        else:
            st.warning("Data provided is not in specified format")
            return None

def barplot(data,var_select, x_no_numeric) :
    tmp1 = data[(data['Attrition'] != 0)]
    tmp2 = data[(data['Attrition'] == 0)]
    tmp3 = pd.DataFrame(pd.crosstab(data[var_select],data['Attrition']), )
    tmp3['Attr%'] = tmp3[1] / (tmp3[1] + tmp3[0]) * 100
    if x_no_numeric == True  : 
        tmp3 = tmp3.sort_values(1, ascending = False)

    color=['lightskyblue','gold' ]
    trace1 = go.Bar(
        x=tmp1[var_select].value_counts().keys().tolist(),
        y=tmp1[var_select].value_counts().values.tolist(),
        name='Yes_Attrition',opacity = 0.8, marker=dict(
        color='gold',
        line=dict(color='#000000',width=1)))

    
    trace2 = go.Bar(
        x=tmp2[var_select].value_counts().keys().tolist(),
        y=tmp2[var_select].value_counts().values.tolist(),
        name='No_Attrition', opacity = 0.8, marker=dict(
        color='lightskyblue',
        line=dict(color='#000000',width=1)))
    
    trace3 =  go.Scatter(   
        x=tmp3.index,
        y=tmp3['Attr%'],
        yaxis = 'y2',
        name='% Attrition', opacity = 0.6, marker=dict(
        color='black',
        line=dict(color='#000000',width=0.5
        )))

    layout = dict(title =  str(var_select),
              xaxis=dict(), 
              yaxis=dict(title= 'Count'), 
              yaxis2=dict(range= [-0, 75], 
                          overlaying= 'y', 
                          anchor= 'x', 
                          side= 'right',
                          zeroline=False,
                          showgrid= False, 
                          title= '% Attrition'
                         ))

    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    st.plotly_chart(fig)



#------------------PIE CHARTS--------------------------
def plot_pie(attrition, no_attrition,var_select) :
    
    colors = ['gold', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightgrey', 'orange', 'white', 'lightpink']
    trace1 = go.Pie(values  = attrition[var_select].value_counts().values.tolist(),
                    labels  = attrition[var_select].value_counts().keys().tolist(),
                    textfont=dict(size=15), opacity = 0.8,
                    hoverinfo = "label+percent+name",
                    domain  = dict(x = [0,.48]),
                    name    = "attrition employes",
                    marker  = dict(colors = colors, line = dict(width = 1.5)))
    trace2 = go.Pie(values  = no_attrition[var_select].value_counts().values.tolist(),
                    labels  = no_attrition[var_select].value_counts().keys().tolist(),
                    textfont=dict(size=15), opacity = 0.8,
                    hoverinfo = "label+percent+name",
                    marker  = dict(colors = colors, line = dict(width = 1.5)),
                    domain  = dict(x = [.52,1]),
                    name    = "Non attrition employes" )

    layout = go.Layout(dict(title = var_select + " distribution in employes attrition ",
                            annotations = [dict(text = "Yes_attrition",
                                                font = dict(size = 13),
                                                showarrow = False,
                                                x = .22, y = -0.1),
                                            dict(text = "No_attrition",
                                                font = dict(size = 13),
                                                showarrow = False,
                                                x = .8,y = -.1)]))
                                          

    fig  = go.Figure(data = [trace1,trace2],layout = layout)
    st.plotly_chart(fig)


def plots(data):
    #data = file_input()
    data.Attrition.replace(to_replace = dict(Yes = 1, No = 0), inplace = True)

    attrition = data[(data['Attrition'] != 0)]
    no_attrition = data[(data['Attrition'] == 0)]
    trace = go.Pie(labels = ['No_attrition', 'Yes_attrition'], values = data['Attrition'].value_counts(), 
               textfont=dict(size=15), opacity = 0.8,
               marker=dict(colors=['lightskyblue','gold'], 
                           line=dict(color='#000000', width=1.5)))

    layout = dict(title =  'Distribution of attrition variable')
           
    fig = dict(data = [trace], layout=layout)
    st.plotly_chart(fig)

    barplot(data,'DistanceFromHome', False)
    barplot(data,'NumCompaniesWorked',False)
    barplot(data,'PercentSalaryHike', False) 
    barplot(data,'TotalWorkingYears', False)
    barplot(data,'TrainingTimesLastYear',False)
    barplot(data,'YearsAtCompany', False)
    barplot(data,'YearsInCurrentRole', False)
    barplot(data,'YearsSinceLastPromotion', False)

    plot_pie(attrition,no_attrition,"Gender")
    plot_pie(attrition,no_attrition,'OverTime')
    plot_pie(attrition,no_attrition,'BusinessTravel')
    plot_pie(attrition,no_attrition,'JobRole')
    plot_pie(attrition,no_attrition,'Department') 
    plot_pie(attrition,no_attrition,'MaritalStatus') 
    plot_pie(attrition,no_attrition,'EducationField') 
    plot_pie(attrition,no_attrition,'Education')
    plot_pie(attrition,no_attrition,'EnvironmentSatisfaction')
    plot_pie(attrition,no_attrition,'JobInvolvement')
    plot_pie(attrition,no_attrition,'JobLevel')
    plot_pie(attrition,no_attrition,'JobSatisfaction')
    plot_pie(attrition,no_attrition,'PerformanceRating')
    plot_pie(attrition,no_attrition,'RelationshipSatisfaction')
    plot_pie(attrition,no_attrition,'StockOptionLevel')
    plot_pie(attrition,no_attrition,'WorkLifeBalance')