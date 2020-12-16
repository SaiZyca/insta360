# coding=UTF-8

import requests
import os
from datetime import datetime
from PySide2 import QtCore
import socket

class SignalSystem(QtCore.QObject):
    log = QtCore.Signal(object)
    connect_state = QtCore.Signal(bool)
class InstaCamera(object):
    '''
    Insta360 Camera
    '''
    def __init__(self):

        self._fingerprint = ''
        self._status = ''
        self.connected = False
        self.post_dic = {}
        self.post_dic['headers'] = {}
        self.post_dic['headers']['content-type'] = 'application/json'
        self.rtmp_server = None
        self.camera_adress = None
        self.signals = SignalSystem()
        

    def inital_service(self, parm_dict):
        self.rtmp_server = parm_dict['rtsp_server']
        self.camera_adress = parm_dict['camera_ip']
        self.command_api = "%s%s" % (parm_dict['camera_ip'], ":20000/osc/commands/execute")
        self.state_api = "%s%s" % (parm_dict['camera_ip'], ":20000/osc/state")
        self.file_api = "%s%s" % (parm_dict['camera_ip'], ":8000")
        self.preview_api = "%s%s" % (parm_dict['camera_ip'], ":1935/live/preview")
        
        return self.rtmp_server, self.camera_adress

    def get_current_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def get_state(self):
        return self._status

    def ping_camera(self):
        results = False
        ip = self.camera_adress[7:]
        response = os.system("ping -c 1 " + ip)

        if response == 0:
            self.signals.log.emit("get ip and connecting....") 
            results = True
        else:
            self.signals.log.emit("Ping Camera Adress Fail") 
            results = False

        return results

    def connect_camera(self, parm_dict):
        self.inital_service(parm_dict)
        self.post_dic['json'] = {
            "name": "camera._connect",
            "parameters":
                {
                    "hw_time": "MMDDhhmm[[CC]YY][.ss]",
                    "time_zone": "GMT+08:00/GMT-08:00"
                }
        }

        if self.ping_camera():
            try:
                response = requests.post(self.command_api, **self.post_dic)
                if response.status_code == 200:
                    self.connected = True
                    results = (response.json())['results']
                    self._fingerprint = results['Fingerprint']
                    self._status = results['last_info']['state']
                    self.post_dic['headers']['Fingerprint'] = self._fingerprint
                    self.connected = True
                    self.signals.log.emit(results)
                else:
                    self.connected = False

            except Exception as e: 
                self.connected = False
                self.signals.log.emit(e)

            return self.connected 

    def camera_state(self, parm_dict):
        self.inital_service(parm_dict)
        response = requests.post(self.state_api, **self.post_dic)
        self.signals.log.emit(response.json()['state'])
        

    def start_preview(self, parm_dict):
        results = False
        if self.connected:
            self.post_dic['json'] = {
                "name": "camera._startPreview",
                "parameters": {
                    "origin": {
                        "mime": "h264",
                        "width": 1920,
                        "height": 1440,
                        "framerate": 30,
                        "bitrate": 20480 
                    },
                    "stiching": {
                        "mode": "pano",
                        "mime": "h264",
                        "width": 3840,
                        "height": 1920,
                        "framerate": 30, 
                        "bitrate": 10240 
                    },
                    "audio": {
                    "mime":'aac', 
                    "sampleFormat":'s16',
                    "channelLayout":'stereo',
                    "samplerate":48000,
                    "bitrate":128
                    }
                },
                "stabilization": True
            }
            try:
                response = requests.post(self.command_api, **self.post_dic)
                if response.status_code == 200:
                    self.signals.log.emit(response.json())
                    self.signals.log.emit("previe url: rtsp://%s/live/preview" % (self.camera_adress[7:]) )
                    results = True
                else:
                    self.signals.log.emit(response.json())
                    results =  False
            except Exception as e: 
                self.connected = False
                self.signals.log.emit(e)
            
            return results
            

    def stop_preview(self):
         if self.connected:
            self.post_dic['json'] = {"name": "camera._stopPreview"}
            try:
                response = requests.post(self.command_api, **self.post_dic)
                if response.status_code == 200:
                    self.signals.log.emit(response.json())
                    results = True
                else:
                    self.signals.log.emit(response.json())
                    results =  False
            except Exception as e: 
                self.connected = False
                self.signals.log.emit(e)
            
            return results
            

    def get_option(self):
        self.post_dic['json'] = {
            "name": "camera._getOptions",
            "parameters": {
                "property": "origin"
            }
        }
        response = requests.post(self.command_api, **self.post_dic)
        return response

    def start_live(self, parm_dict):
        liveUrl = "%s/live" % (self.rtmp_server) 

        if self.connected:
            self.post_dic['json'] = {
                "name": "camera._startLive",
                "parameters": {
                    "origin": {
                        "mime": "h265",
                        "width": 3840,
                        "height": 2160, #2880 for max size,2160 for stitching
                        "framerate": 30,
                        "bitrate": 20480,
                        "liveUrl": liveUrl,
                        "saveOrigin": False 
                    },
                    # "stiching": {
                    #     "mode": "pano",
                    #     "mime": "h264",
                    #     "width": 3840, # 3840*1920 for normal, 7680*3840 for max
                    #     "height": 1920,
                    #     "framerate": 30, 
                    #     "bitrate": 10240,
                    #     "_liveUrl": "rtsp://192.168.1.111:8554/live/stitch"
                    # },
                    "audio": {
                    "mime":'aac', 
                    "sampleFormat":'s16',
                    "channelLayout":'stereo',
                    "samplerate":48000,
                    "bitrate":64
                    },
                    "autoConnect":{
                    "enable": True, 
                    "interval": 5,
                    "count": 3
                    }
                },
                "stabilization": False,
                "mode": "origin live"
            }

        try:
            response = requests.post(self.command_api, **self.post_dic)
            if response.status_code == 200:
                self.signals.log.emit(response.json())
                results = True
            else:
                self.signals.log.emit(response.json())
                results =  False
        except Exception as e: 
            self.connected = False
            self.signals.log.emit(e)
        
        return results

    def stop_live(self):
         if self.connected:
            self.post_dic['json'] = {"name": "camera._stopLive"}
            try:
                response = requests.post(self.command_api, **self.post_dic)
                if response.status_code == 200:
                    self.signals.log.emit(response.json())
                    results = True
                else:
                    self.signals.log.emit(response.json())
                    results =  False
            except Exception as e: 
                self.connected = False
                self.signals.log.emit(e)
        
            return results

                
    def get_image_param(self):
        self.post_dic['json'] = {"name": "camera._getImageParam"}
        response = requests.post(self.command_api, **self.post_dic)
        self._status = response
        return response
