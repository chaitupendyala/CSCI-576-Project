import librosa
import matplotlib.pyplot as plt
import sklearn

file_name = '../Data_Sets/Ready_Player_One_rgb/InputAudio.wav'

x, sr = librosa.load(file_name)

X = librosa.stft(x)

Xdb = librosa.amplitude_to_db(abs(X))

# plt.figure(figsize = (10, 5))
# librosa.display.specshow(Xdb, sr = sr, x_axis = 'time', y_axis = 'hz')
# plt.colorbar()

spectral_centroids = librosa.feature.spectral_centroid(y=x, sr=sr)[0]
spectral_centroids.shape(775, )
# Computing the time variable for visualization
plt.figure(figsize = (12, 4))
frames = range(len(spectral_centroids))
t = librosa.frames_to_time(frames)
# Normalising the spectral centroid for visualisation
def normalize(x, axis = 0):
  return sklearn.preprocessing.minmax_scale(x, axis = axis)
#Plotting the Spectral Centroid along the waveform
librosa.display.waveplot(x, sr = sr, alpha = 0.4)
plt.plot(t, normalize(spectral_centroids), color = 'b')
plt.show()