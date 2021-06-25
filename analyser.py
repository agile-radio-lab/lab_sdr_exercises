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

    
    fig = plt.figure(figsize=(10, 10))

    
    # Real
    ax = plt.subplot(2, 2, 1)
    plt.plot(samples.real,".")
    plt.ylabel("Real")
    #plt.xlabel("N-Samples")
    plt.grid(True)


    # Imaginary
    ax = plt.subplot(2, 2, 3)
    plt.plot(samples.imag,".")
    plt.ylabel("Imaginary")
    plt.xlabel("N-Samples")
    plt.grid(True)


    # Z-Plane 
    ax = plt.subplot(2, 2, 2)
    plt.plot(samples.real, samples.imag, "r.")
    plt.xlabel("In-Phase")
    plt.ylabel("Quadrature")
    plt.grid(True)


    # FFT
    ax = plt.subplot(2, 2, 4)
    fft_result_pss = dsp_utils.calc_fft_psd(samples.real, samples.imag, args.fft_size)
    plt.plot(fft_result_pss.real)#, ".")
    plt.xlabel("FFT size")
    plt.grid(True)


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
