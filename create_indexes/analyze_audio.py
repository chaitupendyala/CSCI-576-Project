import librosa
import numpy as np
import matplotlib.pyplot as plt

# Split audio into short segments
def split_audio(audio, sr, segment_length=3):
    segment_samples = sr * segment_length
    n_segments = len(audio) // segment_samples
    return [audio[i * segment_samples : (i + 1) * segment_samples] for i in range(n_segments)]

# Compute audio features
def compute_features(audio, sr):
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=audio)
    return np.concatenate([mfccs, spectral_contrast, spectral_centroid, zero_crossing_rate], axis=0)

# Calculate the difference between consecutive features
def calculate_feature_diff(features):
    return np.abs(np.diff(features, axis=1))

# Determine threshold
def determine_threshold(feature_diff):
    return np.mean(feature_diff) + np.std(feature_diff)

# Detect scene changes
def detect_scene_changes(audio, sr, threshold):
    segments = split_audio(audio, sr)
    segment_features = [compute_features(segment, sr) for segment in segments]
    feature_diff = calculate_feature_diff(segment_features)
    change_points = np.argwhere(feature_diff > threshold)[:, 1] + 1
    return change_points

# Plot audio waveform with scene change lines
def plot_scene_changes(audio, sr, change_points):
    plt.figure(figsize=(10, 4))
    plt.plot(np.arange(len(audio)) / sr, audio)
    for point in change_points:
        plt.axvline(x=point * 3, color='r', linestyle='--')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()

# Example usage
audio, sr = librosa.load("../Data_Sets/Ready_Player_One_rgb/InputAudio.wav")
threshold = determine_threshold(calculate_feature_diff(compute_features(audio, sr)))
change_points = detect_scene_changes(audio, sr, threshold)
print(change_points)
print(type(change_points))
plot_scene_changes(audio, sr, change_points)