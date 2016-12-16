# -*- coding: utf-8 -*-
"""Methods for analysis audio files and generate symbolic data.

Essentia library, v. 2.0.1, is required.

"""

from essentia import *
from essentia.standard import *

def pitch_extract(file,minFrequency=80,maxFrequency=600):
    """Extract fondamental frequencies (f0).
    
    For now, the method used is PredominantMelody() from the Essentia package (v. 2.0.1).

    Args:
        file (str): the absolute path of the audio .wav file.
        minFrequency: the minimum frequency for PredominantMelody().
        maxFrequency: the maximum frequency for PredominantMelody().
     
    Return:
        file (str): the path of the .txt file where frequencies were written. Zeros pitches are replaced by NaN values.
    """
    audio = MonoLoader(filename = file)() # creation de l'instance
#    melodie = PredominantMelody(minFrequency=minFrequency, maxFrequency = maxFrequency) # creation de l'instance
    melodie = PitchMelodia(minFrequency=minFrequency, maxFrequency = maxFrequency) # creation de l'instance
    pitch, confidence = melodie(audio)

    return pitch
