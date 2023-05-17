# -*- coding: utf-8 -*-
import sys
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5 import uic
from typing import Dict, Any, Tuple
from functools import partial

from static.main import label_style, btn_style


class StartFrame(QFrame):

    logoLabel: QLabel       # 로고 라벨
    startBtn: QPushButton   # 로그인 버튼

    def __init__(self, parent, check):
        super(StartFrame, self).__init__(parent=None)  # 부모 클래스 호출

        self.logoLabel = QLabel()
        self.logoLabel.setAlignment(Qt.AlignCenter)
        # self.logoLabel.setStyleSheet(label_style['start_page']['logo'])

        self.startBtn = QPushButton()
        # self.startBtn.setStyleSheet(btn_style['start_page']['start'])
        self.startBtn.setFixedHeight(192)
        self.startBtn.setFixedWidth(192)

        if check == 0:
            vbox = QVBoxLayout()

            vbox.setContentsMargins(10, 200, 10, 200)
            vbox.addWidget(self.logoLabel)
            vbox.addWidget(self.startBtn, alignment=Qt.AlignCenter)

            self.setLayout(vbox)

        if check == 1:
            hbox = QHBoxLayout()

            hbox.setContentsMargins(200, 10, 200, 10)
            hbox.addWidget(self.logoLabel)
            hbox.addWidget(self.startBtn, alignment=Qt.AlignCenter)

            self.setLayout(hbox)




# 메인 윈도우 프레임
class MainFrame(QFrame):
    title_frame: QFrame  # 타이틀 frame

    titleLabel: QLabel  # 타이틀 라벨
    subtitleLabel: QLabel  # 서브타이틀 라벨

    nav_frame: QFrame  # 네비게이션 프레임

    backBtn: QPushButton  # 뒤로가기 버튼
    homeBtn: QPushButton  # 홈 버튼
    listBtn: QPushButton  # 리스트 버튼

    mainStack: QStackedWidget    # 서브 스택

    def __init__(self, parent, check):
        super(MainFrame, self).__init__(parent=None)  # 부모 클래스 호출

        self.nav_frame = QFrame()
        self.nav_frame.setStyleSheet("border: 0px;")

        # list 버튼 설정
        self.listBtn = QPushButton('list')
        self.listBtn.setFixedHeight(30)
        # self.listBtn.setStyleSheet()

        # home 버튼 설정
        self.homeBtn = QPushButton('home')
        self.homeBtn.setFixedHeight(30)
        # self.homeBtn.setStyleSheet()

        # back 버튼 설정
        self.backBtn = QPushButton('back')
        self.backBtn.setFixedHeight(30)
        # self.backBtn.setStyleSheet()

        # 레이아웃 설정

        if check == 0:
            box = QHBoxLayout()
        else:
            box = QVBoxLayout()

        box.setContentsMargins(10, 10, 10, 10)

        box.addWidget(self.listBtn)
        box.addWidget(self.homeBtn)
        box.addWidget(self.backBtn)

        # self.nav_frame.setStyleSheet()
        self.nav_frame.setLayout(box)

        self.mainStack = QStackedWidget()

        if check == 0:
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()

        layout.addWidget(self.mainStack, 10)
        layout.addWidget(self.nav_frame, 1)

        self.setLayout(layout)


class TitleFrame(QFrame):

    title_frame: QFrame  # 타이틀 frame

    titleLabel: QLabel  # 타이틀 라벨
    subtitleLabel: QLabel  # 서브타이틀 라벨

    def __init__(self, check):
        self.title_frame = QFrame()
        self.title_frame.setStyleSheet("border: 0px;")

        self.check = check

        self.titleLabel = QLabel()
        # self.titleLabel.setStyleSheet()

        self.subtitleLabel = QLabel()
        # self.subtitleLabel.setStyleSheet()

        vbox = QVBoxLayout()
        vbox.setContentsMargins(10, 10, 10, 10)
        vbox.setSpacing(10)
        vbox.addWidget(self.titleLabel)
        vbox.addWidget(self.subtitleLabel)

        self.title_frame.setLayout(vbox)

    def setUI(self, title, sub_title):
        self.titleLabel.setText(title)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet('color: white;')

        self.subtitleLabel.setText(sub_title)
        self.subtitleLabel.setStyleSheet('color: white;')
        self.subtitleLabel.setAlignment(Qt.AlignCenter)

        if title == 'LOGIN':
            self.titleLabel.setFont(QFont("SUIT", 111))
            self.subtitleLabel.setFont(QFont("SUIT", 41))
            if self.check == 1:
                self.titleLabel.setFont(QFont("SUIT", 90))
                self.subtitleLabel.setFont(QFont("SUIT", 30))
        else:
            self.titleLabel.setFont(QFont("SUIT", 80))
            self.subtitleLabel.setFont(QFont("SUIT", 40))
            if self.check == 1:
                self.titleLabel.setFont(QFont("SUIT", 55))
                self.subtitleLabel.setFont(QFont("SUIT", 20))



class RecommandVideoFrame(QFrame):

    video_frame: QFrame  # 비디오 frame

    titleLabel: QLabel  # 타이틀 라벨
    imgLabel: QLabel  # 서브타이틀 라벨

    def __init__(self):
        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("border: 0px;")
        self.video_frame.setFixedHeight(404)
        self.video_frame.setFixedWidth(449)

        self.imgBtn = QPushButton()
        self.imgBtn.setFixedHeight(292)
        self.imgBtn.setFixedWidth(400)
        # self.imgBtn.setStyleSheet()

        self.titleLabel = QLabel()
        self.titleLabel.setFont(QFont('SUIT', 10))
        # self.titleLabel.setStyleSheet()

        vbox = QVBoxLayout()
        vbox.setContentsMargins(10, 10, 10, 10)
        vbox.setSpacing(5)
        vbox.addWidget(self.imgBtn)
        vbox.addWidget(self.titleLabel)

        self.video_frame.setLayout(vbox)

        return self.video_frame, self.imgBtn, self.titleLabel.text()


# class ExerciseFrame(QFrame):
#
#     imgLabel: QLabel  # 상단 이미지 라벨
#
#     def __init__(self):
#         super(ExerciseFrame, self).__init__()  # 부모 클래스 호출
#         self.imgLabel = QLabel()

