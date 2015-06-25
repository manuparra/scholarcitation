Google Scholar citation indices tool
====================================

This package contain a few tools to query Google Scholar API

* Search and Retrieve citations indices by author name
* Search and Retrieve citations indices by author id


### Installation:

Downloag package:

https://github.com/manuparra/scholarcitation.git


Install package
```bash
python setup.py install
```


#### Command line tools

Use commandline tool directly for retrieve authors :

```bash
python scholarcitation/scholarcitation.py -a "Jose M. Benitez"
```
It returns authors name list and authors Scholar IDs

Use commandline tool directly for retrieve citations :
```bash
python scholarcitation/scholarcitation.py -c "HULIk-QAAAAJ"
```


