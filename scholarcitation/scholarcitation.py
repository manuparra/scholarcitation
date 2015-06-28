#! /usr/bin/env python
"""
This command-line application provides tools for querying Google Scholar
Authors and Citation indices.
It currently only processes the first results page.

Copyright 2015 Manuel Parra Royon manuelparra@decsai.ugr.es

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import optparse
import os
import sys
import re
import urlparse





try:
	# Try importing for Python 3	
	from urllib.parse import quote, unquote
	from http.cookiejar import MozillaCookieJar
except ImportError:	
	from urllib2 import Request, build_opener, HTTPCookieProcessor, urlopen
	from urllib import quote, unquote    
	from cookielib import MozillaCookieJar


# Import BeautifulSoup -- try 4 first, fall back to older
try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        print('Install BeautifulSoup package  sorry...')
        sys.exit(1)

try:
	from requests import get 
except ImportError:
	print('Install Requests packages, sorry...')
	sys.exit(1)
else:
	import requests 


# Support unicode in both Python 2 and 3. In Python 3, unicode is str.
if sys.version_info[0] == 3:
    unicode = str # pylint: disable-msg=W0622
    encode = lambda s: s # pylint: disable-msg=C0103
else:
    def encode(s):
        if isinstance(s, basestring):
            return s.encode('utf-8') # pylint: disable-msg=C0103
        else:
            return str(s)


class ScholarAuthors(object):
	"""Scholar Authors Class.

    """

	def __init__(self,author_name=None, author_id=None):
		self.author_name=author_name
		self.author_id=author_id
	
	def __str__(self):
		
		_strret= '{0:30}     {1:12}\n'.format("Author", "Scholar ID")
		_strret=_strret + '{0:30}     {1:20}\n'.format("------------------------------", "---------------")
		_strret=_strret + '{0:30}     {1:12}\n'.format(self.author_name, self.author_id)

		return _strret


class ScholarAuthorsCitations(object):
	"""Scholar Authors Citation Class.

    """
	def __init__(self,all_cit=None, f2010_cit=None,hindex_cit=None,
					f2010hindex_cit=None,i10index_cit=None,fi10index_cit=None):
		"""
		Init method
		
		"""
		self.all_cit=int(all_cit)
		self.f2010_cit=int(f2010_cit)
		self.hindex_cit=int(hindex_cit)
		self.f2010hindex_cit=int(f2010hindex_cit)
		self.i10index_cit=int(i10index_cit)
		self.fi10index_cit=int(fi10index_cit)

	def __str__(self):
		
		_strret= '{0:6d}  {1:6d}  {2:4d}  {3:4d}  {4:4d}  {5:4d}\n'.format(self.all_cit,self.f2010_cit,self.hindex_cit,self.f2010hindex_cit,self.i10index_cit,self.fi10index_cit)
		
		return _strret	



class ScholarConf(object):
	"""Scholar Configuration class

	This class contains basic configuration parameters about the Scholar API

    """
	VERSION = '2.9'
	LOG_LEVEL = 1
	MAX_PAGE_RESULTS = 20 # Current maximum for per-page results
	SCHOLAR_SITE = 'https://scholar.google.com/'
	USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'
	


class ParserAuthors(object):
	"""XHTML Scholar Authors parser Class

	Parse Authors from XHTML returned by the google scholar app.
	Ids: gsc_1usr_name and gs_hlt are parsed.
    """

	def __init__(self,data):
		"""
		Init method

		"""		
		self.chunk=data
		self.results=[]
	def __call__(self,data):
		"""
		Call method

		"""
		self.chunk=data
		self.results=[]

	def __process(self):
		"""
		Process method

		"""
		bs=BeautifulSoup (self.chunk)
		lst_auths_html=bs.findAll("h3",{"class":"gsc_1usr_name"})
		
		for l in lst_auths_html:
			a_code=l.find_all("a",href=True)
			a_name=l.findAll("span",{"class":"gs_hlt"})
			for a in a_code:			
				url = urlparse.urlparse(a["href"])
				params = urlparse.parse_qs(url.query)			
				self.results.append(ScholarAuthors(author_name=a.text,author_id=params['user'][0]))		

	def parse(self):	
		"""
		Parse method

		"""	
		self.__process()			


class ParserCitation(object):
	"""XHTML Scholar Citation parser Class

	Parse Citation Number from XHTML returned by the google scholar app.
	Ids: gsc_rsb_st and gsc_rsb_std are parsed.
    """

	def __init__(self,data):
		"""
		Init function
		"""
		self.chunk=data
		self.result=None

	def __process(self):
		"""
		Process method 

		"""
		bs=BeautifulSoup (self.chunk)
		lst_citations_html=bs.findAll("table",{"id":"gsc_rsb_st"})

		for l in lst_citations_html:
			lst_cit_row=l.findAll("td",{"class":"gsc_rsb_std"})
			all_cit=lst_cit_row[0].text
			f2010_cit=lst_cit_row[1].text
			hindex_cit=lst_cit_row[2].text
			f2010hindex_cit=lst_cit_row[3].text
			i10index_cit=lst_cit_row[4].text
			fi10index_cit=lst_cit_row[5].text
			self.result=ScholarAuthorsCitations(all_cit=all_cit, f2010_cit=f2010_cit,hindex_cit=hindex_cit,f2010hindex_cit=f2010hindex_cit,i10index_cit=i10index_cit,fi10index_cit=fi10index_cit)
		
	def parse(self):	
		"""
		Parse Method
		"""	
		self.__process()					


class ScholarQ(object):
	"""Scholar Query Class

	Prepare the query and run for Google Scholar.
    """


	GET_AUTHOR_URL=ScholarConf.SCHOLAR_SITE + "citations"
	def __init__(self):
		"""
		Init method
		"""
		self.url_authors_params = {	'view_op':'search_authors',
									'mauthors':'',
									'hl':'en',
									'oi':'ao'} 

		self.url_author_params = {	'user':'',								
									'hl':'en'} 
		self.author_name=""
		self.author_id=""
		self.author_list=[]
		self.citations_list=[]
		

	def set_author(self,author):
		"""
		Set the authors name

		"""
		self.author_name=author
		self.url_authors_params['mauthors']=author

	def set_author_id(self,id_user):
		"""
		Set the author id for the author name

		"""
		self.author_id=id_user
		self.url_author_params['user']=id_user

	def get_authors(self):
		"""
		Get authors list.

		"""
		r = requests.get(self.GET_AUTHOR_URL, verify=False, 
            	params=self.url_authors_params, 
              	headers={'User-Agent': ScholarConf.USER_AGENT})

		auth_list=ParserAuthors(data=r.text)
		auth_list.parse()
		self.author_list=auth_list.results		
		
	def get_citations(self):
		"""
		Get citations's list

		"""
		r = requests.get(self.GET_AUTHOR_URL, verify=False, 
            	params=self.url_author_params, 
              	headers={'User-Agent': ScholarConf.USER_AGENT})

		cit_list=ParserCitation(data=r.text)
		cit_list.parse()
		self.citations_list=cit_list.result

	def print_authors(self):
		"""
		Print 
		"""


def main():

	import urlparse
	#Disable warnings
	requests.packages.urllib3.disable_warnings()

	#Sintax msg
	usage = """scholarcitation.py [options] <query string>

A python command-line interface to Google Scholar citation indices
	
Examples:	
# Query the author by name and return name of authors and users ID.
scholarcitation.py -a 'Jose M. Benitez'

#It returns Google Scholar ID for the given researcher.

# Query citation for the user ID.
scholarcitation.py -i 'HULIk-QAAAAJ'

#It returns Google Scholar citantions for the given ID researcher following next scheme:
AllCites  CitesFrom2010  h-index  h-indexFrom2010 i10-index  i10-indexFrom2010."""




	
	#Command line options
	fmt = optparse.IndentedHelpFormatter(max_help_position=50, width=100)
	parser = optparse.OptionParser(usage=usage, formatter=fmt)
	
	group = optparse.OptionGroup(parser, 'Query arguments',
                                 'These options define search query arguments and parameters.')
	#Author option
	group.add_option('-a', '--author', metavar='AUTHOR', default=None,
                     help='Authors option')

	#Cites option
	group.add_option('-c', '--cites', metavar='CITES', default=None,
                     help='Citation option' )

	#Parse data from arguments
	parser.add_option_group(group)

	options, _ = parser.parse_args()


	#0 Arguments: exit
	if len(sys.argv) == 1:
		parser.print_help()
		return 1
	
	sq=ScholarQ()
	if options.author!=None:
		#Executing Author Option 		
		sq.set_author(author=options.author)
		sq.get_authors()
		for i in sq.author_list:
			print i

	else:
		#Executing Citations Option
		sq.set_author_id(id_user=options.cites)
		sq.get_citations()

		print sq.citations_list			





if __name__ == "__main__":
	"""
	Main function


	"""

	main()
	sys.exit(0)


