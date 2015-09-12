=================================================
Music22: Modal Musical Analysis
=================================================

Overview
========

Music22 is a Python2 package for musicological analysis, especially modal music and melodies. The analysis is done from audio files.

For now, it's main features are :

* Fondamental frequencies extraction (using *PredominentMelody()* from **Essentia**);
* Getting the main frequencies as peaks of the probability density function from frequencies;
* Comparing PDFs using a correlation coefficient;
* Getting a similarity matrix between melodies.

Installation
============

To use Music22, you need to manually install `Essentia`_. `In futur versions, it will be also possible to use` `TimeSide`_.

Then, install Music22 with the following :

.. code:: python
	
	pip install music22

Or using ``git``:

.. code:: python

	git clone https://github.com/AnasGhrab/music22
	python setup.py install


.. _Essentia: http://essentia.upf.edu/
.. _TimeSide: https://github.com/Parisson/TimeSide

Basic Usage
===========

To use Music22 :

.. code:: python

	from music22 import modalis,scale
	path = "path/to/a/folder/with/audios/wav/files/"
	Kchants = modalis.melodies(path,transpose='Yes',freqref=300)
	
Then you can

.. code:: python

	Kchants.pdf_show()
	Kchants.matrix()
	Kchants.melodies[0].scale
		
To Do
=====


Contact
=======

Homepage: http://anas.ghrab.tn

Email:

 * Anas Ghrab <anas.ghrab@gmail.com>

License
=======

The MIT License (MIT)

Copyright (c) 2015 Anas Ghrab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

