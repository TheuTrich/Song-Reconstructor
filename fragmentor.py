import wave
import os
import numpy as np

def convert_audio(audio, target_rate=44100, target_width=2, target_channels=1):
    """ Convert audio to 44.1 kHz, 16-bit signed, mono """
    params = audio.getparams()
    frames = np.frombuffer(audio.readframes(audio.getnframes()), dtype=np.int16)  # Read as signed 16-bit

    # Convert to mono if needed
    if params.nchannels > 1:
        frames = frames.reshape(-1, params.nchannels).mean(axis=1).astype(np.int16)

    # Convert sample rate manually (simple nearest-neighbor resampling)
    original_rate = params.framerate
    if original_rate != target_rate:
        ratio = target_rate / original_rate
        indices = (np.arange(0, len(frames) * ratio) / ratio).astype(int)
        frames = frames[indices]

    return frames.tobytes(), target_rate, target_width, target_channels

def extract_fragments(input_file, output_folder, fragment_length=0.002):
    """ Extracts fragments of given length from an audio file """
    with wave.open(input_file, 'rb') as audio:
        frames, rate, width, channels = convert_audio(audio)
        fragment_frames = int(rate * fragment_length)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        fragment_count = 0  # Adjust if needed
        for i in range(0, len(frames), fragment_frames * 2):  # 2 bytes per sample (16-bit)
            frag_data = frames[i:i + (fragment_frames * 2)]
            if len(frag_data) < fragment_frames * 2:
                break  # Ignore last fragment if incomplete

            fragment_file = os.path.join(output_folder, f"frag_{fragment_count:05d}.wav")
            with wave.open(fragment_file, 'wb') as frag:
                frag.setnchannels(1)  # Mono
                frag.setsampwidth(2)  # 16-bit = 2 bytes per sample
                frag.setframerate(rate)
                frag.writeframes(frag_data)

            fragment_count += 1

    print(f"Extracted {fragment_count} fragments to {output_folder}")

# Example usage:
extract_fragments("badmono.wav", "fragments")
