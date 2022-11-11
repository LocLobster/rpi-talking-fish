#!/usr/bin/python3
import os
import math
import struct
import subprocess
import tempfile
import mouth_motor_controller

mc = mouth_motor_controller.MouthMotorController()

BARS_NUMBER = 5
OUTPUT_BIT_FORMAT = "16bit"
RAW_TARGET = "/dev/stdout"

conpat = """
[general]
framerate = 60
autosens = 0
sensitivity = 5
bars = %d
sleep_timer = 0

[output]
channels = mono
method = raw
raw_target = %s
bit_format = %s

[smoothing]
monstercat = 0
waves = 0
ignore = 0
noise_reduction = 0
"""
config = conpat % (BARS_NUMBER, RAW_TARGET, OUTPUT_BIT_FORMAT)
bytetype, bytesize, bytenorm = ("H", 2, 65535) if OUTPUT_BIT_FORMAT == "16bit" else ("B", 1, 255)
THRESHOLD = 20

def analyze(sample):
    output = math.trunc((sample[2] + sample[3] + sample[4] - (sample[0] + sample[1]))*1000)
    if output > THRESHOLD:
        #print(output)
        mc.mouth_open()
    else:
        mc.mouth_stop()
        pass

def run():
    with tempfile.NamedTemporaryFile() as config_file:
        config_file.write(config.encode())
        config_file.flush()

        process = subprocess.Popen(["cava", "-p", config_file.name], stdout=subprocess.PIPE)
        chunk = bytesize * BARS_NUMBER
        fmt = bytetype * BARS_NUMBER

        if RAW_TARGET != "/dev/stdout":
            if not os.path.exists(RAW_TARGET):
                os.mkfifo(RAW_TARGET)
            source = open(RAW_TARGET, "rb")
        else:
            source = process.stdout

        while True:
            data = source.read(chunk)
            if len(data) < chunk:
                break
            sample = [i / bytenorm for i in struct.unpack(fmt, data)]
            analyze(sample)

if __name__ == "__main__":
    run()
