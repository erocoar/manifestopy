# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 15:04:07 2017

@author: Frederik
"""

import json
import requests
import pandas as pd
import operator


class Manifesto(object):
    #functions: meta_format, text_format, mp_request, mp_maindataset, mp_coreversions, mp_metaversions,
    #mp_corecitation, mp_corpuscitation, mp_meta, mp_corpus
    
    def __init__(self, key): 
        try:
            self.api_key = key
            self.key_text = '?api_key=' + self.api_key
            
        except:
            'Missing API key. Please find key at https://manifestoproject.wzb.eu > Profile > API Key.'

        self.manifesto_url = 'https://manifesto-project.wzb.eu'
        self.manifesto_api = 'https://manifesto-project.wzb.eu/tools/'

        self.manifesto_functions = {'versions' : 'api_list_core_versions.json', 'main' : 'api_get_core.json', 'meta' : 'api_metadata.json',
                           'text' : 'api_texts_and_annotations.json', 'metaversions' : 'api_list_metadata_versions.json', 
                           'corecitation' : 'api_get_core_citation.json', 'corpuscitation' : 'api_get_corpus_citation.json'}
        
        self.versions = None
        self.metaversions = None
        self.mp_dataset = None
        
        self.operators = {'>' : operator.gt, '<' : operator.lt,
                          '==' : operator.eq, '>=' : operator.ge,
                          '<=' : operator.le}
                          
    
    def __meta_format__(self, ids):
        
        ids = ['keys[]=' + id_ for id_ in ids]
        ids = '&'.join(ids)
        
        return ids
    
    
    def __text_format__(self, ids):
        
        ids = ['keys[]=' + id_ for id_ in ids]
        ids = '&'.join(ids)
        print(ids)
        return ids
    
        
    def __mp_request__(self, fun, params = None, version = None):
        
        fun = self.manifesto_functions[fun]

        if fun == self.manifesto_functions['text'] or fun == self.manifesto_functions['meta']:
            version = '&version=' + version
            
            if fun == self.manifesto_functions['text']:
                return requests.get(self.manifesto_api + fun + self.key_text + '&' + self.__text_format__(params) + version)
            
            elif fun == self.manifesto_functions['meta']:
                print("test2")
                print(self.manifesto_api + fun + self.key_text + '&' + self.__meta_format__(params) + version)
                return requests.get(self.manifesto_api + fun + self.key_text + '&' + self.__meta_format__(params) + version)
                
        elif not params == None:          
            return requests.get(self.manifesto_api + fun + self.key_text + '&key=' + params)
            
        else:
            return requests.get(self.manifesto_api + fun + self.key_text)
                   

    def mp_maindataset(self, version = 'current'):
        
        if not isinstance(self.versions, pd.core.frame.DataFrame):
            self.mp_coreversions()

        if version == 'current':
            version = self.versions.iloc[-1, 0]
            
        else:
            version = version
            
        r = self.__mp_request__(fun = 'main', params =  version)
                      
        jslist = json.loads(r.text)
               
        self.mp_dataset = pd.DataFrame(data = jslist[1:], columns = jslist[0])
        
        self.mp_dataset['edate']  = pd.to_datetime(self.mp_dataset['edate'], dayfirst = True)
        
        return self.mp_dataset
          
        
    def mp_coreversions(self):
        
        r = self.__mp_request__(fun = 'versions')
        self.versions = pd.DataFrame(json.loads(r.text)['datasets'])
        
        return self.versions
    
        
    def mp_metaversions(self):
        
        r = self.__mp_request__(fun = 'metaversions')
        self.metaversions = pd.DataFrame(json.loads(r.text))
        
        return self.metaversions
    
        
    def mp_corecitation(self, key):
        
        r = self.__mp_request__(fun = 'corecitation', params = key)
        cit = json.loads(r.text)['citation']
        
        return cit
    
    
    def mp_corpuscitation(self, key):
        
        r = self.__mp_request__('corpuscitation', params = key)
        cit = json.loads(r.text)['citation']
        
        return cit

        
    def mp_meta(self, version = 'current', keys = None, date = None, country = None):
        
        if not isinstance(self.versions, pd.core.frame.DataFrame):
            self.mp_coreversions()
            
        if version == 'current':
            if self.metaversions is not None:
                version = self.metaversions.iloc[-1, 0]
            else:
                self.mp_metaversions()
                version = self.metaversions.iloc[-1, 0]
            
        if self.mp_dataset is None:
            self.mp_maindataset()
        
        if country is not None and date is not None:
            if len(date.split()) > 1:
                key_inds = self.mp_dataset[(self.operators[date.split()[0]](self.mp_dataset['edate'], date.split()[1])) & (self.mp_dataset['countryname'] == country)]
                keys = list(key_inds['party'] + '_' + key_inds['date'])
                
            else:
                key_inds = self.mp_dataset[(self.mp_dataset['edate'] == date) & (self.mp_dataset['countryname'] == country)]
                keys = list(key_inds['party'] + '_' + key_inds['date'])
                
        elif date is not None:
            if len(date.split()) > 1:
                key_inds = self.mp_dataset[self.operators[date.split()[0]](self.mp_dataset['edate'], date.split()[1])]
                keys = list(key_inds['party'] + '_' + key_inds['date'])
                
            else:
                key_inds = self.mp_dataset[self.mp_dataset['edate'] == date]
                keys = list(key_inds['party'] + '_' + key_inds['date'])
                
        elif country is not None:           
            key_inds = self.mp_dataset[self.mp_dataset['countryname'] == country]
            keys = list(key_inds['party'] + '_' + key_inds['date'])
            
        else:
            if not isinstance(keys, list):
                keys = [keys]
            
            else: 
                pass
                        
        r = self.__mp_request__(fun = 'meta', params = keys, version = version)
        
        return pd.DataFrame(json.loads(r.text)['items'])
    

    def mp_corpus(self, version = 'current', keys = None, date = None, country = None):
                       
        if not isinstance(self.versions, pd.core.frame.DataFrame):
            self.mp_coreversions()
        
        if version == 'current':
            if self.metaversions is not None:
                version = self.metaversions.iloc[-1, 0]
            else:
                self.mp_metaversions()
                version = self.metaversions.iloc[-1, 0]
                
        keys = self.mp_meta(version = version, keys = keys, date = date, country = country)
        keys = keys['manifesto_id']       
        
        r = self.__mp_request__(fun = 'text', params = keys, version = version)
        
        r = json.loads(r.text)
        
        return r

