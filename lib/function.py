#coding:utf-8
from urllib.parse import urlparse
from urllib.parse import parse_qs

# Fonction qui permet de injecter un payload dans chaque paramètres de l'url tout en conservant ces valeurs d'origine
# Retourne une liste
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
