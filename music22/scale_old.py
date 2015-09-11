# -*- coding: utf-8 -*-
"""
Scale: Analyse Intervals
===========================

The module **scale** focuses on the analysis of the intervals and the scale of a melody.
 
It's main features are :
 
* Getting the main frequencies as peaks of the probability density function from frequencies;
* Plotting the melody;
* Plotting the PDF of the frequencies of the melody;

"""

from numpy import *
from numpy import log2,log10

set_printoptions(precision=4)

import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde
from scipy.stats.mstats import mode
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage,dendrogram
from math import log10

import glob, os.path, time, os


class Melody:
    """Analysis of the scale of a melody.
    
    This class analyses the scale of a melody as a Probability Density Function.
    
    """    
    def __init__(self, file,
                xmin=0, xmax=500,
                minFrequency=55, maxFrequency=600,
                freqref=300, bw_method=.1,
                percent=0.5,method="mode",
                transpose = "No",transpositionref = "mode",
                ):
        self.file_path = file
        self.folder_path = os.path.split(self.file_path)[0]+'/'
        self.file_name = os.path.split(self.file_path)[1]
        self.file_label = self.file_name.split(".")[0]
        self.file_exten = self.file_name.split(".")[1]
        
        self.minFrequency = minFrequency
        self.maxFrequency = maxFrequency
    
        self.percent = percent
        self.method = method
        self.freqref = freqref
        self.transpose = transpose
        self.transpositionref = transpositionref
        self.bw_method = bw_method
    
        self.xmin = xmin
        self.xmax = xmax
    
        self.x = numpy.linspace(self.xmin,self.xmax,self.xmax-self.xmin)			
    
        self.frequences = numpy.loadtxt(file)
        self.n_frames = len(self.frequences)
    
        self.freq = self.frequences[~numpy.isnan(self.frequences)]
        #self.fmin = min(self.freq)
        self.fmax = max(self.freq)
        self.fmean = numpy.mean(self.freq)
        self.fstd = numpy.std(self.freq)
    
        if self.file_exten == 'txt':
                        self.analyse()
    
        if self.file_exten == 'wav':
            self.file_pitch_extract()
    
    def __str__(self):
        return "File : %s" % (self.file_name)
    
    def analyse(self):
       """Analyse : gets the peaks of the pdf."""
       if self.transpose=="Yes":
           self.freqtransmode = self.transmode()
           print self.file_name,"(transposed)"
           self.pdf = gaussian_kde(self.freqtransmode[~numpy.isnan(self.freqtransmode)],self.bw_method)
       if self.transpose=="No":
           print self.file_name,"(not transposed)"
           self.pdf = gaussian_kde(self.freq[~numpy.isnan(self.freq)],self.bw_method)
       self.pdf = self.pdf(self.x)
       
       self.peaks()
    
    def pdf(self):
        """
        Estime la densite de probabilite
    
        Parameters
        ----------
        x : array_like
    
        Returns
        -------
        y : array_like
            Returns a ....
    
        """
    
        return self.pdf.evaluate(self.x)
    
    def pdf_show(self):
        """Affichage de la fonction de la densite de probabilite."""    
        plt.plot(self.x,self.pdf,linewidth=3,alpha=.6,label=self.file_label)
        plt.plot(self.peaks, self.peakspdf, "ro")
        for i in range(0,len(self.peaks)):
            plt.annotate(
                    "%.2f" % self.peaks[i],
                    xy=(self.peaks[i], self.peakspdf[i]),
                    xytext=(self.peaks[i], (self.peakspdf[i]+0.0001)))
        plt.legend()
    
    def peaks(self):
        """Obtenir les Peaks du PDF."""
        c = (numpy.diff(numpy.sign(numpy.diff(self.pdf))) < 0).nonzero()[0] + 1 # local max
    
        self.peaks = self.x[c]
        self.peakspdf = self.pdf[c]
        c1 = numpy.array(self.peaks, float)
        c2 = numpy.array(self.peakspdf, float)
        c = numpy.array([c1,c2])
        c = c.transpose()
        c = c[c[:,1].argsort()]
        self.ordredpeaks = c[::-1]
    
        return self.ordredpeaks
    
    def transmode(self):
         """Transpose all the frequencies by setting the mode on a given reference frequency
    
         :params freqref : The frequency reference to be transposed to. Default = 300 ?
         ref : The note reference : mode or tonic. Default = mode
         : return the transposed frequencies
         """
    
         if self.transpositionref=="mode":
             interv_transpo = mode(self.freq)[0]/self.freqref
         if self.transpositionref=="tonic":
            T = float(self.tonique(self.percent,self.method)[1])
            print "Tonic :",T
            if T > self.freqref :
                interv_transpo = T/self.freqref
            if T < self.freqref :
                interv_transpo = self.freqref/T
         print "Intervalle de tranposition :",interv_transpo
         self.freqtransposed = self.freq / interv_transpo
         return self.freqtransposed
    
    def tonique(self,percent,method):
        """
        Get the tonic frequency defined as the mode of the last frequencies array.
        These as selected by the percent argument. Two methods are possible : pdf or mode.
        
        Input :
        -----------
            percent (optional) : a percentage of the number of frames from the total size
            of the frequencies array to give the last frequencies. Default percent= 8
        
        Output :
        -----------
    
            M : the mode
            N : the mode converted inside an octave
            Final_Freqs : the last frequencies according to the percentage
        """
        self.percent = percent
        self.method = method
    
        L = len(self.freq)
        Nb_Frames = L*self.percent/100
        Final_Freqs = self.freq[(L-Nb_Frames):L]
    
        if self.method=="pdf":
            # Down to the same octave centered on the mode
            #Final_Freqs[Final_Freqs>mode(self.freq)[0]*2] = Final_Freqs[Final_Freqs>mode(self.freq)[0]*2]/2.
            #Final_Freqs[Final_Freqs<(mode(self.freq)[0]/2.)] = Final_Freqs[Final_Freqs<mode(self.freq)[0]/2.]*2
    
            self.final_pdf = gaussian_kde(Final_Freqs)
            lmax= numpy.argmax(self.final_pdf(self.x))+self.xmin
            #plt.plot(self.x,self.final_pdf(self.x))
            return self.final_pdf,lmax,Final_Freqs
    
        if self.method=="mode":
            M = mode(Final_Freqs)
            if M[0] > mode(self.freq)[0]*2:
                N = M[0]/2
            if M[0] < mode(self.freq)[0]/2:
                N = M[0]*2
            else:
                N = M[0]
            return M[0],int(N.tolist()[0]),Final_Freqs
    
    def get_intervals(self,percent=0.5,method="mode",unit="savart"):
        """
        Converts the frequencies into a linear space
    
        Input :
        -----------
            percent (optional) : percent from the last frequencies to take in consideration. Default = 0.5%
            method (optional) : Two available methods : _pdf_ and _mode_. Default = mode
            unit (optional) : the Unit to use : savart of cent. Default = savart.
        
        Output :
        -----------
            self.intervals : the intervals in the choosen unit.
        """
        self.intervals = []
        if unit == "savart":
            self.intervals = (numpy.log10(self.ordredpeaks[:,0]/self.tonique(percent,method)[1]))*1000
        if unit == "cent":
            self.intervals = (numpy.log2(self.ordredpeaks[:,0]/self.tonique(percent,method)[1]))*1200
        return self.intervals
    
    def plot(self):
        """
        Plots the melody frequencies
    
        """
        hopSize = 128
        frameSize = 2048
        sampleRate = 44100
    
        n_frames = self.n_frames
        fig = plt.figure(figsize=(16,8))
        plt.plot(range(self.n_frames), self.frequences, 'bo')
        n_ticks = 10
        xtick_locs = [i * (n_frames / 10.0) for i in range(n_ticks)]
        xtick_lbls = [i * (n_frames / 10.0) * hopSize / sampleRate for i in range(n_ticks)]
        xtick_lbls = ["%.2f" % round(x,2) for x in xtick_lbls]
        plt.xticks(xtick_locs, xtick_lbls)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Pitch (Hz)')
        plt.suptitle(self.file_label)
