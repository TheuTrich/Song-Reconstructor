import os
import numpy as np
import wave
import shutil
import sys
from scipy.spatial import KDTree

SIMILARITY_THRESHOLD = 0.90  # Adjust as needed

def load_fragments(fragment_folder):
    """ Load fragments as numpy arrays and build a lookup dictionary """
    fragments = []
    filenames = []

    for file in sorted(os.listdir(fragment_folder)):
        if file.endswith(".wav"):
            with wave.open(os.path.join(fragment_folder, file), 'rb') as frag:
                frag_data = np.frombuffer(frag.readframes(frag.getnframes()), dtype=np.int8)
                fragments.append(frag_data)
                filenames.append(file)

    return fragments, filenames

def compute_feature_vector(fragment):
    """ Convert fragment into a low-dimensional feature vector for fast comparison """
    return np.histogram(fragment, bins=64, range=(-128, 127))[0]  # 64-bin histogram

def filter_similar_fragments(fragment_folder, filtered_folder):
    """ Move similar fragments to a filtered folder using KDTree """
    if not os.path.exists(filtered_folder):
        os.makedirs(filtered_folder)

    fragments, filenames = load_fragments(fragment_folder)
    feature_vectors = np.array([compute_feature_vector(f) for f in fragments])  # Convert to features

    tree = KDTree(feature_vectors)  # Build KDTree for fast lookup
    removed = set()
    moved_count = 0

    for i in range(len(fragments)):
        if filenames[i] in removed:
            continue

        # Find similar fragments
        distances, indices = tree.query(feature_vectors[i], k=10)  # Get 10 closest
        for j in indices[1:]:  # Skip itself (index 0)
            if j >= len(filenames) or filenames[j] in removed:
                continue
            shutil.move(os.path.join(fragment_folder, filenames[j]), os.path.join(filtered_folder, filenames[j]))
            removed.add(filenames[j])
            moved_count += 1

        # Print progress
        sys.stdout.write(f"\rProcessing {i+1}/{len(fragments)} | Filtered: {moved_count} | {round(((i+1)/(len(fragments)))*100,2)}%   ")
        sys.stdout.flush()

    print(f"\nFiltering complete. Moved {moved_count} similar fragments.")

# Example usage:
filter_similar_fragments("fragments", "filtered")
