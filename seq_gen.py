# -*- coding: utf-8 -*-
""" Sequence generator to json
"""

import argparse
import numpy as np

import utils

DEFAULT_AMPLITUDE = 0.5
DEFAULT_PERIOD = 10
DEFAULT_N_SAMPLES = 100
DEFAULT_PULSE_WIDTH = 10/3
DEFAULT_SEQ_PATH = "sample.seq.json"

ZADOFF_CHU_ROOTS = [25,29,34]
PSS_LENGTH = 61

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

def seq_cos_sq(t: np.array, freq: float, amp: float) -> np.array:
    cos_samples = seq_cos(t, freq, amp)
    return cos_samples**2

def seq_pss(root_id: int = 0) -> np.array:
    root = ZADOFF_CHU_ROOTS[root_id]
    pss_seq = np.arange(PSS_LENGTH, dtype=complex)
    pss_seq[:31] = np.exp((-1j*np.pi*root*pss_seq[:31]*(pss_seq[:31]+1))/63)
    pss_seq[31:62] = np.exp((-1j*np.pi*root*(pss_seq[31:62]+1)*(pss_seq[31:62]+2))/63)
    return pss_seq

seqs = {
    "ones": seq_ones,
    "zeros": seq_zeros,
    "rectangular": seq_rectangular,
    "exp": seq_exp,
    "negative_exp": seq_negative_exp,
    "cos": seq_cos,
    "cos_sq": seq_cos_sq,
    "pss": seq_pss
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

    if args.seq in ["exp", "negative_exp", "cos", "cos_sq"]:
        freq = 1 / args.period
        t = np.arange(args.n_samples, dtype=complex)
        samples = generator(t, freq, args.amplitude)
    elif args.seq in ["ones", "zeros"]:
        samples = generator(args.n_samples)
    elif args.seq in ["rectangular"]:
        samples = generator(args.n_samples, args.period, args.pulse_width)
    elif args.seq in ["pss"]:
        samples = generator()

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

