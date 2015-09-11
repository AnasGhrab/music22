"""
Stats : Module for statistical analysis.
----------------------------------------

"""

import numpy
from os import path

from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage,dendrogram

import matplotlib.pyplot as plt

def corr(list,metric='KL'):
    """Calculate distances between PDFs.
    
    Args:
        list (list) : list of pdf lists.
        metric (str) : the metric method : euclidian, KL (Kullback-Leibler). Default is KL.
    Return:
        distances
    """            
    if metric=='euclidian':
        distances = pdist(PDFS,metric='euclidean')        
    if metric=='KL':
        DKL = []
        for i in range(0,len(list)):
            p = list[i]
            for j in range(i+1,len(list)):
                q = list[j]
                KL = kl(p,q) # METHODE DEFINIT ICI
                DKL.append(KL)
            distances = DKL
    return distances

def matrix(distances,labels):
    """Draw Matrix and Heatmap.
    
    Args:
        distances (array) : array of distances values.
        
    Return:
        a simatrix with heatmap showing the hirarchical clustering.
    """

    Y = linkage(distances, method='complete')
    
    # As explained here : http://nbviewer.ipython.org/github/OxanaSachenkova/hclust-python/blob/master/hclust.ipynb
    # Compute and plot first dendrogram.
    fig = plt.figure(figsize=(8,8))
    # x ywidth height
    ax1 = fig.add_axes([0.17,0.1,0.17,0.6])
    Z1 = dendrogram(Y, orientation='right',labels=labels) # adding/removing the axes
    ax1.set_xticks([])
    
    # Compute and plot second dendrogram.
    ax2 = fig.add_axes([0.4,0.73,0.6,0.17])
    Z2 = dendrogram(Y,labels=labels) # adding/removing the axes
    ax2.set_yticks([])
    
    #Compute and plot the heatmap
    axmatrix = fig.add_axes([0.4,0.1,0.6,0.6])
    idx1 = Z1['leaves']
    idx2 = Z2['leaves']
    D = squareform(distances)
    D = D[idx1,:]
    D = D[:,idx2]
    im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap=plt.cm.YlGnBu)
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])
    
    # Plot colorbar.
    axcolor = fig.add_axes([1.01,0.1,0.02,0.6])
    plt.colorbar(im, cax=axcolor);
    return fig

def kl(p, q):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions

    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
    """
    p = numpy.asarray(p, dtype=numpy.float)
    q = numpy.asarray(q, dtype=numpy.float)
 
    return numpy.sum(numpy.where(p != 0, p * numpy.log(p / q), 0))