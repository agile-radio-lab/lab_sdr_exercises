# -*- coding: utf-8 -*-
""" Sequence generator to json
"""

import argparse
import numpy as np

import utils
import seq_utils

DEFAULT_DEPTH = 1.0
DEFAULT_AMPLITUDE = 0.1
DEFAULT_PERIOD = 100
DEFAULT_N_SAMPLES = 2000
DEFAULT_PULSE_WIDTH = 10/3
DEFAULT_SEQ_PATH = "sample.seq.json"
DEFAULT_SEQ_TYPE = seq_utils.SEQ_TYPES[0]
DEFAULT_PSS_ROOT_ID = 0


def main(args: argparse.Namespace):
    if not args.seq in seq_utils.SEQS:
        print(
            f"{args.seq} is not a valid sequence type, choose from {seq_utils.SEQ_TYPES_STR}")
        return

    generator = seq_utils.SEQS[args.seq]
    samples: np.array = None

    if args.seq in ["cos_m"]:
        freq = 1 / args.period
        t = np.arange(args.n_samples, dtype=complex)
        samples = generator(t, freq, args.amplitude, args.depth)
    elif args.seq in ["exp", "negative_exp", "cos", "cos_sq","sin"]:
        freq = 1 / args.period
        t = np.arange(args.n_samples, dtype=complex)
        samples = generator(t, freq, args.amplitude)
    elif args.seq in ["ones", "zeros"]:
        samples = generator(args.n_samples)
    elif args.seq in ["rectangular"]:
        samples = generator(args.n_samples, args.period, args.pulse_width)
    elif args.seq in ["pss"]:
        samples = generator(args.pss_root_id)

    utils.export_json(samples, args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sequence generator')
    parser.add_argument('--output', type=str, default=DEFAULT_SEQ_PATH,
                        help=f'path to output file')
    parser.add_argument('--seq', type=str, default=DEFAULT_SEQ_TYPE,
                        help=f'signal type from {seq_utils.SEQ_TYPES_STR}')

    parser.add_argument('--depth', type=float, default=DEFAULT_DEPTH,
                        help=f'modulation depth')
    parser.add_argument('--amplitude', type=float, default=DEFAULT_AMPLITUDE,
                        help=f'signal amplitude')
    parser.add_argument('--period', type=int, default=DEFAULT_PERIOD,
                        help=f'period')
    parser.add_argument('--n-samples', type=int, default=DEFAULT_N_SAMPLES,
                        help=f'number of samples')

    parser.add_argument('--pss-root-id', type=int, default=DEFAULT_PSS_ROOT_ID,
                        help=f'pss root ID')

    parser.add_argument('--pulse-width', type=float, default=DEFAULT_PULSE_WIDTH,
                        help=f'pulse width')

    args = parser.parse_args()

    main(args)
