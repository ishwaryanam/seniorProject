Ishwarya Namburu, Karen Severson


Professor Fahim Khan


AI Powered Music Mixing Platform CS491 github

crossFadeTransitions has the transitions created by beatMatchingTransition.py.

musicGenTransitions_AtoA has the audio to audio transitions created by musicGen

musicGenTrasnitions_TtoA has the text to audio transitions.

Prompt 1: Upbeat pop song with trumpets and guitar and a funky vibe

Prompt 2: Classical music with a gloomy sad mood with violin and piano

for beatMatchingTransition.py
Usage:
    python beatMatchingTransition.py <song1> <song1_secs> <song2> <song2_secs> <output_file>

Example:
    python beatMatchingTransition.py ./songPairs/pair1a.mp3 10 ./songPairs/pair1b.mp3 10 test.mp3

music_generation_musicgen.ipynb has all the code relating to the MusicGen model.

songPairs has the specific pairs we used for the transitions in crossFadeTransitions and musicGenTransitions, but the dataset contains more songs.

scoringModels with scoringModels.ipynb has the CLAP and MERT model.

