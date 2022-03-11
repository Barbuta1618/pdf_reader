# from tika import parser
# file = './FACTURI/fact2.pdf'
# file_data = parser.from_file(file)
# text = file_data['content']
# print(text)

import json
import pdfplumber

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

path = './FACTURI/fact3.pdf'


import requests

url = 'http://localhost:5000/api'
data = {'data': getData(path), 'token' : 'admin'}
headers = {'Content-Type': 'application/json'}

r = requests.post(url, data=json.dumps(data), headers=headers)

print(r.text)


