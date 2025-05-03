import sqlite3


class MySQLiteAPI:

    def __init__(self, path_and_name, table_name):
        """
        构建连接SQLite数据库的API，并初始化数据库文件的地址、文件名以及表名。

        :param path_and_name: 数据库文件的存储地址与文件名（不包含扩展名），如MyDB或D:/DBFiles/MyDB；
        :param table_name: 存储的表名，如MyTable；
        """
        self.path_and_name = path_and_name
        self.table_name = table_name

    def open(self):
        # 创建连接
        con = sqlite3.connect(f'{self.path_and_name}.db')
        # 获取cursor对象
        cur = con.cursor()

        return con, cur

    @staticmethod
    def close(connect, cursor):
        # 关闭游标
        cursor.close()
        # 关闭连接
        connect.close()

    def create_sql(self, key_and_other_column_command):
        """
        创建SQLite数据库文件。

        :param key_and_other_column_command: 表头信息与要求定义，包含主键等必要信息，如no INTEGER PRIMARY KEY  AUTOINCREMENT ,
            name varchar(30) NOT NULL ,age INTEGER，无需括号；
        :return: None
        """
        con, cur = self.open()

        # 创建sql命令语句
        sql = f'create table {self.table_name}({key_and_other_column_command})'
        try:
            # 执行sql语句
            cur.execute(sql)
            print(f'{self.path_and_name}/{self.table_name}创建成功')
        except Exception as e:
            print(f'{e}:{self.table_name}创建表失败')
        finally:
            self.close(con, cur)

    def insert_data(self, column_tuple, value_tuple):
        """
        向SQLite数据库文件中插入一条信息。

        :param column_tuple: 要插入的数据的表头元组，如('name','age')，需要括号；
        :param value_tuple: 要插入的数据的值，如('加三三',5)，需要括号；
        :return: None
        """

        con, cur = self.open()

        tag = ''
        column_str = ''

        for i in range(len(column_tuple)):
            if i == (len(column_tuple) - 1):
                tag += '?'
                column_str += column_tuple[i]
            else:
                tag += '?,'
                column_str += (column_tuple[i] + ',')

        sql = f'insert into {self.table_name}({column_str}) values({tag})'
        try:
            cur.execute(sql, value_tuple)
            # 提交事务
            con.commit()
            print(f'{value_tuple}插入成功')
        except Exception as e:
            print(f'{e}:{value_tuple}插入失败')
            con.rollback()
        finally:
            self.close(con, cur)

    def insert_datas(self, column_tuple, values_tuples_list):
        """
        向SQLite数据库文件中插入多条信息。

        :param column_tuple: 要插入的数据的表头元组，如('name','age')，需要括号；
        :param values_tuples_list: 要插入的多条数据的值，并以列表套元组的形式进行组织，如[('加三三',5),('李四',24),('王五',22)]，需要括号；
        :return: None
        """

        con, cur = self.open()

        tag = ''
        column_str = ''

        for i in range(len(column_tuple)):
            if i == (len(column_tuple) - 1):
                tag += '?'
                column_str += column_tuple[i]
            else:
                tag += '?,'
                column_str += (column_tuple[i] + ',')

        sql = f'insert into {self.table_name}({column_str}) values({tag})'
        try:
            cur.executemany(sql, values_tuples_list)
            # 提交事务
            con.commit()
            print(f'{values_tuples_list}插入成功')
        except Exception as e:
            print(f'{e}:{values_tuples_list}插入失败')
            con.rollback()
        finally:
            self.close(con, cur)

    def fetchall_datas(self):
        """
        获取表内的所有数据并返回数据列表。

        :return: 数据列表
        """
        con, cur = self.open()

        sql = f'select * from {self.table_name}'
        try:
            cur.execute(sql)
            # 获取所有数据
            datas = cur.fetchall()
            print(f'{self.table_name}查询成功')
        except Exception as e:
            print(f'{e}:{self.table_name}查询失败')
            datas = list()
        finally:
            self.close(con, cur)
        return datas

    def fetchone_data(self):
        """
        获取表内的一条数据并返回数据元组。

        :return: 数据元组
        """
        con, cur = self.open()

        sql = f'select * from {self.table_name}'
        try:
            cur.execute(sql)
            # 获取一条数据
            data = cur.fetchone()
            print(f'{self.table_name}首记录查询成功')
        except Exception as e:
            print(f'{e}:{self.table_name}首记录查询失败')
            data = set()
        finally:
            self.close(con, cur)
        return data

    def update_data(self, update_kv_tuple):
        """
        更新一条已有数据。

        :param update_kv_tuple: 要更新的数据元组，组织形式为(keyName, changeName, keyValue, changeValue)，如('no','name', 1,'加三三')；
        :return: None
        """
        con, cur = self.open()

        try:

            update_sql = f'update {self.table_name} set {update_kv_tuple[1]}=? where {update_kv_tuple[0]}=?'
            cur.execute(update_sql, (update_kv_tuple[3], update_kv_tuple[2]))
            # 提交事务
            con.commit()
            print(f'{update_kv_tuple}修改成功')
        except Exception as e:
            print(f'{e}:{update_kv_tuple}修改失败')
            con.rollback()
        finally:
            self.close(con, cur)

    def update_datas(self, update_kv_tuples_list):
        """
        更新多条已有数据。

        :param update_kv_tuples_list: 要更新的数据元组列表，以列表套元组的形式进行组织，如
            [(keyName, changeName, keyValue, changeValue),(keyName, changeName, keyValue, changeValue)]；
        :return: None
        """
        con, cur = self.open()

        for update_kv_tuple in update_kv_tuples_list:
            try:

                update_sql = f'update {self.table_name} set {update_kv_tuple[1]}=? where {update_kv_tuple[0]}=?'
                cur.execute(update_sql, (update_kv_tuple[3], update_kv_tuple[2]))
                # 提交事务
                con.commit()
                print(f'{update_kv_tuple}修改成功')
            except Exception as e:
                print(f'{e}:{update_kv_tuple}修改失败')
                con.rollback()

        self.close(con, cur)

    def delete_data(self, delete_kv_tuple):
        """
        删除一条已有数据。

        :param delete_kv_tuple: 要删除的数据元组，以(keyName,keyValue)的形式组织,如('no', 1)；
        :return: None
        """
        con, cur = self.open()

        delete_sql = f'delete from {self.table_name} where {delete_kv_tuple[0]}=?'
        try:
            cur.execute(delete_sql, (delete_kv_tuple[1],))
            # 提交事务
            con.commit()
            print(f'{delete_kv_tuple}删除成功')
        except Exception as e:
            print(f'{e}:{delete_kv_tuple}删除失败')
            con.rollback()
        finally:
            self.close(con, cur)

    def delete_datas(self, delete_kv_tuple_list):
        """
        批量删除多条数据。

        :param delete_kv_tuple_list: 要删除的数据元组列表，以列表套元组的形式进行组织，如[(keyName, keyValue),(keyName, changeValue)]，如
            [('no', 1),('name', '加三三')]；
        :return: None
        """
        con, cur = self.open()

        for delete_kv_tuple in delete_kv_tuple_list:
            try:
                delete_sql = f'delete from {self.table_name} where {delete_kv_tuple[0]}=?'
                cur.execute(delete_sql, (delete_kv_tuple[1],))
                # 提交事务
                con.commit()
                print(f'{delete_kv_tuple}删除成功')
            except Exception as e:
                print(f'{e}:{delete_kv_tuple}删除失败')
                con.rollback()

        self.close(con, cur)


if __name__ == '__main__':
    a = MySQLiteAPI('MyDB', 'person')
    a.create_sql('No INTEGER PRIMARY KEY  AUTOINCREMENT ,Name varchar(20) NOT NULL ,Age INTEGER')
    a.insert_data(('No', 'Name', 'Age'), (7, "加三三", 5))
    b = a.fetchall_datas()
    print(b)
