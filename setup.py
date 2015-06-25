from setuptools import setup

setup(
	name='scholarcitation',
	version='1.0',
	author='Manuel Parra-Royon',
	author_email='manuelparra@decsai.ugr.es',      	
    description = ("Google Scholar citation indices tool "),
    packages= ["scholarcitation"],
    install_requires = ["BeautifulSoup","requests"]
)