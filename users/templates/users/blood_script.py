from bs4 import BeautifulSoup

import requests
import json


url = 'https://mrrofficials.com/search-blood-group/'

r  = requests.get(url)

soup = BeautifulSoup(r.text, 'lxml')

row_data = {}
row_list = []
count = 0

tables = soup.select('table.dataTable')
# print(tables)
for index, table in enumerate(tables):
	rows = table.select('tr')
	
	# print(rows)
	for row in rows:
		# print(type(row.find('td')))
		td = row.select('td')			
		row_data = {
		    'model': 'records.record',
			'pk': count,
			'fields': {
				"name": td[0].text,
			    "email": td[4].text,
			    "permanent_address": td[2].text,
			    "current_address": td[3].text,
			    "phone": td[5].text,
			    "blood_group": td[1].text,
			}

		}

		print(row_data)
		count += 1						
		row_list.append(row_data)

print(row_list)

with open('blood_group.json', 'w') as fout:
	json.dump(row_list, fout)


    	
