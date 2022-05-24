from bs4 import BeautifulSoup
import lxml
import os
import pandas as pd
import yaml

path = 'data/rdf_unregular_eng/test'
data = list()
wrong_list = list()

"""
data = {text: string
        target: string 
        tar_pos_l: int
        tar_pos_r: ing
        amount: float
        currency: str
        amount_pos_l: int
        amount_pos_r: int
        currency_pos_l: int
        currency_pos_r: int
        filename: str
}
"""
iteration = 0


for file in os.listdir(path):
    filename = os.path.join(path, file)
    # print(filename)
    infile = open(filename, "r", encoding='utf-8')
    contents = infile.read()
    soup = BeautifulSoup(contents, 'xml')
    raw_data = [line for line in soup.get_text().replace('\n', ' ').split('  ') if line != '']
    text = soup.find('document_text').text.replace('вЂЁ', '')

    annotations = soup.findAll('annotation')

    amount, currency, amount_pos_l, amount_pos_r, currency_pos_l, currency_pos_r = [], [], [], [], [], []
    for annotation in annotations:
        pv = annotation.find('property_value')
        pt = annotation.find('property_name')
        if pv:
            if pt.text.split('#')[1] == 'ms_major_amount':
                amount.append(pv.text)
                amount_pos_l.append(int(annotation.find('annotation_start').text))
                amount_pos_r.append(int(annotation.find('annotation_end').text))
            elif pt.text.split('#')[1] == 'ms_major_currency':
                currency.append(pv.text)
                currency_pos_l.append(int(annotation.find('annotation_start').text))
                currency_pos_r.append(int(annotation.find('annotation_end').text))

    window = 15
    target, tar_pos_l, tar_pos_r = [], [], []

    if len(currency) > len(amount):
        currency = currency[:len(amount)]
        currency_pos_l = currency_pos_l[:len(amount)]
        currency_pos_r = currency_pos_r[:len(amount)]
    elif len(amount) > len(currency):
        amount = amount[:len(currency)]
        amount_pos_l = amount_pos_l[:len(currency)]
        amount_pos_r = amount_pos_r[:len(currency)]

    for i in range(len(amount)):
        if amount_pos_l[i] > currency_pos_l[i] and amount_pos_r[i] < currency_pos_r[i]:
            wrong_list.append(filename)
            iteration += 1

        if amount_pos_l[i] < currency_pos_l[i]:
            trg = f'{amount[i]} {currency[i]}'
            target.append(trg)
            step = text[amount_pos_l[i]-window:currency_pos_r[i]+window].find(trg)
            if step == -1:
                l = amount_pos_l[i]
                r = currency_pos_r[i]
            else:
                l = amount_pos_l[i] - window + step
                r = currency_pos_r[i] - window + step
            tar_pos_l.append(l)
            tar_pos_r.append(r)
        else:
            trg = f'{currency[i]} {amount[i]}'
            target.append(trg)
            step = text[currency_pos_l[i] - window:amount_pos_r[i] + window].find(trg)
            if step == -1:
                l = currency_pos_l[i]
                r = amount_pos_r[i]
            else:
                l = currency_pos_l[i] - window + step
                r = amount_pos_r[i] - window + step
            tar_pos_l.append(l)
            tar_pos_r.append(r)

    data.append({'text': text,
                 'target': target,
                 'tar_pos_l': tar_pos_l,
                 'tar_pos_r': tar_pos_r,
                 'amount': amount,
                 'currency': currency,
                 'amount_pos_l': amount_pos_l,
                 'amount_pos_r': amount_pos_r,
                 'currency_pos_l': currency_pos_l,
                 'currency_pos_r': currency_pos_r,
                 'filename': filename
                 })

print(len(data))
print(iteration)

for entry in data:
    if entry['filename'] in wrong_list:
        data.remove(entry)
df = pd.DataFrame(data)
df.to_csv('irregular_test_fixed.csv')
