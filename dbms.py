import sqlite3
#Dtabase Management
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

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

def view_form_data():
    c.execute('SELECT * FROM formtable')

def clear_data():
    c.execute('DROP TABLE usertable')

view_form_data()
