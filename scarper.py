import requests
from datetime import datetime, date
import pandas as pd
from bs4 import BeautifulSoup

'''
need to get
pin_no, application_no, new_owner_name, father_or_husband_name, application_date, approved_date, approved_status
'''

url = 'https://mutation.onlinegnn.com/SearchPropertyMutation.aspx'

def to_date(s):
    return datetime.strptime(s, '%d-%m-%Y')

s = requests.Session()
r = BeautifulSoup(s.get(url).text, 'lxml')
table = r.find('table', {'class':'grd', 'id': 'ContentPlaceHolder1_gvApplications'})
header = table.find_all("tr")[0]
rows = table.find_all("tr")[1:]
result = list()
count = 0

for row in rows:
    print(f'Getting the {count} row...')
    row =  row.find_all("td")[1:9]
    pin_no = row[0].text
    application_no = row[1].text
    new_owner_name = row[2].text
    father_or_husband_name = row[3].text
    application_date = to_date(row[4].text)
    approved_date = to_date(row[5].text)
    approved_status = row[6].text
    fields = {
            'pin_no': pin_no,
            'application_no' :application_no,
            'new_owner_name' :new_owner_name,
            'father_or_husband_name' :father_or_husband_name,
            'application_date' :application_date,
            'approved_date' :approved_date,
            'approved_status' :approved_status
            }
    result.append(fields)
    count+=1

print(result)
dataframe = pd.DataFrame(result)
today_date = date.today()
dataframe.to_csv(f'ghaziabd_mutation_application_data_{today_date}.csv', index=False)

