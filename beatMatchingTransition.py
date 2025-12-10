#!/usr/bin/env python3
import sys
import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment


def parse_args():
    if len(sys.argv) != 6:
        print(
            "Usage: python beatMatchingTransition.py "
            "<song1> <song1_secs> <song2> <song2_secs> <output_file>"
        )
        sys.exit(1)

    song1_path = sys.argv[1]
    song2_path = sys.argv[3]
    output_path = sys.argv[5]

    try:
        song1_secs = float(sys.argv[2])
        song2_secs = float(sys.argv[4])
    except ValueError:
        print("Error: <song1_secs> and <song2_secs> must be numbers (seconds).")
        sys.exit(1)

    return song1_path, song1_secs, song2_path, song2_secs, output_path


def to_scalar(x):
    """Convert a NumPy scalar/array or Python number to a plain float."""
    if isinstance(x, np.ndarray):
        # librosa.beat.beat_track may return a scalar or length-1 array
        return float(x[0])
    return float(x)


def main():
    song1_path, song1_secs, song2_path, song2_secs, output_path = parse_args()

    # --- Load audio for tempo estimation and stretching ---
    y1, sr1 = librosa.load(song1_path, duration=60)
    y2, sr2 = librosa.load(song2_path, duration=60)

    tempo1, _ = librosa.beat.beat_track(y=y1, sr=sr1)
    tempo2, _ = librosa.beat.beat_track(y=y2, sr=sr2)

    tempo1 = to_scalar(tempo1)
    tempo2 = to_scalar(tempo2)

    print(f"Tempo 1: {tempo1:.2f} BPM | Tempo 2: {tempo2:.2f} BPM")

    if tempo2 == 0:
        print("Error: tempo of second track is 0, cannot match tempos.")
        sys.exit(1)

    # --- Match tempos by time-stretching song 2 ---
    rate = tempo1 / tempo2
    y2_stretched = librosa.effects.time_stretch(y=y2, rate=rate)

    matched_path = "song2_matched.wav"
    sf.write(matched_path, y2_stretched, sr2)

    # --- Reload audio with pydub for easy slicing / crossfading ---
    song1 = AudioSegment.from_file(song1_path)
    song2 = AudioSegment.from_file(matched_path)

    # Convert desired transition durations (secs) to ms
    transition1_len = int(song1_secs * 1000)
    transition2_len = int(song2_secs * 1000)

    # Clamp to track lengths to avoid weirdness if requested time > track length
    transition1_len = min(transition1_len, len(song1))
    transition2_len = min(transition2_len, len(song2))

    # --- Create transition segments ---
    last_segment = song1[-transition1_len:] if transition1_len > 0 else AudioSegment.silent(duration=0)
    first_segment = song2[:transition2_len] if transition2_len > 0 else AudioSegment.silent(duration=0)

    # Crossfade between the two segments (2 seconds)
    transition = last_segment.append(first_segment, crossfade=2000)

    # --- Trim original songs and assemble final mix ---
    song1_main = song1[:-transition1_len] if transition1_len > 0 else song1
    song2_main = song2[transition2_len:] if transition2_len > 0 else song2

    final_mix = song1_main + transition + song2_main

    # --- Export result ---
    final_mix.export(output_path, format="mp3")
    print(f"Done. Saved to {output_path}")


if __name__ == "__main__":
    main()
