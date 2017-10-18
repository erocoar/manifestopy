# manifestopy
## accessing manifesto project api in python
manifestopy is a small package to use the basic functions of the manifesto project API in python.

### importing manifestopy
```python
from manifestopy import manifestopy as mp
```
### using manifestopy
connect to the manifesto api by initializing the Manifesto object
```python
manifesto = mp.Manifesto('API key goes here')
```

### functions
* **mp_coreversions**

list the core dataset versions
```python
manifesto.mp_coreversions()
```

* **mp_metaversions

list corpus metadata versions
```python
manifesto.mp_metaversions()
```

* **mp_maindataset

gets the specified version of the core dataset (default = most recent dataset)
```python
manifesto.mp_maindataset(version = 'current')
```

* **mp_meta

corpus metadata for a list of parties in elections, with specified party, date, country
```python
manifesto.mp_meta(version = 'current', keys = None, date = None, country = None)
```

* **mp_corecitation

get citation for the core dataset.
```python
manifesto.mp_corecitation(key)
```

* **mp_corpuscitation

get citation for corpus dataset
```python
manifesto.mp_corpuscitation(key)
```




