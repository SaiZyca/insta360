# coding=UTF-8

import requests
from datetime import datetime

class InstaCamera(object):
    '''
    Insta360 Camera
    '''
    def __init__(self):

        self._connected = False
        self._fingerprint = ''
        self._status = ''
        self.post_dic = {}
        self.post_dic['headers'] = {}
        self.post_dic['headers']['content-type'] = 'application/json'
        self.rtmp_server = "rtsp://localhost:8554"
        self.camera_adress = ""
        self.inital_services()

    def inital_services(self):
        self.command_api = "%s%s" % (self.camera_adress, ":20000/osc/commands/execute")
        self.state_api = "%s%s" % (self.camera_adress, ":20000/osc/state")
        self.file_api = "%s%s" % (self.camera_adress, ":8000")
        self.preview_api = "%s%s" % (self.camera_adress, ":1935/live/preview")
        
        return self.camera_adress

    def get_current_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def set_camera_adress(self, value):
        self.camera_adress = value
        self.inital_services()

    def set_rtmp_server(self, value):
        self.rtmp_server = value
        self.inital_services()

    def get_state(self):
        return self._status

    def connect(self):
        self.post_dic['json'] = {
            "name": "camera._connect",
            "parameters":
                {
                    "hw_time": "MMDDhhmm[[CC]YY][.ss]",
                    "time_zone": "GMT+08:00/GMT-08:00"
                }
        }

        print ("camera ip: %s \n rtsp server:%s" % (self.camera_adress, self.rtmp_server))

        try:
            response = requests.post(self.command_api, **self.post_dic)
            if response.status_code == 200:
                self._connected = True
                results = (response.json())['results']
                self._fingerprint = results['Fingerprint']
                self._status = results['last_info']['state']
                self.post_dic['headers']['Fingerprint'] = self._fingerprint
                # self._fingerprint = response.json()['responses']['Fingerprint']
                self._status = ("response at :%s \n %s" % (self.get_current_time(), response.text) )
                return response
        except Exception as e: 
            self._status = e

    def start_preview(self):
        if self._connected:
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
                "stabilization": False
            }
            response = requests.post(self.command_api, **self.post_dic)
            self._status = response
            return response
            

    def stop_preview(self):
         if self._connected:
            self.post_dic['json'] = {"name": "camera._stopPreview"}

            response = requests.post(self.command_api, **self.post_dic)
            self._status = response
            return response
            

    def get_option(self):
        self.post_dic['json'] = {
            "name": "camera._getOptions",
            "parameters": {
                "property": "origin"
            }
        }
        response = requests.post(self.command_api, **self.post_dic)
        self._status = response
        return response
        

    def start_live(self):
        liveUrl = "%s/live" % (self.rtmp_server) 
        print (liveUrl)
        if self._connected:
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
            self._status = ("response at :%s \n %s" % (self.get_current_time(), response.text) )
            return response
        except Exception as e: 
            self._status = e

    def stop_live(self):
         if self._connected:
            self.post_dic['json'] = {"name": "camera._stopLive"}
            try:
                response = requests.post(self.command_api, **self.post_dic)
                self._status = ("response at :%s \n %s" % (self.get_current_time(), response.text) )
                return response      
            except Exception as e: 
                self._status = e
                
    def get_image_param(self):
        self.post_dic['json'] = {"name": "camera._getImageParam"}
        response = requests.post(self.command_api, **self.post_dic)
        self._status = response
        return response
