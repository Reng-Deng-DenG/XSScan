from urllib.request import *
import urllib.error
from urllib.parse import urlparse, parse_qs

# Retourne le code http reponse d'un url
def get_code(url):

	reponse_code = ''
	try:
		r = urlopen(url)
	except urllib.error.HTTPError as e:
		reponse_code = e.code
	else:
		reponse_code = r.getcode()

	return reponse_code

# Vérifie une url avec des paramètres et des valeurs déclarer
# Exemple : http://example.com/?id=1&page=forum => Valid
# 		  :	http://example.com/?id=&page=forum 	=> Invalid
# Retourn true si l'url est valid
def verify_url_with_query_valid(url):

	valid_url = False

	urlparsed = urlparse(url)# On parse l'url pour récupérer ses composants

	protocol = urlparsed.scheme # Récupération du protocol de l'url
	domain = urlparsed.netloc # Récupartion de l'hôte de l'url
	query = urlparsed.query # Récupération du query de l'url
	para_and_value = parse_qs(urlparsed.query) # Récupération des paramètres et des valeurs de l'url

	if protocol == 'http' or protocol == 'https': # On vérifie sur le protocole est bien http ou https
		if domain is not None:# Que l'hôte est présent
			if query is not None:# Que les querys sont présent
				if len(para_and_value) > 0:# Que les paramètres et les valeurs sont présent
					valid_url = True
					return valid_url
				else:
					print('[!] No query found into the URL')
					valid_url = False
					return valid_url
			else:
				print('[!] No query found into the URL')
				valid_url = False
				return valid_url
		else:
			print('[!] Invalid URL')
			valid_url = False
			return valid_url
	else:
		print('[!] You must specify http or https into the URL')
		valid_url = False
		return valid_url

# Vérifie une url avec un mot-clées, ici c'est <xss>
# Retourne true si l'url est valide
def verify_url_with_a_keyword(url):

	valid_url = False

	urlparsed = urlparse(url)# On parse l'url pour récupérer ses composants
	protocol = urlparsed.scheme # Récupération du protocol de l'url
	domain = urlparsed.netloc # Récupartion de l'hôte de l'url

	if protocol == 'http' or protocol == 'https':
		if domain is not None:
			if '<xss>' in url:
				valid_url = True
				return valid_url
			else:
				print('[!] You must specify the keyword <xss> into the URL')
				valid_url = False
				return valid_url
		else:
			print('[!] Invalid URL')
			valid_url = False
			return valid_url
	else:
		print('[!] You must specify http or https into the URL')
		valid_url = False
		return valid_url

def inject(URL, PAYLOAD):

	urlparsed = urlparse(URL);# Création d'un object urlparse
	ParameterAndValue = parse_qs(urlparsed.query);#Création d'un dico avec Para et Value

	Parameter = [];
	Value = [];
	ValueCopy =  [];

	for p in ParameterAndValue:# Récupération de tout les paramètres
		Parameter.append(p);

	for v in ParameterAndValue.values():# Récupération de tout les valeurs des paramètres
		Value.append(''.join(v));
		ValueCopy.append(''.join(v));# Création d'une copy de Value

	RealURL = urlparsed.scheme+"://"+urlparsed.netloc+urlparsed.path+"?"; # Reconstitution de l'URL (http+hôte+chemin)

	ListQuery = [] # Création d'un liste avec tout les paramètres et les valeurs


	NemberOfQuery = len(Value)
	i = 0

	while i < NemberOfQuery:# Création de la liste
		ListQuery.append(Parameter[i])
		ListQuery.append("=")
		ListQuery.append(Value[i])
		ListQuery.append("&")
		i += 1

	del ListQuery[-1] # Netoyage de la liste

	i = 2
	x = 0

	Result = [];

	while i < len(ListQuery):
		ListQuery[i] = PAYLOAD# Injection du payload
		FinalQuery = RealURL + ''.join(ListQuery)# Création de l'URL pret à être injecter
		Result.append(FinalQuery)# On stocke les URLs dans un tableaux qui seras retourner par notre fonction
		ListQuery[i] = ValueCopy[x]# Après l'injection on remet la valeur d'origine
		i += 4
		x += 1

	return Result
