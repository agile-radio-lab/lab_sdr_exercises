import numpy as np


def fft(samples: np.array, fft_size: int):
    window = np.hamming(samples.shape[0])
    result = np.multiply(window, samples)
    result = np.fft.fft(result, fft_size)
    result = np.fft.fftshift(result)
    return result
