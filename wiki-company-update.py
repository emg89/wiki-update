import requests
import json
import csv
import time

endpointUrl = 'https://www.wikidata.org/w/api.php'
# endpointUrl = 'https://test.wikidata.org/w/api.php'
pause_time = 5
session = requests.Session()

def retrieveCredentials():
	with open('credentials.txt', 'rt') as fileObject:
		lineList = fileObject.read().split('\n')
	username = lineList[0].split('=')[1]
	password = lineList[1].split('=')[1]
	credentials = [username, password]
	return credentials

def getLoginToken():
	parameters = {
		'action':'query',
		'meta':'tokens',
		'type':'login',
		'format':'json'
	}
	j = session.get(endpointUrl, params=parameters).json()
	return j['query']['tokens']['logintoken']

def logIn(token, username, password):
	parameters = {
		'action':'login',
		'lgname':username,
		'lgpassword':password,
		'lgtoken':token,
		'format':'json'
	}
	j = session.post(endpointUrl, data=parameters).json()
	return j

def getCsrfToken():
	parameters = {
		"action": "query",
		"meta": "tokens",
		"format": "json"
	}
	j = session.get(endpointUrl, params=parameters).json()
	return j["query"]["tokens"]["csrftoken"]

def createclaim(editToken, subjectQNumber, propertyPNumber, insert_value):
	parameters = {
		'action':'wbcreateclaim',
		'format':'json',
		'entity':subjectQNumber,
		'snaktype':'value',
		'bot':'1',
		'token': editToken,
		'property': propertyPNumber,
		'value': '"' + insert_value + '"',
		'maxlag':'5'
	}
	j = session.post(endpointUrl, data=parameters).json()
	if 'error' in j.keys():
		print('pause due to max lag')
		time.sleep(pause_time)

	return j

def getclaims(wiki_id):
	params = {
		'action': 'wbgetclaims',
		'entity': wiki_id,
		'format': 'json'
	}
	j = session.get(endpointUrl, params=params).json()
	return j['claims']


# *** MAIN SCRIPT ***
# update_list = 'test-update-list.csv'
update_list = 'wikidata-update-list.csv'
with open(update_list, newline='', encoding="utf-8") as f:
	reader = csv.reader(f)
	companies = list(reader)

props = companies[0][1:]
edit_count = 0

credentials = retrieveCredentials()
print('Credentials: ', credentials)
user = credentials[0]
pwd = credentials[1]

loginToken = getLoginToken()
print('Login token: ',loginToken)

data = logIn(loginToken, user, pwd)
print('Confirm login: ', data)
print()

for company in companies[1:]:
	item = company[0]
	claims = getclaims(item)
	existing_props = claims.keys()

	for prop in props:
		insert_value = company[props.index(prop)+1]
		if prop not in existing_props and len(insert_value)>0:
			csrfToken = getCsrfToken()
			data = createclaim(csrfToken, item, prop, insert_value)
			print('Write confirmation: ', data)
			edit_count += 1

print(edit_count)