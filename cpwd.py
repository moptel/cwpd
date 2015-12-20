import urllib,urllib2
import xml.etree.ElementTree as ET
import random
import os, sys
import threading
import Queue
import argparse
import time
from socket import timeout


def random_ip():
	a=random.randint(212,216)
	b=random. randint(1,254)
	c=random. randint(1,254)
	d=random. randint(1,254)
	return '{}.{}.{}.{}'.format(a,b,c,d)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

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

def search_wp_plugins(target,wpcontent='wp-content',n_threads=8):
	f=open('plugins.lst','r')
	q=Queue.Queue()
	#Arrancamos tantas threads como se indiquen
	for i in range(0,n_threads):
		#El hilo ejecuta find_wp con q y wpcontent como argumentos
		t = threading.Thread(name=str(i),target=find_wp,args=(q,wpcontent))
		t.start()
	#Metemos en cola todos los argumentos que queremos procesar
	for line in f.readlines():
		q.put(line)
	#Esperamos a que todos terminen
	q.join()
	f.close()
	return 
	
def find_wp(q,wpcontent):
	while True:
		try:
			#Intentamos asignar un valor de la cola al thread. Si falla, retornamos
			try:
				plugin=q.get(True,2).split(':')
			except:
				return
			head={'X-Forwarded-For' : random_ip()+','+random_ip(),'User-agent' : random_agent(),'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US;q=0.5,en;q=0.3','Accept-Encoding': 'gzip, deflate','DNT': '1'}
			req=urllib2.Request(target+"/"+wpcontent+plugin[0],headers=head)
			maxtries=0
			#Intentamos hacer la peticion
			while maxtries<10:
				try:
					res=urllib2.urlopen(req,timeout=4)
					code=res.getcode()
					#En caso de que la respuesta sea 200 y la direccion de peticion y respuesta sean iguales,
					#hemos encontrado un plugin
					if code==200 and req.get_full_url()==res.geturl():
						print "\nFound plugin: "+plugin[1].rstrip('\n')
						f=open('data.tmp','a')
						f.write(plugin[1]+'\n')
						f.close()
					break
				except urllib2.HTTPError as e:
					if e.code==403:
					#En caso de respuesta 403 y mensaje con 'forbidden', hemos encontrado un plugin.
					#Posiblemente haya que refinar este metodo
						if 'Forbidden' in str(e.read()):
							print "\nFound plugin: "+plugin[1].rstrip('\n')
							f=open('data.tmp','a')
							f.write(plugin[1]+'\n')
							f.close()
					break
				#En caso de timeout seguimos. Probablemente deberia reintentarlo en ese caso, pero paso
				except (urllib2.URLError,timeout):
					maxtries+=1
					print "Timeout error: "+str(maxtries)
			q.task_done()
		except KeyboardInterrupt:
			raise	
			

print """
 _____                _        _    _               _______                  
/  __ \              | |      | |  | |             | | ___ \                 
| /  \/_ __ _   _  __| | ___  | |  | | ___  _ __ __| | |_/ / __ ___  ___ ___ 
| |   | '__| | | |/ _` |/ _ \ | |/\| |/ _ \| '__/ _` |  __/ '__/ _ \/ __/ __|
| \__/\ |  | |_| | (_| |  __/ \  /\  / (_) | | | (_| | |  | | |  __/\__ \__ \ 
 \____/_|   \__,_|\__,_|\___|  \/  \/ \___/|_|  \__,_\_|  |_|  \___||___/___/
______ _             _        ______     _            _                      
| ___ \ |           (_)       |  _  \   | |          | |                     
| |_/ / |_   _  __ _ _ _ __   | | | |___| |_ ___  ___| |_ ___  _ __          
|  __/| | | | |/ _` | | '_ \  | | | / _ \ __/ _ \/ __| __/ _ \| '__|         
| |   | | |_| | (_| | | | | | | |/ /  __/ ||  __/ (__| || (_) | |            
\_|   |_|\__,_|\__, |_|_| |_| |___/ \___|\__\___|\___|\__\___/|_|            
                __/ |                                                        
               |___/                                                         
"""
print "Crude WordPress Plugin Detector v1.0 by >moptel\n"
start_time=time.time()
parser = argparse.ArgumentParser(description='Rude and crude script to scan for WordPress plugins')
parser.add_argument('host',metavar='host',nargs='?',help='target to be scanned')
parser.add_argument('-w',metavar='folder', type=str,default='wp-content', help='wp-content folder (wp-content by default)')
parser.add_argument('-t', metavar='int',type=int, default=8, help='number of threads (default=8)')
args = parser.parse_args()

if args.host:
	tmp='data.tmp'
	print "Searching "+str(file_len('plugins.lst'))+" plugins..."
	target=args.host

	wpc=args.w
	n_threads=args.t

	search_wp_plugins(target,wpc,n_threads)
	#Guardamos el output en un archivo
	out="cwpd_"+target.replace('https://','')+".txt"
	if os.path.isfile(out):
		os.remove(out)
	f=open(out,"w")
	f.write("---Output of WordPress Plugin Detector---\nDomain: "+target)
	f.write("\nby moptel\n\n")
	f.write("Detected plugins:\n\n")
	tmp_f=open(tmp,'r')
	for line in tmp_f.readlines():
		f.write(line)
	f.close()
	tmp_f.close()
	os.remove(tmp)
else:
	parser.print_help()
elapsed_time=time.time()-start_time
if elapsed_time<60:
	print '\nElapsed time: '+str(elapsed_time)+' seconds'
else:
	print 'Elapsed time: '+str(int(elapsed_time/60))+' minutes and '+str(int(elapsed_time%60))+' seconds'
