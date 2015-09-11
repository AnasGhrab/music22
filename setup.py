from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='music22',
      version='0.0.2',
      description='A tool for musicological analysis from audio files. For a symbolic analysis, you can use Music21 (http://web.mit.edu/music21/). Now it is focused on modal music analysis : Scale analysis, tonic detection',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
      ],
      keywords='musicology analysis from non-symbolic data',
      url='https://github.com/AnasGhrab/music22',
      author='Anas Ghrab',
      author_email='anas.ghrab@gmail.com',
      license='MIT',
      packages=['music22',
		],
      install_requires=[
          'numpy','matplotlib','scipy'
      ],
      zip_safe=False)
