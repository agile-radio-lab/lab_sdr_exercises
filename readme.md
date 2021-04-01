# Laboratory Exercises

## List of Command Line Applications
* Sequence Generator
* Sequence Analyser
* USRP Transmitter
* USRP Receiver

## Sequence generator
Supported shapes, argument `--seq shape_type` and additional parameters
* ones, zeros: `--n-samples`
* rectangular: `--n-samples`, `--period`, `--pulse-width`
* exp, negative_exp, cos: `--n-samples`, `--period`, `--amplitude`

Usage:
```bash
python3 seq_gen.py --seq cos --n-samples 500 --output sample.seq.json
```

Generate all sequence samples:
```bash
./generate_all.sh
```

## Sequence Analyser
Usage:
```bash
python3 analyser.py --input sample.seq.json
```

## USRP Transmitter
Usage:
```bash
python3 usrp_tx.py --config defaults/usrp.config.json --input sample.seq.json
```

## USRP Receiver
Usage:
```bash
python3 usrp_rx.py --config defaults/usrp.config.json --output recording.seq.json
```
