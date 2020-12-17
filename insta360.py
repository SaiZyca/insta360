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
        self.resolution_dict = {
            0: {'text': "3840x2880@30fps", 'width': 3840, 'height': 2880, 'fps': 30},
            1: {'text': "3840x2160@60fps", 'width': 3840, 'height': 2160, 'fps': 60},
            2: {'text': "3840x2160@30fps", 'width': 3840, 'height': 2160, 'fps': 30},
            3: {'text': "3840x1920@60fps", 'width': 3840, 'height': 1920, 'fps': 60},
            4: {'text': "3200x2400@30fps", 'width': 3200, 'height': 2400, 'fps': 30},
            5: {'text': "1920x1440@30fps", 'width': 1920, 'height': 1440, 'fps': 30},
            6: {'text': "1920x1440@120fps", 'width': 1920, 'height': 1440, 'fps': 120}
        }

    def connect_ui_signal(self):
        self.camera.signals.log.connect(self.print_log)
        self.ui.connect_camera.toggled.connect(self.connect_camera)
        self.ui.start_live.clicked.connect(self.start_live)
        self.ui.start_preview.clicked.connect(self.start_preview)
        self.ui.live_stiching.toggled.connect(self.live_stiching)
        # self.ui.take_picture.clicked.connect(self.test_signal)

    def connect_camera(self):
        self.set_camera_parm()
        button = self.ui.connect_camera
        if button.text() == "Connect Camera":
            button.setChecked(self.camera.connect_camera(self.parm_dict))
        else:
            button.setChecked(False)
        ui_text = {True:"Disconnect Camera....", False:"Connect Camera"}
        button.setText(ui_text[button.isChecked()])

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
        button = self.ui.start_preview
        self.camera.connect_camera(self.parm_dict)
        if button.text() == "Satrt Preview":
            button.setChecked(self.camera.start_preview(self.parm_dict))
        else:
            self.camera.stop_preview()
            button.setChecked(False)

        ui_text = {True:"Stop Preview", False:"Satrt Preview"}
        button.setText(ui_text[button.isChecked()])
            
    def live_stiching(self):

        self.ui.resolution.setCurrentIndex(5)

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
