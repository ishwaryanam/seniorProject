#experimenting w/ beat matching...kinda works???
import librosa
import soundfile as sf
from pydub import AudioSegment

# ---- STEP 1: Analyze tempo ----
y1, sr1 = librosa.load("pair1a.mp3", duration=60)
y2, sr2 = librosa.load("pair1b.mp3", duration=60)

tempo1, _ = librosa.beat.beat_track(y=y1, sr=sr1)
tempo2, _ = librosa.beat.beat_track(y=y2, sr=sr2)

tempo1 = float(tempo1)
tempo2 = float(tempo2)

print(f"Tempo 1: {tempo1:.2f} BPM | Tempo 2: {tempo2:.2f} BPM")

# ---- STEP 2: Match song2 tempo to song1 ----
rate = tempo1 / tempo2
y2_stretched = librosa.effects.time_stretch(y=y2, rate=rate)
sf.write("song2_matched.wav", y2_stretched, sr2)

# ---- STEP 3: Load audio ----
song1 = AudioSegment.from_file("pair1a.mp3")
song2 = AudioSegment.from_file("song2_matched.wav")

# ---- STEP 4: Prepare transition parts ----
transition_len = 10_000  # 10 seconds in ms

# Parts used for the transition
last_10 = song1[-transition_len:]
first_10 = song2[:transition_len]

# Create smooth transition (2-second crossfade)
transition = last_10.append(first_10, crossfade=2000)

# ---- STEP 5: Trim songs to avoid duplication ----
song1_main = song1[:-transition_len]  # remove last 10 s
song2_main = song2[transition_len:]   # remove first 10 s

# ---- STEP 6: Combine all three ----
final_mix = song1_main + transition + song2_main

# ---- STEP 7: Export final result ----
final_mix.export("song1_to_song2_seamless.mp3", format="mp3")

print("✅ Exported 'song1_to_song2_seamless.mp3' successfully!")
