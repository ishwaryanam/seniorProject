#experimenting w/ beat matching...kinda works???
import librosa
import soundfile as sf
from pydub import AudioSegment
import sys

#getting args

song1 = sys.argv[1] #28 seconds
song1_secs = sys.argv[2]
song2 = sys.argv[3] #23 seconds
song2_secs = sys.argv[4]
final_file_name = sys.argv[5]

#get respective tempos
y1, sr1 = librosa.load(song1, duration=60)
y2, sr2 = librosa.load(song2, duration=60)

tempo1, _ = librosa.beat.beat_track(y=y1, sr=sr1)
tempo2, _ = librosa.beat.beat_track(y=y2, sr=sr2)

tempo1 = float(tempo1)
tempo2 = float(tempo2)

print(f"Tempo 1: {tempo1:.2f} BPM | Tempo 2: {tempo2:.2f} BPM")

#match tempos
rate = tempo1 / tempo2
y2_stretched = librosa.effects.time_stretch(y=y2, rate=rate)
sf.write("song2_matched.wav", y2_stretched, sr2)

#load audios
song1 = AudioSegment.from_file(song1)
song2 = AudioSegment.from_file("song2_matched.wav")

#transition time <= can get from parse

transition_len = 10_000  # 10 seconds in ms
transition1_len = song1_secs * 1000
transition2_len = song2_secs * 1000

#get segments of transition time
last_10 = song1[-transition1_len:]
first_10 = song2[:transition2_len]

#create the transition, can play around with crossfade
transition = last_10.append(first_10, crossfade=2000)

#trim and combine songs
song1_main = song1[:-transition1_len]  # remove last 10 s
song2_main = song2[transition2_len:]   # remove first 10 s
final_mix = song1_main + transition + song2_main

# save final song
final_mix.export(final_file_name, format="mp3")

print("Done")