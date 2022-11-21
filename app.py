import streamlit as st
import sqlite3
import pandas as pd
from analytics import *
from inference import *
from dbms import*

#Dtabase Management
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# Initializing global vars



def form():
    st.title("Employee Satisfaction Survey")
    st.subheader("This is a completely anonymous form. Your details will NOT be shared with the company")

    with st.form(key = "form1"):
        depname = st.text_input("Department Name", key='depname')

        overall = st.radio("How would you describe your overall level of job satisfaction?", ["Very Satisfied", "Somewhat Satisfied", "Neutral", "Somewhat dissatisfied", "Very dissatisfied"], key='overall')
        st.write('How would you rate the following:')

        salary = st.select_slider("Salary",                                     options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='salary')
        overallbenefits = st.select_slider("Overall Benefits",                  options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='overallbenefits')
        healthbenefits = st.select_slider("Health Benefits",                    options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='healthbenefits')
        physicalwork= st.select_slider("Physical Work Environment",             options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='physicalwork')
        seniorlead= st.select_slider("Senior Leadership",                       options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='seniorlead')
        indivmgmt= st.select_slider("Individual Management",                    options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='indivmgmt')
        perf_feedback= st.select_slider("Performance Feedback",                 options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='perf_feedback')
        emp_eval= st.select_slider("Employee Evaluations",                      options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='emp_eval')
        recognition= st.select_slider("Recognition",                            options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='recognition')
        training= st.select_slider("Training Opportunities",                    options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='training')
        advancement= st.select_slider("Opportunities for advancement",          options = ['Very Poor', 'Poor', 'Average', 'Good', 'Excellent'], key='advancement')
												
        
        valued = st.radio("Do you feel valued at work?", ["Yes", "No"], key='valued')
        reason1 = st.text_area("If no, would you please like to explain?", key='reason1')

        resources = st.radio("Do you have the resources you need to perform your job well?", ["Yes", "No"], key='resources')
        reason2 = st.text_area("If no, would you please like to elaborate", key='reason2')

        mentalhealth = st.radio("Does your job cause you stress or anxiety?", ["Yes", "No"], key='mentalhealth')
        reason3 = st.text_area("If yes, please explain", key='reason3')

        opinions = st.radio("Are sufficient efforts being made to solicit colleague opinions and feedback?", ["Yes", "No"], key='opinions')
        reason4 = st.text_area("If no, please elucidate", key='reason4')

        add_fb = st.text_area("Please provide any additional feedback", key='add_fb')
        submit_buttom = st.form_submit_button(label = 'Submit the Survey')



       

    if submit_buttom : 
        st.success("The survey has been submitted successfully!")
        if (st.session_state['valued'] == "Yes"):
            valued = 1
        else:
            valued = 0
        if (st.session_state['resources'] == "Yes"):
            resources = 1
        else:
            resources = 0
        if (st.session_state['mentalhealth'] == "Yes"):
            mentalhealth = 1
        else:
            mentalhealth = 0
        if (st.session_state['add_fb'] == "Yes"):
            add_fb = 1
        else:
            add_fb = 0
        c.execute("INSERT INTO FORMTABLE VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(st.session_state['depname'], st.session_state['overall'], st.session_state['salary'], st.session_state['overallbenefits'], st.session_state['healthbenefits'], st.session_state['physicalwork'], st.session_state['seniorlead'], st.session_state['indivmgmt'], st.session_state['perf_feedback'], st.session_state['emp_eval'], st.session_state['recognition'], st.session_state['training'], st.session_state['advancement'], valued, st.session_state['reason1'], resources, st.session_state['reason2'], mentalhealth, st.session_state['reason3'], st.session_state['opinions'], st.session_state['reason4'], add_fb))




def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT, password TEXT)')

def create_formtable():
    c.execute("CREATE TABLE IF NOT EXISTS FORMTABLE( depname VARCHAR(255), overall VARCHAR(255), salary VARCHAR(255), overallbenefits VARCHAR(255), healthbenefits VARCHAR(255), physicalwork VARCHAR(255), seniorlead VARCHAR(255), indivmgmt VARCHAR(255), perf_feedback VARCHAR(255), emp_eval VARCHAR(255), recognition VARCHAR(255), training VARCHAR(255), advancement VARCHAR(255), valued BOOLEAN, reason1 TEXT, resources BOOLEAN, reason2 TEXT, mentalhealth BOOLEAN, reason3 TEXT, opinions BOOLEAN, reason4 TEXT, add_fb TEXT);")


def add_userdata(username, password):
    c.execute('INSERT INTO usertable(username, password) VALUES (?,?)', (username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM usertable WHERE username= ? and password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data

def clear_data():
    c.execute('DROP TABLE usertable')

def logged_in():
    task = st.selectbox("Task", ["Analytics", "Inferences", "Feedback"], key="task")
    #user_result = view_all_users()
    #clean_db = pd.DataFrame(user_result, columns = ['Username', 'Password'])
    #st.dataframe(clean_db)
    data = file_input()

    if st.session_state['task'] == "Analytics":
        st.subheader("Analytics")
        try:
            plots(data)
        except:
            pass
    elif st.session_state['task'] == "Inferences":
        st.subheader("Inferences")
        try:
            dt(data)
        except:
            pass
    elif st.session_state['task'] == 'Feedback':
        st.subheader("Feedback")
        create_formtable()
        form()



    if (st.button("Log Out")):
        #task.empty()
        del task
        del data
        logout()
        st.experimental_rerun()

def logout():
    del st.session_state['task']
    del st.session_state['password_correct']
    del st.session_state['logged']

def login_attempt():
    st.session_state['login_attempt'] = True

def password_entered():
    """Checks whether a password entered by the user is correct."""
        
    if (login_user(st.session_state["username"], st.session_state["password"])):
        st.session_state["password_correct"] = True
        del st.session_state["password"]  # don't store username + password
        del st.session_state["username"]
    else:
        st.session_state["password_correct"] = False


#def check_password():

##def check_password():
##    """Returns `True` if the user had a correct password."""
##
##    def password_entered():
##        """Checks whether a password entered by the user is correct."""
##        if (login_user(st.session_state["username"], st.session_state["password"])):
##            st.session_state["password_correct"] = True
##            del st.session_state["password"]  # don't store username + password
##            del st.session_state["username"]
##        else:
##            st.session_state["password_correct"] = False
##
##    if "password_correct" not in st.session_state:
##        # First run, show inputs for username + password.
##        st.text_input("Username", key="username")
##        st.text_input("Password", type="password", key="password")
##        if (st.button("Log in", key="login_button")):
##            password_entered()
##        return False
##
##    if not st.session_state["password_correct"]:
##        # Password not correct, show input + error.
##        st.text_input("Username", key="username")
##        st.text_input("Password", type="password", key="password")
##        if (st.button("Log in", key="login_button")):
##            password_entered()
##        st.error("User not known or password incorrect")
##        user_result = view_all_users()
##        clean_db = pd.DataFrame(user_result, columns = ['Username', 'Password'])
##        st.dataframe(clean_db)
##
##    else:
##        # Password correct.
##        return True


def main():
    if ("logged" not in st.session_state):
        st.session_state['logged'] = False
    if (not st.session_state['logged']):
        user = st.empty()
        user.text_input("Username", key="username") 
        password = st.empty()
        password.text_input("Password", type="password", key="password")
        loginbutton = st.empty()
        loginbutton.button("Log In", key="login_button", on_click=login_attempt)
        if ('login_attempt' in st.session_state):
            password_entered()
            if (st.session_state['password_correct']):
                st.session_state['logged'] = True
                password.empty()
                user.empty()
                loginbutton.empty()
            else:
                st.error("User not known or password incorrect")
                #user_result = view_all_users()
                #clean_db = pd.DataFrame(user_result, columns = ['Username', 'Password'])
                #st.dataframe(clean_db)
            del st.session_state['login_attempt']
    if (st.session_state['logged'] == True):
        logged_in()





#def main_subfunction():
#    """Main subfunction: Provides login/signup interface
#       Return values: 1 <- user logged in
#                      -1 <- User could not log in"""
#    st.title("Attrition Analysis")
#
#    menu = ["Home", "Login", "Sign up"]
#    choice = st.sidebar.selectbox("Menu", menu)
#
#    if choice == "Home":
#        st.subheader("Home")
#    elif choice == "Login":
#        st.subheader("Login")
#
#        if (check_password()):
#            del choice
#            return True
#            
#        else:
#            st.warning("Incorrect Username/Password")
#            user_result = view_all_users()
#            clean_db = pd.DataFrame(user_result, columns = ['Username', 'Password'])
#            st.dataframe(clean_db)
#
#
#    elif choice == "Sign up":
#        st.subheader("Create new Account")
#
#        new_user = st.text_input("Username")
#        new_password = st.text_input("Password", type='password')
#
#        if st.button("Signup"):
#            st.success("You have successfully created a valid Account")
#            st.info("Go to Login Menu to login")
#            add_userdata(new_user, new_password)
#        if st.button("Clear"):
#            clear_data()
#




if __name__ == '__main__':
    main()
