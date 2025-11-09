import numpy as np
from scipy.io import wavfile

def load_audio(file_path):
    """Loads a .wav file and normalizes it."""
    rate, data = wavfile.read(file_path)

    # Convert stereo to mono if needed
    if len(data.shape) == 2:
        data = data.mean(axis=1)

    # Normalize amplitude to range [-1, 1]
    data = data / np.max(np.abs(data))
    return rate, data

def chunk_signal(signal, chunk_size):
    """Divides the signal into smaller overlapping segments."""
    for i in range(0, len(signal), chunk_size):
        yield signal[i:i + chunk_size]
