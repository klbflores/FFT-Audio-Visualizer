import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import load_audio, chunk_signal
import sounddevice as sd
import time

def compute_fft(chunk):
    """Computes the FFT and returns magnitude spectrum."""
    fft_result = np.fft.fft(chunk)
    magnitude = np.abs(fft_result[:len(fft_result)//2])  # one-sided spectrum
    peak = np.max(magnitude)
    if peak > 0:
        magnitude = magnitude / peak  # normalize
    return magnitude

def visualize_audio(file_path, chunk_size=1024, num_bars=64, max_duration=None, play_audio=True):
    rate, data = load_audio(file_path)

    # Apply time limit if specified
    if max_duration is not None:
        max_samples = int(rate * max_duration)
        if len(data) > max_samples:
            data = data[:max_samples]
            print(f"Audio trimmed to {max_duration} seconds for visualization.")

    chunks = list(chunk_signal(data, chunk_size))
    
    # Calculate audio duration
    audio_duration = len(data) / rate
    # Calculate number of frames based on audio duration (50ms per frame)
    interval_ms = 50
    expected_frames = int((audio_duration * 1000) / interval_ms)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(np.arange(num_bars), np.zeros(num_bars), width=0.8)
    ax.set_ylim(0, 1)
    ax.set_xlim(0, num_bars)
    ax.set_xlabel("Frequency Bands")
    ax.set_ylabel("Magnitude")
    ax.set_title("Real-Time FFT Audio Visualizer")

    # Track audio stream and start time
    audio_stream = None
    start_time = None
    # Use a list to hold animation reference (mutable container)
    ani_ref = [None]

    def update(frame):
        # Check if audio is still playing
        if play_audio and audio_stream is not None:
            try:
                # Check if stream is still active
                if not audio_stream.active:
                    # Audio finished, stop animation
                    if ani_ref[0] is not None:
                        ani_ref[0].event_source.stop()
                    return bars
            except:
                pass
        
        # Check if we've exceeded audio duration
        if play_audio and start_time is not None:
            elapsed = time.time() - start_time
            if elapsed >= audio_duration:
                if ani_ref[0] is not None:
                    ani_ref[0].event_source.stop()
                return bars

        # Update visualization
        chunk = chunks[frame % len(chunks)]
        magnitude = compute_fft(chunk)

        # Group frequencies into visual bars
        grouped = np.array_split(magnitude, num_bars)
        avg_values = [np.mean(g) for g in grouped]

        for bar, val in zip(bars, avg_values):
            bar.set_height(val)
            bar.set_color(plt.cm.plasma(val))

        return bars

    if play_audio:
        try:
            sd.stop()  # Stop any currently playing audio
            audio_stream = sd.play(data.astype(np.float32), samplerate=rate, blocking=False)
            start_time = time.time()
        except Exception as e:
            print(f"Audio playback failed: {e}")

    # Use the minimum of expected frames and available chunks
    frames_to_use = min(expected_frames, len(chunks))
    ani = FuncAnimation(fig, update, frames=frames_to_use,
                        interval=interval_ms, blit=False, repeat=False)
    ani_ref[0] = ani  # Store reference for update function
    plt.tight_layout()
    plt.show()

    if play_audio:
        sd.stop()