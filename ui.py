# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName("main")
        main.resize(400, 427)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(main)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.camera_ip = QtWidgets.QLineEdit(main)
        self.camera_ip.setObjectName("camera_ip")
        self.gridLayout.addWidget(self.camera_ip, 0, 1, 1, 1)
        self.stop_live = QtWidgets.QPushButton(main)
        self.stop_live.setObjectName("stop_live")
        self.gridLayout.addWidget(self.stop_live, 4, 0, 1, 2)
        self.rtsp_server = QtWidgets.QLineEdit(main)
        self.rtsp_server.setObjectName("rtsp_server")
        self.gridLayout.addWidget(self.rtsp_server, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(main)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.start_live = QtWidgets.QPushButton(main)
        self.start_live.setObjectName("start_live")
        self.gridLayout.addWidget(self.start_live, 3, 0, 1, 2)
        self.label = QtWidgets.QLabel(main)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.response = QtWidgets.QTextEdit(main)
        self.response.setObjectName("response")
        self.gridLayout.addWidget(self.response, 5, 0, 1, 2)
        self.preview = QtWidgets.QPushButton(main)
        self.preview.setToolTip("")
        self.preview.setCheckable(True)
        self.preview.setChecked(False)
        self.preview.setAutoExclusive(False)
        self.preview.setObjectName("preview")
        self.gridLayout.addWidget(self.preview, 2, 0, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout)

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "Dialog"))
        self.camera_ip.setText(_translate("main", "http://192.168.2.139"))
        self.stop_live.setText(_translate("main", "Stop Live"))
        self.rtsp_server.setText(_translate("main", "rtsp://localhost:8554"))
        self.label_2.setText(_translate("main", "RTSP Server :"))
        self.start_live.setText(_translate("main", "Start Live"))
        self.label.setText(_translate("main", "Camera Adress :"))
        self.preview.setText(_translate("main", "Preview"))