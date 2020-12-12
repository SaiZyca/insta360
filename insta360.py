from PySide2 import QtCore, QtWidgets
from ui import Ui_main
from service import InstaCamera
import sys


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.camera = InstaCamera()
        self.ui = Ui_main()
        self.ui.setupUi(self)
        self.connect_sognal()
        self.count = 1
        self.settings = QtCore.QSettings('insta360.ini', QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.ui.camera_ip.setText(self.settings.value('camera_ip'))
        self.ui.rtsp_server.setText(self.settings.value('rtsp_server'))
        
    def connect_sognal(self):
        self.ui.start_live.clicked.connect(self.start_live)
        self.ui.stop_live.clicked.connect(self.stop_live)

    def start_preview(self):
        self.camera.start_preview()

    def stop_preview(self):
        self.camera.stop_preview()

    def start_live(self):
        self.settings.setValue('camera_ip', self.ui.camera_ip.text())
        self.settings.setValue('rtsp_server', self.ui.rtsp_server.text())
        self.camera.set_camera_adress(self.ui.camera_ip.text())
        self.camera.set_rtmp_server(self.ui.rtsp_server.text())
        self.camera.connect()
        self.ui.response.append(self.camera.get_state())
        self.camera.start_live()
        self.ui.response.append(self.camera.get_state())
        # self.camera.start_live()

    def stop_live(self):
        self.settings.setValue('camera_ip', self.ui.camera_ip.text())
        self.settings.setValue('rtsp_server', self.ui.rtsp_server.text())
        self.camera.set_camera_adress(self.ui.camera_ip.text())
        self.camera.set_rtmp_server(self.ui.rtsp_server.text())
        self.camera.connect()
        self.ui.response.append(self.camera.get_state())
        self.camera.stop_live()
        self.ui.response.append(self.camera.get_state())

    def test_signal(self,message):
        print (message)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())