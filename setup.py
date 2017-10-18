# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 17:12:21 2017

@author: Frederik
"""

from setuptools import setup

setup(name = 'manifestopy',
      version = '0.8',
      description = 'Accessing Manifesto Project API with Python',
      url = 'https://github.com/erocoar/manifesto.py',
      author = 'Frederik Tiedemann',
      author_email = 'f.j.tiedemann@umail.leidenuniv.nl',
      license = 'MIT',
      packages = ['manifestopy'],
      install_requires = ['requests', 
                          'pandas'],
      zip_safe = False)