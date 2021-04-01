# -*- coding: utf-8 -*-
""" USRP transmitter from json
"""

import argparse
import time
import numpy as np
import matplotlib.pyplot as plt

import uhd

import utils
import uhd_utils

DEFAULT_SIGNAL_PATH = "signals/ones.seq.json"
DEFAULT_USRP_CONFIG_PATH = "defaults/usrp.config.json"
DEFAULT_SLEEP_TIME = 0.1
DEFAULT_TX_TIME = 0.1


def main(args: argparse.Namespace):
    sleep_time = args.sleep_time
    tx_time = args.tx_time

    params = uhd_utils.USRPParams()
    params.import_config(args.config)

    samples = utils.import_json(args.input)
    samples = np.array(samples, np.complex64)

    usrp = uhd_utils.init_usrp_tx(params)
    streamer = uhd_utils.init_usrp_streamer_tx(usrp)

    if sleep_time > 0:
        next_sleep_time = time.time() + tx_time

    running = True
    metadata = uhd.types.TXMetadata()
    while running:
        try:
            streamer.send(samples, metadata)

            if sleep_time > 0 and time.time() > next_sleep_time:
                time.sleep(sleep_time)
                next_sleep_time = time.time() + tx_time
        except KeyboardInterrupt:
            running = False
            print("Exiting...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TX Protocol Script')
    parser.add_argument('--input', type=str, default=DEFAULT_SIGNAL_PATH,
                        help=f'path to input signal file')
    parser.add_argument('--config', type=str, default=DEFAULT_USRP_CONFIG_PATH,
                        help=f'path to USRP configuration file')

    parser.add_argument('--sleep-time', type=float, default=DEFAULT_SLEEP_TIME,
                        help=f'path to USRP configuration file')
    parser.add_argument('--tx-time', type=float, default=DEFAULT_TX_TIME,
                        help=f'path to USRP configuration file')

    args = parser.parse_args()

    main(args)
