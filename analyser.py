# -*- coding: utf-8 -*-
""" IQ samples analyser
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt

import utils
import dsp_utils

DEFAULT_OFFSET = 0
DEFAULT_N_SAMPLES = 0
DEFAULT_SIGNAL_PATH = "signals/ones.seq.json"
DEFAULT_FFT_SIZE = 1024


def main(args: argparse.Namespace):
    samples = utils.import_json(args.input)
    if args.n_samples > 0:
        samples = samples[args.offset:args.offset+args.n_samples]

    fft_result = dsp_utils.fft(samples, args.fft_size)

    fig, ax = plt.subplots(1, 4)
    ax[0].plot(samples.real)
    ax[1].plot(samples.imag)

    ax[2].scatter(samples.real, samples.imag)
    ax[3].plot(fft_result.real)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyser Protocol Script')

    parser.add_argument('--input', type=str, default=DEFAULT_SIGNAL_PATH,
                        help=f'path to input signal file')
    parser.add_argument('--fft-size', type=int, default=DEFAULT_FFT_SIZE,
                        help=f'FFT Size')
    parser.add_argument('--offset', type=int, default=DEFAULT_OFFSET,
                        help=f'samples offset')
    parser.add_argument('--n-samples', type=int, default=DEFAULT_N_SAMPLES,
                        help=f'number of samples to analyse')

    args = parser.parse_args()

    main(args)
