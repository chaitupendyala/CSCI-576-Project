import librosa
import numpy as np
from scipy.stats import entropy
from datetime import datetime, timedelta

class AudioSceneDetech:
    def __init__(self, audio_file_name=None) -> None:
        self.audio_file_name = audio_file_name
        self.audio, self.sr = librosa.load(audio_file_name, sr=None)
    
    def _entropy_difference(self, time):
        time_of_interest = datetime.strptime(time, '%H:%M:%S.%f')
        unix_epoch = datetime(1900, 1, 1, tzinfo=time_of_interest.tzinfo)
        time_of_interest_seconds = (time_of_interest - unix_epoch).total_seconds()

        time_index = int(time_of_interest_seconds * self.sr)

        before_index = time_index - (2 * self.sr)
        after_index = time_index + (2 * self.sr)

        signal_before = self.audio[before_index:time_index]
        signal_after = self.audio[time_index:after_index]

        entropy_before = entropy(np.abs(signal_before))
        entropy_after = entropy(np.abs(signal_after))

        entropy_difference = abs(entropy_after - entropy_before)

        return entropy_difference
    
    def compute_audio_entropies(self, change_times):
        entropy_differences = []
        for change_time in change_times:
            entropy_differences.append(self._entropy_difference(change_time))
        
        return entropy_differences