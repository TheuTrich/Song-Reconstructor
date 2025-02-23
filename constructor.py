import wave
import os
import numpy as np
from scipy.spatial import KDTree

def load_fragments(fragment_folder):
    """ Load all fragments as 16-bit signed PCM and build KDTree for fast searching """
    fragments = []
    filenames = []

    for file in sorted(os.listdir(fragment_folder)):
        if file.endswith(".wav"):
            with wave.open(os.path.join(fragment_folder, file), 'rb') as frag:
                frag_data = np.frombuffer(frag.readframes(frag.getnframes()), dtype=np.int16)
                fragments.append(frag_data)
                filenames.append(file)

    fragment_lengths = [len(f) for f in fragments]
    min_length = min(fragment_lengths)  # Normalize length for KDTree

    # Trim or pad all fragments to the same length
    fragments = np.array([f[:min_length] if len(f) > min_length else
                          np.pad(f, (0, min_length - len(f)), mode='constant') for f in fragments])

    tree = KDTree(fragments)  # Build KDTree

    return tree, fragments, filenames, min_length

def reconstruct_audio(target_file, fragment_folder, output_file):
    """ Reconstructs an audio file using the closest-matching fragments with KDTree """
    tree, fragments, filenames, frag_length = load_fragments(fragment_folder)

    with wave.open(target_file, 'rb') as target:
        frames = np.frombuffer(target.readframes(target.getnframes()), dtype=np.int16)
        rate = target.getframerate()
        width = 2  # 16-bit = 2 bytes per sample
        channels = 1  # Mono
        fragment_samples = frag_length

        with wave.open(output_file, 'wb') as output:
            output.setnchannels(channels)
            output.setsampwidth(width)
            output.setframerate(rate)

            for i in range(0, len(frames), fragment_samples):
                target_chunk = frames[i:i+fragment_samples]
                if len(target_chunk) < fragment_samples:
                    break  # Ignore last chunk if too short

                # Trim or pad to match fragment size
                target_chunk = np.pad(target_chunk, (0, fragment_samples - len(target_chunk)), mode='constant')

                # Find best match using KDTree
                _, idx = tree.query(target_chunk)
                best_match = fragments[idx]

                output.writeframes(best_match.astype(np.int16).tobytes())

                # Progress output
                print(f"\rProcessing {i//fragment_samples + 1}/{len(frames)//fragment_samples} chunks...", end="")

    print(f"\nReconstructed audio saved as {output_file}")

# Example usage:
reconstruct_audio("testmono.wav", "fragments", "output.wav")
