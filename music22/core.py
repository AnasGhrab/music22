"""
Core : Functions useful for all the package.
--------------------------------------------

"""

import numpy,time,sys
from os import path, makedirs
from music22 import audio

class file():
    """A class to manage files.
    
    Args:
        path (str) : absolute path of a file.
    
    Attributes:
        path (str) : The path of the file.
        basename (str) : The name of the file.
        dirname (str) : The directory path of the file.
        name (str) : The name of the file.
        extension (str) : The extension of the file.
    
    Example:
        >>> audio = "/Users/anas/Barraq/AUDIO/P0.wav"
        >>> A = file(audio)
        >>> print A.path
        /Users/anas/Barraq/AUDIO/P0.wav
        >>> print A.basename
        P0.wav
        >>> print A.dirname
        /Users/anas/Barraq/AUDIO
        >>> print A.name
        P0
        >>> print A.extension
        wav
    """
    def __init__(self,fichier):
        #self.path = path.abspath('\''+ path + '\'' )
        #self.path = fichier
        self.path = path.abspath(fichier)
	print "Fichier :", self.path
        self._check_exist()
        self._set_names()
    def __repr__(self):
        return '[File: %s]' % (self.path)

    def _check_exist(self):
        if ( not path.isfile(self.path)):
            print("ERROR: File %s does not exist or is not readable !" % self.path)

    def _set_names(self):
        self.basename = path.basename(self.path)
        self.dirname = path.dirname(self.path)
        self.name = self.basename.split(".")[0]
        self.extension = self.basename.split(".")[1]
             
class wavfile(file):
    """A class to manage audio files (.wav)."""
    def __init__(self,path):
        file.__init__(self,path)
        self._check_extension()
    def __repr__(self):
        return '[WavFile: %s]' % (self.path)
        
    def _check_extension(self):
        if path.isfile(self.path) and self.extension == 'wav':
            print "Instance created with the audio file :", self.basename
        else :
            print "ERROR: The file does not seem to be an audio .wav file !"

    def pitch_extract(self):
        """Extracts the fundamental frequencies (f0).
        
        Args:
            self.wav_path (str) : a path to a .wav file.
        Return:
            self.txt_path (str) : a path to a .txt file contraing a list of frequencies.
        """
        start = time.time()
        print 'Extraction of f0 from ',self.path
        sys.stdout.flush()

        pitch = audio.pitch_extract(self.path)
        pitch[pitch==0] = numpy.nan

        try:
            makedirs(self.dirname+'/f0/')
            print 'Folder f0/ in', self.dirname, 'created.'
        except OSError:
            pass

        numpy.savetxt(self.dirname+'/f0/'+self.name+'.txt',pitch,fmt='%1.3f')
    
        end = time.time()
        print 'File',self.basename,'analysed in ',end - start,' seconds'

    
class f0file(file):
    """A class to manage data files (.txt)."""
    def __init__(self,path):
        file.__init__(self,path)
        self._check_extension()
    def __repr__(self):
        return '[TxtFile: %s]' % (self.path)
        
    def _check_extension(self):
        if path.isfile(self.path) and self.extension == 'txt':
            print "Instance created with the txt file :", self.basename
        else :
            print "ERROR: The file does not seem to be a text .txt file !"

    def get_data(self):
        print "Recherche f0 dans",self.path
        self.data = numpy.loadtxt(self.path)

    def clean_data(self):
        """Remove zeros or NaNs in the list.
        
        Args:
            L (numpy.ndarray) : A numpy list.
        Return:
            L (numpy.ndarray) : A `cleaned` numpy list."""
        cleaned_data = self.data[numpy.nonzero(self.data)] # Remove zeros, if any
        self.clean_data = cleaned_data[~numpy.isnan(cleaned_data)] # Remove NaNs, if any
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
