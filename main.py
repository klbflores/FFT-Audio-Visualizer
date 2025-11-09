import sys
from tkinter import Tk, filedialog
from visualizer import visualize_audio

if __name__ == "__main__":
    # Ask user to choose a .wav file
    root = Tk()
    root.withdraw()  # hide main tkinter window
    audio_file = filedialog.askopenfilename(
        title="Select a .wav file",
        filetypes=[("WAV files", "*.wav")]
    )

    if not audio_file:
        print("No file selected. Exiting.")
        sys.exit()

    # Ask for visualization duration
    try:
        duration = float(input("Enter duration to visualize (in seconds): "))
    except ValueError:
        duration = 15
        print("Invalid input. Using default 15 seconds.")

    print(f"\nVisualizing '{audio_file}' for {duration} seconds...\n")

    visualize_audio(audio_file, chunk_size=2048, num_bars=64, max_duration=duration)
