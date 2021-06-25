import numpy as np


def fft(samples: np.array, fft_size: int):
    result = np.fft.fft(samples, fft_size)
    result = np.fft.fftshift(result)
    return result



def psd(samples, fft_size: int):
    window = np.hamming(fft_size)
    result = np.multiply(window, samples)
    result = np.fft.fft(result, fft_size)
    result = np.fft.fftshift(result)
    result = np.square(np.abs(result))
    result = np.nan_to_num(10.0 * np.log10(result))
    return result

def calc_fft_psd(real,imag,fft_size):
    samples = [complex(real[x],imag[x]) for x in range(len(real))]
    n_fft_steps = int(np.floor(len(samples)/fft_size))
    freq_result = np.zeros([n_fft_steps, fft_size])
    for i in range(n_fft_steps):
        bins = psd(samples[i*fft_size:(i+1)*fft_size],fft_size)
        freq_result[i] = bins
    return np.mean(freq_result, axis=0)
    