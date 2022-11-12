import streamlit as st
import sqlite3
import pandas as pd

#Dtabase Management
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT, password TEXT)')


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
    task = st.selectbox("Task", ["Analytics", "Profile","Form"])
    user_result = view_all_users()
    clean_db = pd.DataFrame(user_result, columns = ['Username', 'Password'])
    st.dataframe(clean_db)

    if task == "Analytics":
        st.subheader("Analytics")
    elif task == "Profile":
        st.subheader("User Profiles")
    elif task == "Form":
        st.subheader("Fill in the form")

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (login_user(st.session_state["username"], st.session_state["password"])):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False

    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("User not known or password incorrect")
        user_result = view_all_users()
        clean_db = pd.DataFrame(user_result, columns = ['Username', 'Password'])
        st.dataframe(clean_db)
        return False
    else:
        # Password correct.
        return True


def main():
    if (check_password()):
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
