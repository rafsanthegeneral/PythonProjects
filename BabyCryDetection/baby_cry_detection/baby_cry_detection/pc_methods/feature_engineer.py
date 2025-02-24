# -*- coding: utf-8 -*-

import numpy as np
import logging
import timeit
from librosa.feature import zero_crossing_rate, mfcc, spectral_centroid, spectral_rolloff, spectral_bandwidth,\
    chroma_cens, rms #rms in librpsa 0.7.0, rmse in previous version

__all__ = [
    'FeatureEngineer'
]


class FeatureEngineer:
    """
    Feature engineering
    """

    RATE = 44100   # All recordings in ESC are 44.1 kHz
    FRAME = 512    # Frame size in samples

    def __init__(self, label=None):
        # Necessary to re-use code for training and prediction
        if label is None:
            self.label = ''
        else:
            self.label = label

    def feature_engineer(self, audio_data):
        """
        Extract features using librosa.feature.

        Each signal is cut into frames, features are computed for each frame and averaged [mean].
        The numpy array is transformed into a data frame with named columns.

        :param audio_data: the input signal samples with frequency 44.1 kHz
        :return: a numpy array (numOfFeatures x numOfShortTermWindows)
        """

        zcr_feat = self.compute_librosa_features(audio_data=audio_data, feat_name='zero_crossing_rate')
        rmse_feat = self.compute_librosa_features(audio_data=audio_data, feat_name='rmse')
        mfcc_feat = self.compute_librosa_features(audio_data=audio_data, feat_name= 'mfcc')
        spectral_centroid_feat = self.compute_librosa_features(audio_data=audio_data, feat_name='spectral_centroid')
        spectral_rolloff_feat = self.compute_librosa_features(audio_data=audio_data, feat_name='spectral_rolloff')
        spectral_bandwidth_feat = self.compute_librosa_features(audio_data=audio_data, feat_name='spectral_bandwidth')

        concat_feat = np.concatenate((zcr_feat,
                                      rmse_feat,
                                      mfcc_feat,
                                      spectral_centroid_feat,
                                      spectral_rolloff_feat,
                                      spectral_bandwidth_feat
                                      ), axis=0)

        logging.info('Averaging...')
        start = timeit.default_timer()

        mean_feat = np.mean(concat_feat, axis=1, keepdims=True).transpose()

        stop = timeit.default_timer()
        logging.info('Time taken: {0}'.format(stop - start))

        return mean_feat, self.label

    def compute_librosa_features(self, audio_data, feat_name):
        """
        Compute feature using librosa methods

        :param audio_data: signal
        :param feat_name: feature to compute
        :return: np array
        """
        # # http://stackoverflow.com/questions/41896123/librosa-feature-tonnetz-ends-up-in-typeerror
        # chroma_cens_feat = chroma_cens(y=audio_data, sr=self.RATE, hop_length=self.FRAME)

        logging.info('Computing {}...'.format(feat_name))

        if feat_name == 'zero_crossing_rate':
            return zero_crossing_rate(y=audio_data, hop_length=self.FRAME)
        elif feat_name == 'rmse':
            return rms(y=audio_data, hop_length=self.FRAME)
        elif feat_name == 'mfcc':
            return mfcc(y=audio_data, sr=self.RATE, n_mfcc=13)
        elif feat_name == 'spectral_centroid':
            return spectral_centroid(y=audio_data, sr=self.RATE, hop_length=self.FRAME)
        elif feat_name == 'spectral_rolloff':
            return spectral_rolloff(y=audio_data, sr=self.RATE, hop_length=self.FRAME, roll_percent=0.90)
        elif feat_name == 'spectral_bandwidth':
            return spectral_bandwidth(y=audio_data, sr=self.RATE, hop_length=self.FRAME)
