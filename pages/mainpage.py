import sys
import multiprocessing as mp
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5 import uic

from static.main import btn_style
from module.frame_module import TitleFrame


class MainPageWindow(QWidget):

    page_info = {
        '체형측정': {
            'next': {
                'page': 'BodyWindow',
                'data': 'sub',
            },
            'now': {
                'page': 'MainPageWindow',
                'data': '',
            },
        },
        '기능적측정': {
            'next': {
                'page': 'FunctionWindow',
                'data': '',
            },
            'now': {
                'page': 'MainPageWindow',
                'data': '',
            },
        },
        '보행측정': {
            'next': {
                'page': 'WalkWindow',
                'data': '',
            },
            'now': {
                'page': 'MainPageWindow',
                'data': '',
            },
        },
        'ROM측정': {
            'next': {
                'page': 'ROMWindow',
                'data': '',
            },
            'now': {
                'page': 'MainPageWindow',
                'data': '',
            },
        },
        '운동프로그램': {
            'next': {
                'page': 'MainPageWindow',
                'data': 'sub',
            },
            'now': {
                'page': 'MainPageWindow',
                'data': '',
            },
        },
        '통증유발점': '',
        '필라테스': '',
        '교정운동': '',
        '오늘의 운동': '',
        '근골격계 운동': '',
        '골프 컨디셔닝': '',
        '피트니스': '',
    }

    def __init__(self, parent, check, page_queue, data):
        super(MainPageWindow, self).__init__(parent)

        self.page_queue = page_queue
        self.title_frame = TitleFrame(check)
        self.title_frame.setUI('BODY ASSESSMENT', '원하시는 측정 모드를 클릭해 주세요.')

        if data == 'subprogram':
            self.title_frame.setUI('EXERCISE PROGRAM', '원하시는 운동 프로그램을 클릭해 주세요.')

        btn_list = list(btn_style[data].keys())

        gbox = QGridLayout()
        h, c = 0, 0

        for key in btn_list:
            btn = self.make_button(key, data)


            if c > (1 if check == 0 else 2):
                h += 1
                c = 0
            gbox.addWidget(btn, h, c)
            c += 1

        vbox = QVBoxLayout()
        vbox.addWidget(self.title_frame.title_frame)
        vbox.addLayout(gbox)

        self.setLayout(vbox)

    def make_button(self, i, data):
        button = QPushButton()
        button.setStyleSheet(btn_style[data][i])
        button.setFixedWidth(472)
        button.setFixedHeight(402)
        button.clicked.connect(partial(self.btn_click, i))

        return button

    def btn_click(self, i):
        self.page_queue.put(self.page_info[i])