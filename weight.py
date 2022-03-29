from ast import If
from math import fabs
import requests as req
from bs4 import BeautifulSoup
import urllib.parse
import re

results = []
debug = False
min_value = 0.2

print("Enter/Paste your content and type 'go' or 'debug'")
items = []
while True:
    try:
        line = input()
        if line.casefold() == 'go'.casefold():
            break
        if line.casefold() == 'debug'.casefold():
            debug = True
            break
    except EOFError:
        break
    item = line.strip()
    if len(item) > 2:
        items.append(item)

with open("output.txt", "w") as txt_file:
    for item in items:
        try:
            url = 'https://www.google.com/search?q=' + urllib.parse.quote_plus(item) + "+weight"
            web = req.get(url)

            soup = BeautifulSoup(web.content, 'html.parser')
            table = soup.select_one('table:nth-of-type(1)')
            result = {}
            for row in table.findAll('tr'):
                aux = row.findAll('td')
                result[aux[0].string] = aux[1].string

            weight_string = next((v.replace(',','.') for (k,v) in result.items() if 'weight'.casefold() in k.casefold()), '-1')

            is_lb = 'lb'.casefold() in weight_string or 'pound'.casefold() in weight_string
            is_oz = 'oz'.casefold() in weight_string or 'ounce'.casefold() in weight_string

            # convert to Kg and round
            weight_float = float(re.findall(r"(?:\d*\.\d+|\d+)", weight_string)[0])
            weight_kg = weight_float / 2.205 if is_lb else weight_float / 35.274 if is_oz else weight_float
            weight_kg = round(weight_kg, 2)

            # check if less than minimum weight
            if weight_kg < min_value:
                weight_kg = min_value

            # formatting
            result_string = f'{item}\t{weight_string}\t{weight_kg}' if debug else f'{item}\t{weight_kg}'
            result_string = result_string.replace('.', ',')

            # result
            print(result_string)
            txt_file.write(f'{result_string}\n')

        except:
            txt_file.write(f'{item}\t-1\t-1\n' if debug else f'{item}\t-1\t')      
