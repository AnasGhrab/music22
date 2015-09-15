"""
Scale : Analyse the scale of a melody.
----------------------------------------

This module provides function to analyse the scale of a melody. 

* Evaluate the PDF of the frequencies
* Get Peaks of the main frequencies
* Plots the PDF and the Peaks
* Gives the scale and compare intervals to reference epimoric intervals

"""

import numpy
from pandas import Series,DataFrame

from music22 import core,diastema

from scipy.stats.kde import gaussian_kde
from scipy.stats.mstats import mode

import matplotlib.pyplot as plt

xmin = 0
xmax = 500
x = numpy.linspace(xmin,xmax,xmax-xmin)

bw_method = 'scott'

def set_xrange(min,max):
    """Set the limits of x for plots and pdfs.
    
    Args :
        xmin (int): x-minimum
        xmax (int): x-maximum
    """
    global xmin,xmax,x
    xmin = min
    xmax = max
    x = numpy.linspace(xmin,xmax,xmax-xmin)

def set_bw_method(method):
    """Set the bw_method for gaussian.kde.
    
    Args :
        bw_method (str or scalar) : 'scott' (default), 'silvermann'
    """
    global bw_method
    bw_method = method
    
def kde(freqs):
    """Estimate the pdf of the freqs using a Kernel Density Estimation.
    
    The estimation is done on the frequencies (0,500).
    
    Args:
        freqs (numpy.ndarray) : A list of frequencies in Hz.
        
    Returns:
        pdf (scipy.stats.kde.gaussian_kde) : the pdf function of freqs.
    
    Exemple:
        >>> from music22 import diastema,scale
        >>> import matplotlib.pyplot as plt
        
        >>> file_path = "/Users/anas/AUDIO/Barraq/txt/P0.txt"
        >>> freqs = numpy.loadtxt(file_path)
        >>> freqs = music22.core.clean_list(freqs)
        >>> pdf = music22.scale.kde(freqs)
        >>> plt.plot(pdf)
        >>> plt.show()
    """
    global x, bw_method
    kde = gaussian_kde(freqs,bw_method)
    pdf = kde.evaluate(x)
    return pdf

def peaks(pdf):
    """Get the peaks of the estimated Probability Density Function.
    
    The estimation is done on the frequencies (0,500).
    
    Args:
        pdf (numpy.array) : the probability of the frequencies in the range 0-500 Hz.
    Returns:
        xpeaks (numpy.array) : the peaks frequencies. 
        ypeaks (numpy.array) : the probability of the peaks.
    """
    global x
    c = (numpy.diff(numpy.sign(numpy.diff(pdf))) < 0).nonzero()[0] + 1 # local max
        
    peaks = x[c]
    peakspdf = pdf[c]
    xpeaks = numpy.array(peaks, float)
    ypeaks = numpy.array(peakspdf, float)
    
    return xpeaks, ypeaks
    
def pdf_show(pdf,xpeaks,ypeaks,label="pdf"):
        """Plot the PDF and the peaks of the frequencies.
        
        Args:
            pdf (numpy.ndarray) : the PDF of the frequencies given by kde()
            xpeaks (numpy.ndarray) : frequencies of the peaks, given by peaks()
            ypeaks (numpy.ndarray) : pdf values of the peaks, given by peaks()
            label (str) : label to give to the figure (`optional`)
            
        Returns :
            A plot
        """ 
        global x

        plt.plot(x,pdf,linewidth=3,alpha=.6,label=label)
        plt.plot(xpeaks, ypeaks, "ro")
        for i in range(0,len(xpeaks)):
            plt.annotate(
                    "%.2f" % xpeaks[i],
                    xy=(xpeaks[i], ypeaks[i]),
                    xytext=(xpeaks[i], (ypeaks[i]+0.0001)))
        plt.legend()
    
def order_peaks(xpeaks,ypeaks):
    """Orders the peaks following their probability
    
    Args:
        xpeaks (numpy.array) : list of peaks (Hz.)
        ypeaks (numpy.array) : probability of the peaks
    Returns:
        ordredpeaks (pandas.core.frame.DataFrame) : a table with ordered frequencies 
    """
    data = {'xpeaks': xpeaks,'ypeaks': ypeaks}
    table = DataFrame(data)
    ordredpeaks = table.sort_index(by='ypeaks',ascending=False)
    return ordredpeaks
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()