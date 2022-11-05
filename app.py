import streamlit as st
import sqlite3
import pandas as pd

#Dtabase Management
conn = sqlite3.connect('data.db')
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


def main():
    """Simple login feature"""
    st.title("Attrition Analysis")

    menu = ["Home", "Login", "Sign up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
    elif choice == "Login":
        st.subheader("Login")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        #if st.sidebar.checkbox("Login"):
        if st.sidebar.button("Login"):
            # if password == '12345':
            create_usertable()
            result = login_user(username, password)
            if result:

                st.success("Logged in as {}".format(username))

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
            
            else:
                st.warning("Incorrect Username/Password")
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result, columns = ['Username', 'Password'])
                st.dataframe(clean_db)


    elif choice == "Sign up":
        st.subheader("Create new Account")

        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
            add_userdata(new_user, new_password)
        if st.button("Clear"):
            clear_data()





if __name__ == '__main__':
    main()