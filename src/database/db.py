from decouple import config
import pymysql


def get_connection():
    try:
        data = get_db_data()
        return pymysql.connect(
            host=data.host,
            database=data.database,
            user=data.user,
            password=data.password)
    except pymysql.Error as e:
        print(f"An error occurred stablishin connection: {str(e)}")


def get_db_data():
    return Data(
        config('MYSQL_HOST'), 
        config('MYSQL_DB'),
        config('MYSQL_USER'), 
        config('MYSQL_PASSWORD'))
 

class Data:
    def __init__(self, Host, Database, User, Password):
        self.host = Host
        self.database = Database
        self.user = User
        self.password = Password
