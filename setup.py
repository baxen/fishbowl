#!/usr/bin/env python

from setuptools import setup, find_packages

requirements = [
    'matplotlib>=2.0.0'
]

setup(
    name='fishbowl',
    version='0.3.1',
    description='Customizable matplotlib style extension',
    author='Bradley Axen',
    author_email='bradley.axen@gmail.com',
    url='https://github.com/baxen/fishbowl',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: Visualization',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='style plotting matplotlib',
    install_requires=requirements,
    package_data={
        'fishbowl': ['config/fishbowl.axes.json',
                     'config/fishbowl.palettes.json']
    }
)
