# Searches popular plugins on wordpress and saves them in plugins.lst

 
import urllib,urllib2
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import random
import zlib
import time
import os.path

def remove_duplicates(file):
	print "\nRemoving duplicates..."
	f=open(file,'r')
	lines=f.readlines()
	f.close()
	f=open(file,'w')
	lines_seen=[]
	for line in lines:
		if line not in lines_seen:
			f.write(line)
			lines_seen.append(line)

def random_agent():
	e=ET.parse('useragents.xml').getroot()
	ua_list=[]
	#Leemos el archivo xml. Por como esta estructurado, tocan los if
	#para evitar los separadores y entrar en lo de folder.	
	for child in e:
		if child.tag=='useragent':
			ua_list.append(child.attrib['useragent'])
		elif child.tag=='folder':
			for children in child:
				if children.tag=='useragent':
					ua_list.append(children.attrib['useragent'])
	#Se devuelve un user agent al "azar"
	return ua_list[random.randint(0,len(ua_list)-1)]

	
	
def listmaker(i):
	print "Processing page "+str(i)
	head={'User-agent' : random_agent(),'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US;q=0.5,en;q=0.3','Accept-Encoding': 'gzip, deflate','DNT': '1'}
	base="https://wordpress.org/plugins/browse/popular/"
	maxtries=0
	
	if i==1:
		req=urllib2.Request(base,headers=head)
	else:
		req=urllib2.Request(base+"page/"+str(i),headers=head)
	while maxtries<10:	
		try:
			res=urllib2.urlopen(req)
			break
		except urllib2.HTTPError:
			maxtries+=1
			print str(req.get_full_url())+" FAILED "+str(maxtries)+" times!!"
			print "Sleeping {} seconds".format(maxtries*10)
			time.sleep(maxtries*10)
	data=res.read()
	if 'gzip' in str(res.info()):
		decomp = zlib.decompressobj(16 + zlib.MAX_WBITS)
		decdata = decomp.decompress(data)
	else:
		decdata=data
	soup=BeautifulSoup(decdata)
	atags=soup.findAll('h4')
	
	for tag in atags:
		z=tag.contents
		titulo=tag.string
		s=str(z[0])
		b=s.find("\"")+1
		e=s.find("\"",b)
		n=s[b:e].split('https://wordpress.org')
		f=open('plugins.lst','a')
		f.write(n[1].encode('UTF-8')+'readme.txt:'+titulo.encode('UTF-8')+'\n')
		f.close()
		
		
print """                                                                                ;##;
                                                           ```                  ;@@'
                                                           @@@,                 ;@@'
                                                           @@@,                 ;@@'
                .      .`          .`             `.       @@@.        `.       ;@@'
.,,`     #@@;;@@@@@  @@@@@      +@@@@@@     #@@:+@@@@@   @@@@@@@@    @@@@@@:    ;@@'
,,,,`    #@@@@@@@@@;@@@@@@@    @@@@@@@@@,   #@@@@@@@@@@  @@@@@@@@   @@@@@@@@#   ;@@'
 :,,,    #@@@@,:@@@@@;.@@@@   +@@@@,:@@@@   #@@@@:,@@@@@ ##@@@###  @@@@  .@@@   ;@@'
  :,,,`  #@@@   .@@@    @@@   @@@;    @@@@  #@@#    '@@@   @@@,   ,@@@     @@@  ;@@'
   :,,,  #@@;    @@@    @@@   @@@     .@@@  #@@:     @@@   @@@,   @@@.     @@@  ;@@'
    :;,  #@@;    @@@    @@@  ,@@@      @@@  #@@:     @@@`  @@@,   @@@@@@@@@@@@  ;@@'
    ,;,  #@@;    @@@    @@@  ,@@@      @@@  #@@:     @@@`  @@@,   @@@@@@@@@@@@  ;@@'
   ,,,:  #@@;    @@@    @@@   @@@     ;@@@  #@@:     @@@   @@@,   @@@+          ;@@'
  ,,,:   #@@;    @@@    @@@   @@@@    @@@'  #@@@    @@@@   @@@;    @@@          ;@@'
 ,,,:    #@@;    @@@    @@@   `@@@@@@@@@@   #@@@@@@@@@@'   @@@@@@  @@@@@:;@@@   ;@@'
 :,:     #@@;    @@@    @@@    ;@@@@@@@@    #@@:@@@@@@@    `@@@@@   @@@@@@@@@   ;@@'
  :      @@@;    @@@    @@@      @@@@@'     #@@: @@@@'      ;@@@@    :@@@@@'    '@@+
                                            #@@:                                    
                                            #@@:                                    
                                            #@@:                                    
                                            #@@:                                    
"""
print "CWPD List Generator v1.0"
print "Now with 25% more zinc!"
print "Scraping wordpress for plugin names since 2015!\n"


if os.path.isfile('plugins.lst'):
	print "Warning! You already have a file named 'plugins.lst'. If you continue this file will be overwritten!"
	cont=raw_input("Do you wish to continue?(y/n): ")
	if cont=='y' or cont=='Y':
		print "Making the list...(BIP)"
		for i in range(1,51):
			listmaker(i)
		remove_duplicates('plugins.lst')
		print "Done!"
	else:
		print "Aborting..."
else:
	print "Making the list...(BIP)"
	for i in range(1,51):
		listmaker(i)
	remove_duplicates('plugins.lst')
	print "Done!"
