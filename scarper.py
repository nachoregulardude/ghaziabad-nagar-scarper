#!/usr/bin/env python3

import requests
from datetime import datetime, date
import pandas as pd
from bs4 import BeautifulSoup


def to_date(s):
    return datetime.strptime(s, '%d-%m-%Y')

def main():
    url = 'https://mutation.onlinegnn.com/SearchPropertyMutation.aspx'
    s = requests.Session()
    r = BeautifulSoup(s.get(url).text, 'lxml')
    table = r.find('table', {'class':'grd', 'id': 'ContentPlaceHolder1_gvApplications'})
    content = table.find_all("tr")
#    headers = content[0]
    rows = content[1:]
    result = list()
    count = 0

    for row in rows:
        print(f'Getting the {count} row...')
        row_contents =  row.find_all("td")[1:9]
        pin_no = row_contents[0].text
        application_no = row_contents[1].text
        new_owner_name = row_contents[2].text
        father_or_husband_name = row_contents[3].text
        application_date = to_date(row_contents[4].text)
        approved_date = to_date(row_contents[5].text)
        approved_status = row_contents[6].text
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

    print(f'{count} rows parsed')
    dataframe = pd.DataFrame(result)
    filename = f'ghaziabd_mutation_application_data_{date.today()}.csv'
    dataframe.to_csv(filename, index=False)
    print(f'Results saved to {filename}')

if __name__=='__main__':
    main()
