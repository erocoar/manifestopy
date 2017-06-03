# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 15:04:07 2017

@author: Frederik
"""

import urllib
import json
import requests

class Manifesto(object):
    def __init__(self, api):
        self.manifesto_url = 'https://manifesto-project.wzb.eu'
        self.manifesto_api = 'https://manifesto-project.wzb.eu/tools/'
        self.api_key = api

        self.manifesto_functions = {'versions' : 'api_list_core_versions.json', 'main' : 'api_get_core.json', 'meta' : 'api_metadata.json',
                           'text' : 'api_texts_and_annotations.json', 'metaversions' : 'api_list_metadata_versions.json', 
                           'corecitation' : 'api_get_core_citation.json', 'corpuscitation' : 'api_get_corpus_citation.json'}
 
    def mp_request(self, function):
        r = requests.get(self.manifesto_url + function)