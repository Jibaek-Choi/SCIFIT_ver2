from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QDate, QSize
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QImage, QFont
from PyQt5 import uic, QtCore, QtWidgets

from tkinter import *

from module.frame_module import StartFrame, MainFrame

import os
import signal
import subprocess
import sys
import pandas as pd
import multiprocessing as mp
import time
import traceback
import resources_rc

from pages.login import LoginWindow
from pages.mainpage import MainPageWindow
from process.db_process import DBProcess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# form_class = uic.loadUiType(BASE_DIR + "/ui/main.ui")[0]

# SCIFIT QThread
class SFThread(QThread):

    # 뒤로가기 페이지 정보
    back_page_data = []
    # 다음 페이지 정보
    next_page_data = {}

    back_type = False

    # 뒤로가기 시그널
    back_click_signal = pyqtSignal(dict)
    # 다음 페이지 시그널
    next_page_signal = pyqtSignal(dict)

    def __init__(self, page_queue, parent=None):
        super(SFThread, self).__init__(parent)
        self.page_queue = page_queue

    def run(self):
        while True:
            if self.page_queue.qsize() > 0:
                page_dict = self.page_queue.get()
                next_page = page_dict['next']
                now_page = page_dict['now']

                print(next_page)
                print(now_page)

                self.back_page_data.append(now_page)

                print(self.back_page_data)

                try:
                    self.next_page_signal.emit(next_page)
                except:
                    print(traceback.format_exc())

            if self.back_type is True:
                if len(self.back_page_data) == 0:
                    return
                pre_page = self.back_page_data.pop()
                self.back_click_signal.emit(pre_page)
                self.back_type = False

    def stop(self):
        self.quit()


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow): # form_class):

    """
    0 = 세로
    1 = 가로
    """
    page_design = 0

    # main 스택 페이지 이름 - 인덱스 딕셔너리
    stack_page_dict = {
        'LoginWindow': 0,
        'MainPageWindow': 1,
        'SubProgram': 2,
    }

    now_page: int       # 현재 페이지
    page_queue: mp.Queue       # 페이지 정보

    pw: str     # 로그인 패스워드 저장

    def __init__(self, parent=None):
        super(WindowClass, self).__init__(parent)

        #멀티 프로세스 관련 변수들
        manager = mp.Manager()
        self.log_manager = mp.Queue()  # 로그 관리 매니저

        self.select_manager = manager.Namespace()
        self.select_manager.user_measure = []

        self.insert_queue = mp.Queue()
        self.update_queue = mp.Queue()
        self.select_queue = mp.Queue()
        self.select_return_queue = mp.Queue()
        self.update_return_queue = mp.Queue()
        self.insert_return_queue = mp.Queue()

        try:
            self.db_process = mp.Process(target=DBProcess, args=(
                self.insert_queue, self.update_queue, self.select_queue, self.select_return_queue, self.update_return_queue,
                self.insert_return_queue,
                self.select_manager, self.log_manager))  # DB프로세스

            self.db_process.start()
        except:
            print(traceback.format_exc())

        self.select_queue.put(['login'])

        #
        while True:
            if self.select_return_queue.qsize() > 0:
                device_status: pd.DataFrame = self.select_return_queue.get()
                device_info = device_status.to_dict('records')
                print(device_info)
                self.pw = device_info[0]['pw']
                break

        self.page_queue = mp.Queue()        # 페이지 정보를 위한 큐

        self.sfThread = SFThread(self.page_queue)       # 페이지 전환을 위한 쓰레드
        self.sfThread.start()
        self.sfThread.next_page_signal.connect(self.next_page)
        self.sfThread.back_click_signal.connect(self.back_page)

        self.now_page = 0

        self.setUI()

    def __del__(self):
        self.sfThread.stop()
        self.db_process.kill()

   # UI셋팅
    def setUI(self):

        # 모니터 해상도 확인
        tk = Tk()

        monitor_height = tk.winfo_screenheight()
        monitor_width = tk.winfo_screenwidth()

        # 만약 화면이 가로라면
        if monitor_width > monitor_height:
            self.page_design = 1

        if self.page_design == 0:
            self.setFixedWidth(1080)
            self.setFixedHeight(1920)

        elif self.page_design == 1:
            self.setFixedWidth(1920)
            self.setFixedHeight(1080)

        # 메인 스택 화면 구성
        self.windowStack = QStackedWidget()

        # 시작 화면 구성
        start_frame = StartFrame(self, self.page_design)
        start_frame.startBtn.clicked.connect(self.start_click)

        self.windowStack.addWidget(start_frame)

        # 메인 화면 구성
        self.main_frame = MainFrame(self, self.page_design)
        self.main_frame.backBtn.clicked.connect(self.back_click)
        self.main_frame.homeBtn.clicked.connect(self.home_click)
        self.main_frame.listBtn.clicked.connect(self.list_click)

        self.windowStack.addWidget(self.main_frame)

        login_page = LoginWindow(self, self.page_design, self.page_queue, self.pw)
        main_page = MainPageWindow(self, self.page_design, self.page_queue, 'main_page')
        sub_page = MainPageWindow(self, self.page_design, self.page_queue, 'subprogram')

        # main stack 페이지 삽입
        self.main_frame.mainStack.addWidget(login_page)
        self.main_frame.mainStack.addWidget(main_page)
        self.main_frame.mainStack.addWidget(sub_page)

        self.mainWidget = QWidget()
        # self.mainWidget.setObjectName("centralWidget")
        self.mainWidget.setStyleSheet("#centralWidget {background: url(:/img/img/background.png);}")

        if self.page_design == 1:
            self.mainWidget.setStyleSheet("#centralWidget {background: url(:/img/img/background_width.png);}")

        self.setCentralWidget(self.mainWidget)

        self.mainLayout = QVBoxLayout(self.mainWidget)
        self.mainLayout.addWidget(self.windowStack)

        # self.setLayout(self.mainLayout)

        # self.windowStack.setCurrentIndex(0)

    def start_click(self):
        self.windowStack.setCurrentIndex(1)

    def next_page(self, next_data):
        try:
            print('now = ', self.stack_page_dict[next_data['page']])
            next_page = self.stack_page_dict[next_data['page']]

            if next_data['data'] == 'sub':
                next_page = self.stack_page_dict['SubProgram']

            if self.now_page != next_page:
                self.main_frame.mainStack.setCurrentIndex(next_page)
                self.now_page = next_page
        except:
            print(traceback.format_exc())

    def back_page(self, back_data):
        back_page = self.stack_page_dict[back_data['page']]
        print(back_page)
        self.main_frame.mainStack.setCurrentIndex(back_page)
        self.now_page = back_page

    def back_click(self):
        self.sfThread.back_type = True

    def home_click(self):
        print("home")

    def list_click(self):
        pass


if __name__ == "__main__" :
    try:
        # 화면 해상도에 따른 자동 폰트 및 크기 변경
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        mp.freeze_support()
        #QApplication : 프로그램을 실행시켜주는 클래스
        app = QApplication(sys.argv)
        # app = QApplication(sys.path)
        #WindowClass의 인스턴스 생성
        myWindow = WindowClass()
        #프로그램 화면을 보여주는 코드
        myWindow.show()
        # myWindow.showFullScreen()
        #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
        app.exec_()
        sys.exit(app.exec())
    except:
        print(traceback.format_exc())
