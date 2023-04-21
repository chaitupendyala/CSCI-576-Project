import librosa
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt

file_name = '../Data_Sets/Ready_Player_One_rgb/InputAudio.wav'

'''
 \*
  * Load an audio file as a floating point time series.
  * sr=None makes sure lobrosa does not resample the audio at a different rate
  * Returns:
      * y: n dimentional np array, this is the audio time series.
      * sr: sampling rate
'''
x, sr = librosa.load(file_name, sr=None)
print(type(x), type(sr))
print("x.shape, sr: ", x.shape, sr)

# Flatten the audio signal to later determine the entropy change
x.flatten()

# Define frame size and hop size in samples
frame_size = int(0.02 * sr) # 20 ms
hop_size = int(0.01 * sr) # 10 ms

# Segmenting the audio signal into smaller parts, 20ms in this case
window = np.hanning(frame_size)
n_frames = 1 + (len(x) - frame_size) // hop_size
frames = np.lib.stride_tricks.as_strided(x, shape=(n_frames, frame_size),
                                         strides=(x.strides[0]*hop_size, x.strides[0]))
frames = frames * window


# Computing power spectrum for each frame using fft
power_spectrum = np.abs(np.fft.fft(frames))**2
normalized_spectrum = power_spectrum / np.sum(power_spectrum, axis=1, keepdims=True)

# Computing entropy for each frame
entropy_values = entropy(normalized_spectrum.T)

# Computing entropy difference between two subsequent frames
entropy_change = np.abs(np.diff(entropy_values))
print(entropy_change)

# Plotting the entropy change
plt.plot(entropy_change)
plt.xlabel('Frame index')
plt.ylabel('Entropy change')
plt.show()