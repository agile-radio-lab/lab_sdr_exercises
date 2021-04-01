# -*- coding: utf-8 -*-
""" USRP receiver to json
"""

import argparse
import time
import numpy as np

import uhd

import utils
import uhd_utils

DEFAULT_SIGNAL_PATH = "recording.seq.json"
DEFAULT_USRP_CONFIG_PATH = "defaults/usrp.config.json"
DEFAULT_N_SAMPLES = 2000

DEFAULT_RECORDING_DELAY = 1.0


def main(args: argparse.Namespace):
    params = uhd_utils.USRPParams()
    params.import_config(args.config)

    usrp = uhd_utils.init_usrp_rx(params)
    streamer = uhd_utils.init_usrp_streamer_rx(usrp)

    n_samples = streamer.get_max_num_samps()
    buffer = np.empty((1, n_samples), dtype=np.complex64)
    samples = np.empty((1, args.n_samples), dtype=np.complex64)

    metadata = uhd.types.RXMetadata()
    stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
    streamer.issue_stream_cmd(stream_cmd)

    start_rx_time = time.time() + args.recording_delay

    running = True
    n_total_recv = 0
    while running and n_total_recv < args.n_samples:
        try:
            n_recv = streamer.recv(buffer, metadata)
            if metadata.error_code != uhd.types.RXMetadataErrorCode.none:
                print(metadata.strerror())

            if time.time() > start_rx_time and n_recv:
                n_write = min(args.n_samples - n_total_recv, n_recv)
                samples[:, n_total_recv:n_total_recv +
                        n_write] = buffer[:, 0:n_write]
                n_total_recv += n_write
        except KeyboardInterrupt:
            running = False
            print("Exiting...")

    stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
    streamer.issue_stream_cmd(stream_cmd)

    samples = np.array(samples[0], dtype=complex)
    utils.export_json(samples, args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RX Protocol Script')
    parser.add_argument('--output', type=str, default=DEFAULT_SIGNAL_PATH,
                        help=f'path to output signal file')
    parser.add_argument('--config', type=str, default=DEFAULT_USRP_CONFIG_PATH,
                        help=f'path to USRP configuration file')
    parser.add_argument('--n-samples', type=int, default=DEFAULT_N_SAMPLES,
                        help=f'number of samples to record')
    parser.add_argument('--recording-delay', type=float, default=DEFAULT_RECORDING_DELAY,
                        help=f'recording delay')

    args = parser.parse_args()

    main(args)
