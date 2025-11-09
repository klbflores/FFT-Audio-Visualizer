import math
import time

import numpy as np

from visualizer import compute_fft

# ---------- TEST 1: Signal Reconstruction ----------
x = np.random.rand(8)  # random signal vector
X = np.fft.fft(x)       # FFT
x_reconstructed = np.fft.ifft(X)  # inverse FFT

print("Test 1: FFT Reconstruction Check")
print("Original signal:", x)
print("Reconstructed:", np.round(x_reconstructed.real, 5))
print("Reconstruction accurate?", np.allclose(x, x_reconstructed.real))
print("\n")

# ---------- TEST 2: Energy Preservation (Parseval's Relation) ----------
energy_time = np.sum(np.abs(x)**2)
energy_freq = np.sum(np.abs(X)**2) / len(X)

print("Test 2: Parseval's Theorem Check")
print("Energy in time domain:", energy_time)
print("Energy in frequency domain:", energy_freq)
print("Energies approximately equal?", np.isclose(energy_time, energy_freq))

# ---------- TEST 3: Frequency Peak Verification ----------

# Sampling setup
fs = 44100           # Sampling frequency (Hz)
duration = 1.0       # Duration in seconds
f_target = 440       # Target frequency (Hz) — A4 note
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Generate a pure sine wave at 440 Hz
x = np.sin(2 * np.pi * f_target * t)

# Perform FFT
X = np.fft.fft(x)
N = len(X)
freqs = np.fft.fftfreq(N, d=1/fs)

# Use only the positive half of the spectrum
X_magnitude = np.abs(X[:N//2])
freqs = freqs[:N//2]

# Find the frequency with the maximum magnitude
peak_index = np.argmax(X_magnitude)
peak_freq = freqs[peak_index]

print("Test 3: Frequency Peak Verification")
print(f"Expected frequency: {f_target:.2f} Hz")
print(f"Detected frequency: {peak_freq:.2f} Hz")
print("Accuracy check:", np.isclose(peak_freq, f_target, atol=2.0))  # within ±2 Hz tolerance

# ---------- TEST 4: Performance Test (Frame Rate & Complexity) ----------

chunk_sizes = [256, 512, 1024, 2048]
iterations = 200
normalized_costs = []

print("\nTest 4: Performance & Complexity Evaluation")

for chunk_size in chunk_sizes:
    data = np.random.rand(iterations, chunk_size)
    start = time.perf_counter()
    for chunk in data:
        compute_fft(chunk)
    elapsed = time.perf_counter() - start
    avg_time = elapsed / iterations
    frame_rate = 1.0 / avg_time if avg_time > 0 else float('inf')
    complexity_cost = avg_time / (chunk_size * math.log2(chunk_size))
    normalized_costs.append(complexity_cost)

    print(f"Chunk size: {chunk_size:4d} | Avg time per frame: {avg_time*1e3:6.3f} ms | "
          f"Approx. frame rate: {frame_rate:6.1f} fps")

reference_cost = normalized_costs[0]
scaling_checks = [cost / reference_cost for cost in normalized_costs]

print("Complexity normalization (should stay roughly constant for O(N log N)):")
for size, ratio in zip(chunk_sizes, scaling_checks):
    print(f"  Size {size:4d} -> Normalized cost ratio: {ratio:6.3f}")