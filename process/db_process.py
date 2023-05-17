import time
import datetime
import traceback

import pandas as pd

from datetime import datetime
from module.db_module import DBClass
from typing import Dict, List, Any


class DBProcess:
    index: int = 0
    pre_second = -1
    def __init__(self, insert_queue, update_queue, select_queue, select_return_queue, update_return_queue, insert_return_queue, select_manager, log_manager):

        print("DBPROcess")
        self.insert_queue = insert_queue
        self.update_queue = update_queue
        self.select_queue = select_queue
        self.select_return_queue = select_return_queue
        self.select_manager = select_manager
        self.update_return_queue = update_return_queue
        self.insert_return_queue = insert_return_queue
        self.log_manager = log_manager

        self.db_instance = DBClass()

        self.addLog(f"DB에 연결되었습니다.")

        while True:
            self.now_time = datetime.now()
            self.db_instance.open()
            self.insertData()
            self.updateData()
            self.selectData_queue()

            if self.pre_second != self.now_time.second:
                self.selectData()
                self.pre_second = self.now_time.second

            self.db_instance.close()
            time.sleep(0.01)

    def selectData(self):
        try:
            user_measure = self.db_instance.selectData("user_measure")
            self.select_manager.user_measure = user_measure
        except:
            pass


    def selectData_queue(self):
        while self.select_queue.qsize() > 0:
            select_queue_data: List = self.select_queue.get()

            print(select_queue_data)

            select_df: pd.DataFrame
            table_name = select_queue_data[0]
            if len(select_queue_data) >= 2:
                column_data = select_queue_data[1]
                select_df = self.db_instance.selectData(table_name, column_data)
            else:
                select_df = self.db_instance.selectData(table_name)

            print(select_df)

            self.select_return_queue.put(select_df)


    def insertData(self):
        while self.insert_queue.qsize() > 0:
            insert_queue_data: List = self.insert_queue.get()

            table_name = insert_queue_data[0]
            column_data = insert_queue_data[1]

            return_flag = False
            try:
                self.db_instance.insertData(table_name, column_data)
                self.addLog(f"{table_name} {column_data} insert 완료.")
                # self.addLog(f"{table_name[0]}에 insert가 완료됐습니다.")
                return_flag = True
            except:
                self.addLog(f"{table_name} {column_data}에서 insert 중 에러발생.")

            self.insert_return_queue.put(return_flag)


    def updateData(self):
        while self.update_queue.qsize() > 0:
            update_queue: List = self.update_queue.get()

            table_name = update_queue[0]
            where = update_queue[1]
            fix = update_queue[2]
            print(table_name, '   ', where , '    ', fix)
            return_flag = False
            try:
                self.db_instance.updateData(table_name, where, fix)
                self.addLog(f"{table_name} {where} -> {fix} update 완료.")
                return_flag = True
            except:
                print(traceback.format_exc())
                self.addLog(f"{table_name} {where} -> {fix}에서 update 중 에러발생.")

            self.update_return_queue.put(return_flag)


    def addLog(self, msg):
        self.log_manager.put(f"{msg}")
        # self.log_manager.put("{checkdate} {msg}".format(checkdate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg=msg))