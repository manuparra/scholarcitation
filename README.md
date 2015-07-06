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
python scholarcitation/scholarcitation.py -a "Benitez"
```
It returns authors name list and authors Scholar IDs:

```bash
Claudia Benitez-Nelson                            	nEuGaD4AAAAJ
Pablo Benítez                                    	  xUa4mvQAAAAJ
Carmen Benitez                                    	nKmzlbUAAAAJ
Jose M. Benitez                                   	1iSTbIkAAAAJ
Fernando Caballero Benítez                       	  nb2teTwAAAAJ
Bruno A Benitez                                   	oKv9jsUAAAAJ
Diego S. Benitez                                  	tUshCMcAAAAJ
Julio Cesar Benitez Medina                        	vq_KS3UAAAAJ
Miguel López-Benítez                            	  CPeHC9IAAAAJ
Antonio Benítez-Burraco                          	  BIgRcW4AAAAJ
```

And then you can use commandline tool directly for retrieve author ID citations:
```bash
python scholarcitation/scholarcitation.py -c "1iSTbIkAAAAJ"
```
It returns full list of citation indices with the next format:

AllCitation CitationFrom2010 h-index h-index2010 i10index i10index2010

i.e.

```bash
1174     770    15    15    22    18
```



