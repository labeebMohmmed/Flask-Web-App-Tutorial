from website import create_app
import pyodbc
app = create_app()


class ItemDatabase:
        def __init__(self):
            #self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=WIN-7MTCGVUN6J9;DATABASE=AhwalDataBase;')
            #self.conn = pyodbc.connect('DRIVER={SQL Server};DESKTOP-KUPSRH8 ;DATABASE=AhwalDataBase;;')
            self.conn = pyodbc.connect('DRIVER={SQL Server};server=DESKTOP-KUPSRH8 ;DATABASE=AhwalDataBase;UID=SQLSerAdmin;PWD=sqlSER@jed80')
            self.cursor = self.conn.cursor()

        def get_Items(self):
             result = []
             query = "select * from TableUser"
             self.cursor.execute(query)
             for row in self.cursor.fetchall():
                  item_dict = {}
                  item_dict["ID"] = row[0]             
                  item_dict["EmployeeName"] = row[1]             
                  item_dict["UserName"] = row[2]                     
                  print(item_dict)
                  result.append(item_dict)          
             return result
        
        def get_item(self, item_id):             
             query = f"select * from TableUser where ID = '{item_id}'"
             self.cursor.execute(query)
             for row in self.cursor.fetchall():
                  item_dict = {}
                  item_dict["ID"] = row[0]             
                  item_dict["EmployeeName"] = row[1]             
                  item_dict["UserName"] = row[2]                                       
                  return item_dict
        
        def add_item(self, body):
             query = f"insert into TableUser (EmployeeName) values (N'{body['shortname']}')"
             self.cursor.execute(query)
             self.conn.commit()
             pass
        
        def put_item(self, body):
             query = f"update TableUser set EmployeeName = N'{body['shortname']}' where ID = '{body['id']}'"
             self.cursor.execute(query)
             self.conn.commit()

#dirdb = ItemDatabase()

    #dirdb.put_item (body ={'shortname':'لبيب محمد لبيب','id':'6054'})

if __name__ == '__main__':
    app.run(debug=True)
