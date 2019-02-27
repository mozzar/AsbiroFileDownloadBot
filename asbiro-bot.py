#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib
import urllib2
import requests

from lxml import html

import re
from os.path import basename
import os
from urlparse import urlsplit
import platform
import sys

''' DEFINICJE '''
''' Bot stworzony wyłącznie w celach edukacyjnych i po to by ułatwić studentom asbiro pobieranie materiałów z wyszukiwania :)'''



'''czy ma pobierac plik , czy tylko zapisac linki do samego pliku? True=pobierac False = nie pobierac'''
pobieranie = False

'''typ pliku do wyszukania i ewentualnego pobrania (mp3 , mp4, pdf)'''
typpliku = "pdf" 

'''ilosc stron w wyszukiwaniu na asbiro ( by obliczyć do ilości stron z asbiro dodajemy +1 czyli jak mamy 2 strony wyszukiwania to wpisujemy 3 )'''
przedzial_plikow = 41 

'''dane do logowania na asbiro.pl'''
username = 'użytkownik'
password = 'hasło'


''' Jak nie wiesz jak zmienić to najlepiej nie zmieniaj'''
lineczek = "https://www.asbiro.pl/nagrania/?search[phrase]=&search[category]=&search[access]=yes&search[watched]=&search[lang]=&search[sort]=0&page_no="
'''plik start (od jakiej strony z linkami do dzialow ma zaczac najlepiej nie zmieniaj!!!'''
plikstart = 1





''' Ponizej najlepiej nic nie zmieniaj bo zepsujesz ;) '''

vers = platform.python_version()
splv = vers.split(".")
pyver = splv[0] + "."+ splv[1]
if pyver != "2.7":
	sys.exit("Program wymaga wersji pythona 2.7.12!")


def url2name(url):
    return basename(urlsplit(url)[2])

def download(url, out_path):
    localName = url2name(url)
    req = urllib2.Request(url)
    checkav = True
    try:
        r = urllib2.urlopen(req)
		
    except urllib2.HTTPError as e:
        checkav = False
        if e.code == 404:
            print "pliku juz nie ma"
           
        else:
            print "nieznany blad"
    except urllib2.URLError as e:
        checkav = False
        print "connection refused "
		
    
    if checkav == True:    
        if r.info().has_key('Content-Disposition'):
      
            localName = r.info()['Content-Disposition'].split('filename=')[1]
            if localName[0] == '"' or localName[0] == "'":
                localName = localName[1:-1]
        elif r.url != url: 
        
            localName = url2name(r.url)

        localName = os.path.join(out_path, localName)
        f = open(localName, 'wb')
        f.write(r.read())
        f.close()

wp_login = 'https://www.asbiro.pl/wp-login.php'

with requests.Session() as s:
    headers1 = { 'Cookie':'wordpress_test_cookie=WP Cookie check' }
    site="https://www.asbiro.pl/nagrania/?search[phrase]=&search[category]=&search[access]=yes&search[watched]=&search[lang]=&search[sort]=0&page_no=1"

    datas={ 
        'log':username, 'pwd':password, 'wp-submit':'Zaloguj', 
        'redirect_to':site, 'testcookie':'1'  
    }
    s.post(wp_login, headers=headers1, data=datas)
    #41
    for x in range(przedzial_plikow):
		if x > 0:
			nazwa = str(x)+".txt"
			if os.path.isfile(nazwa) == False:
				site=lineczek+str(x)
				resp = s.get(site)
				
				tree = html.fromstring(resp.content)
				
				links = tree.xpath('//a[contains(@class,"neutral")]/@href')
				
			
				f = open( nazwa, "w+")
				f.write(str(links).replace("'", "").replace("[", "").replace("]", "").replace(", /polityka-prywatnosci-i-cookies/, /zasady-uzytkowania", ""))
				f.close()
			
if plikstart-1 > 0:
	numerowanie =(plikstart-1)*10
else:
	numerowanie = 0	
	

count =0
for x in range(przedzial_plikow):
	if x > 0:
		if x >= plikstart: 
			f=open(str(x) + ".txt", "r")
			if f.mode == 'r':
				contents = f.read()
				contents = str(contents)
				splited = contents.split(',')
				count = len(splited)
				print "Pobieram wyniki z strony: " + str(x)
				
				for y in range(count):
					resp = s.get(splited[y])
					tree = html.fromstring(resp.content)
					links = tree.xpath('//a[contains(@href,"'+typpliku+'")]/@href')
					nazwa = "linki-"+str(x)+ "-link-"+ str(y)+"-" +typpliku+".txt"
					tytul = tree.xpath('//h1[contains(@itemprop,"headline")]/text()')
				
				
					#tytul = re.sub('[^A-Z a-z]+', '', str(tytul))
					#print str(tytul)
					numerowanie = numerowanie+1
				
					tytnew = str(tytul).replace("[u'", "").replace("/", "").replace("?", "").replace("[", "").replace("\xf3w", "a").replace("\xf3", "ó").replace("'", "").replace("]", "").replace("']", "").replace("\u0105","ą").replace("\u0107","ć").replace("\u017a","ź").replace("\u017c","ż").replace("\u00f3","ó").replace("\u0142","ł").replace("\u0119","ę").replace("\u015b","ś").replace("\u0144","ń")
					if numerowanie < 10:
						dodatek = "00"
					if numerowanie >= 10: 
						dodatek = "0"
					if numerowanie > 99:
						dodatek = ""
					
				
					tytul = dodatek + str(numerowanie) + " "+ tytnew
					if os.path.isdir(str(tytul)) == False:
						os.makedirs(str(tytul))
						
						opis = tree.xpath('//div[contains(@class, "text")]/text()')
						formatted = str(opis).replace("[u'", "").replace("'", "").replace("']", "").replace("\xf3w", "a").replace("\xf3", "ó").replace("\u0105","ą").replace("\u0107","ć").replace("\u017a","ź").replace("\u017c","ż").replace("\u00f3","ó").replace("\u0142","ł").replace("\u0119","ę").replace("\u015b","ś").replace("\u0144","ń")
					
					
						k = open(tytul +"/opis.txt", "w+")
					
						
						formacik = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', formatted, flags=re.M)
					
						k.write(str(formacik))
						k.close()
					
					
					n=open( tytul+"/"+nazwa,"w+")
					czar = str(links).replace("'", "").replace("[", "").replace("]", "")
					n.write(czar)
					n.close()
					pik = czar.split(',')
					ran = len(pik)
				
				
					if pobieranie == True:
						if "https" in pik[0]:
							for z in range(ran):
								download(pik[z], tytul + "/")
						else:
							print("brak plikow typu "+typpliku+" w tytule: " + tytul + "")

				
				
