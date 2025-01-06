
from random import random
import subprocess
import os, random
from contextlib import contextmanager


#		    Created by Aero25x
#		      For HiddenCode
#
#		https://t.me/hidden_coding
#
#
#      _    _ _     _     _             _____          _
#     | |  | (_)   | |   | |           / ____|        | |
#     | |__| |_  __| | __| | ___ _ __ | |     ___   __| | ___
#     |  __  | |/ _` |/ _` |/ _ \ '_ \| |    / _ \ / _` |/ _ \
#     | |  | | | (_| | (_| |  __/ | | | |___| (_) | (_| |  __/
#     |_|  |_|_|\__,_|\__,_|\___|_| |_|\_____\___/ \__,_|\___|
#
#
#	For More Software and bots visit Our Market:
#		https://t.me/hcmarket_bot
#
#



class Xvfb:
    def __init__(self, width=410, height=900, colordepth=24):
        self.width = width
        self.height = height
        self.colordepth = colordepth
        self.process = None

    def start(self):

        hiddenCode_uid = str(random.randint(50, 99))


        cmd = [
            'Xvfb',
            f':{random_uid}',
            '-screen',
            '0',
            f'{self.width}x{self.height}x{self.colordepth}'
        ]
        self.process = subprocess.Popen(cmd)
        os.environ['DISPLAY'] = f':{hiddenCode_uid}'

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()




@contextmanager
def conditional_xvfb(use_xvfb, width=360, height=840, colordepth=24):
    if use_xvfb:
        with Xvfb(width=width, height=height, colordepth=colordepth) as xvfb:
            yield xvfb
    else:
        yield None
