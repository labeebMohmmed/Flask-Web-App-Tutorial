
import pyodbc
class genPreferences:
     def colNameQuery(self, table):          
          query = f"SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('" + table + "')"
          self.cursor.execute(query)                                             
          return self.cursor.fetchall()

getClass = genPreferences()

class AuthenticationsDB:
     def __init__(self):
            self.conn = pyodbc.connect('DRIVER={SQL Server};server=DESKTOP-KUPSRH8;DATABASE=AhwalDataBase;UID=SQLSerAdmin;PWD=sqlSER@jed80')
            self.cursor = self.conn.cursor()
   
     def getTodaysList(self, date): 
             #print(getClass.colNameQuery("TableAuth"))            
             query = f"select * from TableAuth where التاريخ_الميلادي = N'{date}'"
             self.cursor.execute(query)                                             
             return self.cursor.fetchall()
        
class ItemDatabase:
        def __init__(self):
            self.conn = pyodbc.connect('DRIVER={SQL Server};server=DESKTOP-KUPSRH8;DATABASE=AhwalDataBase;UID=SQLSerAdmin;PWD=sqlSER@jed80')
            self.cursor = self.conn.cursor()

        def get_User(self, rowID):             
             query = f"select * from TableUser where ID = '{rowID}'"
             self.cursor.execute(query)                                             
             return self.cursor.fetchall()
        def get_UserByUserName(self, username):             
             query = f"select * from TableUser where UserName = '{username}'"
             self.cursor.execute(query)                                             
             return self.cursor.fetchall()
        
        def get_Users(self):             
             query = f"select * from TableUser"
             self.cursor.execute(query)                                             
             return self.cursor.fetchall()
        
        def get_Items(self):
             result = []
             query = f"select * from TableUser"
             self.cursor.execute(query)
             item_dict = {}
             for row in self.cursor.fetchall():                  
                  item_dict["ID"] = row[0]             
                  item_dict["arabName"] = row[1]             
                  item_dict["JobPosition"] = row[2]  
                  item_dict["Gender"] = row[3]  
                  item_dict["UserName"] = row[4]  
                  item_dict["greDate"] = row[5]  
                  item_dict["Pass"] = row[6]   
                  item_dict["Aproved"] = row[7]
                  item_dict["role"] = row[8]
                  item_dict["engName"] = row[9]    
                                              
             return self.cursor.fetchall()
        
        def get_item(self, item_id):             
             query = f"select * from TableUser where ID = '{item_id}'"
             self.cursor.execute(query)
             for row in self.cursor.fetchall():
                  item_dict = {}
                  item_dict["ID"] = row[0]             
                  item_dict["EmployeeName"] = row[1]             
                  item_dict["UserName"] = row[2]                                       
                  return item_dict
             
        def chech_user(self, username):             
             query = f"select * from TableUser where UserName = '{username}'"
             self.cursor.execute(query)
             for row in self.cursor.fetchall():
                  item_dict = {}
                  item_dict["ID"] = row[0]             
                  item_dict["EmployeeName"] = row[4]             
                  item_dict["JobPosition"] = row[2]  
                  item_dict["Gender"] = row[3]  
                  item_dict["arabName"] = row[1]  
                  item_dict["greDate"] = row[5]  
                  item_dict["Pass"] = row[6]   
                  item_dict["Aproved"] = row[7]
                  item_dict["role"] = row[8]
                  item_dict["engName"] = row[9]
                  return item_dict

        def chech_userName_arabName(self, body):             
             query = f"select * from TableUser where UserName = N'{body['userName']}' and arabName = N'{body['arabName']}'"
             self.cursor.execute(query)
             for row in self.cursor.fetchall():
                  item_dict = {}
                  item_dict["ID"] = row[0]             
                  item_dict["userName"] = row[4]             
                  item_dict["JobPosition"] = row[2]  
                  item_dict["Gender"] = row[3]  
                  item_dict["arabName"] = row[1]  
                  item_dict["greDate"] = row[5]  
                  item_dict["Pass"] = row[6]   
                  item_dict["Aproved"] = row[7]
                  item_dict["role"] = row[8]
                  item_dict["engName"] = row[9]
                  return item_dict
             
            
                
               
        def get_password(self, username):             
             query = f"select Pass from TableUser where UserName = '{username}'"
             self.cursor.execute(query)
             item_dict = {}             
             for row in self.cursor.fetchall():                 
                  item_dict["Pass"] = row[0] 
             for item in  item_dict:  
                 return item_dict[item]
        
        def get_actualName(self, username):             
             query = f"select EmployeeName from TableUser where UserName = '{username}'"
             self.cursor.execute(query)
             item_dict = {}             
             for row in self.cursor.fetchall():                 
                  item_dict["EmployeeName"] = row[0] 
             for item in  item_dict:  
                 return item_dict[item]
             
        def add_item(self, body):
             query = f"insert into TableUser (EmployeeName) values (N'{body['shortname']}')"
             self.cursor.execute(query)
             self.conn.commit()
             pass
        
        def AdminUpdateUserInfo(self, body):
             query = f"update TableUser set role = N'{body['role']}', arabName = N'{body['arabName']}',engName=N'{body['engName']}', jobPosition=N'{body['jobPosition']}', Gender=N'{body['sexOption']}', Aproved=N'{body['isActive']}' where ID = '{body['id']}'"
             self.cursor.execute(query)
             self.conn.commit()

        def UserUpdateUserInfo(self, body):  
             print("**************UserUpdateUserInfo************")
             print(body)           
             query = f"update TableUser set arabName = N'{body['arabName']}',engName=N'{body['engName']}', jobPosition=N'{body['jobPosition']}', Gender=N'{body['sexOption']}' where ID = '{body['id']}'"
             self.cursor.execute(query)
             self.conn.commit()

        def UserUpdatePassword(self, newpass, userid):  
                       
             query = f"update TableUser set Pass = N'{newpass}' where ID = '{userid}'"
             self.cursor.execute(query)
             self.conn.commit()

        def UserSignUp(self, body):
             query = f"INSERT INTO TableUser (arabName,JobPosition,Gender,UserName,greDate,Pass,Aproved,role,engName) values (N'{body['arabName']}', N'{body['jobPosition']}',N'{body['sexOption']}',N'{body['userName']}',N'{body['greDate']}', N'{body['Pass']}', N'{body['Aproved']}', N'{body['role']}',N'{body['engName']}')"
             self.cursor.execute(query)
             self.conn.commit()