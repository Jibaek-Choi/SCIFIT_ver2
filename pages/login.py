import sys
import multiprocessing as mp
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5 import uic
import traceback

from module.qt_module import message_event_nomal
from static.main import btn_style
from module.frame_module import TitleFrame

class LoginWindow(QWidget):

    number: str = ""        # 내가 친 비밀번호 저장 변수
    login_data: str = ""
    show_flag: bool = True

    pw: str     # 비밀번호 저장 변수

    def __init__(self, parent, check, page_queue, pw):
        super(LoginWindow, self).__init__(parent)

        self.page_queue = page_queue

        self.pw = pw        # 비밀번호 저장 변수

        self.title_frame = TitleFrame(check)
        self.title_frame.setUI('LOGIN', '비밀번호를 입력해주세요.')

        # 비밀번호 보여주는 라인에딧
        self.pwLineEdit = QLineEdit()
        self.pwLineEdit.setFont(QFont('SUIT', 20))
        self.pwLineEdit.setEchoMode(QLineEdit.Password)

        # 비밀번호 확인 용 버튼
        self.showBtn = QPushButton()
        self.showBtn.setStyleSheet(btn_style['login_page']['on'])
        self.showBtn.setFixedWidth(80)
        self.showBtn.setFixedHeight(80)

        hbox = QHBoxLayout()
        hbox.addWidget(self.pwLineEdit)
        hbox.addWidget(self.showBtn)

        # 비밀번호 창 프레임
        pw_frame = QFrame()
        pw_frame.setStyleSheet('background-color: white; border-radius: 40px;')
        pw_frame.setFixedHeight(112)
        pw_frame.setFixedWidth(686)
        pw_frame.setLayout(hbox)

        gbox = QGridLayout()
        h, c = 0, 0

        for i in range(1, 13):
            btn = self.make_button(i)

            if c > 2:
                h += 1
                c = 0

            gbox.addWidget(btn, h, c)
            gbox.setSpacing(5)

            c += 1

        vbox = QVBoxLayout()
        vbox.addWidget(pw_frame, alignment=Qt.AlignCenter)
        vbox.addLayout(gbox)
        vbox.setSpacing(20)

        pw_border_frame = QFrame()
        pw_border_frame.setStyleSheet('background-color:rgba(255, 255, 255, 0.6); border-radius: 40px;')
        pw_border_frame.setContentsMargins(20, 20, 20, 20)
        pw_border_frame.setFixedHeight(947)
        pw_border_frame.setFixedWidth(760)
        pw_border_frame.setLayout(vbox)

        loginBtn = QPushButton()
        loginBtn.setStyleSheet(btn_style['login_page']['login'])
        loginBtn.setFixedHeight(108)
        loginBtn.setFixedWidth(442)

        if check == 0:
            layout = QVBoxLayout()
            layout.setContentsMargins(50, 100, 50, 50)
            layout.addWidget(self.title_frame.title_frame, 2, alignment=Qt.AlignCenter)
            layout.addWidget(pw_border_frame, 10, alignment=Qt.AlignCenter)
            layout.addWidget(loginBtn, 1, alignment=Qt.AlignCenter)
        else:
            layout = QHBoxLayout()
            layout.setContentsMargins(100, 10, 100, 10)

            leftbox = QVBoxLayout()
            leftbox.addWidget(self.title_frame.title_frame, 2, alignment=Qt.AlignCenter)
            leftbox.addWidget(loginBtn, 1, alignment=Qt.AlignCenter)

            layout.addLayout(leftbox, 1)
            layout.addWidget(pw_border_frame, 1, alignment=Qt.AlignCenter)

        self.showBtn.clicked.connect(self.show_click)  # 눈모양 버튼 클릭
        loginBtn.clicked.connect(self.login_click)  # 로그인 버튼 클릭

        self.setLayout(layout)

    def make_button(self, i):
        button = QPushButton()
        i = str(i)
        if i == '11':
            button.setText('0')
        elif i == '10':
            button.setText('정정')
        elif i == '12':
            button.setText('삭제')
        else:
            button.setText(str(i))
        button.setStyleSheet(btn_style['login_page']['num'])
        button.setFont(QFont("SUIT SemiBold", 45))
        button.setFixedWidth(225)
        button.setFixedHeight(175)
        button.clicked.connect(partial(self.btn_click, i))

        return button

    def btn_click(self, i):
        try:
            if i == '11':
                self.number = '0'
            elif i == '10':
                self.login_data = self.login_data[:-1]
                self.pwLineEdit.setText(self.login_data)
                return
            elif i == '12':
                self.pwLineEdit.clear()
                self.login_data = ""
                return
            else:
                self.number = i
            self.login_data += self.number
            self.pwLineEdit.setText(self.login_data)
        except:
            print(traceback.format_exc())


    # 입력 버튼 클릭 함수 호출
    def login_click(self):

        if self.pw == self.pwLineEdit.text():
            page = {
                'next': {
                    'page': 'MainPageWindow',
                    'data': '',
                },
                'now': {
                    'page': 'LoginWindow',
                    'data': '',
                },
            }

            self.page_queue.put(page)
        else:
            try:
                message_event_nomal(self, '비밀번호 오류', '비밀번호가 일치하지 않습니다.\n다시 입력해 주세요.')
            except:
                print(traceback.format_exc())


    # 비번 보기 버튼
    def show_click(self):
        try:
            if self.show_flag is True:
                self.pwLineEdit.setEchoMode(QLineEdit.Normal)
                self.showBtn.setStyleSheet(btn_style['login_page']['off'])
                self.show_flag = False
            else:
                self.pwLineEdit.setEchoMode(QLineEdit.Password)
                self.showBtn.setStyleSheet(btn_style['login_page']['on'])
                self.show_flag = True
        except:
            print(traceback.format_exc())
