# -*- coding: utf-8 -*-
""" Sequence generator to json
"""

__author__ = "Igor Kim"
__credits__ = ["Igor Kim"]
__maintainer__ = "Igor Kim"
__email__ = "igor.skh@gmail.com"
__status__ = "Development"
__date__ = "04/2021"
__license__ = ""

import argparse
import numpy as np

import utils

DEFAULT_AMPLITUDE = 0.5
DEFAULT_PERIOD = 10
DEFAULT_N_SAMPLES = 100
DEFAULT_PULSE_WIDTH = 10/3
DEFAULT_SEQ_PATH = "sample.seq.json"


def seq_ones(n_samples: int) -> np.array:
    return np.ones(n_samples)

def seq_zeros(n_samples: int) -> np.array:
    return np.zeros(n_samples)

def seq_rectangular(n_samples: int, period: float, pulse_width: float) -> np.array:
    rect = np.arange(n_samples) % period < pulse_width
    return [float(sample) for sample in rect]

def seq_exp(t: np.array, freq: float, amp: float) -> np.array:
    return amp*np.exp(2j*np.pi*freq*t)

def seq_negative_exp(t: np.array, freq: float, amp: float) -> np.array:
    return amp*np.exp(-2j*np.pi*freq*t)

def seq_cos(t: np.array, freq: float, amp: float) -> np.array:
    return amp*np.cos(2*np.pi*freq*t)


seqs = {
    "ones": seq_ones,
    "zeros": seq_zeros,
    "rectangular": seq_rectangular,
    "exp": seq_exp,
    "negative_exp": seq_negative_exp,
    "cos": seq_cos
}
seq_types = list(seqs.keys())
seq_types_str = ", ".join(seq_types)
DEFAULT_SEQ_TYPE = seq_types[0]


def main(args: argparse.Namespace):
    if not args.seq in seqs:
        print(f"{args.seq} is not a valid sequence type, choose from {seq_types_str}")
        return

    generator = seqs[args.seq]
    samples: np.array = None

    if args.seq in ["exp", "negative_exp", "cos"]:
        freq = 1 / args.period
        t = np.arange(args.n_samples, dtype=np.complex)
        samples = generator(t, freq, args.amplitude)
    elif args.seq in ["ones", "zeros"]:
        samples = generator(args.n_samples)
    elif args.seq in ["rectangular"]:
        samples = generator(args.n_samples, args.period, args.pulse_width)

    utils.export_json(samples, args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sequence generator')
    parser.add_argument('--output', type=str, default=DEFAULT_SEQ_PATH,
                        help=f'path to output file')
    parser.add_argument('--seq', type=str, default=DEFAULT_SEQ_TYPE,
                        help=f'signal type from {seq_types_str}')

    parser.add_argument('--amplitude', type=float, default=DEFAULT_AMPLITUDE,
                        help=f'signal amplitude')
    parser.add_argument('--period', type=int, default=DEFAULT_PERIOD,
                        help=f'period')
    parser.add_argument('--n-samples', type=int, default=DEFAULT_N_SAMPLES,
                        help=f'source freq')
                        
    parser.add_argument('--pulse-width', type=float, default=DEFAULT_PULSE_WIDTH,
                        help=f'pulse width')

    args = parser.parse_args()

    main(args)

