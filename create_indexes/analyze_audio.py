import librosa
import matplotlib.pyplot as plt
import sklearn

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

'''
  \*
   * Trying to plot the spetral plot.
   * According to the spectral plot we can 
      a lot of entropy difference while a scene changes
   * This change in entropy can be used to check the scene change
'''
X = librosa.stft(x)
Xdb = librosa.amplitude_to_db(abs(X))
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar()
plt.show()