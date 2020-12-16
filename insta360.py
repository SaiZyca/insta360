from PySide2 import QtCore, QtWidgets
from ui import Ui_main
from service import InstaCamera
from datetime import datetime
import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.camera = InstaCamera()
        self.ui = Ui_main()
        self.ui.setupUi(self)
        self.connect_ui_signal()
        self.settings = QtCore.QSettings('insta360.ini', QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.ui.camera_ip.setText(self.settings.value('camera_ip'))
        self.ui.rtsp_server.setText(self.settings.value('rtsp_server'))
        self.parm_dict = {}
        self.ui_camera_setting = [self.ui.take_picture,
                              self.ui.from_ev, 
                              self.ui.to_ev, 
                              self.ui.start_preview,
                              self.ui.start_live,
                              self.ui.live_stiching,
                              self.ui.stabilization,
                              self.ui.bitrate,
                              self.ui.resolution
                              ]
        self.disable_ui_camera_setting()

    def disable_ui_camera_setting(self):
        for item in self.ui_camera_setting:
            item.setEnabled(False)

    def enable_ui_camera_setting(self):
        for item in self.ui_camera_setting:
            item.setEnabled(True)

    def connect_ui_signal(self):
        self.camera.signals.log.connect(self.print_log)
        self.ui.connect_camera.clicked.connect(self.connect_camera)
        self.ui.start_live.clicked.connect(self.start_live)
        self.ui.start_preview.clicked.connect(self.start_preview)
        # self.ui.take_picture.clicked.connect(self.test_signal)

    def connect_camera(self):
        self.set_camera_parm()
        if self.ui.connect_camera.text() == "Connect Camera":
            if self.camera.connect_camera(self.parm_dict):
                self.enable_ui_camera_setting()
                self.ui.connect_camera.setText("Disconnect Camera...")
                self.ui.connect_camera.setChecked(True)
        else:
            # self.camera.camera_state(self.parm_dict)
            self.ui.connect_camera.setText("Connect Camera")
            self.disable_ui_camera_setting()
            self.ui.connect_camera.setChecked(False)


    def set_camera_parm(self):
        self.settings.setValue('camera_ip', self.ui.camera_ip.text())
        self.settings.setValue('rtsp_server', self.ui.rtsp_server.text())
        self.parm_dict = {'camera_ip': self.ui.camera_ip.text(), 
                        'rtsp_server': self.ui.rtsp_server.text(), 
                        'from_ev': self.ui.from_ev.value(),
                        'to_ev': self.ui.to_ev.value(), 
                        'bitrate': self.ui.bitrate.value(),
                        'resolution': self.ui.resolution.currentIndex(),
                        'live_stiching':self.ui.live_stiching.isChecked(),
                        'stabilization':True
                        }

    def start_preview(self):

        if self.ui.start_preview.isChecked():
            self.camera.connect_camera(self.parm_dict)
            self.camera.start_preview(self.parm_dict)
            self.ui.start_preview.setText('Stop Preview')
            
        else:
            self.camera.connect_camera(self.parm_dict)
            self.camera.stop_preview()
            self.ui.start_preview.setText('Satrt Preview')
            

    def start_live(self):
        if self.ui.start_live.isChecked():
            self.camera.start_live(self.parm_dict)
            self.ui.start_live.setText('Stop Live')
        else:
            self.camera.stop_live()
            self.ui.start_live.setText('Start Live')

    def take_picture(self):
        pass
    
    @QtCore.Slot(str)
    def print_log(self, message):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.ui.log.append("===== %s =====" % (current_time))
        if type(message) is dict:
            for key in message.keys():
                self.ui.log.append("%s = %s" % (key, message[key]))
        else:
            self.ui.log.append(str(message))
        self.ui.log.append("\n")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
