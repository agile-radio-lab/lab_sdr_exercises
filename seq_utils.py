import numpy as np

ZADOFF_CHU_ROOTS = [25, 29, 34]
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

def seq_sin(t: np.array, freq: float, amp: float) -> np.array:
    return amp*np.sin(2*np.pi*freq*t)


def seq_cos_m(t: np.array, freq: float, amp: float, m: float) -> np.array:
    return amp*(1+m*np.cos(2*np.pi*freq*t))


def seq_cos_sq(t: np.array, freq: float, amp: float) -> np.array:
    cos_samples = seq_cos(t, freq, amp)
    return cos_samples**2


def seq_pss(root_id: int = 0) -> np.array:
    root = ZADOFF_CHU_ROOTS[root_id]
    pss_seq = np.arange(PSS_LENGTH, dtype=complex)
    pss_seq[:31] = np.exp((-1j*np.pi*root*pss_seq[:31]*(pss_seq[:31]+1))/63)
    pss_seq[31:62] = np.exp(
        (-1j*np.pi*root*(pss_seq[31:62]+1)*(pss_seq[31:62]+2))/63)
    return pss_seq


SEQS = {
    "ones": seq_ones,
    "zeros": seq_zeros,
    "rectangular": seq_rectangular,
    "exp": seq_exp,
    "negative_exp": seq_negative_exp,
    "cos": seq_cos,
    "cos_sq": seq_cos_sq,
    "pss": seq_pss,
    "cos_m": seq_cos_m,
    "sin":seq_sin
}
SEQ_TYPES = list(SEQS.keys())
SEQ_TYPES_STR = ", ".join(SEQ_TYPES)
