# coding=UTF-8

import requests
# import base64
# import logging

class InstaCamera(object):
    '''
    Insta360 Camera
    '''
    def __init__(self):

        self._connected = False
        self._fingerprint = ''
        self._status = ''

        self.server = "http://192.168.1.195"
        self.command_api = "%s%s" % (self.server, ":20000/osc/commands/execute")
        self.state_api = "%s%s" % (self.server, ":20000/osc/state")
        self.file_api = "%s%s" % (self.server, ":8000")
        self.preview_api = "%s%s" % (self.server, ":1935/live/preview")
        self.post_dic = {}
        self.post_dic['headers'] = {}
        self.post_dic['headers']['content-type'] = 'application/json'
        

    def state(self):
        response = requests.get(self.state_api)
        return response

    def connect(self):

        self.post_dic['json'] = {
            "name": "camera._connect",
            "parameters":
                {
                    "hw_time": "MMDDhhmm[[CC]YY][.ss]",
                    "time_zone": "GMT+08:00/GMT-08:00"
                }
        }

        response = requests.post(self.command_api, **self.post_dic)
        if response.status_code == 200:
            self._connected = True
            results = (response.json())['results']
            self._fingerprint = results['Fingerprint']
            self._status = results['last_info']['state']
            self.post_dic['headers']['Fingerprint'] = self._fingerprint
            # self._fingerprint = response.json()['responses']['Fingerprint']
            return response

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
            return response

    def stop_preview(self):
         if self._connected:
            self.post_dic['json'] = {"name": "camera._stopPreview"}

            response = requests.post(self.command_api, **self.post_dic)
            return response       

    def get_option(self):
        self.post_dic['json'] = {
            "name": "camera._getOptions",
            "parameters": {
                "property": "origin"
            }
        }
        response = requests.post(self.command_api, **self.post_dic)
        return response

    def start_live(self):
        if self._connected:
            self.post_dic['json'] = {
                "name": "camera._startLive",
                "parameters": {
                    "origin": {
                        "mime": "h264",
                        "width": 1920,
                        "height": 1440,
                        "framerate": 30,
                        "bitrate": 20480,
                        "liveUrl": "rtsp://192.168.1.23:8554/live"
                    },
                    # "stiching": {
                    #     "mode": "pano",
                    #     "mime": "h264",
                    #     "width": 3840,
                    #     "height": 1920,
                    #     "framerate": 30, 
                    #     "bitrate": 10240,
                    #     "_liveUrl": "rtsp://192.168.1.23:8554/live/live"
                    # },
                    "audio": {
                    "mime":'aac', 
                    "sampleFormat":'s16',
                    "channelLayout":'stereo',
                    "samplerate":48000,
                    "bitrate":128
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
            response = requests.post(self.command_api, **self.post_dic)
            return response

    def stop_live(self):
         if self._connected:
            self.post_dic['json'] = {"name": "camera._stopLive"}

            response = requests.post(self.command_api, **self.post_dic)
            return response      

    def get_image_param(self):
        self.post_dic['json'] = {"name": "camera._getImageParam"}
        response = requests.post(self.command_api, **self.post_dic)
        return response

insta = InstaCamera()
insta.connect()
print (insta.stop_live().json())
# print (insta.start_live().json())
# print (insta._status)
# insta.stop_preview()
# print (insta.start_preview().json())

# print (insta.stop_preview().json())