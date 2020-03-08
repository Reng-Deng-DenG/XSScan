from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import warnings
warnings.filterwarnings('ignore')
import time
from lib.function import *
from urllib.parse import urlencode

# Options de chrome
chrome_options = Options()
chrome_options.add_argument('--headless') # Utilise chrome sans interface graphique
chrome_options.add_argument('--disable-xss-auditor')# Déactivation de la protection XSS
chrome_options.add_argument('--disable-web-security')# Déactivation de la sécurité web
chrome_options.add_argument('--ignore-certificate-errors')# Ignore les erreurs lié au certificat SSL
chrome_options.add_argument('--log-level=3')# Déactive les messages
chrome_options.add_argument('--disable-notifications')# Déactive les notifications
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36')# Modification de l'user-agent
chrome_options.add_experimental_option('excludeSwitches',['enable-logging']);# Supprime le message "DevTools listening on"

# Connexion au driver + emplacement du fichier
# Lien de téléchargement https://chromedriver.chromium.org/downloads
try:
	driver = webdriver.Chrome(executable_path="C:\\Users\\lucas-pc\\Desktop\\chromedriver.exe", options=chrome_options)
except WebDriverException as exception:
	print('[!] Unable to connect to the webdriver ! ')
	print('[?] Verify your web driver path')
	exit();

# Fonction qui retourne True si une url est vulnérable à la faille XSS
def xss(url, thread=1):

	xss = False
	time.sleep(thread)# Temps de connexion à l'url
	driver.get(url)# Simple requête GET
	time.sleep(1)# On met le driver en pauses le temps que le JS s'éxécute
	close_alert = 0	

	try:
		alert_obj = driver.switch_to.alert # On essaye de capturer une alert
		while alert_obj:
			alert_obj.accept()
			close_alert += 1
	except WebDriverException as exception:# Si il n'y a pas d'alert le driver produit une exepection
		xss = False
	
	if close_alert > 0:
		xss = True

	return xss


# Fonction qui permet de initialiser des cookies
# Prend l'url d'origine en paramètres
# Cette fonction n'a pas était tester à 100%
def init_cookie(url):

	urlparsed = urlparse(url)

	domain = urlparsed.netloc# Récupération du domain  

	if 'www' in domain:
		domain.replace('www', '.')# On remplace www par un point, se qui donne (.domain.com) 
	else:
		domain = '.' + domain# On ajoute un point, se qui donne (.domain.com)

	cookie_name = input('[?] Nane of cookie (ex: PHPSESSID) : ')
	cookie_name = cookie_name.strip()
	cookie_value = input('[?] Value of cookie (ex: 0j69jtouvjhf8) : ')
	cookie_value = cookie_value.strip()

	cookie_items = {'domain': domain,'name': cookie_name,'value': cookie_value,'path': '/','expires': 'None'}# Ajout des cookies dans un dictionnaire

	domain = urlparsed.scheme + '://' + urlparsed.netloc# Création de l'url pour iniatialiser les cookies

	driver.get(domain)# Connexion au domain
	driver.delete_all_cookies()# Suppresion des cookies qui sont prêt à être chargées
	driver.add_cookie(cookie_items)# Injection des cookies
	driver.get(url);

	print('\n')#Affichage
	print('[+] Adding cookie for', urlparsed.netloc)
	print('[*] Set-Cookie [{}={}]'.format(cookie_name, cookie_value))

# Fonction pour récupérer les payloads dans le fichier payload.txt
# Retourne une list content les payloads
def get_payload():

	try:
		file = open('payload.txt', 'r')
		payload = file.readlines()
		file.close()
	except FileNotFoundError:
		print("[!] Unable to open the file contain all payloads")
		exit();

	return payload

banner = """
 __  __  ___   ___                    
 \ \/ / / __| / __|  __   __ _   _ _  
  >  <  \__ \ \__ \ / _| / _` | | ' \ 
 /_/\_\ |___/ |___/ \__| \__,_| |_||_|


"""
print(banner)

# 
# Méthode Manuel
#
def manually_scan(url):

	payload = get_payload()# Récupération des payloads

	# Affichage
	print('\n')
	print('[+] {} Payloads Loaded '.format(len(payload)))
	print('\n')

	for p in payload:

		p = p.replace('\n', '')# Netoyage de la list
		url = url.replace('<xss>', p)# On replace <xss> par un payload
		code = get_code(url)# Récupéraion du code réponse de la requête
		vuln = xss(url)# Fuzzing

		# Affichage
		if vuln == True:
			print('[XSS FOUND] [{}] {}'.format(code, url))
		else :
			print('[{}] {}'.format(code, url))


		url = url.replace(p, '<xss>')# On remet l'url à sa valeur d'origine



#
# Méthode Automatique
#
def auto_scan(url):

	payload = get_payload()# Récupération des payloads

	# Affichage
	print('\n')
	print('[+] {} Payloads Loaded '.format(len(payload)))
	print('\n')

	for p in payload:

		p = p.replace('\n', '')# Netoyage de la liste
		all_url = inject(url, p)# Injection des payload dans les paramètre

		for u in all_url:# Récupération des urls

			code = get_code(url)# Récupéraion du code réponse de la requête
			vuln = xss(u)# Fuzzing

			if vuln == True:
				print('[XSS FOUND] [{}] {}'.format(code, u))
			else:
				print('[{}] {}'.format(code, u))

#
# Menu Départ
#
choice = input('[?] [M]anually adding payload or [A]uto : ')# On demande quel méthode l'utilisateur veut utiliser

if choice == 'm' or choice == 'M':
	print('[~] For this method you need to specify the key-word <xss> into the url')
	url = input('[?] Enter URL : ')

	valid_url = verify_url_with_a_keyword(url)# Vérification de l'url

	while valid_url == False:
		url = input('[?] Enter URL : ')
		valid_url = verify_url_with_a_keyword(url)


	if valid_url == True:

		choice = input('[?] Do you want add cookies ? (y/n) : ')# On demande si l'utilisateur veut ajouter des cookies

		if choice == 'y' or choice == 'Y':# Si oui
			init_cookie(url)# On initialise les cookies

		manually_scan(url)

elif choice == "a" or choice == 'A':
	print('[~] For this method you need a valid url like this http://x.com/?q=john')
	url = input('[?] Enter URL : ')

	valid_url = verify_url_with_query_valid(url)

	while valid_url == False:
		url = input('[?] Enter URL : ')
		valid_url = verify_url_with_query_valid(url)

	if valid_url == True:

		choice = input('[?] Do you want add cookies ? (y/n) : ')

		if choice == 'y' or choice == 'Y':
			init_cookie(url)

		auto_scan(url)
else:
	exit()


