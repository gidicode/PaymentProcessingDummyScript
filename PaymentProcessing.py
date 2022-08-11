import sqlite3
from sqlite3 import Error

def create_connection():
    connect_db = None

    try:
        connect_db = sqlite3.connect('Payment.db')        
        return connect_db
    except Error as e:
        print(e)    
    return connect_db

def create_table(connect_db, create_sql_table):
    try:
        c = connect_db.cursor()
        c.execute(create_sql_table)
    except Error as e:
        print('CREATE TABLE ERROR:', e)        

connect_db = create_connection()
def main():
    
    sql_create_users = """ CREATE TABLE IF NOT EXISTS allUsers (
                                        id integer PRIMARY KEY,                                       
                                        username text UNIQUE,
                                        first_name text,
                                        last_name text,
                                        login_status integer
                                    );"""

    sql_create_transactions_table = """ CREATE TABLE IF NOT EXISTS allTransactions (
                                        id integer PRIMARY KEY,                                       
                                        amount integer,
                                        confirmation_code integer,
                                        status text,
                                        processed_with text,
                                        type_of_payment text,
                                        users text,
                                        duration text
                                    );"""        

    if connect_db is not None:
        create_table(connect_db, sql_create_transactions_table)
        create_table(connect_db, sql_create_users)                
    else:
        print("Error!!")    

class Creating:

    def __init__(self, connect_db) -> None:        
        self.connect_db = connect_db
        self.cur = connect_db.cursor()
        self.data = None
        self.sql_insert = "INSERT INTO"        
        self.values = None
        self.table = None
        self.argument = None
        self.selectFrom = 'SELECT * FROM'

    #Handles all data creation
    def create(self):
        sql  = f'{self.sql_insert} {self.table} {self.argument} VALUES{self.values}'        
        try:
            self.cur.execute(sql, self.data)
            print('created sucessfully')
            self.connect_db.commit()        
        except Error as e:                    
            print('******** Error Occured **********', e)                
        return self.cur.lastrowid            

    def getUserData(self):
        try:
            self.cur.execute(f'{self.selectFrom} allUsers WHERE id = 1')
            row = self.cur.fetchall()
            user_data = {}
            for item in row:
                user_data['id'] = item[0]
                user_data['username'] = item[1]
                user_data['first_name'] = item[2]
                user_data['last_name'] = item[3]
                user_data['login_status'] = item[4]            
        except Error as e:
            print('********* Error Occured *********', e)
        return user_data    

    def transactionStatus(self, status):
        user_data = self.getUserData()
        users = user_data.get('username')        
        sql = f'{self.selectFrom} allTransactions WHERE status="{status}" AND users="{users}"'

        try:
            self.cur.execute(sql)
        except Error as e:
            print('****** Not Found *********', e)

        row  = self.cur.fetchall()        
        if row:
            for item in row:                
                data = {
                    'id': item[0], 
                    'amount': item[1], 
                    'confirmation code': item[2], 
                    'status': item[3], 
                    'processed with': item[4],
                    'type of payment': item[5], 
                    'users' : item[6],
                    'duration': item[7]
                    }
                print(data)        
        else:
            print('Query Not found')

    def createUser(self):             
        username = input('Enter Username: ')
        first_name = input('Enter First Name: ')
        last_name = input('Enter Last Name: ')
        self.table = 'allUsers'
        self.values = '(?,?,?)'
        self.argument = '(username, first_name, last_name)'
        self.data = (username, first_name, last_name)        
        return self.create()        

    def createTransaction(self, amount, username, p_with, t_payment):        
        self.amount = amount
        self.confirmation_code = 5555   
        self.status = 'paid'   
        self.processed_with = p_with
        self.type_of_payment = t_payment
        self.user = username
        self.duration = None
        self.table = 'allTransactions'
        self.values = '(?,?,?,?,?,?,?)'
        self.argument = '(amount, confirmation_code, status, processed_with, type_of_payment, users, duration)'
        self.data = (self.amount, self.confirmation_code, self.status, self.processed_with, self.type_of_payment, self.user, self.duration)                        
        self.create()                
        return self.processInvoice()
    
    def processInvoice(self):
        fname_lname = self.getUserData()
        print(f''' INVOICE         
        \n Name: {fname_lname.get('first_name'), fname_lname.get('last_name')} 
        \n Amount: {self.amount} 
        \n Processed With: {self.processed_with} 
        \n Payment Type: {self.type_of_payment} 
        \n Status: {self.status}''')
          
    def login(self):    
        print('Enter Username to login account')
        username = input('Enter username:  ')        
        user_data = self.getUserData()
        get_availableUser = user_data.get('username')    
        print(username, get_availableUser)

        if username == get_availableUser:                    
            sql = """ UPDATE allUsers SET login_status =1 WHERE id = 1"""
            self.cur.execute(sql)        
            self.connect_db.commit()
            
            check_status = self.getUserData()
            login_status = check_status.get('login_status')            
            if login_status == 1:
                print('Login Succesfull')
                startPortal()
            else:
                print('User not logged in')

        else:
            print(f''' ***Username Not correct pls try again***
            \n1) Select 1 to try again.
            \n2) Select 2 to close. 
            \n''')

            value = int(input('Enter number: '))        
            if value == 1: 
                startPortal() 
            else: 
                print('///Portal Closed///')

    def logout(self):        
        sql = """ UPDATE allUsers SET login_status = 0 WHERE id = 1"""
        self.cur.execute(sql)        
        self.connect_db.commit()  
        self.connect_db.close()    
 

def startPortal():
    #Getting class attributes
    p = Creating(connect_db)
    available_user = p.getUserData() 

    """For the purpose of this program we would only be dealing with one use user
        per login session, which means we cant register more than one person intp this database,        
    """
    #check to see if ther is a registered user            
    login_status = available_user.get('login_status')    

    if available_user and  login_status == False :        
        p.login()

    elif available_user and login_status == True:
        while login_status == True:

            print('''Welcome! \n
                Select Action \n
                1) Make Payment 
                2) Payment Status
                3) User Details
                4) Close'''
            )
                
            selected = int(input('Enter number: '))
            #Make Payment
            if selected == 1:        
                payment_type_option = {1: 'One time', 2: 'Subscription'}                
                payment_method_option = {1: 'Paypal', 2: 'Credit Card', 3:'Pay with bank'}
                print(''' Select Payment Type \n
                    1) Onetime Payment
                    2) Subscription payment'''
                )
                
                payment_type_selection = int(input('Enter Number: '))                                
                
                if payment_type_selection in payment_type_option.keys():
                    getting_type_option = payment_type_option.get(payment_type_selection)                    
                    print(''' One Time Payment: 
                        \n Please Select Payment method 
                        \n1) Paypal
                        \n2) Credit Card 
                        \n3) Pay with bank ''')
                    
                    payment_method_input = int(input('Enter Number: '))

                    if payment_method_input in payment_method_option.keys():
                        getting_pay_method_option = payment_method_option.get(payment_method_input)
                        get_username = available_user.get('username')   
                                                 
                        if payment_method_input == 3:
                            amount = int(input('Enter Amount: '))
                            print('''Make payment into this bank account: 
                            \n BANK NAME: XXXXXXXXXXX 
                            \n ACCOUNT NUMBER: XXXXXXXXX ''')
                            p.createTransaction(
                                amount, 
                                get_username, 
                                getting_pay_method_option, 
                                getting_type_option
                            )
                        elif payment_method_input == 1 or 2:
                            amount = int(input('Enter Amount: '))
                            input('CREDIT CARD NUMBER: ')
                            input('EXPIRY DATE (MM/YY): ')
                            input('CVV NUMBER: ')                            
                            p.createTransaction(
                                amount, 
                                get_username, 
                                getting_pay_method_option, 
                                getting_type_option
                            )
                        
                        else:
                            print('You choosed a wrong option')
                    
                    else:
                        print('*******Wrong option selected********')
                
                else:
                    print('*******Wrong option selected********')

            #Payment Status
            elif selected == 2:
                print('''Select Payment Status \n 
                    1) Pending  
                    2) Paid 
                    3) Canceled '''
                )
                status_option = {1: 'pending', 2: 'paid', 3:'canceled'}
                selection_input = int(input('Enter Number: '))

                if selection_input in range(1, 3):
                    get_status = status_option.get(selection_input)                                
                    p.transactionStatus(get_status)                                            

                else:
                    print('Wrong Selection Entered')     

            #User details
            elif selected == 3:
                print(F''' Profile Details 
                    FIRST NAME: {available_user.get('first_name')} 
                    LAST NAME: {available_user.get('last_name')} 
                    USERNAME: {available_user.get('username')} 
                    TOTAL PAID AMOUNT: {0}'''
                )

            elif selected == 4:
                print('Close Portal \n 1) Close \n 2) Logout')
                close_input = int(input('Enter Number: '))

                if close_input == 1:
                    login_status = False
                    print('Portal Closed')

                elif close_input == 2:
                    print('Logging you out')
                    login_status = False
                    p.logout()
                    print('Logged out succesfully')

            else: 
                print('The option you selected is incorrect')                
                
    else:
        p.createUser()        
  
if __name__ == '__main__':        
    main()
    startPortal()