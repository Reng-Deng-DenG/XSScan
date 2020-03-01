#coding:utf-8
from selenium import webdriver
from selenium.common.exceptions import *
from urllib.parse import urlparse
from urllib.parse import parse_qs
from lib.function import inject
import os
import warnings
from colorama import init
from colorama import Fore, Back, Style
warnings.filterwarnings('ignore')
init()

print(Style.BRIGHT)# On met le style en brillant

# Connexion au driver + emplacement du fichier
# Lien de téléchargement du driver https://phantomjs.org/download.html
try:
	driver = webdriver.PhantomJS("C:\\Users\\lucas-pc\\Desktop\\XSScan\\phantomjs.exe");
except WebDriverException as exception:
	print(Fore.RED+ '[!] Impossible de se connecter au driver' + Fore.RESET);
	print(Fore.YELLOW +'[?] Vérifier l\'emplacement du chemin du driver' + Fore.RESET);
	exit();

# Fonction qui retourne True si une url est vulnérable à la faille XSS
def xss(URL):
	driver.get(URL);# Connexion à l'url
	page = driver.page_source;# On récupére le corp de la page
	if '1ts+Vu1nerab1e!' in page: # Si le mot-clée est trouver dans la page alors c'est vulnérable
		return True;
	else:
		return False;
# Fonction pour iniatialiser des cookies
# /!\ En cour de test /!\
def init_cookie(url):

	urlparsed = urlparse(url)# On parse l'url pour récupérer ses composants

	domain = urlparsed.netloc# Récupération du domain 

	if 'www' in domain:
		domain.replace('www', '.')# On remplace www par un point, se qui donne (.domain.com) 
	else:
		domain = '.' + domain# On ajoute un point, se qui donne (.domain.com)

	cookie_name = input('[?] Nom de la cookie (ex: PHPSESSID) : ')
	cookie_name = cookie_name.strip()
	cookie_value = input('[?] Valeur de la cookie (ex: 0j69jtouvjhf8) : ')
	cookie_value = cookie_value.strip()
	cookie_items = []

	cookie_items.append(domain)# Ajout du domaine
	cookie_items.append(cookie_name)# Ajout du nom de la cookie
	cookie_items.append(cookie_value)# Ajout de la valeur du cookie

	domain = urlparsed.scheme + '://' + urlparsed.netloc# Création de l'url pour iniatialiser les cookies

	driver.get(domain)# Connexion au domain
	driver.delete_all_cookies()# Suppresion des cookies qui sont prêt à être chargées
	driver.add_cookie({'domain': cookie_items[0], 'name': cookie_items[1],'value': cookie_items[2], 'path': '/','expires': None})# Ajout des cookies
	driver.get(url);


banner = """
 __  __  ___   ___                    
 \ \/ / / __| / __|  __   __ _   _ _  
  >  <  \__ \ \__ \ / _| / _` | | ' \ 
 /_/\_\ |___/ |___/ \__| \__,_| |_||_|


Mise à jour :
Plus de payload, possibilité d'ajouter via le fichier txt 
Vous pouvez scanner plusieurs urls à la suite sans que le web driver se recharge
Possibilité d'ajouter des cookies (en cours de test)



Mise à jour à venir :
Ajout de couleur
Plusieurs vérification pour faciliter l'installation

"""
print(Fore.GREEN + banner + Fore.RESET)


def xsscan():

	valid_url = False
	message = Fore.RED + "[!]  L'URL est invalide" + Fore.RESET

	# Vérification de l'url
	while valid_url == False:
		url = input('[?] URL : ')
		urlparsed = urlparse(url)# On parse l'url pour récupérer ses composants
		if urlparsed.scheme == '':# Vérification si le protocole est bien déclarer dans l'url
			valid_url = False
			print(message)
		elif urlparsed.netloc == '':# Vérification si l'hôte et bien déclarer dans l'url
			valid_url = False
			print(message)
		elif urlparsed.query == '':# Vérification si le l'url à des paramètres et des valeurs
			valid_url = False
			print(message)
		else:
			valid_url = True

	choice = input('[?] Voulez vous ajouter des cookies [en cours de test] (y/n) : ')
	if 'y' in choice:
		init_cookie(url)

	# Récupération des payloads le fichier txt
	try:
		file = open('payload.txt', 'r')
		payload = file.readlines()
		file.close()
	except FileNotFoundError:
		print("[WARNING] Imposible d'ouvrire le fichier qui contient les payloads")
		exit();

	# Affichage
	print('\n')
	print('[+]', len(payload), 'payloads chargées')
	print('[+] Fuzzing pour : ', url,'\n')

	for p in payload:
		allurl = inject(url, p)# Injection des payloads dans l'url
		for u in allurl:# Injection des urls dans le fuzzeur
			if xss(u):
				print('[!]', u,  Fore.RED, 'XSS Found !\n', Fore.RESET)
			else:
				print('[*]', u, Fore.GREEN, 'Is Safe\n', Fore.RESET)

	question = input('[?] Do you want continue scanning ? (y/n) : ')

	if question == 'y':
		xsscan()
	else:
		print('Bye-bye')
		exit();
	
xsscan()




