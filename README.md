# FFT Sound Visualizer

A real-time audio visualizer that applies the Fast Fourier Transform (FFT) to display the frequency spectrum of `.wav` audio files through animated, color-coded bar charts.
This project demonstrates how linear algebra and signal processing concepts translate into interactive visual computation.

## Features

- **Real-time FFT Analysis**: Continuously extracts and displays frequency data as the audio plays.
- **Interactive File Selection**: GUI-based file picker for selecting WAV files.
- **Customizable Duration**: Specify the number of seconds to visualize.
- **Synchronized Playback**: Visualization stops precisely when the audio ends.
- **Color-coded Visualization**: Uses a plasma colormap to represent frequency magnitudes.
- **Automatic Audio Handling**: Automatically converts stereo to mono and normalizes amplitude.

## Requirements

- Python 3.6+
- Libaries: numpy, matplotlib, scipy, sounddevice

## Installation

1. Clone or download this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the main program:

```bash
python main.py
```

2. Select a `.wav` file from the file dialog.
3. Enter the duration (in seconds) you want to visualize when prompted.
   - Press Enter to use the default (15 seconds)
4. The visualization window will open and the audio will start playing automatically.

## How It Works

1. **Audio Loading**: The program loads a WAV file and converts it to mono if stereo, then normalizes the amplitude.
2. **Chunking**: The audio signal is divided into overlapping chunks (default: 2048 samples per chunk).
3. **FFT Processing**: Each chunk is processed using FFT to extract frequency components `X[k]`.
4. **Magnitude Calculation**: The amplitude of each frequency component is computed and normalized.
5. **Visualization**: The frequency spectrum is grouped into bars (default: 64 bars) and displayed as animated bars that react to sound intensity.
6. **Real-time Updates**: The visualization updates every 50ms, synchronized with audio playback.

## Project Structure

```
fft_sound_visualizer/
├── main.py           # Main entry point - handles file selection and user input
├── visualizer.py     # Core visualization logic with FFT computation
├── utils.py          # Audio loading and signal processing utilities
├── requirements.txt  # Python dependencies
├── tests.py          # Test files (optional)
└── assets/           # Sample audio files for testing
```

## Technical Details

- **Chunk Size**: 2048 samples (configurable)
- **Number of Bars**: 64 frequency bands (configurable)
- **Update Interval**: 50ms per frame
- **FFT Window**: Uses one-sided spectrum (Nyquist frequency)
- **Normalization**: Frequency magnitudes are normalized to [0, 1] range

## Example

```python
from visualizer import visualize_audio

# Visualize an audio file
visualize_audio(
    'path/to/audio.wav',
    chunk_size=2048,
    num_bars=64,
    max_duration=30,
    play_audio=True
)
```

## Notes

- Only WAV files are supported.
- The visualization automatically stops when the audio finishes playing.
- If the specified duration exceeds the audio length, the full audio will be visualized.
- The program handles both mono and stereo audio files.

## Academic Context

This project was developed as part of a Linear Algebra final project.
It demonstrates the application of vector transformations, complex number operations, and matrix-based computation in digital signal processing and computer visualization.

## License

This project is intended for academic and educational use.
© 2025 – FFT Sound Visualizer | Developed by Kauri Lorraine Flores for the Linear Algebra Final Project