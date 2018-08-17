from pymysql import  connect,cursors
from pymysql.err import OperationalError
import os,re
import configparser as cparser

#读取db_config.ini的数据
base_dir  = str(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)
base_dir =base_dir.replace('\\','/')
print(base_dir)
file_path = os.path.split(base_dir)[0]+'/db_config.ini'
print(file_path)

cf = cparser.ConfigParser()
cf.read(file_path)

host = cf.get('mysqlconf','host')
port = cf.get('mysqlconf','port')
db_name = cf.get('mysqlconf','db_name')
user = cf.get('mysqlconf','user')
password = cf.get('mysqlconf','password')


#基本操作封装   增删改查
class DB:
    def __init__(self):
        '''数据库基本配置，链接信息'''
        try:
            self.conn = connect(host=host,
                                # port=port,
                                user=user,
                                password=password,
                                db_name=db_name,
                                charset='utf8mb4',
                                cursorclass=cursors.DictCursor)
        except OperationalError as e:
            print('MySql Error %d:%s '%(e.args[0],e.args[1]))

    #清除数据
    def clear(self,table_name):
        real_sql = "delete from"+table_name+";"
        with self.conn.cursor() as cursors:
            cursors.execute('SET FOREIGN_KEY_CHECK=0;')
            cursors.execute(real_sql)
        self.conn.commit()

    #插入输入
    def insert(self,table_name,table_data):
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.keys())
        real_sql = 'Insert Into'+table_name +"("+key+")Values("+value+")"

        with self.conn.cursor() as cursors:
            cursors.execute(real_sql)
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__=="__main__":
    db = DB()
    table_name = 'sign_event'
    data = {'id':1,'name':'one plus 3 event','status':True,
            'limit':20,'address':'上海闵行','start_time':'2018-07-27 17:06:00'}

    db.clear(table_name)
    db.insert(table_name,data)
    db.close()