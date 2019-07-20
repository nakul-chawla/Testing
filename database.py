import pymysql
import pymysql.cursors
class db:
    #Initializing
    def __init__(self):
        self.connection=False
        self.host=''
        self.user=''
        self.password=''
        self.database=''
        self.connect_db()

    #Creating Database connection
    def connect_db(self):
        if(not self.connection):
            try:
                self.connection = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    db=self.database)
                #print("Databese connected successfully")
            except Exception:
                return print("Failed to connect database")
    
    #Executing Query
    def exec(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
            self.connection.commit()
        finally:
            self.connection.close()
        return cursor

    #Destroying connection (calling destructor)
    def __del__(self):
        if(self.connection):
            self.connection=False
