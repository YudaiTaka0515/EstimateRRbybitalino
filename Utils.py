import csv
import numpy as np
from scipy import signal
from scipy.fftpack import fft
from PIL import Image
from SaveData import *
import cv2


def Convert16to8bit(images_u16):
    maxV, minV = np.amax(images_u16), np.amin(images_u16)
    # maxV, minV = (60000, 50000)
    # print(maxV, minV)
    alpha = 255.0 / (maxV - minV)
    images_u8 = np.add(images_u16, -minV)
    images_u8 = images_u8 * alpha
    images_u8 = images_u8.astype(np.uint8)
    return images_u8


def ApplyMovingAverageFilter(signal, num=5):
    # 移動平均の個数
    b = np.ones(num) / num

    preprocessed_signal = np.convolve(signal, b, mode='same')  # 移動平均

    return preprocessed_signal


def ConvertTiff2Numpy(_src_path):
    pil_images = Image.open(_src_path)
    n_frame = pil_images.n_frames
    print("shape : ", pil_images.size)
    height, width = pil_images.height, pil_images.width
    np_images = np.zeros((height, width, n_frame), dtype='uint16')

    print("n_frame : ", n_frame)
    list_images = []
    for i in range(n_frame):
        pil_images.seek(i)
        np_images[:, :, i] = np.asarray(pil_images.copy())
        u8_image = Convert16to8bit(np_images[:, :, i])
        plt.imshow(u8_image)
        plt.show()

    print("shape : ", np_images.shape)
    return np_images


def CalculateRR(_times, _signals, output_dir):
    output_path = os.path.join(output_dir, "fourier.png")
    N = len(_times)
    _signals = _signals - np.mean(_signals)
    _signals = signal.detrend(_signals)
    dt = _times[-1] - _times[-2]
    frequency = np.linspace(0, 1.0 / dt, N)
    signal_f = fft(_signals) / (N / 2)
    signal_f = np.abs(signal_f)
    plt.figure()
    plt.plot(frequency, signal_f)
    plt.savefig(output_path)
    for i in range(100):
        index = np.where(signal_f == np.sort(signal_f)[-i])
        rr_candidates = frequency[index]
        # print(rr_candidates)
        for rr_candidate in rr_candidates:
            if (rr_candidate > 0.1) and (rr_candidate < 2):
                return rr_candidate*60

    print("Error")
    return -1


if __name__ == '__main__':
    tiff_path = 'test1/video.tiff'
    csv_path = 'test1/signal.csv'
    times = []
    signals = []

    with open(csv_path) as f:
        _reader = csv.reader(f)
        for row in _reader:
            if len(row) != 0:
                times.append(float(row[0]))
                signals.append(float(row[1]))

    print(times)
    print(signals)
    ConvertTiff2Numpy(tiff_path)
    RR = CalculateRR(times, signals)
    print(RR)
