# Song-Reconstructor
This project takes a bunch of audio samples(referred to as "fragments" in the code) and attempts to reconstruct a given song using the closest matching fragments.

These Python scripts I ask ChatGPT to write(as I'm not very experienced in programing). Also, be careful when opening the `fragments` and `filtered` folders, it might *freezed* or *crash* your file explorer. 

# Here is how it works
To start, you need a lot of samples or fragments, this is done by using the `fragmentor.py`, which will break down a WAV audio file into a lot lot of samples and store them into a `fragments` folder. You then can use it right away with the `constructor.py` but it will take a **long time** and many of them may be duplicates. That's when you use the `filter.py` to check and remove it base on similarity(configurable), then will be moved to the `filtered` folder.

# Script function
## fragmentor.py
There are 2 value you can change in the script is the audio file, which will then be used to chopped down to multiple sample. By default the **input** is `badmono.wav`, you can change this to what audio file you want, but it must have these same value to work correctly:
* **Encoding:** Signed 16 bit
* **Samplerate:** 44100 Hz
* **Channels:** Mono

The next value is the **fragment length** for each sample, you can find it at **line 23**(`fragment_length = 0.002`). You can change this to your liking.
The smaller value will result in better accuracy but also increase the processing time.

## filter.py
This script is designed to filter out the duplicate or near duplicate fragments to improve processing speed. **Similarity threshold** set at **0.90** by default(**line 8**). Closer to **1.0** will only remove highly siliar fragments while closer to **0.0** make it remove not so similar fragments.

## constructor.py
This script reconstruct an audio `output.wav` by using the closest match fragments from the `fragments` folder. **Base audio** is `testmono.wav` by default. **The output** is `output.wav` by default. You can change these at **line 65**.

# Requirement Library
There are some library that might required you to install them first, but as I coding it, I might already installed them so I don't have a proper `requirement.txt` for you.
* `numpy` may require manual install to works
