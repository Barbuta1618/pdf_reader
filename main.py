from datetime import datetime
from datetime import date
from os import listdir
import os
from os.path import isfile, join
import requests
import json
import pdfplumber
import time


def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()
    current_date = today.strftime("%d.%m.%Y")


    current_date_time = current_time + ' ' + current_date

    return current_date_time

def getData(path):
    with pdfplumber.open(path) as pdf:
        

        data = []
        for first_page in pdf.pages:
            text = first_page.extract_text()
            start_string = '1 2 3 3 4 5 6 7 8'
            final_string = 'WinMENTOR 896.02'


            if first_page == pdf.pages[len(pdf.pages) - 1]:
                final_string = 'Observatii:'
            index_start = text.find(start_string)
            index_end = text.find(final_string)
            final_text = text[index_start + len(start_string):index_end].strip()
            lines = final_text.split('\n')

            for line in lines:
                buc_text = 'Buc'
                buc_index = line.find(buc_text)
                nr_prod = line[buc_index + len(buc_text) + 1:].split(' ')[0]
                words = line.split(' ')
                
                id = words[0]
                code = words[1]
                color = words[2]
                size = words[3]


                if color.upper() == 'NGR':
                    color = 'NEGRU'
                
                data.append((id, code, color, size, int(float(nr_prod.replace(',', '.')))))

        return data

url = 'https://aroti-backend.herokuapp.com/api'
headers = {'Content-Type': 'application/json'}
path = './FACTURI/'
destination_path = './FACTURI_PROCESATE/'


while True:
    files = [f for f in listdir(path) if isfile(join(path, f))]

    for file in files:
        file_path = path + file
        data = {'data': getData(file_path), 'token' : 'admin'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print(r.text)

        time.sleep(10)
        time_str = getCurrentTime()
        os.replace(file_path, destination_path + time_str + '.pdf')
    
    time.sleep(60)








