import traceback

import pymysql
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from typing import Dict, Any, Tuple


class DBClass:

    db : pymysql

    def __init__(self):
        self.open()
        self.engine = sqlalchemy.create_engine("mysql://{user}:{pw}@{ip}:{port}/{db}".format(user='root', pw='root', ip='127.0.0.1', port=3306, db='scifit'))
        self.conn = self.engine.connect()

    def open(self):
        self.db = pymysql.connect(
            user='root',  # cijd / root
            passwd='root',  # tsei1234 / root
            host='127.0.0.1',  # 1.253.30.55 #127.0.0.1
            port=3306,  # 33333 #3306
            db='scifit',
            charset='utf8',
            # autocommit=True,  # 결과 DB 반영 (Insert or update)
            # cursorclass=pymysql.cursors.DictCursor  # DB조회시 컬럼명을 동시에 보여줌
        )

        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def close(self):
        self.db.commit()
        self.db.close()

    def selectData(self, table_name: str, search_data: str = None) -> list:
        sql: str = f"SELECT * FROM {table_name}"
        if search_data is not None:
            # 찾을 데이터가 None 이 아닐 경우
            sql += search_data

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        result = pd.DataFrame(result)
        return result

    # 데이터 베이스 삽입 함수
    def insertData(self, table_name: str, column_data: Dict[str, Any]):
        print('insertData')
        sql_columns_list: list = list(column_data.keys())  # 칼럼명 저장 변수
        print(sql_columns_list)

        sql_columns: str = ', '.join(map(str, sql_columns_list))
        sql_values: str = ''

        count = 0
        for i in sql_columns_list:
            sql_values += f"{column_data[i]}"
            if count < len(sql_columns_list) - 1:
                # 마지막 요소가 아닐 경우
                sql_values += ", "
            count += 1

        sql = f"INSERT INTO {table_name} ({sql_columns}) VALUES ({sql_values})"
        print(sql)

        self.cursor.execute(sql)
        # self.cursor.execute(sql, column_data)

    # 데이터 베이스 수정 함수
    def updateData(self, table_name: str, search_data: Tuple[str, Any], column_data: Dict[str, Any]):
        print("DB update")
        try:
            search_data_select = f' WHERE {search_data[0]}={search_data[1]}'
            return_data: pd.DataFrame = self.selectData(table_name, search_data_select)
            if return_data.empty is True:
                # 데이터가 없을 경우 생성
                print("to insert")
                self.insertData(table_name, column_data)
                return

            print([f"{k}={v}" for k, v in column_data.items()])

            sql: str = f"UPDATE {table_name} SET "
            sql += ', '.join([f"{k}={v}" for k, v in column_data.items()])
            sql += f" WHERE {search_data[0]}={search_data[1]};"

            print("======UPDATE=========")
            print(sql)
            self.cursor.execute(sql)
        except:
            print(traceback.format_exc())

    # insert / update / delete
    def dmlData(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    def deleteData(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    # insert
    def insertData_df(self, table_name, insert_df):
        insert_df.to_sql(name = table_name, con=self.engine, if_exists='append', index = False)

if __name__ == "__main__":
    DBClass = DBClass()