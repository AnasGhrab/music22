.. _tuto_tonique:

Quelle fréquence représenterait la tonique ?
============================================

Si nous concevons qu'une note musicale peut être représentée par une
fréquence (La = 440 ?), et puisque musicalement nous définissons la
tonique comme une note d'appui avec laquelle se termine la mélodie,
alors, cette note devrait être représentée par la dernière fréquence
d'une liste mélodique.

Cependant, la réalité musicale et acoustique font qu'il n'est pas aussi
évident de déterminer une fréquence représentative de la tonique, pour
les raisons suivantes :

-  La note n'est pas en réalité une fréquence, mais un ensemble de
   fréquences. Une meilleure représentation de la note serait une loi
   normale (https://fr.wikipedia.org/wiki/Loi\_normale) avec une
   fréquence centrale et un écart type;
-  Si nous devons faire le d'une fréquence parmi les « dernières
   fréquences », comment déterminer celles-ci et sur quelle base faire
   ce choix ?
-  Dans un contexte de voix nue, les dernières fréquences ont tendance à
   être chantée plus basse qu'à l'intérieur du chant.

En utilisant music22, nous tenterons de mieux cerner le problème et nous
verrons comment ajuster les paramètres liés à la détection de la
tonique.

.. code:: python

    import music22.modalis # Importation du module modalis

.. code:: python

    path = '/Users/anas/AUDIO/Barraq/f0/P1.txt'
    barraq1 = music22.modalis.melodia(path) # Création d'une instance pour une seule mélodie


.. parsed-literal::

    Instance created with the txt file : P1.txt


Par défaut, l'attribut .tonique nous donne une fréquence représentative
de la tonique :

.. code:: python

    barraq1.tonique




.. parsed-literal::

    166.466



Avant de voir en détail les paramètres utilisés pour cette détection,
observons la dernière fréquence de la liste :

.. code:: python

    barraq1.clean_freqs




.. parsed-literal::

    array([ 155.564,  157.372,  160.123, ...,  159.201,  158.284,  156.466])



Nous voyons que la dernière fréquence que nous donne l'algorithme
utilisé pour la détection des fréquences fondamentales est la fréquence
156.466 Hz, différente de la fréquence représentative analysée, 166.466
Hz.

Les dernières fréquences d'une mélodie
--------------------------------------

Il est évident qu'on ne peut pas définir les dernières fréquences d'une
mélodie par un nombre fixe dl'éléments (*les x dernières fréquences*)
car toutes les mélodies n'ont pas la même longeur. On utilisera alors un
pourcentage de toutes les fréquences de la mélodie. Pour avoir le
pourcentage des dernières fréquences utilisées, il faut faire appel à
l'attribut .percent.

.. code:: python

    barraq1.percent




.. parsed-literal::

    0.5



Pour la détection de la fréquence, par défaut, music22 utilisant les
0.5% dernières fréquences. Varions ce pourcentage pour voir de quelle
manière cela influe sur la fréquence détectée. On peut indiquer le
pourcentage à utiliser lors de la création de l'instance :

.. code:: python

    barraq1.get_tonique(percent=0.5)
    barraq1.tonique




.. parsed-literal::

    166.466



.. code:: python

    barraq1.get_tonique(percent=0.1)
    barraq1.tonique




.. parsed-literal::

    159.466



.. code:: python

    barraq1.get_tonique(percent=1)
    barraq1.tonique




.. parsed-literal::

    162.871



.. code:: python

    barraq1.get_tonique(percent=2)
    barraq1.tonique




.. parsed-literal::

    163.871



.. code:: python

    barraq1.get_tonique(percent=5)
    barraq1.tonique




.. parsed-literal::

    183.871



.. code:: python

    barraq1.get_tonique(percent=7)
    barraq1.tonique




.. parsed-literal::

    182.871



.. code:: python

    barraq1.get_tonique(percent=10)
    barraq1.tonique




.. parsed-literal::

    184.871



La fonction suivante nous permet d'obtenir ces résultats de manière plus
automatisée :

.. code:: python

    pourcentages = [0.1,0.5,1,2,5,7,10]  # Liste des différents pourcentage à utiliser
    toniques = []  # Liste vide pour y placer les toniques détectées
    for pourcentage in pourcentages:
        tonique = barraq1.get_tonique(pourcentage)
        toniques.append(barraq1.tonique) # On rajoute la tonique détectée dans la liste

.. code:: python

    toniques




.. parsed-literal::

    [159.466, 166.466, 162.871, 163.871, 183.871, 182.871, 184.871]



Nous voyons que dans cet exemple, jusqu'à 2% des dernières fréquences,
la tonique détectée se trouve dans la zone entre 159.46 et 166.46 Hz.
Avec les pourcentages 5, 7 et 10, elle devient dans la zone de 182 Hz,
ce qui corresponderait à une autre note. Plusieurs exemples nous on
amené à prendre la 0.5% comme valeur par défaut.

Maintenant, on peut se poser la question, sur quelle base le choix de la
tonique a-t-été effectué à partir de ces dernières fréquences ?

La fréquence tonique parmi les dernières fréquences
---------------------------------------------------

Deux méthodes sont disponibles dans ``music22`` pour la détection de la
tonique :

-  La fréquence tonique pourrait être la fréquence la plus présente
   parmi les dernières fréquences : le mode (en termes statistiques);
-  La fréquence pourrait être la fréquence la plus probable, obtenue par
   une Kernel Density Estimation (par défaut).

On peut aussi indiquer la méthode à utiliser comme paramètre de la
méthode .get\_tonique()

.. code:: python

    barraq1.get_tonique(percent=0.5,method="mode")

.. code:: python

    barraq1.tonique




.. parsed-literal::

    167.696



.. code:: python

    barraq1.get_tonique(percent=0.5,method="pdf")

.. code:: python

    barraq1.tonique




.. parsed-literal::

    166.466



Comparons les résultats avec différents pourcentages :

.. code:: python

    pourcentages = [0.1,0.5,1,2,5,7,10]
    toniques_mode = []
    toniques_pdf = []
    for pourcentage in pourcentages:
        tonique_mode = barraq1.get_tonique(pourcentage,method="mode")
        toniques_mode.append(barraq1.tonique) # On rajoute dans la liste toniques_mode
        tonique_pdf = barraq1.get_tonique(pourcentage,method="pdf")
        toniques_pdf.append(barraq1.tonique) # On rajoute dans la liste toniques_pdf

.. code:: python

    toniques_mode




.. parsed-literal::

    [159.201, 167.696, 167.696, 163.866, 184.999, 184.999, 184.999]



.. code:: python

    toniques_pdf




.. parsed-literal::

    [159.466, 166.466, 162.871, 163.871, 183.871, 182.871, 184.871]



Nous voyons que les valeurs détectées par les deux méthodes sont
relativement proches.
