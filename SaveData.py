import csv
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image
import cv2
from Utils import *


def WriteSignal2CSV(_times, _signals, _output_dir):
    signal_data = []
    output_path = os.path.join(_output_dir, "signal.csv")
    with open(output_path, 'w') as f:
        writer = csv.writer(f)
        for i in range(len(_times)):
            writer.writerow([_times[i], _signals[i]])


def WriteSignal2Graph(_times, _signals, _output_dir):
    output_path = os.path.join(_output_dir, "signal.png")
    filtered_signals = ApplyMovingAverageFilter(_signals)
    plt.figure()
    plt.plot(_times[3:-3], filtered_signals[3:-3])
    plt.savefig(output_path)


def SaveTIFF(_u16_frames, _save_dir):
    save_path = os.path.join(_save_dir, "video.tiff")
    stack = []
    for u16_frame in _u16_frames:
        stack.append(Image.fromarray(u16_frame))
    stack[0].save(save_path, compression="tiff_deflate", save_all=True, append_images=stack[1:])


def SaveMP4(_u16_frames, _save_dir, _frame_rate):
    output_path = os.path.join(_save_dir, "video.mp4")
    size = (_u16_frames[0].shape[1], _u16_frames[0].shape[0])

    print(size)

    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(output_path, fmt, _frame_rate, size)  # ライター作成
    for u16_frame in _u16_frames:
        u16_frame = np.stack([u16_frame, u16_frame, u16_frame], axis=-1)
        u8_frame = Convert16to8bit(u16_frame)
        writer.write(u8_frame)  # 画像を1フレーム分として書き込み

    writer.release()  # ファイルを閉じる

