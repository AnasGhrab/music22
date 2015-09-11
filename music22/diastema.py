"""
Diastema : Core operations on intervals.
----------------------------------------

This module defines functions for basic operations on intervals, i. e. `conversions` from logarithmic into linear spaces, a list of reference `epimoric intervals` and a function for setting the `unit` be used.
 
You can also get the closest `epimoric reference` interval to an interval in the current unit, and the difference. If we are using the savart units :

>>> get_inter_ref(300)
('300.00', '2/1', '-', '1.03')
>>> get_inter_ref(303)
('303.00', '2/1', '+', '1.97')

"""

from numpy import log2,log10
    
inter = {'2/1*4/3':2/1.*4/3.,'2/1*5/4':2/1.*5/4.,'2/1*6/5':2/1.*6/5.,
         '2/1*9/8':2/1.*9/8.,'2/1*10/9':2/1.*10/9.,'2/1*12/11':2/1.*12/11.,
         '2/1':2/1.,'3/2*5/4':3/2.*5/4.,'3/2*6/5':3/2.*6/5.,'3/2*9/8':3/2.*9/8.,
         '3/2*10/9':3/2.*10/9.,'3/2':3/2.,'4/3':4/3.,'5/4':5/4.,'9/8*12/11':9/8.*12/11.,
          '6/5':6/5.,'9/8':9/8.,'10/9':10/9.,'12/11':12/11.,'1/1':1/1.}
#Int = [] # A list where the method convert_ref() puts converted ratio into a linear space
unit = "savart" # Sets the default unit to be savart
        
def set_unit(x):
    """Set the unit to be used : possible units are savart and cent.

        >>> set_unit("savart")
        Unit is now set to : savart
    
    """
    global unit
    unit_types = ["savart","cent"]
    if x in unit_types:
        unit = x
    	print "Unit is now set to :",unit
    else:
        raise ValueError("Accepted units : 'savart','cent'")

def get_intervals():
    """Prints de list of all available reference intervals."""
    global inter
    print inter
    
def get_unit():
    """Get the currently used unit."""
    global unit
    print unit

def cent(y):
    """Convert the given interval (as ratio) to cent.
    
        >>> cent(3/2.)
        701.95500086538743
    """
    inter_cent = log2(y)*1200
    return inter_cent

def savart(y):
    """Convert the given interval (as ratio) to savart.
    
        >>> savart(3/2.)
        176.09125905568123

    """
    inter_savart = log10(y)*1000
    return inter_savart

def dias(y):
    """
    Convert the given interval (as ratio) to the global chosen unit. Default is savart.
    
        >>> dias(3/2.)
        176.09125905568123
    """
    global unit
    if unit=="savart":
        y = savart(y)
    if unit == "cent":
        y = cent(y)
    return y

def convert_ref():
    """Convert all the reference intervals (given by get_intervals()) from ratios to a linear space."""
    global inter
    Int = []
    I = inter.values()
    for i in range(0,len(I)):
        Int.append(dias(I[i])) # Tous les intervalles en savarts
    return Int

def get_inter_ref(x):
    """Look for the closest epimoric interval.

    Args:
        x (int) : an interval in savart/cent.

    Returns:
        y (tuple) : the closest interval from the reference intervals.
        
    Example:            
        >>> get_inter_ref(300)
        ('300.00', '2/1', '-', '1.03')
        >>> get_inter_ref(303)
        ('303.00', '2/1', '+', '1.97')

    """
    global inter
    Int = convert_ref() # Converting intervals
    dist = []
    for j in range(0,len(Int)):
        dist.append(abs(abs(x)-abs(Int[j])))
    Index_Intervalle_Proche = dist.index(min(dist))
    Nom_Intervalle_Proche = inter.keys()[dist.index(min(dist))]
    Difference = "{:.2f}".format(min(dist))
    if x>=log10(inter.values()[dist.index(min(dist))])*1000:
        signe = '+'
    else: signe  = '-'
    y = "{:.2f}".format(x),Nom_Intervalle_Proche,signe, Difference
    return y

def get_scale(echelle):
    """Compare given intervals to reference intervals.
    
    Args:
        echelle (list): a list containing intervals in a linear scale.
        
    Returns:
        Prints a list of tuples

    Example :
        >>> a = [125,256,300]
        ('125.00', '4/3', '+', '0.06')
        ('256.00', '3/2*6/5', '+', '0.73')
        ('300.00', '2/1', '-', '1.03')    
    """
    for i in range(0,len(echelle)):
        print get_inter_ref(echelle[i])


if __name__ == "__main__":
    import doctest
    doctest.testmod()