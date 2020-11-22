import numpy
import cv2
import threading
import time
from bitalino import BITalino
from flirpy.camera.boson import Boson
import os
from SaveData import *
from Utils import *
MAC_ADDRESS = "20:15:12:22:81:92"

# 実行時間
START = 10
END = 25
MEASURED_TIME = END - START
# サンプリングレート
SAMPLING_RATE = 100
# 取得チャネル（A3）
ACQUIRED_CHANNEL = [2]
# 取得サンプル数
N_SAMPLE = SAMPLING_RATE * (END-START)

SAVE_DIR = 'test_rr15'
if not os.path.exists(SAVE_DIR):
    os.mkdir(SAVE_DIR)
    txt_file = os.path.join(SAVE_DIR, "info.txt")

else:
    print("change directory")
    exit()


def workerForBItalino(output_dir=''):
    """15秒間のBItalinoデータを保存"""
    print("a")
    device = BITalino(MAC_ADDRESS)
    print(device.version())
    dt = 1 / SAMPLING_RATE

    _times = []
    _signals = []

    time.sleep(START)
    device.start(SAMPLING_RATE, ACQUIRED_CHANNEL)
    print("start bitalino")
    data = device.read(N_SAMPLE)
    print("end bitalino")
    for i in range(len(data)):
        _times.append(dt * i)
        _signals.append(data[i][-1])

    device.stop()
    device.close()
    time.sleep(5)

    with open(txt_file, 'a') as f:
        f.write("Sampling Rate={}\n".format(SAMPLING_RATE))
        f.write("RR={}\n".format(CalculateRR(_times, _signals, output_dir)))

    f.close()
    print("Number of signals", len(_signals))
    WriteSignal2CSV(_times, _signals, output_dir)
    WriteSignal2Graph(_times, _signals, output_dir)


def workerForBoson(output_dir=' '):
    """15秒間のThermalデータを保存"""
    print()
    camera = Boson()
    u16_frames = []
    _times = []
    initial_time = time.clock()
    while True:
        u16_frame = camera.grab(0)
        elapsed_time = time.clock()
        if elapsed_time - initial_time > END:
            print("time : ", elapsed_time-initial_time)
            break
        elif elapsed_time - initial_time > START:
            u16_frames.append(u16_frame)
            _times.append(elapsed_time-initial_time)

    fps = len(u16_frames)/MEASURED_TIME
    print("Number of frame : ", len(u16_frames))
    print("estimated fps : ", )
    with open(txt_file, 'a') as f:
        f.write("estimated fps={}\n".format(fps))
    f.close()
    SaveTIFF(u16_frames, output_dir)
    SaveMP4(u16_frames, output_dir, fps)


def generateDataset():
    t1 = threading.Thread(target=workerForBItalino, args=(SAVE_DIR, ))
    t2 = threading.Thread(target=workerForBoson, args=(SAVE_DIR, ))
    t1.start()
    t2.start()


generateDataset()

# workerForBItalino()
