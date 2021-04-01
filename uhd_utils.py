import json
import uhd

class USRPParams:
    _params = {
        "sampling_rate": 1e6,
        "gain": 76,
        "channel": 0,
        "freq": 900e6,
        "args": ""
    }

    def set_param(self, param: str, value: any):
        self._params[param] = value

    def get_param(self, param: str) -> any:
        return self._params[param]

    def export_config(self, path: str):
        with open(path, "w") as f:
            json.dump(self._params, f)

    def import_config(self, path: str):
        with open(path, "r") as f:
            self._params = json.load(f)

def init_usrp_rx(params: USRPParams) -> uhd.usrp.MultiUSRP:
    channel_id = params.get_param("channel")

    usrp = uhd.usrp.MultiUSRP()
    usrp.set_rx_rate(params.get_param("sampling_rate"), channel_id)
    usrp.set_rx_freq(uhd.types.TuneRequest(params.get_param("freq")), channel_id)
    usrp.set_rx_gain(params.get_param("gain"), channel_id)
    return usrp

def init_usrp_streamer_rx(usrp: uhd.usrp.MultiUSRP) -> uhd.libpyuhd.usrp.rx_streamer:
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    return usrp.get_rx_stream(st_args)

def init_usrp_tx(params: USRPParams) -> uhd.usrp.MultiUSRP:
    channel_id = params.get_param("channel")

    usrp = uhd.usrp.MultiUSRP()
    usrp.set_tx_rate(params.get_param("sampling_rate"), channel_id)
    usrp.set_tx_freq(uhd.types.TuneRequest(params.get_param("freq")), channel_id)
    usrp.set_tx_gain(params.get_param("gain"), channel_id)
    return usrp

def init_usrp_streamer_tx(usrp: uhd.usrp.MultiUSRP) -> uhd.libpyuhd.usrp.tx_streamer:
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    return usrp.get_tx_stream(st_args)