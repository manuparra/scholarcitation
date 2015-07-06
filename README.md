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

It will solve packages dependences, but if you want resolve manually, scholarcitation requiere the next python packages:

* BeautifulSoup
* requests

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

```bash
1174     770    15    15    22    18
|        |      |     |     |     |
|        |      |     |     |     + --- i10 index from 2010
|        |      |     |     + --- i10 index
|        |      |     + --- h-index from 2010
|        |      + --- h-index
|        + --- Citation from 2010
+ --- AllCitation
```







