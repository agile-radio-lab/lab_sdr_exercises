import json
import numpy as np


def import_json(path: str) -> np.array:
    with open(path, "r") as read_file:
        iq_seq = json.load(read_file)

    return np.array(iq_seq['real']) + \
        np.array(iq_seq['imag']) * 1j

def export_json(signal_samples: np.array, path: str):
    data = {}
    data['real'] = list(np.real(signal_samples))
    data['imag'] = list(np.imag(signal_samples))

    with open(path, 'w') as f:
        json.dump(data, f, indent=4)